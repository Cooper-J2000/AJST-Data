# 文献级索引：Gorbovskoy+2012 (MASTER 五暴光学观测专文)

- paper_key: gorbovskoy2012
- paper: Gorbovskoy+2012, MNRAS 421, 1874（DOI 10.1111/j.1365-2966.2012.20195.x；arXiv:1111.3625；VizieR J/MNRAS/421/1874 仅收录 table1/4/5/8/9，即只覆盖 GRB 100901A 与 GRB 100906A）
- date: 2026-10-27
- helper: fsy@代理
- sources: GRB100901A, GRB100902A, GRB100905A, GRB100906A, GRB101020A

## 为什么是文献级卡

该文是 MASTER 团队对五个 GRB（100901A/100902A/100905A/100906A/101020A，全部库内在册）的 prompt/early/afterglow 光学观测专文：两暴（100901A、100906A）有正式测光表，三暴（100902A、100905A、101020A）只有上限表。按 §3.11 覆盖 ≥3 个库内源先建本索引卡，不为各源单独开源级卡（增量判读见下表与「增量门槛判读」节）。

**版本状态**：本卡建卡时实际阅读 arXiv:1111.3625v1（2011-11-15，Accepted 2011-11-13）全文 PDF；VoR（OUP/DOI 10.1111/j.1365-2966.2012.20195.x）403（Cloudflare）未取到；VizieR `J/MNRAS/421/1874` 有 table1（GRB 100901A MASTER 测光）、table4/5（GRB 100906A MASTER/OSN）、table8/9（定标星）机读表可核。VoR 与 arXiv v1 数值是否一致**未核**，接手者审对应源时须先取 VoR。

## 原文口径（接手者注意，未换算）

- 各源 T0：100901A/100906A 见正文引 GCN（100906A "At 13:49:27 UT"）；100905A 正文 "Swift/BAT at 15:08:15 UT (Marshall et al. 2010)"——**与本库 info 的 2010-09-05T15:08:14Z 差 1 s**，接手者须按触发仪器官方值裁定；101020A 正文 "at 23:40:41 UT"，本库已采 23:40:41.709060Z（Swift/BAT 目录/官方页亚秒）。
- 表内时间均为相对 T0：Table 1 明言 "Times t - T0 are the middle times of exposures"；Table 2/3 给 tstart/tend(UT)+tstart−T0(s)；Table 7 给 tstart−T0(s)/tmiddle(s)/Exp(s)。
- MASTER coadd 上限表（Table 2/7）末列 Coadded number 为合并帧数；两垂直偏振筒（V+P1/V+P2）同窗同时曝光（"MASTER II have 2 images per exposition time"）。
- 定标：§3.2——无滤光片星等以 Kislovodsk MASTER 历元零点改正；偏振双筒相对精度约 2%；偏振改正基于标准星双偏振均值匹配。星等系统原文未声明（接手者按 §3.3 处理）。
- 银消光（NED EGC，图 12 用）：100902A AV=1.037、100905A AV=0.191、101020A AV=0.051。
- 原文笔误：GCN 11359/11361 与本文 §2.5 均把 GRB 101020A 误写作 "GRB 101008A"（同句引 Saxton et al. 2010 = GCN 11357，即本源）。

## 涉及源一览

| 源 | 表号 | 源级卡 | status | 增量判读 |
|---|---|---|---|---|
| GRB100901A | Table 1（MASTER R/W/I/V 测光，正文仅样例行，全表在线电子版=VizieR table1）+ Table 8（SDSS 定标星） | 无 | mention-only | 过门槛(1)(3)：专篇测光表+定标星表；VizieR table1 机读可取 |
| GRB100902A | Table 2（偏振上限 4 行单曝+1 行 coadd，含 UT 端点与 tstart−T0） | 无 | mention-only | 过门槛(1)：上限表含 UT 端点，比 GCN 通报更全 |
| GRB100905A | Table 3（偏振上限 4 行，含 UT 端点与 tstart−T0） | 无 | mention-only | 过门槛(1)：同上；另注意正文 T0=15:08:15 UT 与本库 15:08:14Z 差 1 s |
| GRB100906A | Table 4（MASTER 双偏振测光）+ Table 5（OSN UBVRI）+ Table 6（NOT R 三点）+ Table 9（定标星） | 无 | mention-only | 过门槛(1)(3)：三台设备测光表+定标星；VizieR table4/5 机读可取 |
| GRB101020A | Table 7（V 上限 2 行 coadd：106→116 s V>14.9；472→2836 s V>18.5） | 无 | extracted | 已由 GRB101020A 审核采用（两行 coadd 入 lc，reference=GCN 11361，表 7 同值佐证） |

## 增量门槛判读

- 五源均过门槛：该文是这些 MASTER 观测的正式发表版（bibcode 2012MNRAS.421.1874G），Table 1–7 为作者自表，不是 GCN 汇总转引。
- 各源接手者：先取 VoR（本卡未能取到，OUP 403）与 VizieR 机读表（100901A/100906A），逐值核对后再入库；100902A/100905A/101020A 仅有上限表。
- 100901A 的 lc 已有 853 行、100906A 已有 487 行——注意与 Table 1/4/5/6 去重（同一次 MASTER 测量的 GCN 行 vs VoR 行）。

## 未核对

- 未逐值提取任何源的数据行（101020A 的 Table 7 两行除外，已入该源 lc 并经 PR 核查）；未与各源现有 lc 对重；未做消光/系统换算；未核 VoR 与 arXiv v1 数值一致性。

## 待决

- GRB100905A 的 T0 分歧（正文 15:08:15 UT vs 本库 15:08:14Z）在该源被审核时按触发仪器官方通告（Marshall et al. 2010 = GCN 11229 一类）裁定。
- CDS 未收录 table2/3/6/7 的机读版；若 VoR 持续不可得，接手者按 §3.3 用 arXiv v1 取值并在 comment 标注「VoR 补充材料不可得，取自 arXiv v1 表N」。
