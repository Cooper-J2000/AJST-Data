- paper_key: kumar2022
- paper: Kumar+2022, New Astronomy 97, 101889（DOI 10.1016/j.newast.2022.101889；arXiv:2206.00950）——VoR ScienceDirect 反爬不可得，arXiv v1 PDF 实读（unverified.tsv substituted 登记）
- date: 2026-11-20
- helper: wa1kmoon@zcode
- sources: GRB171010A, GRB171205A, GRB111209A

# 为什么是文献级卡

Kumar+2022（DOT 4K×4K CCD Imager 光变＋MINIM 拟合样本文）覆盖 3 个库内源：GRB171010A/SN 2017htp（Table 1 主样本，4 行数据表——论文该节有自身排版缺陷行，仅存 "3×300s" 孤单元格无 JD/星等）、GRB171205A/SN 2017iuk（Table 1，5 行）、GRB111209A（Table 2/3 对 SLSN 2011kl 的 MINIM 拟合参数，无新测光行）；另有 Table A1（171010A 场次级标准星 9 星 UBVRl）与 Table A2（171205A 场次级标准星 7 星 UBVRl）两张定标星表。

## 涉及源一览

| 源 | 表号 | 源级卡 | status | 增量判读 |
|---|---|---|---|---|
| GRB171010A | Table 1（4 行 DOT）+ Table A1（标准星） | 已审（PR #1120，行已入库：time 按 JD−T0 重算、仪器更正 4K×4K CCD Imager） | extracted | 已消化 |
| GRB171205A | Table 1（5 行 DOT）+ Table A2（标准星 7 星 UBVRl） | audit/leads/GRB171205A.md | extracted | 库内 GRB171205A 无此来源，增量明确（未发 GCN 的测光行） |
| GRB111209A | Table 2/3（SLSN 2011kl MINIM 拟合参数） | audit/leads/GRB111209A.md | mention-only | 无新测光行，磁体起源参数备查 |

## 增量门槛判读

- GRB171205A：过门槛（作者自算 Δt/JD 测光行，库内 GCN 检索无此来源）——已有源级卡。
- GRB171010A：过门槛（已审消化）。
- GRB111209A：不过门槛（拟合参数无测光行）——mention-only 卡。

## 待决

- Table A1/A2 为定标星表，无入库义务；本次仅作核验旁证未转录（GRB171205A 卡已含 Table A2 全部 35 值待核清单）。
