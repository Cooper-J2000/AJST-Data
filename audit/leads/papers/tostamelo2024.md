# 文献索引：Tosta e Melo+2024（GRANDMA「Ready for O4 II」Swift GRB 观测汇编）

- paper_key: tostamelo2024
- paper: Tosta e Melo+2024, A&A 682, A141（DOI 10.1051/0004-6361/202347938；arXiv:2310.17287；2024-02）
- date: 2026-11-16
- helper: fsy@zcode
- sources: GRB220403B, GRB220325A, GRB220408A, GRB220412A, GRB220427A, GRB220430A, GRB220501A, GRB220514A

## 为什么是文献级卡

GRANDMA 网络 2022 年春八周 Swift GRB 跟随训练 campaign 的正式发表版：§5.1/§5.2 逐暴小节 + 附录 B 两张表（B.1 逐帧探测/上限日志、B.2 每镜一选上限）。VoR 排版版已经 HAL（hal-04274105）取得并通读；aanda.org 被 DataDome 403。库内 9 个源被覆盖（GRB220412A 由 PR #1093 直接审核并采纳其 Table B.2 三行）；GRB220404A/GRB220412B 文内明确"触发但未观测"，无数据行（库外/无增量）。

## 涉及源一览

| 源 | 表号 | 源级卡 | status | 增量判读 |
|---|---|---|---|---|
| GRB220403B | B.1（26 行）+ B.2（1 行） | `audit/leads/GRB220403B.md`（#1093） | extracted | **过门槛**：GCN 31883 仅 7 行，B.1 的 ~19 行（含 g/r 逐帧探测、SNOVA B=22.22±0.12、UBAI/AZT-22 G>21.0）GCN 拿不到 |
| GRB220325A | B.2（3 行） | `audit/leads/GRB220325A.md`（#1093） | extracted | **过门槛**：NOWT 4.72 h 20.9 / KAO 8.11 h 21.5 R / KAO 10.16 h 21.6 R 均不在库内 lc |
| GRB220408A | B.2（2 行） | `audit/leads/GRB220408A.md`（#1093） | extracted | **过门槛**：UBAI/AZT-22 R 19.3（1.82 h）/20.6（4.95 h）不在库内 lc（32 行） |
| GRB220412A | B.2（3 行）+ §5.1 小节 | 无（PR #1093 已直接采纳入库） | extracted | PR #1093 已把 C2PU-Omicron r>21.7、Xinglong-TNT Clear>20.5/r>20.3 入库；本卡仅索引 |
| GRB220427A | B.1（12 行）+ B.2（2 行） | `audit/leads/GRB220427A.md`（#1093） | extracted | **过门槛**：KNC-T-CAT/TAROT 12 行探测/上限不在库内 lc（10 行）；论文 §5.2 光度红移 z=0.82±0.09（非本卡范围，接手者回原文） |
| GRB220430A | B.2（3 行） | `audit/leads/GRB220430A.md`（#1093） | extracted | **过门槛**：SNOVA 17.74 h Clear 19.3 / TRT-SRO 6.59 h R 20.3 / GMG-2.4 3.22 h Clear 18.7 不在库内 lc（12 行） |
| GRB220501A | §5.1 小节（r>16.0，触发后 ~30 min 起，业余镜） | 无 | mention-only | **不过门槛**：同测量已入库（GCN 31984 GRANDMA/TJML r 16.0 行），纯转引 |
| GRB220514A | B.1（7 行）+ B.2（3 行） | `audit/leads/GRB220514A.md`（#1093） | extracted | **过门槛**：TAROT/TRE、Les Makes/T60、VIRT 各行不在库内 lc（11 行） |

## 增量门槛判读

- 开源级卡 6 张（220403B/220325A/220408A/220427A/220430A/220514A）：判据 1（VoR 表值经程序化比对不在库内 lc，且抽查明 GCN 31883 仅 7 行、远少于 B.1，其余暴 GRANDMA GCN 亦为节选）+ 判据 3（新 VoR 引用）。
- 不开卡：GRB220501A（§5.1 限值=GCN 31984 同测量，纯转引）、GRB220412B（文内明确未观测）、GRB220404A（文内明确未观测）。
- 原始行均已逐字转录进各源级卡（pdftotext 留痕在 PR 作者 `_conv/lit-GRB220412A/` 工作目录：page1314.txt/page15.txt），**未换算、未去重、未对齐库内 T0——不得直接抄进 lc/**。

## 待决

- GRB220404A 库外无源：按契约应开 `new-source: GRB220404A（来自 10.1051/0004-6361/202347938 的多目标线索）` Issue——本 PR 作者无 gh 权限，请主会话代办（文内明确其无 GRANDMA 数据行，仅为 campaign 目标）。
- B.1 表 Telescope 列为多行合并布局，pdftotext 转录的归属需接手者回 VoR PDF 复核。
- B.1 注自称"只报探测"但表内含 `>` 上限行（原文自身口径），转录未改。
