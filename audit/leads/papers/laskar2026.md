- paper_key: laskar2026
- paper: Laskar+2026, "Revealing the Structure and Magnetization of GRB Jets with ALMA Polarization Observations", arXiv:2607.20604v1（2026-07-22 提交；preprint-only，Crossref/OpenAlex 检索无正式发表版 @2026-11-16）
- date: 2026-11-16
- helper: fsy@zcode
- sources: GRB171205A,GRB190114C,GRB190829A,GRB191221B,GRB210610B,GRB210702A,GRB220521A,GRB221009A,GRB250327B,GRB251013C

## 为什么是文献级卡

ALMA 3mm 偏振样本专篇（11 个 GRB、24 次观测，其中 20 次新观测），主表（tab:grb_pol）给出每个历元的
Stokes I（mJy）、Q/U/V（μJy）、P_L（μJy）、Π_L（%）、χ（°）；附录表 tab:grb_pol_pipe 为 ALMA pipeline
独立复算对照；表 tab:obs 给出各历元日期、项目号与定标链。库内命中 10 个源（另 GRB 220921A 为本卡提出者的
审核对象，其两历元 I 值已随 PR #1076 入库）。本卡只做索引；可采纳数值在通过增量门槛的源级卡里。

## 涉及源一览

| 源 | 表号 | 源级卡 | status | 增量判读 |
|---|---|---|---|---|
| GRB171205A | Table 1（3 历元，其中 2 行标 *＝转引 uth+19/lhc20） | 无 | mention-only | 中：lc 已有同历元 97.5GHz 行但为另一缩减版（数值有别）；本文 36.04 d 历元疑 lc 未载——需接手者开原文逐历元比对 |
| GRB190114C | Table 1（8 历元，前 3 行标 *＝转引 lag+19） | GRB190114C.md | extracted | 高：5 个新历元（1.12–86.97 d）Stokes I 不在 lc（lc 仅 0.1–0.24 d 早历元） |
| GRB190829A | Table 1（1 历元） | GRB190829A.md | extracted | 高：lc 无 97.5GHz ALMA 偏振历元（仅 GCN25589 90GHz 早历元） |
| GRB191221B | Table 1（4 历元，后 2 行标 *＝转引 utc+23） | GRB191221B.md | extracted | 高：lc 无任何 GHz 行；2 个新历元为本文首报 |
| GRB210610B | Table 1（1 历元） | GRB210610B.md | extracted | 高：lc 无 GHz 行 |
| GRB210702A | Table 1（1 历元） | GRB210702A.md | extracted | 高：与 lc 同历元（≈1.1 d）数值冲突（GCN30423 0.1 mJy vs 本文 I=2.133 mJy），需接手者裁定 |
| GRB220521A | Table 1（2 历元） | GRB220521A.md | extracted | 高：晚历元（56/82 d）深限 I 值不在 lc（lc 仅 GCN32110 早历元 1 行） |
| GRB221009A | Table 1（2 历元：145 GHz @3.39 d、97.5 @5.32 d） | 无（源已 reviewed 2026-11-13，Rusty-Harpoon@zcode） | mention-only | 中：145 GHz 历元疑为 lc 未载；已审源，是否补行请维护者裁定（不写源级卡以免滞留告警） |
| GRB250327B | Table 1（1 历元） | GRB250327B.md | extracted | 高：本文 1.20 d 历元不在 lc（lc 仅 GCN39933 2.07 d 一行） |
| GRB251013C | Table 1（1 历元） | GRB251013C.md | extracted | 高：本文 8.24 d 历元不在 lc（lc 仅 GCN42243 0.96 d 一行） |

## 增量门槛判读

- 过门槛（有源级卡）：190114C、190829A、191221B、210610B、210702A、220521A、250327B、251013C——
  判据 1（未单独发 GCN 的测光表：ALMA 偏振计划 Stokes I 为本文首报/未入 lc）。
- 不过门槛（仅本卡索引）：171205A（lc 已有同历元另一缩减版，接手者逐历元判读即可）、
  221009A（已 reviewed；145 GHz 历元交维护者裁定）。

## 待决

- 本文为 preprint-only：VoR 出版后各源级卡数值需回代核对（尤其表内 t 的精确定义与各历元观测窗口）。
- 221009A（已审）的 145 GHz 历元是否补入其 lc：维护者裁定。
