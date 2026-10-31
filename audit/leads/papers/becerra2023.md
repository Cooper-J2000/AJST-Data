# 文献级卡：Becerra+2023（TAROT/COATLI/RATIR 样本）

- paper_key: becerra2023
- paper: Becerra+2023, MNRAS 525, 3262（DOI 10.1093/mnras/stad2513，arXiv 2308.07882）「Understanding the nature of the optical emission in gamma-ray bursts: analysis from TAROT, COATLI, and RATIR observations」
- date: 2026-10-31
- helper: Rusty-Harpoon@zcode
- sources: GRB180706A, GRB180812A
- out_of_repo:

## 为什么是文献级卡

本文为 227 个 GRB（TAROT/COATLI/RATIR 观测样本）的统计文章。表 3 为逐源汇总表（Trigger 号、E(B−V)、z、T90，自述转引 GCN/TAN 与 Swift/BAT repository）——纯转引、无增量、不开源级卡。真正的原始数据只有两张专表：表 1（GRB 180706A，3 行 COATLI）与表 2（GRB 180812A，41 行 COATLI）。库内被本文覆盖的其余样本源（约百余个 Swift 时代 GRB）均属表 3 转引，不逐一列入本卡。

## 涉及源一览

| 源 | 表号 | 源级卡 | status | 增量判读 |
|---|---|---|---|---|
| GRB180706A | 表 1（3 行 COATLI w） | 无（未开） | extracted | 表值 w≈17.1（T=615–634 s）与 GCN 22910 同仪器 coadd w=18.73、GCN 22922 UVOT white 18.11 冲突约 1.6 mag，疑似校准/转写问题，未入库；见 PR #669 待决事项 ① |
| GRB180812A | 表 2（41 行 COATLI w，5 s 逐帧） | `audit/leads/GRB180812A.md` | extracted | 逐帧测光为 GCN 23132（仅给个别数值）拿不到的量，过增量门槛第 1 条 |

## 增量门槛判读

- GRB180706A：数值过第 1 条（专表）但与同仪器 GCN 值冲突，属「数值找不到可信出处」情形，待维护者裁决后再定去留——未给该源开卡、未把数值写进该源 comment 以外的任何地方（该源由本 PR 同批审核）。
- GRB180812A：过门槛，已开源级卡。
- 其余样本源：表 3 纯转引 GCN/Swift/BAT 目录，不开卡。

## 待决

- 表 1（GRB 180706A）3 点与 GCN 22910 的冲突需维护者裁定（PR #669 待决事项 ①）。
- VoR（OUP）整站 403，两表均取自 arXiv 2308.07882；unpaywall 显示无其他 OA 副本。若维护者可通读 VoR，请顺带核对表 1/表 2 与 arXiv 版是否一致。
