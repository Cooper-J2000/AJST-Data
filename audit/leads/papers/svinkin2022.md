# 文献索引：Svinkin+2022（IPN 对 Konus 短暴定位的第二版目录）

- paper_key: svinkin2022
- paper: Svinkin D.S., Hurley K., Ridnaia A.V., Lysenko A.L. et al. 2022, ApJS 259, 34, "The Second Catalog of Interplanetary Network Localizations of Konus Short-duration Gamma-Ray Bursts"（DOI 10.3847/1538-4365/ac4607，已验证解析；机读表 VizieR J/ApJS/259/34 table2.dat/table3.dat/table4.dat，2026-10-28 实取并逐行解析；VoR 全文未逐页核对，本卡仅依据 CDS 机读表）
- date: 2026-10-28
- helper: fsy@代理
- sources: GRB110212A, GRB110529A, GRB110802A, GRB111121A, GRB111222A, GRB120804A, GRB120830A, GRB130310A, GRB130515A, GRB130603B, GRB130912A, GRB131125A, GRB131126A, GRB140209A, GRB140611A, GRB140930B, GRB141202A, GRB150424A, GRB150512A, GRB150702A, GRB150831A, GRB160303A, GRB160408A, GRB160612A, GRB160702A, GRB160709A, GRB161011A, GRB161218A, GRB170101A, GRB170121B, GRB170127C, GRB170206B, GRB170428A, GRB180204A, GRB180324A, GRB180402A, GRB180618A, GRB180626B, GRB180626C, GRB180703B, GRB181123B, GRB190427A, GRB190606A, GRB190610A, GRB191031D, GRB200219A, GRB200325B, GRB200415A, GRB200826A, GRB200907A, GRB201221D, GRB201227A, GRB210323A, GRB210424B, GRB210715B

## 为什么是文献级卡

该文是 IPN 对 Konus-Wind 短暴定位的第二个目录：2011-01 至 2020-12 共 199 个 Konus 短暴（table2 199 行：Konus 触发时刻 + 各星载仪器触发/增长率清单；table3 592 行：2-4 条 3σ 三角定位环——环心 RA/Dec、半径 θ 与 3σ 上下不确定度；table4 208 行：199 个事件的最概然位置 + 误差盒 MaxDim/MinDim/Area）。

对本库的价值有两类：**T0 锚点**（Konus 自触发 UT 时刻，精确到毫秒）与**定位增量**（table4 发表版精化误差盒通常远小于对应 GCN Circular 的 preliminary 盒——建卡源 GRB141202A 即一例：GCN 17131 preliminary 盒 max dim 3.2°，本目录 table4 精化盒 0.221°×0.099°、最概然位置 143.100/+54.404，已按发表版优先原则采用，见该源 PR）。本表不含任何测光数据。

成员判定口径：① 表 2 Name 列与库内源 ID 精确一致（46 个，A 组）；② 表 2 匿名/异名行按「Konus 触发时刻与库内 T0 差 ≤180 s 且日期相符」互证（3 个，B 组——注意这三例目录用名与库内 ID 字母不一致，如目录 GRB170121A ↔ 库内 GRB170121B，接手者须确证命名归属）；③ 表 2 匿名行与库内源同日期、但库内 T0 为占位（name_date/meta_trigger）无法时刻互证（6 个，C1 组——仅日期匹配，本表 Konus 时刻是其 T0 的唯一强候选）。**日期匹配≠同一事件**：同日多暴必须逐源确证。

## 涉及源一览

> `status` 全部 `mention-only`（仅完成「表行 ↔ 库内源」交叉匹配，未提取任何数值入库；环参数与精化盒坐标以原文表为准，接手者自行实取）。源级卡一律未开（由接手各源的审核员按需自取）。

| 源 | 表 2 行（Konus 触发 UT） | 目录用名 | 源级卡 | status | 增量判读 |
|---|---|---|---|---|---|
| GRB110529A | T02920（00:48:40.249） | GRB110529A | 无 | mention-only | 名字精确互证；table4 精化 IPN 盒为定位增量（待接手者实取核对） |
| GRB110802A | T55156（15:19:16.191） | GRB110802A | 无 | mention-only | 名字精确互证；table4 精化 IPN 盒为定位增量（待接手者实取核对） |
| GRB111121A | T59182（16:26:22.640） | GRB111121A | 无 | mention-only | 名字精确互证；table4 精化 IPN 盒为定位增量（待接手者实取核对） |
| GRB111222A | T53515（14:51:55.918） | GRB111222A | 无 | mention-only | 名字精确互证；table4 精化 IPN 盒为定位增量（待接手者实取核对） |
| GRB120804A | T03255（00:54:15.749） | GRB120804A | 无 | mention-only | 名字精确互证；table4 精化 IPN 盒为定位增量（待接手者实取核对） |
| GRB120830A | T25623（07:07:03.562） | GRB120830A | 无 | mention-only | 名字精确互证；table4 精化 IPN 盒为定位增量（待接手者实取核对） |
| GRB130310A | T72588（20:09:48.897） | GRB130310A | 无 | mention-only | 名字精确互证；table4 精化 IPN 盒为定位增量（待接手者实取核对） |
| GRB130515A | T04880（01:21:20.440） | GRB130515A | 无 | mention-only | 名字精确互证；table4 精化 IPN 盒为定位增量（待接手者实取核对） |
| GRB130603B | T56956（15:49:16.448） | GRB130603B | 无 | mention-only | 名字精确互证；table4 精化 IPN 盒为定位增量（待接手者实取核对） |
| GRB130912A | T30902（08:35:02.290） | GRB130912A | 无 | mention-only | 名字精确互证；table4 精化 IPN 盒为定位增量（待接手者实取核对） |
| GRB131125A | T59572（16:32:52.927） | GRB131125A | 无 | mention-only | 名字精确互证；table4 精化 IPN 盒为定位增量（待接手者实取核对） |
| GRB131126A | T14048（03:54:08.270） | GRB131126A | 无 | mention-only | 名字精确互证；table4 精化 IPN 盒为定位增量（待接手者实取核对） |
| GRB140209A | T27060（07:31:00.493） | GRB140209A | 无 | mention-only | 名字精确互证；table4 精化 IPN 盒为定位增量（待接手者实取核对） |
| GRB140611A | T13864（03:51:04.927） | GRB140611A | 无 | mention-only | 名字精确互证；table4 精化 IPN 盒为定位增量（待接手者实取核对） |
| GRB140930B | T70907（19:41:47.149） | GRB140930B | 无 | mention-only | 名字精确互证；table4 精化 IPN 盒为定位增量（待接手者实取核对） |
| GRB141202A | T40626（11:17:06.305） | GRB141202A | 无 | mention-only | 名字精确互证；table4 精化 IPN 盒为定位增量（待接手者实取核对） |
| GRB150424A | T27781（07:43:01.073） | GRB150424A | 无 | mention-only | 名字精确互证；table4 精化 IPN 盒为定位增量（待接手者实取核对） |
| GRB150702A | T86198（23:56:38.645） | GRB150702A | 无 | mention-only | 名字精确互证；table4 精化 IPN 盒为定位增量（待接手者实取核对） |
| GRB150831A | T38049（10:34:09.519） | GRB150831A | 无 | mention-only | 名字精确互证；table4 精化 IPN 盒为定位增量（待接手者实取核对） |
| GRB160408A | T23144（06:25:44.202） | GRB160408A | 无 | mention-only | 名字精确互证；table4 精化 IPN 盒为定位增量（待接手者实取核对） |
| GRB160612A | T72767（20:12:47.893） | GRB160612A | 无 | mention-only | 名字精确互证；table4 精化 IPN 盒为定位增量（待接手者实取核对） |
| GRB160702A | T44544（12:22:24.054） | GRB160702A | 无 | mention-only | 名字精确互证；table4 精化 IPN 盒为定位增量（待接手者实取核对） |
| GRB160709A | T71345（19:49:05.896） | GRB160709A | 无 | mention-only | 名字精确互证；table4 精化 IPN 盒为定位增量（待接手者实取核对） |
| GRB170101A | T08757（02:25:57.802） | GRB170101A | 无 | mention-only | 名字精确互证；table4 精化 IPN 盒为定位增量（待接手者实取核对） |
| GRB170127C | T05744（01:35:44.660） | GRB170127C | 无 | mention-only | 名字精确互证；table4 精化 IPN 盒为定位增量（待接手者实取核对） |
| GRB170428A | T33218（09:13:38.719） | GRB170428A | 无 | mention-only | 名字精确互证；table4 精化 IPN 盒为定位增量（待接手者实取核对） |
| GRB180204A | T09372（02:36:12.902） | GRB180204A | 无 | mention-only | 名字精确互证；table4 精化 IPN 盒为定位增量（待接手者实取核对） |
| GRB180324A | T16629（04:37:09.939） | GRB180324A | 无 | mention-only | 名字精确互证；table4 精化 IPN 盒为定位增量（待接手者实取核对） |
| GRB180402A | T35100（09:45:00.353） | GRB180402A | 无 | mention-only | 名字精确互证；table4 精化 IPN 盒为定位增量（待接手者实取核对） |
| GRB180618A | T02591（00:43:11.201） | GRB180618A | 无 | mention-only | 名字精确互证；table4 精化 IPN 盒为定位增量（待接手者实取核对） |
| GRB180626B | T06442（01:47:22.786） | GRB180626B | 无 | mention-only | 名字精确互证；table4 精化 IPN 盒为定位增量（待接手者实取核对） |
| GRB180626C | T33832（09:23:52.424） | GRB180626C | 无 | mention-only | 名字精确互证；table4 精化 IPN 盒为定位增量（待接手者实取核对） |
| GRB180703B | T82008（22:46:48.633） | GRB180703B | 无 | mention-only | 名字精确互证；table4 精化 IPN 盒为定位增量（待接手者实取核对） |
| GRB181123B | T19981（05:33:01.096） | GRB181123B | 无 | mention-only | 名字精确互证；table4 精化 IPN 盒为定位增量（待接手者实取核对） |
| GRB190427A | T16454（04:34:14.918） | GRB190427A | 无 | mention-only | 名字精确互证；table4 精化 IPN 盒为定位增量（待接手者实取核对） |
| GRB190606A | T06903（01:55:03.800） | GRB190606A | 无 | mention-only | 名字精确互证；table4 精化 IPN 盒为定位增量（待接手者实取核对） |
| GRB190610A | T41263（11:27:43.560） | GRB190610A | 无 | mention-only | 名字精确互证；table4 精化 IPN 盒为定位增量（待接手者实取核对） |
| GRB191031D | T77011（21:23:31.324） | GRB191031D | 无 | mention-only | 名字精确互证；table4 精化 IPN 盒为定位增量（待接手者实取核对） |
| GRB200219A | T27405（07:36:45.513） | GRB200219A | 无 | mention-only | 名字精确互证；table4 精化 IPN 盒为定位增量（待接手者实取核对） |
| GRB200415A | T31681（08:48:01.401） | GRB200415A | 无 | mention-only | 名字精确互证；table4 精化 IPN 盒为定位增量（待接手者实取核对） |
| GRB200826A | T16195（04:29:55.106） | GRB200826A | 无 | mention-only | 名字精确互证；table4 精化 IPN 盒为定位增量（待接手者实取核对） |
| GRB200907A | T51859（14:24:19.501） | GRB200907A | 无 | mention-only | 名字精确互证；table4 精化 IPN 盒为定位增量（待接手者实取核对） |
| GRB201221D | T83197（23:06:37.636） | GRB201221D | 无 | mention-only | 名字精确互证；table4 精化 IPN 盒为定位增量（待接手者实取核对） |
| GRB201227A | T54846（15:14:06.705） | GRB201227A | 无 | mention-only | 名字精确互证；table4 精化 IPN 盒为定位增量（待接手者实取核对） |
| GRB210323A | T79334（22:02:14.600） | GRB210323A | 无 | mention-only | 名字精确互证；table4 精化 IPN 盒为定位增量（待接手者实取核对） |
| GRB210424B | T28916（08:01:56.081） | GRB210424B | 无 | mention-only | 名字精确互证；table4 精化 IPN 盒为定位增量（待接手者实取核对） |
| GRB170121B | T05812（01:36:52.788） | GRB170121A | 无 | mention-only | 时刻互证（Konus 触发与库内 T0 差 +2.2 s）但目录用名 GRB170121A 与库内 ID 字母不一致，须确证命名归属 |
| GRB170206B | T39121（10:52:01.226） | GRB170206A | 无 | mention-only | 时刻互证（Konus 触发与库内 T0 差 -4.2 s）但目录用名 GRB170206A 与库内 ID 字母不一致，须确证命名归属 |
| GRB200325B | T11908（03:18:28.659） | GRB200325A | 无 | mention-only | 时刻互证（Konus 触发与库内 T0 差 +2.3 s）但目录用名 GRB200325A 与库内 ID 字母不一致，须确证命名归属 |
| GRB110212A | T47551（13:12:31.101） | -- | 无 | mention-only | 仅日期匹配（库内 T0 为占位）；本表 Konus 时刻是其 T0 唯一强候选 |
| GRB150512A | T46609（12:56:49.794） | -- | 无 | mention-only | 仅日期匹配（库内 T0 为占位）；本表 Konus 时刻是其 T0 唯一强候选 |
| GRB160303A | T73318（20:21:58.359） | -- | 无 | mention-only | 仅日期匹配（库内 T0 为占位）；本表 Konus 时刻是其 T0 唯一强候选 |
| GRB161011A | T18824（05:13:44.426） | -- | 无 | mention-only | 仅日期匹配（库内 T0 为占位）；本表 Konus 时刻是其 T0 唯一强候选 |
| GRB161218A | T19166（05:19:26.402） | -- | 无 | mention-only | 仅日期匹配（库内 T0 为占位）；本表 Konus 时刻是其 T0 唯一强候选 |
| GRB210715B | T74795（20:46:35.280） | -- | 无 | mention-only | 仅日期匹配（库内 T0 为占位）；本表 Konus 时刻是其 T0 唯一强候选 |

## 增量门槛判读

- 上表全部 55 个源均过「定位/时刻增量」门槛（table3/table4 为 GCN preliminary 通告之外的发表版数值），但本卡只做索引、不含可采纳数值；各源审核时由接手者直接从 VizieR J/ApJS/259/34 实取 table3/table4 行并自行换算（pos_error 若取 IPN 盒，按库内先例用外接圆半径近似并记 pos_error_confidence=3sigma，先例 GRB030217=885″、GRB141202A=398″）。
- 不开源级卡：本目录为即发辐射参数目录，无测光表，不存在「测光增量」类源级卡。

## 待决

1. **同日异名候选（未列入 sources）**：下列库内源与表 2 某行同日期，但目录用名与库内 ID 字母不一致或库内 T0 为实值且与 Konus 触发时刻不符——很可能是同日不同事件，也可能存在命名错位，须逐源确证后才可归属：GRB111123A、GRB120612A、GRB120624B、GRB120802A、GRB120811A、GRB120811C、GRB120816A、GRB120817A、GRB121011A、GRB130122A、GRB130504A、GRB130504C、GRB130701A、GRB140414A、GRB140428A、GRB140906A、GRB150118B、GRB150710B、GRB150811A、GRB150819A、GRB151022A、GRB170604A、GRB170803A、GRB170827A、GRB180728A、GRB190706B、GRB191227A、GRB200623A、GRB210307A。
2. **库外事件**：目录 199 个事件中 117 个在库内完全无同日期源；另有 27 个事件虽有同日期库内源但未能互证（2026-10-28 独立核查按严格同日期口径复算更正：原记 79/65 拆分不可复现）（目录用名与库内 ID 字母不一致、或库内 T0 为实值且与 Konus 触发时刻不符——见待决 1 的 29 个库内源）。完全无对应的事件按 §3.11 属维护者裁量的 new-source Issue 事项，本卡不代开、不逐一枚举；接手者审核同日源时若需消歧可回查本表。

