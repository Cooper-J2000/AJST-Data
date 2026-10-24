# `audit/` —— 认领快照（机器生成）· 维护者预留（人工维护）· 线索卡（人工维护）

`state.tsv` 只做一件事：让"某个源已经有人在审"对所有协作者可见。多个外部 agent 并行审核时，
这是避免重复劳动的**唯一可见层**——因为 `claimed`（有人在做）这个状态不在数据文件里，只在 PR 上。
同目录的 `leads/` 是另一件独立的事：人工维护的**多目标文献线索卡**，只读、不参与状态机（见文末）。

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
| `state` | `claimed`＝open **draft** PR（认领中）；`in-review`＝open 正式 PR；`stale-claim` / `stale-pr`＝超过 TTL 未更新，可接手。`reserved`（维护者预留）**不写入本文件**，见 `reserved.tsv` |
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

## `reserved.tsv` —— 维护者预留（人工维护，**参与**状态机）

维护者要把一批源**暂时自留**时，写进 `audit/reserved.tsv`——不是开 draft PR，更不是改
`info/*.json`。被预留的源由 `audit_queue.py` 派生为 `reserved` 状态：**不进入**
`--limit` / `--bucket` / `--pack` 候选，`--id <源ID>` 必显示预留人与截止日，`--reserved` 列全部。

| 列 | 含义 |
|---|---|
| `source_id` | 源 id（与 `info/<id>.json` 同名；允许写尚未入库的源，工具会标「尚未入库」） |
| `holder` | 预留人，`人名@角色`（如 `ajst@maintainer`）；`?`＝该行缺字段，预留仍生效 |
| `since` / `until` | 预留起始 / **截止日**（`until` 必填：无截止日＝硬锁） |
| `reason` | 为什么自留（外部协作者看到的就是这句） |
| `ref` | 关联记录（Issue / PR / 内部批次），可空 |

规则：

- **外部协作者：不得认领、不得开 `claim: <源ID>` PR、不得改这个文件。** 确需推进就在 Issue 里说明理由。
- **到期**：`until` 过后派生为 `reserved-expired`，可认领性降为 `takeover` —— 走与过期认领相同的
  **48 小时沟通**协议（先在相关 Issue/PR 留言再接手）。
- **台账问题只告警**：缺 `holder`、重复、`until` 非法 → `--reserved` 末尾列出、`validate.py` 警告；
  缺 `holder` 的行按 `?` **保留**（fail-closed：坏行不等于放人）。
- 续期＝改 `until` 一行；撤销＝删行；源已 `reviewed` 的残留行由 `validate.py` 警告、维护者清理。
- **不写进 `info/*.json`**：预留是协调状态，不是数据；进了数据文件，每次预留都会变成一次数据 diff。
- **不进 `state.tsv`**：后者是 PR 认领的**派生产物**（机器生成，勿手改），`reserved` 是人写的权威记录；
  快照头部只带 `reserved=N` 计数，避免只看快照的人把自留源当 `free`。
- **PR 守卫（警告级）**：`python3 tools/audit_queue.py --check-reserved --base origin/main`
  在 PR 里检查改动是否触及自留源，命中就打 `::warning::` 注解——**不阻断**。

与 `leads/` 的区别：线索卡**不参与**状态机（有卡 ≠ 有人在做）；预留**参与**（`reserved` 是一个状态）。

## `denied.tsv` —— 已否证源（人工维护，**不参与**状态机）

维护者裁定**删除**的源写进 `audit/denied.tsv`：触发或探测已被官方撤回、与另一源重复、或本就是
噪声涨落。它们已从 `info/` 与 `lc/` 删除，**不该再存在**——这张表的作用是让人在导入/复审时
立刻知道「这个源已经被否证过、判据是什么」，而不是重新审一遍已被推翻的天体记录（Issue #183）。

| 列 | 含义 |
|---|---|
| `source_id` | 被否证的源 id（已删除，不应再出现 `info/<id>.json`） |
| `reason_code` | `retracted`（触发/探测被官方撤回）\| `duplicate`（并入另一源）\| `noise`（噪声涨落）\| `other` |
| `evidence` | 判据：GCN 号 + 原文结论 / DOI / commit，必须能独立复核 |
| `decided_by` / `date` | 裁定人与日期 |
| `ref` | 关联 PR / commit / Issue |

规则：

- **审核前必查**：`grep <源ID> audit/denied.tsv`（或 `python3 tools/audit_queue.py --id <源ID>`，
  命中会直接回「已被否证」）。命中就停手，不要认领、不要开 PR、不要重建。
- **源复活＝报警**：`validate.py` 发现 denied 里的源又出现 `info/` 或 `lc/` 文件就警告——那说明
  源被重新导入或误恢复了（`bot_created` 是一次性建库，库没有常态化导入管线；见 Issue #183），
  应按 `evidence` 再否证一次。
- **不参与状态机**：它没有 `info` 文件，本来就不在可认领队列里；`audit_queue.py --denied` 只读展示。
- **删除要留得下判据**：`evidence` / `decided_by` / `date` / `ref` 缺一项就告警。只写「已删除」
  的记录等于没写——下一个人还得从头查一遍 GCN。

## 不要做的事


- **不要手改 `state.tsv`**：它是派生产物，下次运行即被覆盖；审核 PR 里出现对它的改动会被要求撤掉。
- 不要把它当数据源入库（数据在 `info/`、`lc/`）。
- 不要把 `leads/` 里的卡当成认领记录或核验结果：有卡 ≠ 有人在做，卡里的数值也未经核验。
- 不要把 `reserved.tsv` 当成"谁在审"的记录：它是维护者的**授权性预留**；外部协作者开工的唯一方式是
  开 `claim: <源ID>` draft PR。也不要用 draft PR 去占用一批源（那会把 PR 列表淹掉）。

## `leads/` —— 多目标文献线索卡（人工维护）

一篇文献常同时给出多个库内源的数据。审核员在审自己的源时顺手读到的其他源数据，写进
`audit/leads/<源ID>.md` 交给下一位审核员，**随被审源的同一个数据 PR 提交**（《数据审核提示词》§3.11）。

- **不参与状态机**：`audit_queue.py` 只读取展示。源的 `free/claimed/reviewed` 判定仍只看
  `info/*.json` 的 `extra_data.audit` 与改动了 `info/<id>`、`lc/<id>` 的 open PR。
- 所以写卡**绝不能**碰目标源的 `info/lc`、不能写它的 `audit` 标记、不能把它的 ID 放进 PR 标题
  （否则会被当成认领，误占他人的工作入口）。
- **增量门槛**：只写「库内 GCN/目录检索拿不到的量、不同口径、新正式文献引用」；纯汇总表转引 GCN 的行
  不开源级卡（2026-10-24 起）。判据见 [`leads/README.md`](leads/README.md)。
- **多源文献（≥3 个库内源）先建文献级索引卡** `leads/papers/<paper_key>.md`（一篇一张），
  它只做索引、不代替源级卡；契约见 [`leads/papers/README.md`](leads/papers/README.md)，
  查看 `python3 tools/audit_queue.py --paper <paper_key>`。
- 接手的审核员仍须自己打开原文逐值核验；审完（或否证）在**自己的 PR** 里删掉这张卡。
- 格式、模板与硬性禁令：见 [`leads/README.md`](leads/README.md)。
- 查看：`python3 tools/audit_queue.py --leads`；单源：`--id <源ID>`；队列里带 `+lead` 标记。

## Issue 模板（审核中发现的系统性问题 / 未覆盖情形）

审核中遇到本提示词未覆盖的**系统性**情形（跨多源、或涉及导入管线）时，另开 Issue 记档；
数据 PR 里不就地批量改（见《数据审核提示词》§9.4/§9.5）。Issue 正文按下列模板，**必须自带复现路径**，
不要让读者依赖别人机器上的临时文件：

```markdown
## 现象
（一两句：哪个字段/哪个环节偏差，方向与量级）

## 影响范围
- 命中源数 / 全库源数；是否集中在某目录、某年代、某导入批次
- 逐源明细（可折叠，或附一段可复现的统计命令）

## 复现
```bash
python3 tools/<脚本>.py [--tsv /tmp/out.tsv]     # 只读；脚本随 Issue 一起进 tools/
```

## 建议口径
（怎么改、改哪一侧：目录导入管线 / 现有数据 / 契约文档）

## 已有数据是否需要批改
（是/否、批改的粒度与可回滚方式；不批改时是否需要逐源在审核中处理）

## 相关
（关联 PR / Issue / 目录 README）
```

已开示例：#67（Fermi 系 T0 漏扣闰秒）、#68（`t0_basis=meta_trigger` 不可信）、#69（alias 伪形与 float32 坐标残渣）。

## 认领纪律（摘要；全文见《数据审核提示词》）

- 开工第一件事：开 draft PR 认领，标题 `claim: <源ID>`。
- 一个源同时只应有一个未过期认领：普通源 **14 天**、`lc` 超过 1000 行的巨源 **30 天**（自最后一次更新算起）。
- 遇到别人**未过期**的认领：在该 PR 评论询问并等 **48 小时**；仍无响应再接手，并在自己的 PR 里说明。
- 遇到**已过期**认领：可直接开工，同时在对方 PR 上留言。
