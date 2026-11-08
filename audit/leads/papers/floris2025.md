paper_key: floris2025
paper: Floris A. et al. 2025, A&A 703, A81, "Polarimetric diversity in tidal disruption events: Comparative study of low-polarised sources with AT2020mot", DOI 10.1051/0004-6361/202555626（bibcode 2025A&A...703A..81F；VoR aanda.org DataDome 反爬，arXiv:2509.08895 可读）
date: 2026-11-07
helper: Rusty-Harpoon@zcode
sources: AT2020mot,AT2020afhd,AT2022dbl,AT2022fpx,AT2022gri,AT2022hvp,AT2022upj,AT2022wtn,AT2023clx,AT2023ugy,AT2023lli,AT2024bgz,AT2024gre

## 为什么是文献级卡

13 个有偏振观测的 TDE 样本比较文章（AT2020mot 为 headline 源），13/13 全部为库内已存在源。
文章内容为**偏振测量与样本级拟合参数**，不含逐历元测光表：

- Table 1（样本表）：Name / Spectral type / z / Πmax（最大偏振度）；
- Table 2/3/5：log L_bol、T_bb、TDEMass/MOSFiT 的 M_BH 与 M_*、t_peak、t_rise（样本级拟合派生量）；
- Table 6：AT2020mot 与其余 12 源的参数对比；
- Table 7（45 行）/Table 8（13 行）：逐历元偏振测量（MJD、Δt_peak、Π/Πcorr、Θ、q/u、Telescope、Filter）；
- Table 4：拟合模型公式（非数据）。

## 涉及源一览

| 源 | 表号 | 源级卡 | status | 增量判读 |
|---|---|---|---|---|
| AT2020mot | 表1/2/3/5/6/7/8 | 无 | mention-only | 偏振数据完整（峰值 Π=25±4%，Liodakis+2023 专篇已入库其测光）；本卡建立时该源同 PR 审核完成（#984） |
| AT2020afhd | 表1/7 | 无 | mention-only | 偏振历元表 7 有该源行；无测光表 |
| AT2022dbl | 表1/7 | 无 | mention-only | 同上 |
| AT2022fpx | 表1/7 | 无 | mention-only | 同上 |
| AT2022gri | 表1/7 | 无 | mention-only | 同上 |
| AT2022hvp | 表1/7 | 无 | mention-only | 同上 |
| AT2022upj | 表1/7 | 无 | mention-only | 同上 |
| AT2022wtn | 表1/7 | 无 | mention-only | 同上 |
| AT2023clx | 表1/7 | 无 | mention-only | 同上 |
| AT2023ugy | 表1/7 | 无 | mention-only | 同上 |
| AT2023lli | 表1/7 | 无 | mention-only | 同上 |
| AT2024bgz | 表1/7 | 无 | mention-only | 同上 |
| AT2024gre | 表1/7 | 无 | mention-only | 同上 |

## 增量门槛判读

- **不开源级卡**：本文给的是偏振测量（Π/Θ/q/u）与样本级拟合派生量（log L_bol、T_bb、M_BH、
  t_peak 等），**无任何逐历元测光表**——不满足源级卡的增量门槛（非测光数据、非 T0/定标/消光
  关键口径）；纯「样本列表 + 偏振历元」性质；
- 但为库内源提供了**新的正式文献引用**（Floris+2025 bibcode 级）与偏振量记档价值：
  各源审核时可在 `comment` 记「Πmax=<值>%（Floris+2025 表1）」，偏振逐历元值接手者可按需
  自取（arXiv:2509.08895 表7）。

## 待决

- 无（偏振测量不属于测光车道，不入 lc；若维护者后续想为 TDE 偏振建立数据位（params 或
  专项存储），可在 Issue 层面另议，本卡只做索引。）
