# 线索：SN2020rsc（ZTF20aburywx；Ho+2023 表2/表5/表6/表7 覆盖）

- source_id: SN2020rsc
- status: extracted
- paper: Ho+2023, ApJ 949, 120（DOI 10.3847/1538-4357/acc533; arXiv:2105.08811v2）：表5 UVOT 上限、表6 Swift/XRT、表7 mm/射电、表2 sources_all
- pr: #889
- helper: Rusty-Harpoon@zcode
- date: 2026-11-05

## 版本状态

IOP VoR 被 Radware Bot Manager 反爬（2026-11-05 实测），未通读 VoR；行值取自 **arXiv:2105.08811v2**（2023-05-31，清样后版本）TeX 源逐行提取。表 4（tab:ztf-lc）机读表未取得（IOP 反爬）——本源在其样本内，g/r 光变机读行未入库。已登记 `audit/unverified.tsv`（见 CSS161010 行）。

## 原文口径（原样记录，**未做任何换算**）

- 表 2（sources_all）：ZTF20aburywx，RA 01:19:56.51、Dec +38:11:09.5，SN 2020rsc，Peak MJD 59081.47，Peak g 19.36±0.07，t_1/2,g 3.3±0.3 d，g−r −0.2，z 0.0313，IIb，文献 [36]。
- 表 5（UVOT）：JD + Δt（自 first ZTF detection，历元未核）；AB 星等；本源仅 2 行上限（>）。
- 表 7（mm/射电）：Start Date 为 JD，f_ν 单位 μJy，上限=3× image RMS。
- 表 6（XRT）：**X 射线行不在库审核范围，仅记录**。
- 表 8：本源无 VLASS/RACS/VAST 行。

## 已核对 / 未核对

- 已核对：表 5/6/7 本源行逐行对照 arXiv v2 TeX（下方原始行即原样转录）。
- 未核对：未换算 T0、未去重、未查其他文献（[36] 未展开）、表 4 机读 g/r 光变未取得。

## 原始行（原样）

表 5 UVOT（JD / Δt d / 滤光 / AB mag，两行均为上限）：

| JD | Δt | 滤光 | mag |
|---|---|---|---|
| 2459087.78 | 6.87 | UVW1 | >21.0（上限） |
| 2459092.83 | 11.92 | U | >20.0（上限） |

表 7 mm/射电（仪器 / 程序(PI) / JD / Δt d / ν GHz / f_ν μJy / L_ν）：

| 仪器 | 程序 (PI) | JD | Δt | ν | f_ν | L_ν |
|---|---|---|---|---|---|---|
| VLA | 20A-374 (Ho) | 2459100.73 | 19.82 | 10 | <15 μJy | <3.6×10²⁶ |

表 6 XRT（**X 射线，不在库审核范围，仅记录**）：JD 2459087.78/6.87 ct<7.08 flux<2.91 lum<7.00；2459092.83/11.92 <22.96/<9.43/<22.68。

## 备注

本卡随 CSS161010 数据 PR（#889）提交。另见 `papers/ho2023.md` 索引卡。
