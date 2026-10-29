#!/usr/bin/env python3
"""PR 范围守卫 —— 「一源一 PR」+ 改动路径白名单，把越界变成 CI 上看得见且**会红**的事实。

背景（2026-10-29 批次 155 个 PR 实测暴露的两个洞口）：
  1. `check_duplicate_claim.py` 只看「同一个源被多个 open PR 占用」，看不见
     **一个 PR 改多个源**：#490（`GRB220711B`+`GRB220712B`）、#495（`GRB220403A`+`GRB220403B`）
     都是 §3.7 源级处置（迁入/幽灵条目），一路绿到维护者手检才被拦下。
  2. 数据 PR 顺带改配置/工具文件无人拦：#550 顺手在仓库根 `filters.json` 加了 `infra-Kp` 键。

判据（提示词 §3.6 / §7、AGENTS.md 第 5 条）：
  * 本 PR 的 `info/<id>.json`、`lc/<id>.csv` 源集合必须 ≤ 1；
  * 改动路径只能是这些数据文件 + `audit/leads/*.md`（§3.11 卡）+ 文档白名单；
  * **维护者**（author_association ∈ OWNER/MEMBER/COLLABORATOR）的 PR 豁免范围检查
    （改 `tools/`、文档、配置走维护者 PR）；
  * 文档-only PR（只改提示词/AGENTS/SCHEMA/README 等）单独放行，不要求带源。

用法 / Usage:
  python3 tools/check_pr_scope.py --selftest              # 离线跑判定用例（不联网）
  python3 tools/check_pr_scope.py --pr 550                # 本地查单个 PR（需 gh token）
  python3 tools/check_pr_scope.py --files a.txt           # 本地查文件清单（每行一个路径）
  python3 tools/check_pr_scope.py --strict                # CI：读环境变量，违规非零退出
环境变量：GITHUB_REPOSITORY、GITHUB_EVENT_PULL_REQUEST_NUMBER、（可选）
          GITHUB_EVENT_PULL_REQUEST_AUTHOR_ASSOCIATION、GH_TOKEN / GITHUB_TOKEN
退出码：0 = 通过（可带警告）；1 = 有 ERROR；2 = 查询失败（拿不到文件清单，不要当成通过）
"""
import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request

API = 'https://api.github.com'
DATA_RE = re.compile(r'^(?:info|lc)/(?P<src>[^/]+)\.(?:json|csv)$')
LEAD_RE = re.compile(r'^audit/leads/(?:papers/)?[^/]+\.md$')
CLAIM_RE = re.compile(r'^\s*claim\s*[:：]\s*(?P<src>[A-Za-z0-9_.\-]+)', re.I)
# 标题里的源名 token（与维护者侧 review.py 同一套；不认 IceCube-/HAWC- 会误判，见 PR#563）
TITLE_SRC_RE = re.compile(
    r'\b(GRB\d{6}[A-Z]?|EP\d{6}[a-z]|AT\d{4}[a-z]{3}|SN\d{4}[a-z]{2}|ZTF\d+[a-z]+'
    r'|IceCube-\d{6}[A-Z]?|HAWC-\d{6}[A-Z]?)\b')
MAINTAINER_ASSOC = {'OWNER', 'MEMBER', 'COLLABORATOR'}
# 文档-only PR 的白名单（提示词 §9：文档修订走单独 PR，不必带源）
DOC_FILES = {
    'AGENTS.md', 'README.md', 'SCHEMA.md', 'CONTRIBUTING.md',
    '数据审核提示词.md', '数据统一列定义.md', '部分数据说明及导入记录.md',
    'audit/README.md', 'audit/leads/README.md', 'audit/leads/papers/README.md',
}
MAX_FILE_PAGES = 3          # 100/页；超了只警告（不阻断），避免大 PR 卡住


def gh(path, token, timeout=30):
    req = urllib.request.Request(f'{API}{path}', headers={
        'Authorization': f'Bearer {token}',
        'Accept': 'application/vnd.github+json',
        'User-Agent': 'ajst-data-pr-scope-guard',
    })
    with urllib.request.urlopen(req, timeout=timeout) as fh:
        return json.loads(fh.read().decode() or '{}')


def pr_files(repo, number, token):
    """→ (文件名列表, 是否被截断)"""
    out, truncated = [], False
    for page in range(1, MAX_FILE_PAGES + 1):
        batch = gh(f'/repos/{repo}/pulls/{number}/files?per_page=100&page={page}', token)
        out.extend(f.get('filename') or '' for f in batch)
        if len(batch) < 100:
            break
    else:
        truncated = True
    return [f for f in out if f], truncated


def is_doc(path):
    return path in DOC_FILES or path.startswith('.github/')


def evaluate(files, title='', assoc=''):
    """纯函数：文件清单 → (errors, warnings, sources)。--selftest 直接吃这一层。"""
    errors, warnings = [], []
    sources = set()
    for f in files:
        m = DATA_RE.match(f)
        if m:
            sources.add(m.group('src'))
    if assoc.upper() in MAINTAINER_ASSOC:
        return [], [f'维护者 PR（author_association={assoc}）：范围检查豁免'], sources
    if not files:                      # 纯认领 PR（只有空提交）没有任何改动文件
        return [], [], sources
    bad = [f for f in files if not (DATA_RE.match(f) or LEAD_RE.match(f) or is_doc(f))]
    data_side = [f for f in files if DATA_RE.match(f) or LEAD_RE.match(f)]
    if not data_side and not bad:      # 文档-only PR：提示词 §9 允许单独 PR，不要求带源
        return [], [], sources
    if bad:
        errors.append(
            '越界文件：' + '、'.join(sorted(bad)[:5]) + (f' 等 {len(bad)} 个' if len(bad) > 5 else '')
            + '（数据 PR 只允许 info/<源ID>.json、lc/<源ID>.csv、audit/leads/*.md；'
              '配置/工具/文档改动请单独提 PR —— 提示词 §7）')
    if len(sources) > 1:
        errors.append(
            '一源一 PR 违规：本 PR 触碰 ' + str(len(sources)) + ' 个源（'
            + '、'.join(sorted(sources)) + '）。§3.7 源级处置也要拆成两个 PR（保留源 / 待删源各一个），'
            '除非维护者在本 PR 下明确裁定接受（提示词 §3.6 / §7）')
    if sources:
        claim = CLAIM_RE.match(title or '')
        if claim and claim.group('src') not in sources:
            warnings.append(f'标题 claim: {claim.group("src")} 与 diff 源 {sorted(sources)} 不一致')
        elif not claim:
            t_ids = set(TITLE_SRC_RE.findall(title or ''))
            if t_ids and not (t_ids & sources):
                warnings.append(f'标题源 {sorted(t_ids)} 与 diff 源 {sorted(sources)} 不一致'
                                '（确认标题写的是本源 ID，别人靠 `in:title` 查认领）')
    return errors, warnings, sources


def report(pr_label, files, errors, warnings, sources, ci):
    say = (lambda m: print(f'::error::{m}')) if ci else (lambda m: print(f'  [ERROR] {m}'))
    sayw = (lambda m: print(f'::warning::{m}')) if ci else (lambda m: print(f'  [WARN ] {m}'))
    print(f'{pr_label}：{len(files)} 个改动文件，源 {sorted(sources) or "（无，纯文档/认领）"}')
    for w in warnings:
        sayw(w)
    for e in errors:
        say(e)
    print(f'  汇总：{len(errors)} 错误 / {len(warnings)} 警告 → '
          + ('FAIL' if errors else 'PASS'))
    return 0 if not errors else 1


SELFTEST_CASES = [
    ('单源数据 PR 通过', ['info/GRB200803A.json', 'lc/GRB200803A.csv'],
     'data: 审核 GRB200803A（补测光）', 'NONE', 0),
    ('带线索卡的数据 PR 通过', ['info/GRB200803A.json', 'lc/GRB200803A.csv',
                        'audit/leads/GRB190821A.md', 'audit/leads/papers/fong2015.md'],
     'data: 审核 GRB200803A', 'NONE', 0),
    ('两个源 → 违规', ['info/GRB220711B.json', 'lc/GRB220711B.csv',
                  'info/GRB220712B.json', 'lc/GRB220712B.csv'],
     'data: 审核 GRB220712B', 'NONE', 1),
    ('越界文件 → 违规', ['info/GRB000214.json', 'lc/GRB000214.csv', 'filters.json'],
     'data: 审核 GRB000214', 'NONE', 1),
    ('两源 + 越界 → 两条错误', ['info/A.json', 'lc/A.csv', 'info/B.json', 'tools/validate.py'],
     'data: 审核 A', 'NONE', 2),
    ('维护者 PR 豁免', ['tools/validate.py', 'tools/check_pr_scope.py', 'filters.json'],
     'tools: 新增 PR 范围守卫', 'OWNER', 0),
    ('文档-only PR 通过', ['数据审核提示词.md', 'AGENTS.md', '.github/PULL_REQUEST_TEMPLATE.md'],
     'docs: 契约修订', 'NONE', 0),
    ('纯认领 PR 通过', [], 'claim: GRB001019', 'NONE', 0),
    ('认领标题与源不一致只警告', ['info/GRB001019.json', 'lc/GRB001019.csv'],
     'claim: GRB010326A', 'NONE', 0),
]


def selftest():
    ok = True
    for name, files, title, assoc, want_err in SELFTEST_CASES:
        errors, warnings, sources = evaluate(files, title, assoc)
        good = len(errors) == want_err
        ok = ok and good
        print(('PASS' if good else 'FAIL') + f'\t{name}\t错误 {len(errors)}（期望 {want_err}）'
              + (f'\t警告 {len(warnings)}' if warnings else ''))
        if not good:
            for e in errors:
                print('      →', e)
    print('自检结果：' + ('全部通过' if ok else '有失败'))
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--pr', type=int)
    ap.add_argument('--files', help='本地文件清单（每行一个路径）')
    ap.add_argument('--repo', default=os.environ.get('GITHUB_REPOSITORY'))
    ap.add_argument('--title', default=os.environ.get('GITHUB_EVENT_PULL_REQUEST_TITLE', ''))
    ap.add_argument('--assoc', default=os.environ.get('GITHUB_EVENT_PULL_REQUEST_AUTHOR_ASSOCIATION', ''))
    ap.add_argument('--strict', action='store_true')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args()

    if a.selftest:
        return selftest()

    ci = bool(os.environ.get('GITHUB_ACTIONS'))
    if a.files:
        files = [x.strip() for x in open(a.files, encoding='utf-8') if x.strip()]
        title, assoc, label = a.title, a.assoc, f'文件清单 {a.files}'
    else:
        n = a.pr or int(os.environ.get('GITHUB_EVENT_PULL_REQUEST_NUMBER') or 0)
        token = os.environ.get('GH_TOKEN') or os.environ.get('GITHUB_TOKEN')
        if not n or not a.repo or not token:
            print('缺少 --pr / --repo / token（GH_TOKEN）：本地用法见文件头', file=sys.stderr)
            return 2
        try:
            files, truncated = pr_files(a.repo, n, token)
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, ValueError) as e:
            print(f'查询 PR 文件列表失败：{e}', file=sys.stderr)
            return 2
        if truncated:
            print(f'::warning::PR 改动文件超过 {MAX_FILE_PAGES * 100} 个，只检查了前 {len(files)} 个')
        if not a.title or not a.assoc:
            try:
                meta = gh(f'/repos/{a.repo}/pulls/{n}', token)
                title = a.title or (meta.get('title') or '')
                assoc = a.assoc or (meta.get('author_association') or '')
            except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, ValueError):
                title, assoc = a.title, a.assoc
        else:
            title, assoc = a.title, a.assoc
        label = f'PR #{n}'
    errors, warnings, sources = evaluate(files, title, assoc)
    return report(label, files, errors, warnings, sources, ci)


if __name__ == '__main__':
    sys.exit(main())
