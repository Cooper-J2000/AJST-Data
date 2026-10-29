---
paper_key: fynbo2001
paper: Fynbo, J. P. U., Jensen, B. L., Gorosabel, J., et al. 2001, A&A 369, 373–379, DOI 10.1051/0004-6361:20010112（astro-ph/0101425；VoR 未见，本次经 ar5iv 全文与 arXiv TeX 源码核对 arXiv 版；卷页与作者名单 2026-10-30 经 GRB000323 审核复核更正）
date: 2026-10-29
helper: Rusty-Harpoon@zcode
sources: GRB000630, GRB980329A, GRB980613A, GRB970228A, GRB980326, GRB990712A, GRB981226, GRB990506, GRB970828, GRB000418A, GRB000131A, GRB990316, GRB970815, GRB990217, GRB990704, GRB990806, GRB991014, GRB991105, GRB000615, GRB000307
out_of_repo:
---

# 为什么是文献级卡

Fynbo+2001（ESO 望远镜对 BeppoSAX/WFC GRB 误差盒的光学搜索汇总）表 2 给出 **43 行、约 19 个无光学对应体（OT）GRB** 的 R 波段上限与观测历元（Δt），行级数值均为对相应 GCN 通告（V/Larsen+2001 等 ESO 通告）的**汇总转引**，未提供 GCN 之外的独立测量。按 §3.11 增量门槛，**全部源均不过源级卡门槛**（纯汇总表转引 GCN），信息压入本卡即可。

# 涉及源一览

> 库内映射按 ID 命名规则（`GRB<YYMMDD>[A]`）得出；同日多触发源的 letter 后缀与 Fynbo 表行的对应关系（触发号）接手者须自行核验。

| 源 | 表 2 涉及 | 源级卡 | status | 增量判读 |
|---|---|---|---|---|
| GRB000630 | **表 1 主角（非表 2）** | 无（本源已由 PR #630 直接审核入库） | extracted→已入库 | 2026-10-30 更正：本源系本文探测到 OT 的正文主角（表 1 给 10 行独立测光），**不在表 2**（表 2 只收无 OT 的 43 暴）——此前「纯转引 GCN」判读有误。表 1 数据已由 PR #630 逐值核对入库（VoR 经作者镜像 PDF 核对） |
| GRB980329A | 有 | 无 | mention-only | 同上 |
| GRB980613A | 有 | 无 | mention-only | 同上 |
| GRB970228A | 有 | 无 | mention-only | 同上 |
| GRB980326 | 有 | 无 | mention-only | 同上 |
| GRB990712A | 有 | 无 | mention-only | 同上 |
| GRB981226 | 有 | 无 | mention-only | 同上 |
| GRB990506 | 有 | 无 | mention-only | 同上 |
| GRB970828 | 有 | 无 | mention-only | 同上 |
| GRB000418A | 有 | 无 | mention-only | 同上 |
| GRB000131A | 有 | 无 | mention-only | 同上（letter 后缀对应关系待核） |
| GRB990316 | 有 | 无 | mention-only | 同上 |
| GRB970815 | 有 | 无 | mention-only | 同上 |
| GRB990217 | 有 | 无 | mention-only | 同上 |
| GRB990704 | 有 | 无 | mention-only | 同上 |
| GRB990806 | 有 | 无 | mention-only | 同上 |
| GRB991014 | 有 | 无 | mention-only | 同上 |
| GRB991105 | 有 | 无 | mention-only | 同上 |
| GRB000615 | 有 | 无 | mention-only | 同上 |
| GRB000307 | 有 | 无（本源已由 PR #597 直接审核入库） | extracted→已入库 | 表 2 对本源仅转引 GCN 617 的 R=22.0（Δt=2.11 d），无新测光；已在 GRB000307 审核 PR 中逐值核对完毕 |

# 增量门槛判读

- 表 2 的 R 上限值与观测历元均注明转引自 ESO 系 GCN 通告（原文引用 Larsen+2001 / GCN 9xx 系列），逐源可直接从 GCN 检索到同一数值——不满足增量门槛第 1/3 条；历元与库内口径（相对触发 T0 的秒）换算规则提示词已有明文（§3.8），不构成第 2 条口径冲突。
- 因此**不为任何源开源级卡**；上表 status 全为 mention-only。
- 本卡由 GRB000307 审核（PR #597）期间建立：复查指出「≥3 库内源的多源文献应先建文献级索引卡」，补建于此。

# 待决

- 无。若维护者认为 19 源的映射中存在 letter 后缀错配（同日多触发事件），请在 PR #597 下指出，接手审核相应源时逐个纠正。
