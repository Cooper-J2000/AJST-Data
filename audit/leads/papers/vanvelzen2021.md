# 文献索引：van Velzen+2021（ZTF-I 前 17 个光学 TDE 样本）

- paper_key: vanvelzen2021
- paper: van Velzen+2021, ApJ 908, 4（DOI 10.3847/1538-4357/abc258；arXiv:2001.01409 v1；Seventeen Tidal Disruption Events from the First Half of ZTF Survey Observations: Entering a New Era of Population Studies）
- date: 2026-11-05
- helper: Rusty-Harpoon@zcode
- out_of_repo: AT2019eve（new-source Issue 另报，见 PR 待决）
- sources: AT2018zr, AT2018bsi, AT2018hco, AT2018iih, AT2018hyz, AT2018lni, AT2018lna, AT2019cho, AT2019bhf, AT2019azh, AT2019dsg, AT2019ehz, AT2019mha, AT2019meg, AT2019lwu, AT2019qiz, PS1-10jh, AT2017eqx, PTF09ge, PTF09djl, ASASSN-14ae, ASASSN-14li, ASASSN-15oi, AT2018dyb, AT2018fyk, AT2019ahk, iPTF15af, iPTF16axa

## 为什么是文献级卡

van Velzen+2021 是 ZTF-I 前半程 17 个光学 TDE 的专篇样本文章（GOT 昵称体系：Ned/Jon/Sansa/…）。
**arXiv:2001.01409 v1 源码随文携带逐源光度数据文件 `data/<昵称>.dat`（实测 16 个 .dat；17 个 ZTF TDE 中 AT2018bsi 无 data 文件——其差分光变被参考像污染，作者声明交出版社网站，v1 仅 lc_JonSnow.pdf 等图）**，
列为 Table 5（光变形状参数 t_peak 等）与多波段拟合的输入；另含 22 个文献 TDE（Table 4, tab:known）
的已发表测光转引。库内 28 个源被本文涉及（17−1 库外 AT2019eve ＋ 12 个文献 TDE）。
出版社数据页声明 "will be made available at the publisher website"（§4）；IOP 整站 Radware 反爬
（curl 与浏览器均 captcha，2026-11-05 双通道实测，audit/unverified.tsv 已登记）。
AT2019bhf 的 `Varys.dat` 已在审核该源时逐值核对入库（36 探测行；28 行 flux=0 非探测因原文未给上限值未入库）。

## 涉及源一览

| 源 | 表号（官方数据位置） | 源级卡 | status | 增量判读 |
|---|---|---|---|---|
| AT2018zr | data/NedStark.dat（GOT 昵称 Ned）；表 6 | 无 | mention-only | 过门槛①：逐源光度 .dat（ZTF 差分成像 + UVOT host-subtracted，静止系时标），接手者须自行下载核对 |
| AT2018bsi | 无 data 文件（差分光变被参考像污染，作者声明交出版社网站；v1 仅 lc 图）；表 6 | 无 | mention-only | 门槛①不满足（v1 无机读表，VoR 出版社页可能存在）；过门槛③（分类/参数引用） |
| AT2018hco | data/SansaStark.dat；表 6 | 无 | mention-only | 过门槛①：同上 |
| AT2018iih | data/JorahMormont.dat；表 6 | 无 | mention-only | 过门槛①：同上 |
| AT2018hyz | data/GendryBaratheon.dat；表 6 | 无 | mention-only | 过门槛①：同上 |
| AT2018lni | data/AryaStark.dat；表 6 | 无 | mention-only | 过门槛①：同上 |
| AT2018lna | data/CerseiLannister.dat；表 6 | 无 | mention-only | 过门槛①：同上 |
| AT2019cho | data/PetyrBalish.dat；表 6 | 无 | mention-only | 过门槛①：同上 |
| AT2019bhf | data/Varys.dat；表 6 | 已审核（2026-11-05，见该源 info comment 与 lc） | 已核对入库 | 36 探测行已入库（LT/IO:O u/g、Swift/UVOT host-subtracted AB、ZTF 差分成像 Jy）；28 行 flux=0 未入库 |
| AT2019azh | data/JaimeLannister.dat；表 6 | 无 | mention-only | 过门槛①：同上 |
| AT2019dsg | data/BranStark.dat + Bran_lx_Swift.dat/_ul.dat（Swift/XRT）；表 6 | 无 | mention-only | 过门槛①：同上（另含 X 射线文件，按规则不入库） |
| AT2019ehz | data/Brienne.dat + Brienne_lx_Swift.dat/_ul.dat；表 6 | 无 | mention-only | 过门槛①：同上 |
| AT2019mha | data/Bronn.dat；表 6 | 无 | mention-only | 过门槛①：同上 |
| AT2019meg | data/MargaeryTyrell.dat；表 6 | 无 | mention-only | 过门槛①：同上 |
| AT2019lwu | data/RobbStark.dat；表 6 | 无 | mention-only | 过门槛①：同上 |
| AT2019qiz | data/Melisandre.dat；表 6 | 无 | mention-only | 过门槛①：同上 |
| PS1-10jh | 表 4（tab:known，转引 Gezari+2012 已发表测光） | 无 | mention-only | 过门槛③（正式文献引用）；数据为转引，接手者仍须回原始文献 |
| AT2017eqx | 表 4（PS17dhz；转引 Nicholl+2019） | 无 | mention-only | 过门槛③：同上 |
| PTF09ge | 表 4（转引 Arcavi+2014） | 无 | mention-only | 过门槛③：同上 |
| PTF09djl | 表 4（转引 Arcavi+2014） | 无 | mention-only | 过门槛③：同上 |
| ASASSN-14ae | 表 4（转引 Holoien+2014） | 无 | mention-only | 过门槛③：同上 |
| ASASSN-14li | 表 4（转引 Holoien+2016）；另 data/ 无独立文件 | 无 | mention-only | 过门槛③：同上 |
| ASASSN-15oi | 表 4（转引 Holoien+2016b） | 无 | mention-only | 过门槛③：同上 |
| AT2018dyb | 表 4（ASASSN-18pg；转引 Leloudas+2019） | 无 | mention-only | 过门槛③：同上 |
| AT2018fyk | 表 4（ASASSN-18ul；转引 Wevers+2019） | 无 | mention-only | 过门槛③：同上 |
| AT2019ahk | 表 4（ASASSN-19bt；转引 Holoien+2019） | 无 | mention-only | 过门槛③：同上 |
| iPTF15af | 表 4（转引 Blagorodnova+2019） | 无 | mention-only | 过门槛③：同上 |
| iPTF16axa | 表 4（转引 Hung+2017） | 无 | mention-only | 过门槛③：同上 |

## 增量门槛判读

- 17 个 ZTF TDE（16 在库 + AT2019eve 库外）**过门槛①**：arXiv 源码 `data/*.dat` 逐源光度文件是
  库内 GCN/目录检索拿不到的数值（差分成像纯瞬变口径，与 TDECat/BHTOM 总流量口径不同）。
- 12 个文献 TDE **过门槛③**（新的正式文献引用/光谱分类并列值），但其测光为转引、无新数值。
- 表 4（tab:known）另有 11 个**库外**源（PS1-11af、PTF09axc、ASASSN-15lh、iPTF16fnl、OGLE16aaa、
  SDSS-TDE1/2、GALEX-D1-9/D3-13/D23H-1 及 AT2019eve）：均为样本成员/转引已发表测光，本文未给其新数值
  （除 AT2019eve 有 data/CatelynStark.dat），不逐个开 new-source Issue；如需入库由维护者按流程办理。
- **口径提示（审 AT2019bhf 时确证）**：`data/*.dat` 文件头声明「Time, luminosity, and frequency,
  measured in TDE rest frame and corrected for Galactic extinction. The flux (in Jy) is not corrected
  for Galactic extinction」——day_since_peak 为**静止系**天，须乘 (1+z) 换算到观测系 MJD
  （mjd = 文件头 t_peak + day×(1+z)）；flux_Jy 未做银消改正（Gext_corr=n）；AB 系统（论文正文声明）；
  ZTF/UVOT/LT/SEDM 均为 host-subtracted 口径。flux=0 行为非探测占位（仅 err_lum，未给上限值）。
- 论文正文声明 "All magnitudes are reported in the AB system"（§2 末）；Swift/UVOT 用 uvotsource
  5″ 孔径、AB 系统（§4 UV: Swift/UVOT 小节）。

## 待决

- IOP 出版社数据页（Varys.dat 等 17 文件的 VoR 版）因 Radware 反爬双通道不可达，均以 arXiv v1 源码
  data 文件替代（unverified.tsv 已登记）；若维护者侧可取 VoR 数据页，建议对已入库的 AT2019bhf 36 行做一次复核。
- AT2019eve（ZTF19aatylnl）库外且有独立数据文件，已按 §3.11.5 开 new-source Issue（见本 PR 待决事项）。
