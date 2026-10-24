#!/usr/bin/env python3
"""同源多 PR（认领挤占）守卫 —— 只读，警告级，退出码恒 0。

背景：认领状态有两个来源——`audit/state.tsv` 快照（每日生成、**明显滞后**）与实时 PR 查询。
只读快照的 agent 会把今天刚被认领的源判成 free，于是两个 agent 同时审同一个源
（实测 2026-10-23：`GRB141113A` 被 #100 与 #102 同时认领，快照停在 09:22Z，两个源都不在快照里）。

做法：列出**当前 PR 触碰的 info/lc 源**，再扫全部 open PR，找出触碰同一源的其他 PR。
多于一个就输出 `::warning::`，并指出**谁先开**（按 created_at）。判据一律是实时 PR 状态，
不碰快照——所以它给出的结论与 `tools/audit_queue.py --live` 一致。

用法 / Usage:
  python3 tools/check_duplicate_claim.py --pr 102                     # 本地：查某 PR
  python3 tools/check_duplicate_claim.py                              # CI：读环境变量
环境变量：GITHUB_REPOSITORY、GITHUB_EVENT_PULL_REQUEST_NUMBER、GH_TOKEN（或 GITHUB_TOKEN）
"""
import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request

API = 'https://api.github.com'
SRC_RE = re.compile(r'^(?:info|lc)/(?P<src>[^/]+)\.(?:json|csv)$')
MAX_PR_PAGES = 3          # 100/页；超过只提示，不阻断


def gh(url_path, token, timeout=30):
    req = urllib.request.Request(f'{API}{url_path}', headers={
        'Authorization': f'Bearer {token}',
        'Accept': 'application/vnd.github+json',
        'User-Agent': 'ajst-data-duplicate-claim-guard',
    })
    with urllib.request.urlopen(req, timeout=timeout) as fh:
        return json.load(fh)


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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo', default=os.environ.get('GITHUB_REPOSITORY'))
    ap.add_argument('--pr', default=os.environ.get('GITHUB_EVENT_PULL_REQUEST_NUMBER'))
    args = ap.parse_args()
    token = os.environ.get('GH_TOKEN') or os.environ.get('GITHUB_TOKEN') or ''

    if not (args.repo and args.pr):
        print('::notice::同源多 PR 检查跳过：缺少 repo / PR 号（非 PR 事件或未配置）')
        return 0
    if not token:
        print('::notice::同源多 PR 检查跳过：没有可用 token')
        return 0

    try:
        me = int(args.pr)
        mine = pr_sources(args.repo, me, token)
        if not mine:
            print('::notice::本 PR 未改动任何 info/lc 源（文档或线索卡类），无需查重')
            return 0
        others = []
        for pr in open_prs(args.repo, token):
            if pr['number'] == me:
                continue
            try:
                srcs = pr_sources(args.repo, pr['number'], token)
            except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, ValueError):
                continue
            shared = mine & srcs
            if shared:
                others.append((pr, shared))
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, ValueError) as e:
        print(f'::notice::同源多 PR 检查跳过：取 GitHub 数据失败（{e}）')
        return 0

    if not others:
        print(f'本 PR 触碰的源 {sorted(mine)} 无其他 open PR 触碰——认领无冲突')
        return 0

    me_pr = next((p for p in open_prs(args.repo, token) if p['number'] == me), None)
    me_created = me_pr['created_at'] if me_pr else ''
    for pr, shared in sorted(others, key=lambda x: x[0]['created_at']):
        earlier = pr['created_at'] < me_created
        print(f'::warning::源 {", ".join(sorted(shared))} 同时出现在 #{me} 与 #{pr["number"]}'
              f'（{pr["user"]["login"]}，{pr["created_at"]}，{"**先于本 PR**" if earlier else "晚于本 PR"}）：'
              f'挤占——一个源同时只应有一个未过期认领（《数据审核提示词》§2 第 3 条 / §5 第 6 条）')
        print(f'::notice::#{pr["number"]} {pr["title"][:80]}  （{"先开" if earlier else "后开"}，'
              f'{"正式" if not pr["draft"] else "draft"}）')
        if earlier:
            print('::notice::本 PR 是后开者：应让位（关闭本 PR 或换源），或在其 PR 下按 §5 第 6 条沟通 48 小时')
    print('::notice::判据是**实时 open PR**，不是 audit/state.tsv 快照——快照滞后（每日一次），'
          '本地核对认领请用 `python3 tools/audit_queue.py --live --id <源ID>`')
    return 0


if __name__ == '__main__':
    sys.exit(main())
