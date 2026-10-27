# 文献索引：Hurley+2011（IPN 对 HETE-2 GRB 目录的补编）

- paper_key: hurley2011
- paper: Hurley et al. 2011, ApJS 197, 34, "The Interplanetary Network Supplement to the HETE-2 Gamma-Ray Burst Catalog"（ADS bibcode 2011ApJS..197...34H，https://ui.adsabs.harvard.edu/abs/2011ApJS..197...34H ；机读表 VizieR J/ApJS/197/34 table5.dat，2026-10-27 实取；VoR 论文全文未逐页核对，本卡仅依据 CDS 机读表）
- date: 2026-10-27
- helper: fsy@代理
- sources: GRB001105, GRB010126, GRB010629, GRB020127, GRB020305, GRB020331, GRB020418, GRB020531, GRB020625, GRB020714, GRB020715, GRB020801, GRB021016, GRB021023, GRB021104, GRB021113, GRB021201, GRB030204, GRB030217, GRB030320, GRB030413, GRB030501, GRB030725, GRB031111, GRB040228, GRB040403, GRB040810, GRB041211, GRB041223, GRB050128, GRB050626, GRB051103

## 为什么是文献级卡

该文是 IPN（第三网）对 HETE-2 时代 GRB 的定位补编：2000-11 至 2006-05 共 226 个 FREGATE 探测事件、157 个三角定位。机读表 table5.dat 每行给出：观测日、事件 UT 时刻（秒级）、1–2 条 IPN 环（中心 RA/Dec、半径、1σ 不确定度）、黄道坐标。**不含任何测光数据**。对本库的价值是 **T0 锚点**：库内 2000–2006 的纯 IPN 源大量带 `name_date` 占位 T0（bot 残留，如 GRB030217 原值 00:00:00Z），本表的 UT 时刻往往就是其触发时刻的候选锚（审核 GRB030217 时已按「GCN 1870 09942 s + 本表行 72 02:45:42」双源互证重锚，先例见该源 comment）。

按 GRB 命名日期与 table5 观测日匹配，得 32 个库内源（见下表）；其中 4 个已秒级互证。**同日多暴必须逐源确证**（例如 15/02/2003 有 3 行、04/04/2003 与 11/12/2004 各 2 行），日期匹配≠同一事件。

## 涉及源一览

> `status` 全部 `mention-only`（仅做了「表 5 行 ↔ 库内源」交叉匹配，未提取任何数值入库；环参数与时刻以原文为准）。

| 源 | 表号 | 源级卡 | status | 增量判读 |
|---|---|---|---|---|
| GRB021023 | table5 行57（2:53:46UT） | 无 | mention-only | 时间互证：库内 T0 与本表差 1 s（已审源，独立印证） |
| GRB021113 | table5 行60（6:38:57UT） | 无 | mention-only | 时间互证：库内 T0 与本表差 1 s（已审源，独立印证） |
| GRB050128 | table5 行136（4:19:54UT） | 无 | mention-only | 时间互证：库内 T0 与本表差 1 s（已审源，独立印证） |
| GRB030217 | table5 行72（2:45:42UT） | 无 | mention-only | 本卡建卡源：已按 GCN 1870 09942 s + 本行 02:45:42 重锚 T0（见其 PR） |
| GRB001105 | table5 行2（6:25:28UT） | 无 | mention-only | 仅日期匹配；库内 T0 为 name_date 占位，本表时刻是其 T0 唯一强候选 |
| GRB010126 | table5 行8（9:10:40UT） | 无 | mention-only | 同上（T0 占位） |
| GRB010629 | table5 行17（2:21:06UT） | 无 | mention-only | 仅日期匹配；库内 T0=00:52:00 与本表差 ~8.5 h，须查各源自家 GCN 判归属 |
| GRB020127 | table5 行34（0:57:25UT） | 无 | mention-only | 仅日期匹配；库内 T0 差 ~20 h，须逐源确证 |
| GRB020305 | table5 行38（1:55:25UT） | 无 | mention-only | 仅日期匹配；库内 T0 差 ~20 h，须逐源确证 |
| GRB020331 | table5 行40（6:32:29UT） | 无 | mention-only | 仅日期匹配（T0 占位） |
| GRB020418 | table5 行41（7:43:09UT） | 无 | mention-only | 仅日期匹配（T0 占位；注意库内 T0 日期为 04-19，疑似 ID/UTC 跨日，须确证） |
| GRB020531 | table5 行43（0:26:18UT） | 无 | mention-only | 仅日期匹配；库内 T0 在 05-30 20:15，与本表（05-31 0:26）差 ~4.2 h，须确证 |
| GRB020625 | table5 行44（1:25:49UT） | 无 | mention-only | 仅日期匹配（T0 占位） |
| GRB020714 | table5 行46（5:49:22UT） | 无 | mention-only | 仅日期匹配（T0 占位） |
| GRB020715 | table5 行47（0:03:32UT） | 无 | mention-only | 仅日期匹配（T0 占位） |
| GRB020801 | table5 行49（2:58:42UT） | 无 | mention-only | 仅日期匹配；库内 T0 差 ~6 h，须确证 |
| GRB021016 | table5 行55（0:29:01UT） | 无 | mention-only | 仅日期匹配；库内 T0=10:29:00 与本表差 ~10 h，须确证 |
| GRB021104 | table5 行59（9:06:32UT） | 无 | mention-only | 仅日期匹配；库内 T0 差 ~0.7 h，须确证 |
| GRB021201 | table5 行61（5:30:04UT） | 无 | mention-only | 仅日期匹配；库内 T0 差 ~2 min，须确证 |
| GRB030204 | table5 行68（2:45:34UT） | 无 | mention-only | 仅日期匹配（T0 占位） |
| GRB030320 | table5 行77（8:49:18UT） | 无 | mention-only | 仅日期匹配；库内 T0 在 03-21 02:42，与本表（03-20 8:49）差 ~18 h，须确证 |
| GRB030413 | table5 行83（7:34:44UT） | 无 | mention-only | 仅日期匹配；库内 T0=00:20:00 与本表差 ~7 h，须确证 |
| GRB030501 | table5 行84（0:44:48UT） | 无 | mention-only | 仅日期匹配；库内 T0=01:17:21 与本表差 ~33 min，须确证 |
| GRB030725 | table5 行90（1:46:27UT） | 无 | mention-only | 仅日期匹配；库内 T0=11:46:24 与本表差 ~10 h，须确证 |
| GRB031111 | table5 行99（6:45:13UT） | 无 | mention-only | 仅日期匹配（T0 占位） |
| GRB040228 | table5 行107（0:08:56UT） | 无 | mention-only | 仅日期匹配（T0 占位） |
| GRB040403 | table5 行108（6:55:03UT）、行109（3:23:56UT） | 无 | mention-only | 当日两行，归属待确证 |
| GRB040810 | table5 行120（4:15:36UT） | 无 | mention-only | 仅日期匹配（T0 占位） |
| GRB041211 | table5 行132（7:49:50UT）、行133（3:57:44UT） | 无 | mention-only | 当日两行，归属待确证 |
| GRB041223 | table5 行134（4:06:37UT） | 无 | mention-only | 仅日期匹配；库内 T0=00:06:18 与本表差 ~4 h，须确证 |
| GRB050626 | table5 行141（3:37:32UT） | 无 | mention-only | 仅日期匹配；库内 T0=03:45:16 与本表差 ~7.7 min，须确证 |
| GRB051103 | table5 行148（9:25:41UT） | 无 | mention-only | 仅日期匹配；库内 T0=19:55:47 与本表差 ~10.5 h，须确证 |

## 增量门槛判读

- **不构成测光增量**：本表纯定位数据（环参数），无测光行，不开任何测光类源级卡。
- **T0 锚点增量（条件 2 类）**：对 T0 为 `name_date` 占位的候选源（GRB001105、GRB010126、GRB020331、GRB020418、GRB020625、GRB020714、GRB020715、GRB030204、GRB031111、GRB040228、GRB040810），本表 UT 时刻是 GCN/目录之外多一路的锚点来源；接手者审核时按「自家 GCN（若有）优先 + 本表互证」定锚（GRB030217 即先例）。
- **已审 3 源**（GRB021023、GRB021113、GRB050128）：本表仅作独立印证，无动作。
- 其余「仅日期匹配」且库内已有真实 T0 的源：与本表时刻差从 1 s 到 ~20 h 不等，**不能默认同暴**——必须以各源自家 GCN/IPN 通告的环几何确证归属后才可引用。

## 待决

1. 表内其余 125 个事件不在库内（含 2000-11 起的大量 HETE-2/IPN 暴）；按契约本卡不列 `out_of_repo`（须先开 `new-source` Issue），是否批量建源由维护者定。
2. 「仅日期匹配」候选中库内 T0 与本表相差数小时的（GRB010629、GRB020127、GRB020305、GRB020531、GRB020801、GRB021016、GRB021104、GRB030320、GRB030413、GRB030501、GRB030725、GRB041223、GRB050626、GRB051103），可能存在：同日另一事件、库内 T0 有误、或 ID 日期与 UTC 跨日——接手者先查各源自家 GCN 再判，勿直接采表 5 时刻改 T0。
