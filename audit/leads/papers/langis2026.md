# 文献级索引卡：TDECat（Langis+2026）

- paper_key: langis2026
- paper: Langis+2026, A&A 707, A171（DOI 10.1051/0004-6361/202554882；Repeating flares, X-ray outbursts and delayed infrared emission: A comprehensive compilation of optical tidal disruption events: TDECat）
- date: 2026-11-05
- helper: Rusty-Harpoon@zcode
- sources: ASASSN-14ae,ASASSN-14li,ASASSN-15oi,AT2016fnl,AT2017eqx,AT2017gge,AT2018bsi,AT2018dyb,AT2018fyk,AT2018hco,AT2018hyz,AT2018iih,AT2018jbv,AT2018lna,AT2018lni,AT2018mli,AT2018zr,AT2019ahk,AT2019azh,AT2019bhf,AT2019cho,AT2019dsg,AT2019ehz,AT2019gte,AT2019lwu,AT2019meg,AT2019mha,AT2019qiz,AT2019teq,AT2019vcb,AT2020acka,AT2020afhd,AT2020ddv,AT2020ksf,AT2020mbq,AT2020mot,AT2020neh,AT2020nov,AT2020ocn,AT2020opy,AT2020pj,AT2020qhs,AT2020riz,AT2020ukj,AT2020vdq,AT2020vwl,AT2020wey,AT2020ysg,AT2020yue,AT2020zso,AT2021ack,AT2021axu,AT2021blz,AT2021crk,AT2021ehb,AT2021gje,AT2021jjm,AT2021jsg,AT2021lo,AT2021mhg,AT2021nwa,AT2021qth,AT2021qxv,AT2021sdu,AT2021uqv,AT2021utq,AT2021uvz,AT2021yte,AT2021yzv,AT2022adm,AT2022aee,AT2022agi,AT2022arb,AT2022bdw,AT2022csn,AT2022czy,AT2022dbl,AT2022dsb,AT2022dyt,AT2022emf,AT2022exr,AT2022fpx,AT2022gdw,AT2022gri,AT2022hvp,AT2022ibq,AT2022lri,AT2022pna,AT2022rz,AT2022upj,AT2022wtn,AT2023clx,AT2023cvb,AT2023kvy,AT2023lli,AT2023mfm,AT2023mhs,AT2023rvb,AT2023tmq,AT2023ugy,AT2023vto,AT2023wdb,AT2023xen,AT2024admt,AT2024aepd,AT2024agqx,AT2024as,AT2024bgz,AT2024doo,AT2024eqp,AT2024gre,AT2024gxr,AT2024kt,AT2024lhc,AT2024mvz,AT2024pvu,AT2024qab,AT2024rny,AT2024tvd,AT2024ule,AT2024vip,AT2024wsd,AT2024ymu,AT2024yqo,AT2024zau,LSQ12dyw,PS1-10jh,PTF09djl,PTF09ge,SwiftJ164449.3+573451,SwiftJ2058+08,ZTF22aaajecp,iPTF15af,iPTF16axa
- out_of_repo: 无（134 个 TDE 全部在库内；Swift J1644+57 对应库内 SwiftJ164449.3+573451）

## 为什么是文献级卡

TDECat 是 2026-11-04 全库 TDE 批次（ingest_source=scix_tdecat_20261104）的建源文献，主样本
134 个确认 TDE **全部**已是库内源。本文是这批源共同的机读数据入口，处理口径对每个源都一样，
故一张索引卡覆盖全部，不为每个源开源级卡。

## 涉及源一览

| 源 | 表号/位置 | 源级卡 | status | 增量判读 |
|---|---|---|---|---|
| 全部 134 源（见 sources 键） | 目录级：官方 GitHub TDE_catalogue_all.csv（坐标/发现日期/发现星等/红移/Alternative name）；逐源测光：GitHub `Section 2: Photometry/` 下 `target_<名>_photometry.csv`（BHTOM 编译，文件名用去空格 TNS 名）与 UVOT/X-ray 子目录；光谱：`Section 3: Spectroscopy/`；分类：spectral_classes.csv | 无 | mention-only（本卡建卡时仅 AT2021qth 已逐值处理，见其 PR #888） | 见下方「增量门槛判读」 |

官方数据入口（论文 §3 与 Data availability 节声明）：

- GitHub：https://github.com/dlangis/TDECat（主目录 CSV + 逐源测光/光谱文件 + 本地 App）
- CDS：https://cdsarc.cds.unistra.fr/viz-bin/cat/J/A+A/707/A171（Table 1＝TDE 候选表；2026-11-05 实测 CDS 全站自本机网络不可达，已记 audit/unverified.tsv 通道级行）
- VoR：A&A 官网 HTML/PDF 金 OA；aanda.org 有 DataDome 反爬，curl 403，浏览器路线可过（2026-11-05 实测）

## 增量门槛判读

- **过门槛（通用口径警示，适用于每个源的审核）**：
  1. **逐源测光表只在 GitHub/CDS 机读侧**（正文无表）——`target_<名>_photometry.csv` 把**宿主档案测光**（CRTS 2006-2015、PS1、ALLWISE、NEOWISE、爆发前 ZTF/ATLAS）与 **TDE 爆发段**混在同一文件里，入库前必须区分；
  2. **ZTF 行是双管道×双误差变体**：长精度 MJD 行＝ALeRCE magpsf_corr 口径（差分-宿主改正瞬变星等，可与 ALeRCE API 逐值互证），短精度行＝BHTOM ZTF 编译（管道未注明，与 ALeRCE 值系统差 ~0.023 mag），同一曝光最多 4 行，需按曝光去重；
  3. **星等系统**：论文 §3.1 声明全部转 AB（ZTF/ATLAS/Pan-STARRS/iPTF AB；CRTS/Swift/NEOWISE 原为 Vega）；**UVOT 行已做银消光改正且未扣宿主**（论文 §3.3 自述）；
  4. **逐源爆发窗口（Bayesian blocks 的 start/end）未在正文或 GitHub 发布**——若在 CDS 侧，CDS 不可达期间无法取得，窗口边界只能由审核者按文献拟合峰值+观测间隙自行约定并在 comment 写明。
- **不开源级卡的理由**：各源在本文的条目均为同一结构的目录行/机读表，无逐源特有口径；接手者按上面四条统一处理即可。

## 待决

- TDECat 测光文件中 ATLAS 行存在个别 16-17 mag 离群点（论文自述「some artifacts could be present」）：按库规则原样入库、不做清洗，是否需要库级 artifacts 标记约定，请维护者裁定。
- 论文正文仅 2 张表（重复爆发表、候选示例表），主目录与 103 个 flare 的 timescale 参数表只存在于 GitHub/CDS 机读侧；CDS 恢复可达后建议补查 flare 参数表是否逐源发布。
