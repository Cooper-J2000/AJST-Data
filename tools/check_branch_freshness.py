#!/usr/bin/env python3
"""PR 分支落后检查（只读，仅标准库）。

作用：把「这个 PR 是不是基于过期 main」变成 **PR 页面上可见的事实**。
背景（《数据审核提示词》§2 第 9 条 / §5 第 7 条，2026-10-24 新增）：维护者会直接改
`info/`、`lc/`、`tools/` 与文档；外部 agent 若不 `git pull`，就基于过期数据判断，
我方改动在它的下一次任务里看不见。

做法：调 GitHub compare API 取 `<PR head>...<base>`——返回的 `ahead_by` 就是本分支
**落后 base 的提交数**，`commits` 是落后了哪几个（含标题）。输出 Actions 注解
`::warning::` / `::notice::`，**退出码恒 0**：警告级，永不阻断合并。

用法 / Usage:
  python3 tools/check_branch_freshness.py                 # CI：读环境变量
  python3 tools/check_branch_freshness.py --repo Cooper-J2000/AJST-Data --head <sha> --base main
环境变量：GITHUB_REPOSITORY、GITHUB_EVENT_PULL_REQUEST_HEAD_SHA、GITHUB_BASE_REF、
         GH_TOKEN（或 GITHUB_TOKEN）
"""
import argparse
import json
import os
import sys
import urllib.error
import urllib.request

MAX_LIST = 10
API = 'https://api.github.com'


def fetch_compare(repo, head, base, token, timeout=30):
    url = f'{API}/repos/{repo}/compare/{head}...{base}'
    req = urllib.request.Request(url, headers={
        'Authorization': f'Bearer {token}',
        'Accept': 'application/vnd.github+json',
        'User-Agent': 'ajst-data-branch-freshness',
    })
    with urllib.request.urlopen(req, timeout=timeout) as fh:
        return json.load(fh)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo', default=os.environ.get('GITHUB_REPOSITORY'))
    ap.add_argument('--head', default=os.environ.get('GITHUB_EVENT_PULL_REQUEST_HEAD_SHA'))
    ap.add_argument('--base', default=os.environ.get('GITHUB_BASE_REF'))
    args = ap.parse_args()
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
        return 0

    behind = int(d.get('ahead_by') or 0)     # head...base ⇒ base 领先 head 的提交数 = 本分支落后的提交数
    commits = d.get('commits') or []
    if behind <= 0:
        print(f'分支与 {args.base} 同步（落后 0 个提交）——基于最新 main，好')
        return 0

    print(f'::warning::本分支落后 {args.base} {behind} 个提交——请先 `git pull --rebase origin {args.base}` '
          f'再继续（《数据审核提示词》§2 第 9 条 / §5 第 7 条）。落后的提交如下：')
    for c in commits[:MAX_LIST]:
        sha = (c.get('sha') or '')[:8]
        subj = (c.get('commit', {}).get('message') or '').splitlines()[0][:80]
        print(f'::notice::落后 {args.base}：{sha} {subj}')
    if behind > MAX_LIST:
        print(f'::notice::另有 {behind - MAX_LIST} 个落后提交未列出，见 GitHub 的 "N commits behind" 提示')
    return 0


if __name__ == '__main__':
    sys.exit(main())
