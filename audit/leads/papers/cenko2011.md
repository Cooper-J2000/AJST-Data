# 文献索引：Cenko+2011（Fermi-LAT 四暴余辉专篇）

- paper_key: cenko2011
- paper: Cenko et al. 2011, ApJ 732, 29（DOI 10.1088/0004-637X/732/1/29；arXiv:1004.2900 为同文预印本；VoR HTML 含全部表格，2026-11-22 实取）
- date: 2026-11-22
- helper: Rusty-Harpoon@zcode
- sources: GRB090323A, GRB090328A, GRB090902B, GRB090926A
- out_of_repo:

## 为什么是文献级卡

Fermi-LAT 四个高能暴（090323/090328/090902B/090926A）的多波段余辉专篇：光学/NIR 原始测光表
（Table 1/3/5/7，P60、Gemini-N/S GMOS、Faulkes 等 this work 数据）+ 射电表（Table 2/4/6，VLA 战役、
WSRT），全部为**作者自有数据的正式发表表**（多数未单独发 GCN，属增量类型 1）。机读版经 IOP
「Download table as: ASCII」链接发布（本次 VoR HTML 内嵌全表实取核对 090323 的 Table 1/2）。

原文口径（四表一致，接手者按此核）：Date 列为**曝光开始** UT，Δt 列为**曝光中点**相对 Fermi-GBM
触发；星等系统表注 c：**R 波段 Vega、其余滤光片 AB**；数值均未做银消改正（各暴 E(B-V) 在表注给出，
090323 为 0.025）。GCN 转引值（ref 编号 1-10）被作者统一重定标：090323 的 R 波段 GCN 值整体 +0.16
（标定星 Rc=17.15→SDSS 改正 17.31，正文明确），接手者若同时持有 GCN 行与本表行，两者是**同测量
不同定标**，不得按数值一致去重。射电表单位 μJy。

## 涉及源一览

| 源 | 表号 | 源级卡 | status | 增量判读 |
|---|---|---|---|---|
| GRB090323A | Table 1（39 行光学）+ Table 2（22 行射电） | 无（本源已审，PR #1163 直接入库） | extracted（T1 46 行逐值核对（含 GROND g'r'i'z'JHKs @1.12 d 7 行，Reference 注 1=GCN.9026；Dainotti 转引行按 §3.4 同值去重删除）；T2 22 行中 20 行非 GCN 重复行入库） | 类型 1+2；T1 与 GCN 值 +0.16 关系、T2 与 GCN 9043/9047 两行重复已处置 |
| GRB090328A | Table 3（光学）+ Table 4（VLA） | 无（该源已 reviewed） | mention-only | 类型 1 候选；该源审核时若未取用此表，可按 CDS/IOP 机读版补 |
| GRB090902B | Table 5（光学，含 UVOT U）+ Table 6（射电，含 WSRT 4.8 GHz） | audit/leads/GRB090902B.md（mention-only） | mention-only | 类型 1 候选（P60 光变、UVOT U 表 GCN 未发布） |
| GRB090926A | Table 7（光学/NIR） | audit/leads/GRB090926A.md（mention-only） | mention-only | 类型 1 候选 |

## 增量门槛判读

- GRB090323A：已按 VoR 逐值核对入库（PR #1163）。
- GRB090328A：已 reviewed，无卡；本卡仅留表号索引。
- GRB090902B / GRB090926A：过类型 1 门槛（自有测光表），各写一张 mention-only 源级卡，
  接手者从 IOP suppdata / VoR HTML 实取逐值核对。

## 待决

无。
