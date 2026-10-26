# 文献索引：in 't Zand+2026（BeppoSAX-WFC 快速 X 射线暂现源目录）

- paper_key: intzand2026
- paper: in 't Zand, Guidorzi, Heise, Amati, Kuulkers, Frontera, Gianfagna & Piro 2026, A&A 711, A60（DOI 10.1051/0004-6361/202558641；arXiv:2512.16845）。VoR 机读表 CDS J/A+A/711/A60（tablea2.dat = 表 1，tablea1.dat = 表 2）已于 2026-10-27 下载核对；A&A 网页/PDF 被反爬 403，正文按 arXiv v2（2026-10-26 更新）读取，表值与 CDS 机读表一致。
- date: 2026-10-27
- helper: fsy（审核 GRB991217 时读取）
- sources: GRB971024, GRB971227, GRB980326, GRB980519, GRB981226, GRB990217, GRB990627, GRB990704, GRB990806, GRB990907, GRB991014, GRB991105, GRB991106, GRB991217, GRB000214, GRB000416, GRB000424, GRB000528, GRB000529, GRB000615, GRB000620, GRB000630, GRB001011, GRB001109, GRB010213, GRB010214, GRB010220, GRB010324, GRB010412, GRB011030, GRB020321, GRB020322, GRB020409, GRB020410

## 为什么是文献级卡

该文用 BeppoSAX/WFC 1996-06 至 2002-04 数据统一搜索 149 个快速 X 射线暂现源（FXT），给出逐源的 **MJD(UTC) 事件起始时刻、T90 与误差、R.A./Dec.、68% 位置误差、WFC/GRBM 峰值流量、软度比、类型与证认**（表 1；CDS tablea2.dat）。表 2（tablea1.dat）另给幂律谱拟合（NH、光子指数、2–30 keV 流量）。全文**没有光学/射电光变表**，也没有逐源的光学测光。

表 1 的 ID 与库内 `transient_id` 机械匹配得 37 个；剔除 3 个歧义/非 GRB 行后列 34 个库内源：
- `000210`：目录 identification 写 `GRB990210`（与库内 GRB000210 的对应关系未核），不计入；
- `010119`：目录行类型为 Flare star（Algol flare 3），与库内 GRB010119 不是同一事件，不计入；
- `010324b`：目录行类型为 SFXT（AX J1845.0-0433），与 GRB010324 无关；GRB010324 只对应 `010324a`（GRB）。

**匹配为 ID 机械匹配，未逐源核对**；接手者使用某源行前须自行打开 tablea2.dat 核对位置/类型。

## 涉及源一览

> 除 GRB991217（本源，已在本 PR 审核）外，其余 33 源均为 `mention-only`：只做了 ID 匹配与表结构核对，未提取、未去重、未换算 T0。`源级卡` 全部「无」。

| 源 | 表号 | 源级卡 | status | 增量判读 |
|---|---|---|---|---|
| GRB971024 | 表 1 / tablea2.dat | 无 | mention-only | 目录参数（MJDstart/T90/RA/Dec/峰值流量），无测光；按 §3.11 不开源级卡 |
| GRB971227 | 表 1 / tablea2.dat | 无 | mention-only | 目录参数（MJDstart/T90/RA/Dec/峰值流量），无测光；按 §3.11 不开源级卡 |
| GRB980326 | 表 1 / tablea2.dat | 无 | mention-only | 目录参数（MJDstart/T90/RA/Dec/峰值流量），无测光；按 §3.11 不开源级卡 |
| GRB980519 | 表 1 / tablea2.dat | 无 | mention-only | 目录参数（MJDstart/T90/RA/Dec/峰值流量），无测光；按 §3.11 不开源级卡 |
| GRB981226 | 表 1 / tablea2.dat | 无 | mention-only | 目录参数（MJDstart/T90/RA/Dec/峰值流量），无测光；按 §3.11 不开源级卡 |
| GRB990217 | 表 1 / tablea2.dat | 无 | mention-only | 目录参数（MJDstart/T90/RA/Dec/峰值流量），无测光；按 §3.11 不开源级卡 |
| GRB990627 | 表 1 / tablea2.dat | 无 | mention-only | 目录参数（MJDstart/T90/RA/Dec/峰值流量），无测光；按 §3.11 不开源级卡 |
| GRB990704 | 表 1 / tablea2.dat | 无 | mention-only | 目录参数（MJDstart/T90/RA/Dec/峰值流量），无测光；按 §3.11 不开源级卡 |
| GRB990806 | 表 1 / tablea2.dat | 无 | mention-only | 目录参数（MJDstart/T90/RA/Dec/峰值流量），无测光；按 §3.11 不开源级卡 |
| GRB990907 | 表 1 / tablea2.dat | 无 | mention-only | 目录参数（MJDstart/T90/RA/Dec/峰值流量），无测光；按 §3.11 不开源级卡 |
| GRB991014 | 表 1 / tablea2.dat | 无 | mention-only | 目录参数（MJDstart/T90/RA/Dec/峰值流量），无测光；按 §3.11 不开源级卡 |
| GRB991105 | 表 1 / tablea2.dat | 无 | mention-only | 目录参数（MJDstart/T90/RA/Dec/峰值流量），无测光；按 §3.11 不开源级卡 |
| GRB991106 | 表 1 / tablea2.dat | 无 | mention-only | 目录参数（MJDstart/T90/RA/Dec/峰值流量），无测光；按 §3.11 不开源级卡 |
| GRB991217 | 表 1 / tablea2.dat（ID 991217 行） | 无（本源已在本 PR 审核） | extracted | 已采用 T90、精化位置与类型；见 `info/GRB991217.json` 与 PR #316 |
| GRB000214 | 表 1 / tablea2.dat | 无 | mention-only | 目录参数（MJDstart/T90/RA/Dec/峰值流量），无测光；按 §3.11 不开源级卡 |
| GRB000416 | 表 1 / tablea2.dat | 无 | mention-only | 目录参数（MJDstart/T90/RA/Dec/峰值流量），无测光；按 §3.11 不开源级卡 |
| GRB000424 | 表 1 / tablea2.dat | 无 | mention-only | 目录参数（MJDstart/T90/RA/Dec/峰值流量），无测光；按 §3.11 不开源级卡 |
| GRB000528 | 表 1 / tablea2.dat | 无 | mention-only | 目录参数（MJDstart/T90/RA/Dec/峰值流量），无测光；按 §3.11 不开源级卡 |
| GRB000529 | 表 1 / tablea2.dat | 无 | mention-only | 目录参数（MJDstart/T90/RA/Dec/峰值流量），无测光；按 §3.11 不开源级卡 |
| GRB000615 | 表 1 / tablea2.dat | 无 | mention-only | 目录参数（MJDstart/T90/RA/Dec/峰值流量），无测光；按 §3.11 不开源级卡 |
| GRB000620 | 表 1 / tablea2.dat | 无 | mention-only | 目录参数（MJDstart/T90/RA/Dec/峰值流量），无测光；按 §3.11 不开源级卡 |
| GRB000630 | 表 1 / tablea2.dat | 无 | mention-only | 目录参数（MJDstart/T90/RA/Dec/峰值流量），无测光；按 §3.11 不开源级卡 |
| GRB001011 | 表 1 / tablea2.dat | 无 | mention-only | 目录参数（MJDstart/T90/RA/Dec/峰值流量），无测光；按 §3.11 不开源级卡 |
| GRB001109 | 表 1 / tablea2.dat | 无 | mention-only | 目录参数（MJDstart/T90/RA/Dec/峰值流量），无测光；按 §3.11 不开源级卡 |
| GRB010213 | 表 1 / tablea2.dat | 无 | mention-only | 目录参数（MJDstart/T90/RA/Dec/峰值流量），无测光；按 §3.11 不开源级卡 |
| GRB010214 | 表 1 / tablea2.dat | 无 | mention-only | 目录参数（MJDstart/T90/RA/Dec/峰值流量），无测光；按 §3.11 不开源级卡 |
| GRB010220 | 表 1 / tablea2.dat | 无 | mention-only | 目录参数（MJDstart/T90/RA/Dec/峰值流量），无测光；按 §3.11 不开源级卡 |
| GRB010324 | 表 1 / tablea2.dat（ID 010324a 行） | 无 | mention-only | 目录参数，无测光；010324b 为 SFXT（AX J1845.0-0433），已剔除 |
| GRB010412 | 表 1 / tablea2.dat | 无 | mention-only | 目录参数（MJDstart/T90/RA/Dec/峰值流量），无测光；按 §3.11 不开源级卡 |
| GRB011030 | 表 1 / tablea2.dat | 无 | mention-only | 目录参数（MJDstart/T90/RA/Dec/峰值流量），无测光；按 §3.11 不开源级卡 |
| GRB020321 | 表 1 / tablea2.dat | 无 | mention-only | 目录参数（MJDstart/T90/RA/Dec/峰值流量），无测光；按 §3.11 不开源级卡 |
| GRB020322 | 表 1 / tablea2.dat | 无 | mention-only | 目录参数（MJDstart/T90/RA/Dec/峰值流量），无测光；按 §3.11 不开源级卡 |
| GRB020409 | 表 1 / tablea2.dat | 无 | mention-only | 目录参数（MJDstart/T90/RA/Dec/峰值流量），无测光；按 §3.11 不开源级卡 |
| GRB020410 | 表 1 / tablea2.dat | 无 | mention-only | 目录参数（MJDstart/T90/RA/Dec/峰值流量），无测光；按 §3.11 不开源级卡 |

## 增量门槛判读

- **不满足源级卡条件 1**：该文给的是目录级参数，不是 GCN/目录检索拿不到的测光表；没有逐源光学/射电数值。
- **条件 2（不同口径）仅系统性存在**：表 1 的 `MJD(UTC)` 是**事件起始**（T90 起点），与 GCN 触发时刻可能差数十秒（例：GRB991217 为 04:11:26.3 vs GCN 474 04:11:56.5）；这是全目录统一口径问题，已写进 PR #316 待决事项，不逐源开卡。
- **条件 3（新正式文献引用）成立**：本目录可作为各源的正式文献引用（bibcode 2026A&A...711A..60I）与 T90/位置来源；接手者在各源审核时按需登记 `articles[]`，无需源级卡转手。
- 结论：本卡只做索引，不为 33 个源写源级卡。

## 待决

1. **WFC 目录 T0 口径**：`MJD(UTC)` 为事件起始（T90 起点），GCN 通告给触发/事件时刻，SSDC/GRBCAT 又给另一值；三者可差 <1 min。建议维护者明确 BeppoSAX/WFC 源是否统一采用 GCN 触发时刻（§3.8 优先级 ①），以及目录 MJDstart 能否用于无 GCN 源的 T0。默认处置：有 GCN 用 GCN；仅目录源用 MJDstart 并在 `T0_ref` 注明口径。
2. **ID 机械匹配的 3 个歧义行**（000210、010119、010324b）是否需要另开 Issue 记录目录命名/匹配问题，由维护者定。
