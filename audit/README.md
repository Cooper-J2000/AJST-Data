# `audit/` —— 审核认领快照（机器生成，**勿手改**）

本目录只做一件事：让"某个源已经有人在审"对所有协作者可见。多个外部 agent 并行审核时，
这是避免重复劳动的**唯一可见层**——因为 `claimed`（有人在做）这个状态不在数据文件里，只在 PR 上。

## `state.tsv` 是什么

- **谁生成**：`.github/workflows/audit-snapshot.yml` 每日 04:20 UTC（12:20 CST）自动运行
  `python3 tools/audit_queue.py --emit-snapshot`；本地也可随时重建。正常情况下
  **每天会产生一条 1 行的小提交**（`snapshot_at` 每天都变）——这是刻意保留的"心跳"：
  文件停更就说明 Action 挂了，工具对超过 3 天的快照告警正是据此判定。工作流里那步
  "内容有变化才提交"只用于防同一分钟内重复运行。
- **为什么需要**：`reviewed` 状态在 `info/*.json` 的 `extra_data.audit` 里，`free` 是默认态，
  但 `claimed` / `in-review` 只活在 GitHub 的 open PR 上。没有 `gh`/API 访问的协作者
  （或没登录）看到的将是"全部未审核"，于是重复挑同一个源。
- **只列仓库文件里看不到的状态**：被 open PR 占用的源。`reviewed` 见各 `info/*.json`；
  `free` 就是没被列出来的那些。

## 列

| 列 | 含义 |
|---|---|
| `source_id` | 源 id（与 `info/<id>.json` 同名） |
| `state` | `claimed`＝open **draft** PR（认领中）；`in-review`＝open 正式 PR；`stale-claim` / `stale-pr`＝超过 TTL 未更新，可接手 |
| `holder` | PR 作者（GitHub login） |
| `since` / `updated` | PR 创建 / 最后更新日期 |
| `pr` | PR 编号（同一源多条用逗号分隔） |

文件头注释带 `snapshot_at`、`healthy`、`open_sources`、`reviewed=N/M`，可直接当进度看板读。

## 怎么读（重要）

**快照只能用来"排除已占用"，不能用来"确认空闲"。** 它最长滞后 24 小时：两个人都读到旧快照，
就会双双开工，碰撞原样回来。判据永远是实时查询：

```bash
python3 tools/audit_queue.py --live        # 工具内部走 gh，以实时为准
gh pr list --search "in:title <源ID>"       # 或手查
```

工具在三处会提醒你：文件不存在、`snapshot_at` 超过 **3 天**（视为过期，占用记录标 `?`）时，
输出头部会告警并拒绝把快照当作"空闲"的证据。

## 不要做的事

- **不要手改 `state.tsv`**：它是派生产物，下次运行即被覆盖；审核 PR 里出现对它的改动会被要求撤掉。
- 不要把它当数据源入库（数据在 `info/`、`lc/`）。

## 认领纪律（摘要；全文见《数据审核提示词》）

- 开工第一件事：开 draft PR 认领，标题 `claim: <源ID>`。
- 一个源同时只应有一个未过期认领：普通源 **14 天**、`lc` 超过 1000 行的巨源 **30 天**（自最后一次更新算起）。
- 遇到别人**未过期**的认领：在该 PR 评论询问并等 **48 小时**；仍无响应再接手，并在自己的 PR 里说明。
- 遇到**已过期**认领：可直接开工，同时在对方 PR 上留言。
