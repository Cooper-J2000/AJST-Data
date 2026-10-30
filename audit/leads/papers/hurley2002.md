---
paper_key: hurley2002
paper: Hurley, K., Sazonov, S., Mazaeva, E., et al. 2002, ApJ 567, 447（astro-ph/0107188；VoR IOP 页可达，本次经 arXiv TeX + IOP 页核对）
date: 2026-10-30
helper: Rusty-Harpoon@zcode
sources: GRB010119, GRB000607, GRB001204
out_of_repo:
---

# 为什么是文献级卡

Hurley+2002（IPN 3B 目录前身：1999–2000 年 IPN 观测的 19 个 GRB 编纂）Table 1（触发时刻/时标/流量参数）、Table 2（精化误差盒）、Table 3（编篡测光上限）、Table 4（射电上限）覆盖**库内 3 个源**，达 §3.11 第 8 条「≥3 个库内源先写文献级索引卡」门槛。本卡为纯索引，不含可采纳数值。

# 涉及源一览

| 源 | 涉及表 | 源级卡 | status | 增量判读 |
|---|---|---|---|---|
| GRB010119 | T1/T2/T3/T4 | 无（本源已由 PR #626 直接审核入库） | extracted→已入库 | T3 的 NOT R22.3 行系转引 Gorosabel+2002 T1（已按 Gorosabel 行入库）；T3 的 Palomar 21.5@51h 经 VoR 优先原则用于 GCN 919 行改值（21.0→21.5），处置见 PR #626 待决② |
| GRB000607 | T3 | 无 | mention-only | 各行系转引仓内既有 GCN 720/697 数值，无 GCN 之外增量 |
| GRB001204 | T1/T2/T3/T4 | 无（本源已由 PR #625 直接审核入库） | extracted→已入库 | T2 终盒中心与 T3 的 USNO R_c 18@68 h、Mt. Stromlo V 20.5@74 h 两行（GCN 五篇无此观测）已按新测量入库；T3 的 Stromlo R 20.1/NTT Ks 行与 T4 射电行系转引 GCN 898/908/896，保留 GCN 行 |

# 增量门槛判读

- GRB001204：T3 的 USNO/V 两行 + T2 精化盒为 GCN 检索拿不到的数值/口径（ref 列为「...」），过增量门槛——已在 PR #625 按「同测改值/新测量」规则直接入库（该源审核时 Table 3 已逐值核对）。
- GRB010119：T3 的 Palomar 21.5 为 VoR 重定标值，过增量门槛——已在 PR #626 采纳入库。
- GRB000607：纯转引 GCN，不过门槛；接手审核该源时按卡索引逐值核对 GCN 720/697 原文即可。
- T1 的触发时刻列与官方目录 ECT 普遍存在 1–15 s 内部不一致（先例：GRB001204 的 28855 vs 28869.3/28870.3；GRB010119 的 37178 vs 37179/37179.5）——各源 T0 仍按 §3.8 优先级取触发仪器值，本表值只作互证备查。

# 待决

- 无。
