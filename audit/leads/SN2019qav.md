# 线索：SN2019qav（ZTF19abyjzvd；Ho+2023 表2/表5/表6/表7/表8 覆盖）

- source_id: SN2019qav
- status: extracted
- paper: Ho+2023, ApJ 949, 120（DOI 10.3847/1538-4357/acc533; arXiv:2105.08811v2）：表5 UVOT 测光、表6 Swift/XRT、表7 mm/射电、表8 VLASS、表2 sources_all
- pr: #889
- helper: Rusty-Harpoon@zcode
- date: 2026-11-05

## 版本状态

IOP VoR 被 Radware Bot Manager 反爬（2026-11-05 实测），未通读 VoR；行值取自 **arXiv:2105.08811v2**（2023-05-31，清样后版本）TeX 源逐行提取。表 4（tab:ztf-lc）机读表未取得（IOP 反爬）。已登记 `audit/unverified.tsv`（见 CSS161010 行）。

## 原文口径（原样记录，**未做任何换算**）

- 表 2（sources_all）：ZTF19abyjzvd，RA 16:48:12.90、Dec +48:04:50.0，SN 2019qav，Peak MJD 58739.13，Peak g 18.99±0.06，t_1/2,g 10.8±0.5 d，g−r −0.3，z 0.1353，IIn/Ibn，文献 [17]。
- 表 5（UVOT）：JD + Δt（自 first ZTF detection，历元未核）；AB 星等（Breeveld+2011）。
- 表 7（mm/射电）：Start Date 为 JD，f_ν 单位 μJy，上限=3× image RMS。
- 表 8：Survey / MJD / Δt [d] / RMS [μJy]。
- 表 6（XRT）：**X 射线行不在库审核范围，仅记录**。

## 已核对 / 未核对

- 已核对：表 5/6/7/8 本源行逐行对照 arXiv v2 TeX（下方原始行即原样转录）。
- 未核对：未换算 T0、未去重、未查其他文献（[17] 未展开）、UVOT 单历元 B 波段误差 1.55 mag 的处理。

## 原始行（原样）

表 5 UVOT（JD / Δt d / 滤光 / AB mag）：

| JD | Δt | 滤光 | mag |
|---|---|---|---|
| 2458755.88 | 18.24 | UVW1 | 21.59±0.33 |
| 2458755.88 | 18.24 | U | 21.06±0.49 |
| 2458755.88 | 18.24 | B | 21.64±1.55 |
| 2458755.88 | 18.24 | UVW2 | 22.41±0.33 |
| 2458755.88 | 18.25 | V | 20.20±0.78 |
| 2458755.89 | 18.25 | UVM2 | 22.22±0.27 |

表 7 mm/射电（仪器 / 程序(PI) / JD / Δt d / ν GHz / f_ν μJy / L_ν）：

| 仪器 | 程序 (PI) | JD | Δt | ν | f_ν | L_ν |
|---|---|---|---|---|---|---|
| NOEMA | S19BC (Ho) | 2458753.20 | 15.56 | 90 | <90 μJy | <4.8×10²⁸ |
| VLA | 18B-242 (Perley) | 2458765.42 | 27.78 | 10 | <18 μJy | <9.6×10²⁷ |
| VLA | 20A-374 (Ho) | 2458922.12 | 184.48 | 10 | <27 μJy | <1.4×10²⁸ |

表 8 巡天行：VLASS，MJD 59072，Δt 332 d，RMS 166 μJy。

表 6 XRT（**X 射线，不在库审核范围，仅记录**）：JD 2458755.88/18.25 ct<4.05 flux<1.37 lum<71.12。

## 备注

本卡随 CSS161010 数据 PR（#889）提交。另见 `papers/ho2023.md` 索引卡。
