#!/usr/bin/env python3
"""PR 分支落后 / 契约基线检查（只读，仅标准库）。

作用：把「这个 PR 是不是基于过期 main」变成 **PR 页面上可见、且会红的** 事实。
背景（2026-11-14 维护者裁定）：外部 agent 不 rebase 就开 PR，会拿过期契约写数据 ——
2026-11-14 批次的 #911–#922 用 v2.39 的 25 列表头（v2.40 已撤销）、#913/#918/#919 还沿用
`Gext_corr=y` 的旧语义，全部是「分支基线早于契约定版」造成的机械缺陷，与科学内容无关。

判据（硬闸只认这两条）：
  1. **契约漂移**：本 PR 的 head 若不包含 base 上最近一次改动「契约文件」的提交
     （`SCHEMA.md` / `数据审核提示词.md` / `tools/validate.py`），即本分支基于旧契约 → 失败。
     这条不依赖提交数，直接对准真正的故障模式（契约改了、分支没跟上）。
  2. **落后提交数**：`behind > --max-behind`（默认 50）→ 失败；`0 < behind <= 50` → 只警告。
     目的不是消灭落后，而是拦住「基于三周前 main」那种（2026-11-14 有 18 个 PR 基于 10-24）。

用法 / Usage:
  python3 tools/check_branch_freshness.py                        # CI：读环境变量，仅警告（历史行为）
  python3 tools/check_branch_freshness.py --strict               # CI：契约漂移/落后超阈值即非零退出
  python3 tools/check_branch_freshness.py --repo R --head SHA --base main [--strict] [--max-behind N]
  python3 tools/check_branch_freshness.py --selftest             # 离线跑判定用例（不联网）
环境变量：GITHUB_REPOSITORY、GITHUB_EVENT_PULL_REQUEST_HEAD_SHA、GITHUB_BASE_REF、
         GH_TOKEN（或 GITHUB_TOKEN）
退出码：0 = 通过（可带警告）；1 = 契约漂移或落后过多（仅 --strict）；2 = 查询失败（仅 --strict）
"""
import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from urllib.parse import quote

MAX_LIST = 10
# 落后数硬闸阈值：默认 400。理由：这个仓每天有 4–6 个 audit 快照提交、一次批次合并会推进
# 上百个提交，所以「落后几十上百」是常态、不代表分支不可用（GitHub 跑的是 merge ref）；
# 400 对应「两三周前的 main」，正是会引发契约/数据冲突的量级。批次刚合完导致的几百落后属正常，
# rebase 即转绿；真正的硬伤由「契约漂移」那条判据兜。
DEFAULT_MAX_BEHIND = 400
# 「契约文件」：改了它们就等于改了所有 PR 必须遵守的口径。
CONTRACT_FILES = ('SCHEMA.md', '数据审核提示词.md', 'tools/validate.py')
API = 'https://api.github.com'


def _get(url, token, timeout=30):
    req = urllib.request.Request(url, headers={
        'Authorization': f'Bearer {token}',
        'Accept': 'application/vnd.github+json',
        'User-Agent': 'ajst-data-branch-freshness',
    })
    with urllib.request.urlopen(req, timeout=timeout) as fh:
        return json.load(fh)


def fetch_compare(repo, head, base, token, timeout=30):
    return _get(f'{API}/repos/{repo}/compare/{head}...{base}', token, timeout)


def last_contract_commit(repo, base, path, token, timeout=30):
    """base 上最近一次改 path 的提交 → (sha, 标题)。"""
    d = _get(f'{API}/repos/{repo}/commits?sha={base}&path={quote(path, safe="")}&per_page=1',
             token, timeout)
    if not d:
        return None, None
    c = d[0]
    return c['sha'], (c.get('commit', {}).get('message') or '').splitlines()[0][:80]


def contract_drift(repo, head, base, token, timeout=30):
    """返回 [(file, sha8, subject)]：head 不包含的这些契约提交。"""
    out = []
    for path in CONTRACT_FILES:
        try:
            sha, subj = last_contract_commit(repo, base, path, token, timeout)
            if not sha:
                continue
            cmp_ = _get(f'{API}/repos/{repo}/compare/{sha}...{head}', token, timeout)
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, ValueError):
            continue            # 查不到就不据此阻断（另一条判据仍生效）
        # behind_by > 0 ⇒ 该契约提交不在 head 的祖先里 ⇒ 本分支基于旧契约
        if int(cmp_.get('behind_by') or 0) > 0:
            out.append((path, sha[:8], subj))
    return out


def decide(behind, drift, max_behind, strict):
    """纯函数：输入判据，输出 (退出码, 输出行)。便于 --selftest 离线验证。"""
    lines = []
    for path, sha, subj in drift:
        line = f'{path} 最近一次改动是 {sha}「{subj}」——本分支不含该提交，即基于旧契约'
        lines.append(('::error::' if strict else '::warning::') + line)
    if behind > 0:
        if strict and behind > max_behind:
            lines.append(f'::error::本分支落后 base {behind} 个提交（阈值 {max_behind}）'
                         f'——请 `git pull --rebase origin <base>` 后再推')
        else:
            lines.append(f'::warning::本分支落后 base {behind} 个提交——'
                         f'请 `git pull --rebase origin <base>` 再继续')
    if not behind and not drift:
        lines.append('分支与 base 同步、契约基线为最新——好')
    fail = bool(drift) or (strict and behind > max_behind)
    if strict:
        if fail:
            lines.append('::error::合并前必须 rebase 到当前 base'
                         '（AGENTS.md「开工顺序」第 6 条，2026-11-14 起为硬闸）')
        else:
            lines.append('::notice::契约基线与落后度检查通过')
    return (1 if (strict and fail) else 0), lines


def selftest():
    cases = [
        # (behind, drift, max_behind, strict, 期望退出码, 期望含 error)
        (0, [], 50, True, 0, False),
        (3, [], 50, True, 0, False),                    # 只警告
        (3, [], 50, False, 0, False),
        (51, [], 50, True, 1, True),                     # 超阈值
        (51, [], 50, False, 0, False),                   # 非 strict 永不失败
        (0, [('SCHEMA.md', 'e256a8e8', 'v2.40')], 50, True, 1, True),   # 契约漂移
        (0, [('SCHEMA.md', 'e256a8e8', 'v2.40')], 50, False, 0, False),
        (300, [('tools/validate.py', 'abc12345', 'x')], 50, True, 1, True),
    ]
    ok = True
    for behind, drift, mx, strict, want_rc, want_err in cases:
        rc, lines = decide(behind, drift, mx, strict)
        has_err = any(l.startswith('::error::') for l in lines)
        good = (rc == want_rc and has_err == want_err)
        ok = ok and good
        print(f'{"PASS" if good else "FAIL"} behind={behind} drift={len(drift)} '
              f'max={mx} strict={strict} → rc={rc} error={has_err}'
              f'（期望 rc={want_rc} error={want_err}）')
    print('自检', '通过' if ok else '失败')
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo', default=os.environ.get('GITHUB_REPOSITORY'))
    ap.add_argument('--head', default=os.environ.get('GITHUB_EVENT_PULL_REQUEST_HEAD_SHA'))
    ap.add_argument('--base', default=os.environ.get('GITHUB_BASE_REF'))
    ap.add_argument('--strict', action='store_true', help='契约漂移或落后超阈值时非零退出')
    ap.add_argument('--max-behind', type=int, default=DEFAULT_MAX_BEHIND)
    ap.add_argument('--selftest', action='store_true')
    args = ap.parse_args()

    if args.selftest:
        return selftest()
    token = os.environ.get('GH_TOKEN') or os.environ.get('GITHUB_TOKEN') or ''
    if not (args.repo and args.head and args.base):
        print('::notice::分支落后检查跳过：缺少 repo / head / base（非 PR 事件或未配置）')
        return 0
    if not token:
        print('::notice::分支落后检查跳过：没有可用 token')
        return 0

    try:
        d = fetch_compare(args.repo, args.head, args.base, token)
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, ValueError) as e:
        print(f'::notice::分支落后检查跳过：取 compare 数据失败（{e}）')
        return 2 if args.strict else 0

    behind = int(d.get('ahead_by') or 0)   # head...base ⇒ base 领先 head 的提交数 = 落后数
    commits = d.get('commits') or []
    drift = contract_drift(args.repo, args.head, args.base, token) if behind else []
    rc, lines = decide(behind, drift, args.max_behind, args.strict)
    for line in lines:
        print(line)
    if behind > 0:
        for c in commits[:MAX_LIST]:
            sha = (c.get('sha') or '')[:8]
            subj = (c.get('commit', {}).get('message') or '').splitlines()[0][:80]
            print(f'::notice::落后 {args.base}：{sha} {subj}')
        if behind > MAX_LIST:
            print(f'::notice::另有 {behind - MAX_LIST} 个落后提交未列出，'
                  f'见 GitHub 的 "N commits behind" 提示')
    return rc


if __name__ == '__main__':
    sys.exit(main())
