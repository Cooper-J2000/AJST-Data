# 文献索引：Smith+1999（RXTE/ASM 定位的 13 个 GRB）

- paper_key: smith1999
- paper: Smith, Levine, Bradt et al. 1999, ApJ 526, 683（DOI 10.1086/308029；arXiv:astro-ph/9907332 v1；VoR 被 IOP/Radware 反爬拦截，2026-10-27 实测）
- date: 2026-10-27
- helper: Rusty-Harpoon@zcode
- sources: GRB970815, GRB970828, GRB971024, GRB971214A, GRB980703A

## 为什么是文献级卡

该文是 RXTE/ASM (SSC) 巡天对 13 个 GRB 的 X 射线对应体定位论文（1996-04 至 1998-12），每暴一节叙述 +
成套表格：表 2（触发时刻、证实卫星旗标、2–12 keV 流量、ASM 误差框中心）、表 3（单 SSC 误差框长宽/位置角）、
表 4（多 SSC 误差框四角坐标）、表 5（BATSE/ASCA/ROSAT/WFC/NFI 交叉定位圆）。这些 ASM 定位与 2–12 keV 流量
不在 GRBCAT / batsegrb / saxgrbmgrb 等任何库内目录快照中，GCN 通告也只有部分暴的 ASM 线或框——
属「目录检索拿不到的数值」，不是转引 GCN 的汇总表。

本文涉及的其余 7 个暴（GRB960416、960529、960727、961002、961019、961029、961230，及正文提到的
961216/971216/981005 未确认个例）均不在库内，已按 §3.11 第 5 条开 new-source Issue：#309（960416）、#310（960529）、#311（960727）、#312（961002）、#313（961019）、#314（961029）、#315（961230）；961216/971216/981005 为正文提及的未确认个例，未开 Issue。

## 涉及源一览

| 源 | 表号 | 源级卡 | status | 增量判读 |
|---|---|---|---|---|
| GRB971024 | 表 2、3、5 | 无（2026-10-27 已由 Rusty-Harpoon@zcode 审核完毕，数值经独立核对入 info comment） | extracted | 已采纳：T0=11:33:32（表 2）、ra/dec=276.25/+49.45（表 2）、2–12 keV 流量 1.1±0.3e-7（comment） |
| GRB970815 | 表 2、4、5 | `audit/leads/GRB970815.md` | mention-only | **过门槛**：ASM 误差框（表 4 四角）+ 2–12 keV 流量（表 2）目录/GCN 拿不到；另给 ASCA 定位圆（表 5） |
| GRB970828 | 表 2、4、5 | `audit/leads/GRB970828.md` | mention-only | **过门槛**：同上，另给 ASCA/ROSAT 定位圆（表 5） |
| GRB971214A | 表 2、3、5 | `audit/leads/GRB971214A.md` | mention-only | **过门槛**：ASM 误差框（表 3）+ 2–12 keV 流量（表 2）；WFC/NFI 交叉圆表 5 与 GCN 同源仅索引 |
| GRB980703A | 表 2、4、5 | `audit/leads/GRB980703A.md` | mention-only | **过门槛**：ASM 误差框（表 4 四角）+ 2–12 keV 流量（表 2）；NFI 圆表 5 与 GCN 同源仅索引 |

## 增量门槛判读

5 个库内源全部过门槛（判据 1：ASM 误差框与 2–12 keV 流量为本文独有量；判据 3：为各源提供
1999ApJ...526..683S 正式引用）。表 5 中 BATSE 圆与 WFC/NFI/ASCA/ROSAT 圆各自转引 GCN/IAUC/文献，
**不是**本文增量，接手者仍需回各自原始通告核对。

## 待决

无。注意：本文表 2 的「Time of GRB」即为触发时刻（证实卫星旗标 a=Ulysses b=BATSE k=KONUS s=BeppoSAX），
可作各源 T0 的正式文献锚点（本文触发时刻取整秒；BATSE 目录亚秒值优先）。
