# 文献索引：Hammerstein+2023（ZTF-I 全期 30 个 TDE 样本）

- paper_key: hammerstein2023
- paper: Hammerstein+2023, ApJ 942, 9（DOI 10.3847/1538-4357/aca283；arXiv:2203.01461 v1；The Final Season Reimagined: 30 Tidal Disruption Events from the ZTF-I Survey）
- date: 2026-11-05
- helper: Rusty-Harpoon@zcode
- out_of_repo: 无（30 个 TDE 全部在库内）
- sources: AT2018zr, AT2018bsi, AT2018hco, AT2018iih, AT2018hyz, AT2018lni, AT2018lna, AT2018jbv, AT2019cho, AT2019bhf, AT2019azh, AT2019dsg, AT2019ehz, AT2019mha, AT2019meg, AT2019lwu, AT2019qiz, AT2019teq, AT2020pj, AT2019vcb, AT2020ddv, AT2020ocn, AT2020opy, AT2020mot, AT2020mbq, AT2020qhs, AT2020riz, AT2020wey, AT2020zso, AT2020ysg

## 为什么是文献级卡

Hammerstein+2023 是 ZTF-I 全期（2018-03–2020-12）30 个光谱分类 TDE 的专篇样本文章，
含光谱分类表（Table 1，含多次改判）、光变形状参数表（t_peak 等，deluxetable "Light curve shape
parameters"）、宿主星系表（host_tab：lgMstar 等）与 MOSFiT 黑洞质量表（MBH_MStar）。
正文声明 ZTF forced photometry 光变 "will be available in machine-readable format at the journal
website"、Figures 17–18 数据在 figure related files——**IOP 整站 Radware 反爬（curl 与浏览器均
captcha，2026-11-05 双通道实测），arXiv v1 源码只有 PDF 图（figures/maglc/、figures/lcfits/）无逐行
数值表，故其逐历元测光本 PR 未入库**（audit/unverified.tsv 已登记 missing）。
AT2019bhf 行的表值（分类、t_peak、宿主质量）已在审核该源时核对并写入其 info comment。

## 涉及源一览

| 源 | 表号（原文位置） | 源级卡 | status | 增量判读 |
|---|---|---|---|---|
| AT2018zr | 表 1（分类）；LCfittab；host_tab；MBH_MStar | 无 | mention-only | 过门槛③：正式文献引用 + 分类/t_peak/宿主参数（接手者自行从 VoR/arXiv 表核对） |
| AT2018bsi | 同上 | 无 | mention-only | 过门槛③：同上 |
| AT2018hco | 同上 | 无 | mention-only | 过门槛③：同上 |
| AT2018iih | 同上 | 无 | mention-only | 过门槛③：同上 |
| AT2018hyz | 同上 | 无 | mention-only | 过门槛③：同上 |
| AT2018lni | 同上 | 无 | mention-only | 过门槛③：同上 |
| AT2018lna | 同上 | 无 | mention-only | 过门槛③：同上 |
| AT2018jbv | 同上 | 无 | mention-only | 过门槛③：同上 |
| AT2019cho | 同上 | 无 | mention-only | 过门槛③：同上 |
| AT2019bhf | 表 1（TDE-H+He，z=0.121）；LCfittab（t_peak=58543.90(+1.47/−1.87) MJD）；host_tab；附录光谱段 | 已审核（2026-11-05，见该源 info comment） | 已核对 | 表 1/LCfittab 值已写入该源 info comment；逐历元测光因 IOP 反爬未取（unverified.tsv missing） |
| AT2019azh | 表 1；LCfittab；host_tab；MBH_MStar | 无 | mention-only | 过门槛③：同上 |
| AT2019dsg | 同上 | 无 | mention-only | 过门槛③：同上 |
| AT2019ehz | 同上 | 无 | mention-only | 过门槛③：同上 |
| AT2019mha | 同上 | 无 | mention-only | 过门槛③：同上 |
| AT2019meg | 同上 | 无 | mention-only | 过门槛③：同上 |
| AT2019lwu | 同上 | 无 | mention-only | 过门槛③：同上 |
| AT2019qiz | 同上 | 无 | mention-only | 过门槛③：同上 |
| AT2019teq | 同上 | 无 | mention-only | 过门槛③：同上 |
| AT2020pj | 同上 | 无 | mention-only | 过门槛③：同上 |
| AT2019vcb | 同上 | 无 | mention-only | 过门槛③：同上 |
| AT2020ddv | 同上 | 无 | mention-only | 过门槛③：同上 |
| AT2020ocn | 同上 | 无 | mention-only | 过门槛③：同上 |
| AT2020opy | 同上 | 无 | mention-only | 过门槛③：同上 |
| AT2020mot | 同上 | 无 | mention-only | 过门槛③：同上 |
| AT2020mbq | 同上 | 无 | mention-only | 过门槛③：同上 |
| AT2020qhs | 同上 | 无 | mention-only | 过门槛③：同上 |
| AT2020riz | 同上 | 无 | mention-only | 过门槛③：同上 |
| AT2020wey | 同上 | 无 | mention-only | 过门槛③：同上 |
| AT2020zso | 同上 | 无 | mention-only | 过门槛③：同上 |
| AT2020ysg | 同上 | 无 | mention-only | 过门槛③：同上 |

## 增量门槛判读

- 30 源全部**过门槛③**（新的正式文献引用：光谱分类——多篇对 van Velzen+2021/Gezari+2018 等有改判，
  如 AT2019bhf TDE-H→TDE-H+He、AT2019cho→TDE-H+He——以及 t_peak、lgMstar、lgMBH 等并列表值）。
- **逐历元测光未入库**：ZTF forced photometry 机读表仅存于 IOP 期刊页（Radware 反爬不可达），
  arXiv 版无替代（maglc/lcfits 只有 PDF 图）；接手者若维护者侧仍取不到，按 §3.3 第 4 级处理
  （unverified.tsv missing 行已登记，不得凭摘要/图读数补值）。
- **改判提示**：表 1 的光谱分类与 vanVelzen+2021（TDE-H/TDE-Bowen/TDE-He 三类体系）多处不一致，
  两文分类应并列记录、不互相覆盖；Langis+2026 正文亦明言三家分类互有出入。
- 附录（Appendix A/B）逐源光谱描述与早晚谱历元（如 AT2019bhf：SEDM 2019-03-30 phase 28、
  LDT/DeVeny 2019-06-29 phase 119）对接手者核对光谱可用性有用。

## 待决

- IOP 机读 ZTF forced photometry 不可达（Radware）；若后续可取，30 源的 ZTF 差分口径光变
  与 TDECat 总流量口径可并存互补，届时按各源审核逐值核对入库。
