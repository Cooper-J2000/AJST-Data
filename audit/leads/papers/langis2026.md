paper_key: langis2026
paper: Langis D. A. et al. 2026, A&A 707, A171, "Repeating flares, X-ray outbursts and delayed infrared emission: A comprehensive compilation of optical tidal disruption events: TDECat", DOI 10.1051/0004-6361/202554882（bibcode 2026A&A...707A.171L；VoR aanda.org DataDome 反爬，arXiv:2506.05476 可读；官方机读数据在 github.com/dlangis/TDECat）
date: 2026-11-07
helper: Rusty-Harpoon@zcode
sources: AT2016fnl,AT2017eqx,AT2017gge,AT2018bsi,AT2018dyb,AT2018fyk,AT2018hco,AT2018hyz,AT2018iih,AT2018jbv,AT2018lna,AT2018lni,AT2018mli,AT2018zr,AT2019ahk,AT2019azh,AT2019bhf,AT2019cho,AT2019dsg,AT2019ehz,AT2019gte,AT2019lwu,AT2019meg,AT2019mha,AT2019qiz,AT2019teq,AT2019vcb,AT2020acka,AT2020afhd,AT2020ddv,AT2020ksf,AT2020mbq,AT2020mot,AT2020neh,AT2020nov,AT2020ocn,AT2020opy,AT2020pj,AT2020qhs,AT2020riz,AT2020ukj,AT2020vdq,AT2020vwl,AT2020wey,AT2020ysg,AT2020yue,AT2020zso,AT2021ack,AT2021axu,AT2021blz,AT2021crk,AT2021ehb,AT2021gje,AT2021jjm,AT2021jsg,AT2021lo,AT2021mhg,AT2021nwa,AT2021qth,AT2021qxv,AT2021sdu,AT2021uqv,AT2021utq,AT2021uvz,AT2021yte,AT2021yzv,AT2022adm,AT2022aee,AT2022agi,AT2022arb,AT2022bdw,AT2022csn,AT2022czy,AT2022dbl,AT2022dsb,AT2022dyt,AT2022emf,AT2022exr,AT2022fpx,AT2022gdw,AT2022gri,AT2022hvp,AT2022ibq,AT2022lri,AT2022pna,AT2022rz,AT2022upj,AT2022wtn,AT2023clx,AT2023cvb,AT2023kvy,AT2023lli,AT2023mfm,AT2023mhs,AT2023rvb,AT2023tmq,AT2023ugy,AT2023vto,AT2023wdb,AT2023xen,AT2024admt,AT2024aepd,AT2024agqx,AT2024as,AT2024bgz,AT2024doo,AT2024eqp,AT2024gre,AT2024gxr,AT2024kt,AT2024lhc,AT2024mvz,AT2024pvu,AT2024qab,AT2024rny,AT2024tvd,AT2024ule,AT2024vip,AT2024wsd,AT2024ymu,AT2024yqo,AT2024zau

## 为什么是文献级卡

TDECat：光 TDE 编译目录（Langis+2026），目录行 138 个 TDE，其中 122 个为库内已存在源（本仓
`tde` 标签源的主体）。本文是**多源机读数据文献**的典型：官方补充仓库 github.com/dlangis/TDECat
给出逐源机读表——Section 1 `TDE_catalogue_all.csv`（目录行：坐标/z/宿主/发现时刻与星等）、
Section 2 `Photometry/Optical and Infrared/target_AT<name>_photometry.csv`（BHTOM 编译
ZTF/ATLAS/CRTS/SDSS/ASAS-SN/NEOWISE/PS1/GSA 等巡天测光，MJD;Magnitude;Error;Facility;Filter;Observer）、
`UVOT/AT<name>_uvot_lightcurve.csv`（Swift/UVOT 六波段）、`X-ray/AT<name>_xray_lightcurve.csv`
（Swift/XRT 等，X 射线不在审核范围）、Section 3 光谱。库内这批 TDE 源大多由 TDECat 建源、
光变待补，审核时以逐源 PR 直接从官方仓库取数入库（先例 PR #896–#944 及本 PR #984）。

## 涉及源一览

上列 122 源在 TDECat 目录行与 Section 2 逐源光度文件中**逐源**出现，共用同一套口径：

- 表号：目录行＝Section 1 `TDE_catalogue_all.csv`（VizieR 镜像 `J/A+A/707/A171/tdecat` 同值）；
  测光＝Section 2 `target_AT<id>_photometry.csv`（CDS/VizieR 未收录光变表，仅 `tdecat`/`table1` 两表）；
- 口径要点（接手者必读）：编译行为**总流量含宿核**（非差分）；星等系统按 §3.1 原文——
  ZTF/ATLAS/Pan-STARRS 记 AB，CRTS/ASAS-SN V/Swift/NEOWISE 记 Vega，**Gaia G 为非 AB/Vega
  内部定标**（mag_system 留空）；CRTS(CL) 无滤光片→band=G 承载；UVOT 行**已银消光改正、
  未扣宿主**（§3.3 原文明言）→ Gext_corr=y；同历元同值双误差行多见（§3.4 保留首行）；
  编译光变可能含 artifacts（论文自述）；
- 源级卡：无（122 源均未开源级卡——各源审核时直接从官方仓库取数入库，无需中间卡；
  已按此路径完成的源见 PR #896–#944、#984 等）。

## 增量门槛判读

- 122 个库内 TDE 源**全部过门槛**：TDECat 机读测光表是「库内 GCN/目录拿不到的数值」，
  且为库内源提供了 Langis+2026 这一新的正式文献引用（bibcode 级）；
- 但**不开源级卡**：本文数据获取路径完全一致（官方 GitHub 仓库逐源 CSV），接手者按
  本卡「口径要点」直接取数即可，卡只保留这一张索引。

## 待决

- 无（TDECat X 射线机读文件按 §3.3/§7 不入库，各源审核时在 comment 记一句即可；
  ATLAS 编译行偶见 ATLAS(H) 等无法唯一判读的波段名，各源自查——先例 AT2019dsg 2 行未入库）。
