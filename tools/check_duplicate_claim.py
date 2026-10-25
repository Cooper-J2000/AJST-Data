#!/usr/bin/env python3
"""同源挤占守卫 —— 检测「同一个源被多个 open PR 同时占用」，并把它变成**看得见**且（后开者）**会红**的事实。

背景（2026-10-24/25 两次实测撞车：#171/#206、#184/#219）三处失效：
  1. 判据窄：旧版只看 `info/lc` 文件。`claim: <源ID>` 的 draft PR 才是设计上的占位手段，
     看不见它 → claim 到 data PR 之间那 4–7 小时的窗口完全没保护。
  2. 没人看得见：旧版只发 `::warning::` 到 check-run annotation，`gh pr checks` 只显示
     `validate pass`，PR 对话页也没痕迹 → 两个 agent 都没理。
  3. 没咬合力：`exit 0` + mergeable，撞车 PR 照样能合。

现在做三件事：
  * 占用 = 本 PR 触碰的 `info/<id>.json` / `lc/<id>.csv` ∪ 标题里的 `claim: <源ID>`；
  * `--comment` / `--label collision`：把冲突写成 PR 上看得见的评论与 label（需写权限的 token；
    fork PR 要用 pull_request_target 跑才能拿到写权限）；
  * `--strict`：**只有后开者**非零退出（先开者仍 0），让撞车在 CI 上变红；绕过必须显式操作。

用法 / Usage:
  python3 tools/check_duplicate_claim.py --selftest                  # 离线跑判定用例
  python3 tools/check_duplicate_claim.py --pr 206                    # 本地只查（恒 0）
  python3 tools/check_duplicate_claim.py --pr 206 --strict --comment --label collision --dry-run
  python3 tools/check_duplicate_claim.py                             # CI：读环境变量
环境变量：GITHUB_REPOSITORY、GITHUB_EVENT_PULL_REQUEST_NUMBER、GH_TOKEN（或 GITHUB_TOKEN）
"""
import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

API = 'https://api.github.com'
SRC_RE = re.compile(r'^(?:info|lc)/(?P<src>[^/]+)\.(?:json|csv)$')
CLAIM_RE = re.compile(r'^\s*claim\s*[:：]\s*(?P<src>[A-Za-z0-9_.\-]+)', re.I)
MARKER = '<!-- ajst-collision-guard -->'
MAX_PR_PAGES = 3          # 100/页；超过只提示，不阻断


# ─── GitHub API ─────────────────────────────────────────────────────────────
def gh(url_path, token, method='GET', data=None, timeout=30):
    body = json.dumps(data).encode() if data is not None else None
    req = urllib.request.Request(f'{API}{url_path}', data=body, method=method, headers={
        'Authorization': f'Bearer {token}',
        'Accept': 'application/vnd.github+json',
        'User-Agent': 'ajst-data-duplicate-claim-guard',
        **({'Content-Type': 'application/json'} if body else {}),
    })
    with urllib.request.urlopen(req, timeout=timeout) as fh:
        raw = fh.read().decode() or '{}'
        return json.loads(raw)


def claimed_source(title):
    """标题 `claim: GRB210503A` → 'GRB210503A'；其它标题（含 `data: 审核 GRBxxx`）→ None。"""
    m = CLAIM_RE.match(title or '')
    return m.group('src') if m else None


def pr_sources(repo, number, token):
    files = gh(f'/repos/{repo}/pulls/{number}/files?per_page=100', token)
    out = set()
    for f in files:
        m = SRC_RE.match(f.get('filename') or '')
        if m:
            out.add(m['src'])
    return out


def open_prs(repo, token):
    prs = []
    for page in range(1, MAX_PR_PAGES + 1):
        batch = gh(f'/repos/{repo}/pulls?state=open&per_page=100&page={page}', token)
        prs.extend(batch)
        if len(batch) < 100:
            break
    return prs


def occupancy(repo, pr, token):
    """→ set(占用的源)：info/lc 文件 ∪ claim 标题。"""
    try:
        occ = pr_sources(repo, pr['number'], token)
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, ValueError):
        occ = set()
    src = claimed_source(pr.get('title'))
    if src:
        occ.add(src)
    return occ


# ─── 判定（纯函数，可离线测）────────────────────────────────────────────────
def decide(mine, me_pr, others):
    """mine: set(源)；me_pr/others: {number,title,created_at,user:{login},draft}

    → (conflicts, has_earlier)；conflicts: [(其他 Pr, 共同源 list, 是否先于本 PR)]
    先后判据：created_at 更早者优先，同秒时 PR 号小者优先。
    """
    me_key = (me_pr.get('created_at') or '', me_pr['number'])
    conf = []
    for pr, shared in others:
        other_key = (pr.get('created_at') or '', pr['number'])
        conf.append((pr, sorted(shared), other_key < me_key))
    conf.sort(key=lambda x: (x[0].get('created_at') or '', x[0]['number']))
    return conf, any(c[2] for c in conf)


def render_comment(mine, me_pr, conf):
    lines = [MARKER,
             '## ⚠️ 同源挤占：这个 PR 与其他 open PR 占用同一个源', '']
    lines.append(f'本 PR（#{me_pr["number"]}，{me_pr["user"]["login"]}，开于 {me_pr["created_at"]}）占用：'
                 f'`{"`, `".join(sorted(mine))}`')
    lines += ['', '| 其他 PR | 作者 | 开于 | 共同源 | 先后 | 形态 |', '|---|---|---|---|---|---|']
    for pr, shared, earlier in conf:
        who = '**先开（你应让位）**' if earlier else '后开'
        kind = 'draft（claim）' if pr.get('draft') else '正式'
        lines.append(f'| #{pr["number"]} {pr["title"][:60]} | {pr["user"]["login"]} | '
                     f'{pr["created_at"]} | `{"`, `".join(shared)}` | {who} | {kind} |')
    lines.append('')
    if any(c[2] for c in conf):
        lines += [
            '### 你要做的（一个源同时只应有一个未过期认领：§2 第 3 条 / §5 第 6 条）',
            '1. **优先让位**：关闭本 PR，或换一个没被占用的源；',
            '2. 确实要争：在**先开者**的 PR 下评论沟通，等 48 小时（§5 第 6 条）；',
            '3. **不要删你的分支**——已做完就把与先开者的**增量**写在这里，维护者合并时会吸收'
            '（2026-10-25 两次竞态都这样处理：#171 的文献级卡、#219 的字段判断都被吸收并记名）。',
            '',
            '⛔ 本 PR 的 CI 会因这一项变**红**（阻断级，不是提示）。',
        ]
    else:
        lines += ['你是先开者，不阻断。后开者沟通让位后，本评论与 label 会自动撤掉。']
    lines += ['', '_由 `tools/check_duplicate_claim.py` 自动生成；冲突解除后自动更新/撤销。_']
    return '\n'.join(lines)


# ─── 可见性（写操作；失败只降级，不影响判定）────────────────────────────────
def upsert_comment(repo, number, token, body, dry_run=False):
    comments = gh(f'/repos/{repo}/issues/{number}/comments?per_page=100', token)
    existing = next((c for c in comments if MARKER in (c.get('body') or '')), None)
    if dry_run:
        print(f'[dry-run] {"PATCH" if existing else "POST"} comment on #{number}:\n{body}\n')
        return
    if existing:
        if (existing.get('body') or '').strip() == body.strip():
            print('挤占评论内容未变，跳过')
            return
        gh(f'/repos/{repo}/issues/comments/{existing["id"]}', token, 'PATCH', {'body': body})
        print(f'已更新挤占评论 {existing["html_url"]}')
    else:
        c = gh(f'/repos/{repo}/issues/{number}/comments', token, 'POST', {'body': body})
        print(f'已发挤占评论 {c["html_url"]}')


def delete_marked_comment(repo, number, token, dry_run=False):
    """冲突解除后把守卫评论撤掉（只删带 MARKER 的那一条，别人的评论一概不碰）。"""
    comments = gh(f'/repos/{repo}/issues/{number}/comments?per_page=100', token)
    existing = next((c for c in comments if MARKER in (c.get('body') or '')), None)
    if not existing:
        return
    if dry_run:
        print(f'[dry-run] DELETE comment {existing["id"]}（冲突已解除）')
        return
    gh(f'/repos/{repo}/issues/comments/{existing["id"]}', token, 'DELETE')
    print('冲突已解除，已撤掉挤占评论')


def ensure_label(repo, name, token):
    try:
        gh(f'/repos/{repo}/labels/{urllib.parse.quote(name, safe="")}', token)
    except urllib.error.HTTPError as e:
        if e.code != 404:
            raise
        gh(f'/repos/{repo}/labels', token, 'POST',
           {'name': name, 'color': 'd93f0b', 'description': '同一源被多个 open PR 占用（挤占）'})


def set_label(repo, number, token, name, present, dry_run=False):
    ensure_label(repo, name, token)
    labels = gh(f'/repos/{repo}/issues/{number}/labels', token)
    has = any(l.get('name') == name for l in labels)
    if dry_run:
        print(f'[dry-run] label `{name}`：{"保持" if has == present else ("加" if present else "撤")}')
        return
    if present and not has:
        gh(f'/repos/{repo}/issues/{number}/labels', token, 'POST', {'labels': [name]})
        print(f'已打 label `{name}`')
    elif not present and has:
        gh(f'/repos/{repo}/issues/{number}/labels/{urllib.parse.quote(name, safe="")}', token, 'DELETE')
        print(f'已撤 label `{name}`')


# ─── 离线用例 ───────────────────────────────────────────────────────────────
def selftest():
    def P(n, t, at, who='a', draft=False):
        return {'number': n, 'title': t, 'created_at': at, 'user': {'login': who}, 'draft': draft}
    bad = 0

    def check(name, cond):
        nonlocal bad
        print(('  PASS  ' if cond else '  FAIL  ') + name)
        bad += 0 if cond else 1

    check('claim: GRB210503A → GRB210503A', claimed_source('claim: GRB210503A') == 'GRB210503A')
    check('全角冒号 claim：GRB210512 也认', claimed_source('claim：GRB210512') == 'GRB210512')
    check('data: 审核 GRB181120A 不算 claim', claimed_source('data: 审核 GRB181120A（T0…）') is None)

    me = P(206, 'data: 审核 GRB181120A', '2026-10-24T19:18:38Z', 'syfu95')
    conf, earlier = decide({'GRB181120A'}, me,
                           [(P(171, 'data: 审核 GRB181120A', '2026-10-24T15:05:29Z', 'Rusty-Harpoon'),
                             {'GRB181120A'})])
    check('#206 是后开者 → 阻断', earlier is True)
    check('冲突条目指向先开者 #171', bool(conf) and conf[0][0]['number'] == 171)

    conf2, earlier2 = decide({'GRB181120A'}, P(171, 'data: 审核 GRB181120A', '2026-10-24T15:05:29Z'),
                             [(P(206, 'data: …', '2026-10-24T19:18:38Z'), {'GRB181120A'})])
    check('#171 是先开者 → 不阻断', earlier2 is False)

    claim = P(227, 'claim: GRB210708A', '2026-10-25T05:26:52Z', 'Rusty-Harpoon', draft=True)
    conf3, earlier3 = decide({'GRB210708A'}, P(999, 'data: 审核 GRB210708A', '2026-10-25T06:00:00Z'),
                             [(claim, {'GRB210708A'} & {claimed_source(claim['title'])})])
    check('claim draft PR 也能挡住后来者', earlier3 is True and conf3[0][0]['number'] == 227)

    check('无重叠 → 不阻断', decide({'GRB180818A'}, me, [(claim, set())])[1] is False)
    print(f'\n{bad} 个用例失败' if bad else '\n全部用例通过')
    return 0 if not bad else 1


# ─── 主流程 ─────────────────────────────────────────────────────────────────
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo', default=os.environ.get('GITHUB_REPOSITORY'))
    ap.add_argument('--pr', default=os.environ.get('GITHUB_EVENT_PULL_REQUEST_NUMBER'))
    ap.add_argument('--strict', action='store_true',
                    help='后开者非零退出（CI 用这个让 PR 变红）；默认恒 0')
    ap.add_argument('--comment', action='store_true', help='在 PR 上发/更新挤占评论（需写权限）')
    ap.add_argument('--label', default='', help='冲突时打/撒的 label 名（需写权限）')
    ap.add_argument('--dry-run', action='store_true', help='只打印将要做的写操作')
    ap.add_argument('--selftest', action='store_true')
    args = ap.parse_args()

    if args.selftest:
        return selftest()

    token = os.environ.get('GH_TOKEN') or os.environ.get('GITHUB_TOKEN') or ''
    if not (args.repo and args.pr):
        print('::notice::同源挤占检查跳过：缺少 repo / PR 号（非 PR 事件或未配置）')
        return 0
    if not token:
        print('::notice::同源挤占检查跳过：没有可用 token')
        return 0

    me = int(args.pr)
    try:
        me_info = gh(f'/repos/{args.repo}/pulls/{me}', token)
        mine = occupancy(args.repo, me_info, token)
        if not mine:
            print('::notice::本 PR 未占用任何源（文档/线索卡类，或 claim PR 标题未写源 ID）——无挤占可查')
            return 0
        others = []
        for pr in open_prs(args.repo, token):
            if pr['number'] == me:
                continue
            shared = mine & occupancy(args.repo, pr, token)
            if shared:
                others.append((pr, shared))
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, ValueError) as e:
        # 取数失败绝不把源判成空闲，也绝不因此阻断
        print(f'::notice::同源挤占检查跳过：取 GitHub 数据失败（{e}）')
        return 0

    conf, has_earlier = decide(mine, me_info, others)

    if not conf:
        print(f'本 PR 占用的源 {sorted(mine)} 无其他 open PR 触碰——认领无冲突')
    else:
        for pr, shared, earlier in conf:
            print(f'::warning::源 {", ".join(shared)} 同时出现在 #{me} 与 #{pr["number"]}'
                  f'（{pr["user"]["login"]}，{pr["created_at"]}，'
                  f'{"**先于本 PR**" if earlier else "晚于本 PR"}）：挤占——'
                  f'一个源同时只应有一个未过期认领（《数据审核提示词》§2 第 3 条 / §5 第 6 条）')
            print(f'::notice::#{pr["number"]} {pr["title"][:80]}'
                  f'（{"先开" if earlier else "后开"}，{"draft" if pr.get("draft") else "正式"}）')
        if has_earlier:
            print('::error::本 PR 是后开者：应让位（关闭本 PR 或换源），或在其 PR 下按 §5 第 6 条沟通 48 小时')
        print('::notice::判据是**实时 open PR**（含 claim 标题），不是 audit/state.tsv 快照；'
              '本地核对用 `python3 tools/audit_queue.py --live --id <源ID>`')

    if args.comment or args.label:
        try:
            if args.comment:
                if conf:
                    upsert_comment(args.repo, me, token, render_comment(mine, me_info, conf),
                                   dry_run=args.dry_run)
                else:
                    delete_marked_comment(args.repo, me, token, dry_run=args.dry_run)
            if args.label:
                set_label(args.repo, me, token, args.label, bool(conf), dry_run=args.dry_run)
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, ValueError) as e:
            print(f'::notice::挤占评论/label 写入失败（{e}）——'
                  f'fork PR 的 GITHUB_TOKEN 是只读的，请改用 pull_request_target 触发；判定结论不受影响')

    return 1 if (args.strict and has_earlier) else 0


if __name__ == '__main__':
    sys.exit(main())
