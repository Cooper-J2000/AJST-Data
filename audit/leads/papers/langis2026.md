# 文献索引：Langis+2026（TDECat——光学 TDE 综合编目）

- paper_key: langis2026
- paper: Langis+2026, A&A 707, A171（DOI 10.1051/0004-6361/202554882；arXiv:2506.05476；Repeating flares, X-ray outbursts and delayed infrared emission: A comprehensive compilation of optical tidal disruption events: TDECat）
- date: 2026-11-05
- helper: Rusty-Harpoon@zcode
- out_of_repo: 无（134 个 TDE 全部在库内；Swift J1644+57 对应库内 SwiftJ164449.3+573451）
- sources: ASASSN-14ae, ASASSN-14li, ASASSN-15oi, AT2016fnl, AT2017eqx, AT2017gge, AT2018bsi, AT2018dyb, AT2018fyk, AT2018hco, AT2018hyz, AT2018iih, AT2018jbv, AT2018lna, AT2018lni, AT2018mli, AT2018zr, AT2019ahk, AT2019azh, AT2019bhf, AT2019cho, AT2019dsg, AT2019ehz, AT2019gte, AT2019lwu, AT2019meg, AT2019mha, AT2019qiz, AT2019teq, AT2019vcb, AT2020acka, AT2020afhd, AT2020ddv, AT2020ksf, AT2020mbq, AT2020mot, AT2020neh, AT2020nov, AT2020ocn, AT2020opy, AT2020pj, AT2020qhs, AT2020riz, AT2020ukj, AT2020vdq, AT2020vwl, AT2020wey, AT2020ysg, AT2020yue, AT2020zso, AT2021ack, AT2021axu, AT2021blz, AT2021crk, AT2021ehb, AT2021gje, AT2021jjm, AT2021jsg, AT2021lo, AT2021mhg, AT2021nwa, AT2021qth, AT2021qxv, AT2021sdu, AT2021uqv, AT2021utq, AT2021uvz, AT2021yte, AT2021yzv, AT2022adm, AT2022aee, AT2022agi, AT2022arb, AT2022bdw, AT2022csn, AT2022czy, AT2022dbl, AT2022dsb, AT2022dyt, AT2022emf, AT2022exr, AT2022fpx, AT2022gdw, AT2022gri, AT2022hvp, AT2022ibq, AT2022lri, AT2022pna, AT2022rz, AT2022upj, AT2022wtn, AT2023clx, AT2023cvb, AT2023kvy, AT2023lli, AT2023mfm, AT2023mhs, AT2023rvb, AT2023tmq, AT2023ugy, AT2023vto, AT2023wdb, AT2023xen, AT2024admt, AT2024aepd, AT2024agqx, AT2024as, AT2024bgz, AT2024doo, AT2024eqp, AT2024gre, AT2024gxr, AT2024kt, AT2024lhc, AT2024mvz, AT2024pvu, AT2024qab, AT2024rny, AT2024tvd, AT2024ule, AT2024vip, AT2024wsd, AT2024ymu, AT2024yqo, AT2024zau, LSQ12dyw, PS1-10jh, PTF09djl, PTF09ge, SwiftJ164449.3+573451, SwiftJ2058+08, ZTF22aaajecp, iPTF15af, iPTF16axa

## 为什么是文献级卡

TDECat 是 134 个 TDE（131 个光学 + 3 个 jetted）的综合编目，**官方补充仓库
github.com/dlangis/TDECat 为每个源提供逐源机读光度文件**（`Section 2: Photometry/Optical
and Infrared/target_<名>_photometry.csv`，另有 UVOT 与 X-ray 两节），以 BHTom 等渠道汇集
CRTS/SDSS/PTF/PS1/ASAS-SN/ATLAS/ZTF/ALLWISE/NEOWISE 公开测光。本库 134 个 tde 源
（2026-11-04 批次建源）与 TDECat 样本**一一对应**（125 个按名直配 + 9 个 pre-AT 时代源按
Alternative name 直配 + Swift J1644+57→SwiftJ164449.3+573451、Swift J2058+08→SwiftJ2058+08），
故一卡覆盖全部。

本卡在审核 AT2021qth（PR #888）与 AT2024pvu（PR #890）时合并建立（两 PR 各自建卡，2026-11-05 复查后按 audit/leads/README.md 冲突规则合并为一份）；两源均已按 24 列契约入库各自的光度 CSV。

## 涉及源一览

| 源 | 表号（官方补充仓库文件） | 源级卡 | status | 增量判读 |
|---|---|---|---|---|
| ASASSN-14ae | target_ASASSN-14ae_photometry.csv（原文记名 ASASSN-14ae） | 无 | mention-only | 过门槛①：逐源光度 CSV（库内检索拿不到的编译光变表），接手者须自行下载核对 |
| ASASSN-14li | target_ASASSN-14li_photometry.csv（原文记名 ASASSN-14li） | 无 | mention-only | 过门槛①：逐源光度 CSV（库内检索拿不到的编译光变表），接手者须自行下载核对 |
| ASASSN-15oi | target_ASASSN-15oi_photometry.csv（原文记名 ASASSN-15oi） | 无 | mention-only | 过门槛①：逐源光度 CSV（库内检索拿不到的编译光变表），接手者须自行下载核对 |
| AT2016fnl | target_AT2016fnl_photometry.csv（原文记名 AT 2016fnl） | 无 | mention-only | 过门槛①：逐源光度 CSV（库内检索拿不到的编译光变表），接手者须自行下载核对 |
| AT2017eqx | target_AT2017eqx_photometry.csv（原文记名 AT 2017eqx） | 无 | mention-only | 过门槛①：逐源光度 CSV（库内检索拿不到的编译光变表），接手者须自行下载核对 |
| AT2017gge | target_AT2017gge_photometry.csv（原文记名 AT 2017gge） | 无 | mention-only | 过门槛①：逐源光度 CSV（库内检索拿不到的编译光变表），接手者须自行下载核对 |
| AT2018bsi | target_AT2018bsi_photometry.csv（原文记名 AT 2018bsi） | 无 | mention-only | 过门槛①：逐源光度 CSV（库内检索拿不到的编译光变表），接手者须自行下载核对 |
| AT2018dyb | target_AT2018dyb_photometry.csv（原文记名 AT 2018dyb） | 无 | mention-only | 过门槛①：逐源光度 CSV（库内检索拿不到的编译光变表），接手者须自行下载核对 |
| AT2018fyk | target_AT2018fyk_photometry.csv（原文记名 AT 2018fyk） | 无 | mention-only | 过门槛①：逐源光度 CSV（库内检索拿不到的编译光变表），接手者须自行下载核对 |
| AT2018hco | target_AT2018hco_photometry.csv（原文记名 AT 2018hco） | 无 | mention-only | 过门槛①：逐源光度 CSV（库内检索拿不到的编译光变表），接手者须自行下载核对 |
| AT2018hyz | target_AT2018hyz_photometry.csv（原文记名 AT 2018hyz） | 无 | mention-only | 过门槛①：逐源光度 CSV（库内检索拿不到的编译光变表），接手者须自行下载核对 |
| AT2018iih | target_AT2018iih_photometry.csv（原文记名 AT 2018iih） | 无 | mention-only | 过门槛①：逐源光度 CSV（库内检索拿不到的编译光变表），接手者须自行下载核对 |
| AT2018jbv | target_AT2018jbv_photometry.csv（原文记名 AT 2018jbv） | 无 | mention-only | 过门槛①：逐源光度 CSV（库内检索拿不到的编译光变表），接手者须自行下载核对 |
| AT2018lna | target_AT2018lna_photometry.csv（原文记名 AT 2018lna） | 无 | mention-only | 过门槛①：逐源光度 CSV（库内检索拿不到的编译光变表），接手者须自行下载核对 |
| AT2018lni | target_AT2018lni_photometry.csv（原文记名 AT 2018lni） | 无 | mention-only | 过门槛①：逐源光度 CSV（库内检索拿不到的编译光变表），接手者须自行下载核对 |
| AT2018mli | target_AT2018mli_photometry.csv（原文记名 AT 2018mli） | 无 | mention-only | 过门槛①：逐源光度 CSV（库内检索拿不到的编译光变表），接手者须自行下载核对 |
| AT2018zr | target_AT2018zr_photometry.csv（原文记名 AT 2018zr） | 无 | mention-only | 过门槛①：逐源光度 CSV（库内检索拿不到的编译光变表），接手者须自行下载核对 |
| AT2019ahk | target_AT2019ahk_photometry.csv（原文记名 AT 2019ahk） | 无 | mention-only | 过门槛①：逐源光度 CSV（库内检索拿不到的编译光变表），接手者须自行下载核对 |
| AT2019azh | target_AT2019azh_photometry.csv（原文记名 AT 2019azh） | 无 | mention-only | 过门槛①：逐源光度 CSV（库内检索拿不到的编译光变表），接手者须自行下载核对 |
| AT2019bhf | target_AT2019bhf_photometry.csv（原文记名 AT 2019bhf） | 无 | mention-only | 过门槛①：逐源光度 CSV（库内检索拿不到的编译光变表），接手者须自行下载核对 |
| AT2019cho | target_AT2019cho_photometry.csv（原文记名 AT 2019cho） | 无 | mention-only | 过门槛①：逐源光度 CSV（库内检索拿不到的编译光变表），接手者须自行下载核对 |
| AT2019dsg | target_AT2019dsg_photometry.csv（原文记名 AT 2019dsg） | 无 | mention-only | 过门槛①：逐源光度 CSV（库内检索拿不到的编译光变表），接手者须自行下载核对 |
| AT2019ehz | target_AT2019ehz_photometry.csv（原文记名 AT 2019ehz） | 无 | mention-only | 过门槛①：逐源光度 CSV（库内检索拿不到的编译光变表），接手者须自行下载核对 |
| AT2019gte | target_AT2019gte_photometry.csv（原文记名 AT 2019gte） | 无 | mention-only | 过门槛①：逐源光度 CSV（库内检索拿不到的编译光变表），接手者须自行下载核对 |
| AT2019lwu | target_AT2019lwu_photometry.csv（原文记名 AT 2019lwu） | 无 | mention-only | 过门槛①：逐源光度 CSV（库内检索拿不到的编译光变表），接手者须自行下载核对 |
| AT2019meg | target_AT2019meg_photometry.csv（原文记名 AT 2019meg） | 无 | mention-only | 过门槛①：逐源光度 CSV（库内检索拿不到的编译光变表），接手者须自行下载核对 |
| AT2019mha | target_AT2019mha_photometry.csv（原文记名 AT 2019mha） | 无 | mention-only | 过门槛①：逐源光度 CSV（库内检索拿不到的编译光变表），接手者须自行下载核对 |
| AT2019qiz | target_AT2019qiz_photometry.csv（原文记名 AT 2019qiz） | 无 | mention-only | 过门槛①：逐源光度 CSV（库内检索拿不到的编译光变表），接手者须自行下载核对 |
| AT2019teq | target_AT2019teq_photometry.csv（原文记名 AT 2019teq） | 无 | mention-only | 过门槛①：逐源光度 CSV（库内检索拿不到的编译光变表），接手者须自行下载核对 |
| AT2019vcb | target_AT2019vcb_photometry.csv（原文记名 AT 2019vcb） | 无 | mention-only | 过门槛①：逐源光度 CSV（库内检索拿不到的编译光变表），接手者须自行下载核对 |
| AT2020acka | target_AT2020acka_photometry.csv（原文记名 AT 2020acka） | 无 | mention-only | 过门槛①：逐源光度 CSV（库内检索拿不到的编译光变表），接手者须自行下载核对 |
| AT2020afhd | target_AT2020afhd_photometry.csv（原文记名 AT 2020afhd） | 无 | mention-only | 过门槛①：逐源光度 CSV（库内检索拿不到的编译光变表），接手者须自行下载核对 |
| AT2020ddv | target_AT2020ddv_photometry.csv（原文记名 AT 2020ddv） | 无 | mention-only | 过门槛①：逐源光度 CSV（库内检索拿不到的编译光变表），接手者须自行下载核对 |
| AT2020ksf | target_AT2020ksf_photometry.csv（原文记名 AT 2020ksf） | 无 | mention-only | 过门槛①：逐源光度 CSV（库内检索拿不到的编译光变表），接手者须自行下载核对 |
| AT2020mbq | target_AT2020mbq_photometry.csv（原文记名 AT 2020mbq） | 无 | mention-only | 过门槛①：逐源光度 CSV（库内检索拿不到的编译光变表），接手者须自行下载核对 |
| AT2020mot | target_AT2020mot_photometry.csv（原文记名 AT 2020mot） | 无 | mention-only | 过门槛①：逐源光度 CSV（库内检索拿不到的编译光变表），接手者须自行下载核对 |
| AT2020neh | target_AT2020neh_photometry.csv（原文记名 AT 2020neh） | 无 | mention-only | 过门槛①：逐源光度 CSV（库内检索拿不到的编译光变表），接手者须自行下载核对 |
| AT2020nov | target_AT2020nov_photometry.csv（原文记名 AT 2020nov） | 无 | mention-only | 过门槛①：逐源光度 CSV（库内检索拿不到的编译光变表），接手者须自行下载核对 |
| AT2020ocn | target_AT2020ocn_photometry.csv（原文记名 AT 2020ocn） | 无 | mention-only | 过门槛①：逐源光度 CSV（库内检索拿不到的编译光变表），接手者须自行下载核对 |
| AT2020opy | target_AT2020opy_photometry.csv（原文记名 AT 2020opy） | 无 | mention-only | 过门槛①：逐源光度 CSV（库内检索拿不到的编译光变表），接手者须自行下载核对 |
| AT2020pj | target_AT2020pj_photometry.csv（原文记名 AT 2020pj） | 无 | mention-only | 过门槛①：逐源光度 CSV（库内检索拿不到的编译光变表），接手者须自行下载核对 |
| AT2020qhs | target_AT2020qhs_photometry.csv（原文记名 AT 2020qhs） | 无 | mention-only | 过门槛①：逐源光度 CSV（库内检索拿不到的编译光变表），接手者须自行下载核对 |
| AT2020riz | target_AT2020riz_photometry.csv（原文记名 AT 2020riz） | 无 | mention-only | 过门槛①：逐源光度 CSV（库内检索拿不到的编译光变表），接手者须自行下载核对 |
| AT2020ukj | target_AT2020ukj_photometry.csv（原文记名 AT 2020ukj） | 无 | mention-only | 过门槛①：逐源光度 CSV（库内检索拿不到的编译光变表），接手者须自行下载核对 |
| AT2020vdq | target_AT2020vdq_photometry.csv（原文记名 AT 2020vdq） | 无 | mention-only | 过门槛①：逐源光度 CSV（库内检索拿不到的编译光变表），接手者须自行下载核对 |
| AT2020vwl | target_AT2020vwl_photometry.csv（原文记名 AT 2020vwl） | 无 | mention-only | 过门槛①：逐源光度 CSV（库内检索拿不到的编译光变表），接手者须自行下载核对 |
| AT2020wey | target_AT2020wey_photometry.csv（原文记名 AT 2020wey） | 无 | mention-only | 过门槛①：逐源光度 CSV（库内检索拿不到的编译光变表），接手者须自行下载核对 |
| AT2020ysg | target_AT2020ysg_photometry.csv（原文记名 AT 2020ysg） | 无 | mention-only | 过门槛①：逐源光度 CSV（库内检索拿不到的编译光变表），接手者须自行下载核对 |
| AT2020yue | target_AT2020yue_photometry.csv（原文记名 AT 2020yue） | 无 | mention-only | 过门槛①：逐源光度 CSV（库内检索拿不到的编译光变表），接手者须自行下载核对 |
| AT2020zso | target_AT2020zso_photometry.csv（原文记名 AT 2020zso） | 无 | mention-only | 过门槛①：逐源光度 CSV（库内检索拿不到的编译光变表），接手者须自行下载核对 |
| AT2021ack | target_AT2021ack_photometry.csv（原文记名 AT 2021ack） | 无 | mention-only | 过门槛①：逐源光度 CSV（库内检索拿不到的编译光变表），接手者须自行下载核对 |
| AT2021axu | target_AT2021axu_photometry.csv（原文记名 AT 2021axu） | 无 | mention-only | 过门槛①：逐源光度 CSV（库内检索拿不到的编译光变表），接手者须自行下载核对 |
| AT2021blz | target_AT2021blz_photometry.csv（原文记名 AT 2021blz） | 无 | mention-only | 过门槛①：逐源光度 CSV（库内检索拿不到的编译光变表），接手者须自行下载核对 |
| AT2021crk | target_AT2021crk_photometry.csv（原文记名 AT 2021crk） | 无 | mention-only | 过门槛①：逐源光度 CSV（库内检索拿不到的编译光变表），接手者须自行下载核对 |
| AT2021ehb | target_AT2021ehb_photometry.csv（原文记名 AT 2021ehb） | 无 | mention-only | 过门槛①：逐源光度 CSV（库内检索拿不到的编译光变表），接手者须自行下载核对 |
| AT2021gje | target_AT2021gje_photometry.csv（原文记名 AT 2021gje） | 无 | mention-only | 过门槛①：逐源光度 CSV（库内检索拿不到的编译光变表），接手者须自行下载核对 |
| AT2021jjm | target_AT2021jjm_photometry.csv（原文记名 AT 2021jjm） | 无 | mention-only | 过门槛①：逐源光度 CSV（库内检索拿不到的编译光变表），接手者须自行下载核对 |
| AT2021jsg | target_AT2021jsg_photometry.csv（原文记名 AT 2021jsg） | 无 | mention-only | 过门槛①：逐源光度 CSV（库内检索拿不到的编译光变表），接手者须自行下载核对 |
| AT2021lo | target_AT2021lo_photometry.csv（原文记名 AT 2021lo） | 无 | mention-only | 过门槛①：逐源光度 CSV（库内检索拿不到的编译光变表），接手者须自行下载核对 |
| AT2021mhg | target_AT2021mhg_photometry.csv（原文记名 AT 2021mhg） | 无 | mention-only | 过门槛①：逐源光度 CSV（库内检索拿不到的编译光变表），接手者须自行下载核对 |
| AT2021nwa | target_AT2021nwa_photometry.csv（原文记名 AT 2021nwa） | 无 | mention-only | 过门槛①：逐源光度 CSV（库内检索拿不到的编译光变表），接手者须自行下载核对 |
| AT2021qth | target_AT2021qth_photometry.csv（原文记名 AT 2021qth） | 无 | mention-only | 过门槛①：逐源光度 CSV（库内检索拿不到的编译光变表），接手者须自行下载核对 |
| AT2021qxv | target_AT2021qxv_photometry.csv（原文记名 AT 2021qxv） | 无 | mention-only | 过门槛①：逐源光度 CSV（库内检索拿不到的编译光变表），接手者须自行下载核对 |
| AT2021sdu | target_AT2021sdu_photometry.csv（原文记名 AT 2021sdu） | 无 | mention-only | 过门槛①：逐源光度 CSV（库内检索拿不到的编译光变表），接手者须自行下载核对 |
| AT2021uqv | target_AT2021uqv_photometry.csv（原文记名 AT 2021uqv） | 无 | mention-only | 过门槛①：逐源光度 CSV（库内检索拿不到的编译光变表），接手者须自行下载核对 |
| AT2021utq | target_AT2021utq_photometry.csv（原文记名 AT 2021utq） | 无 | mention-only | 过门槛①：逐源光度 CSV（库内检索拿不到的编译光变表），接手者须自行下载核对 |
| AT2021uvz | target_AT2021uvz_photometry.csv（原文记名 AT 2021uvz） | 无 | mention-only | 过门槛①：逐源光度 CSV（库内检索拿不到的编译光变表），接手者须自行下载核对 |
| AT2021yte | target_AT2021yte_photometry.csv（原文记名 AT 2021yte） | 无 | mention-only | 过门槛①：逐源光度 CSV（库内检索拿不到的编译光变表），接手者须自行下载核对 |
| AT2021yzv | target_AT2021yzv_photometry.csv（原文记名 AT 2021yzv） | 无 | mention-only | 过门槛①：逐源光度 CSV（库内检索拿不到的编译光变表），接手者须自行下载核对 |
| AT2022adm | target_AT2022adm_photometry.csv（原文记名 AT 2022adm） | 无 | mention-only | 过门槛①：逐源光度 CSV（库内检索拿不到的编译光变表），接手者须自行下载核对 |
| AT2022aee | target_AT2022aee_photometry.csv（原文记名 AT 2022aee） | 无 | mention-only | 过门槛①：逐源光度 CSV（库内检索拿不到的编译光变表），接手者须自行下载核对 |
| AT2022agi | target_AT2022agi_photometry.csv（原文记名 AT 2022agi） | 无 | mention-only | 过门槛①：逐源光度 CSV（库内检索拿不到的编译光变表），接手者须自行下载核对 |
| AT2022arb | target_AT2022arb_photometry.csv（原文记名 AT 2022arb） | 无 | mention-only | 过门槛①：逐源光度 CSV（库内检索拿不到的编译光变表），接手者须自行下载核对 |
| AT2022bdw | target_AT2022bdw_photometry.csv（原文记名 AT 2022bdw） | 无 | mention-only | 过门槛①：逐源光度 CSV（库内检索拿不到的编译光变表），接手者须自行下载核对 |
| AT2022csn | target_AT2022csn_photometry.csv（原文记名 AT 2022csn） | 无 | mention-only | 过门槛①：逐源光度 CSV（库内检索拿不到的编译光变表），接手者须自行下载核对 |
| AT2022czy | target_AT2022czy_photometry.csv（原文记名 AT 2022czy） | 无 | mention-only | 过门槛①：逐源光度 CSV（库内检索拿不到的编译光变表），接手者须自行下载核对 |
| AT2022dbl | target_AT2022dbl_photometry.csv（原文记名 AT 2022dbl） | 无 | mention-only | 过门槛①：逐源光度 CSV（库内检索拿不到的编译光变表），接手者须自行下载核对 |
| AT2022dsb | target_AT2022dsb_photometry.csv（原文记名 AT 2022dsb） | 无 | mention-only | 过门槛①：逐源光度 CSV（库内检索拿不到的编译光变表），接手者须自行下载核对 |
| AT2022dyt | target_AT2022dyt_photometry.csv（原文记名 AT 2022dyt） | 无 | mention-only | 过门槛①：逐源光度 CSV（库内检索拿不到的编译光变表），接手者须自行下载核对 |
| AT2022emf | target_AT2022emf_photometry.csv（原文记名 AT 2022emf） | 无 | mention-only | 过门槛①：逐源光度 CSV（库内检索拿不到的编译光变表），接手者须自行下载核对 |
| AT2022exr | target_AT2022exr_photometry.csv（原文记名 AT 2022exr） | 无 | mention-only | 过门槛①：逐源光度 CSV（库内检索拿不到的编译光变表），接手者须自行下载核对 |
| AT2022fpx | target_AT2022fpx_photometry.csv（原文记名 AT 2022fpx） | 无 | mention-only | 过门槛①：逐源光度 CSV（库内检索拿不到的编译光变表），接手者须自行下载核对 |
| AT2022gdw | target_AT2022gdw_photometry.csv（原文记名 AT 2022gdw） | 无 | mention-only | 过门槛①：逐源光度 CSV（库内检索拿不到的编译光变表），接手者须自行下载核对 |
| AT2022gri | target_AT2022gri_photometry.csv（原文记名 AT 2022gri） | 无 | mention-only | 过门槛①：逐源光度 CSV（库内检索拿不到的编译光变表），接手者须自行下载核对 |
| AT2022hvp | target_AT2022hvp_photometry.csv（原文记名 AT 2022hvp） | 无 | mention-only | 过门槛①：逐源光度 CSV（库内检索拿不到的编译光变表），接手者须自行下载核对 |
| AT2022ibq | target_AT2022ibq_photometry.csv（原文记名 AT 2022ibq） | 无 | mention-only | 过门槛①：逐源光度 CSV（库内检索拿不到的编译光变表），接手者须自行下载核对 |
| AT2022lri | target_AT2022lri_photometry.csv（原文记名 AT 2022lri） | 无 | mention-only | 过门槛①：逐源光度 CSV（库内检索拿不到的编译光变表），接手者须自行下载核对 |
| AT2022pna | target_AT2022pna_photometry.csv（原文记名 AT 2022pna） | 无 | mention-only | 过门槛①：逐源光度 CSV（库内检索拿不到的编译光变表），接手者须自行下载核对 |
| AT2022rz | target_AT2022rz_photometry.csv（原文记名 AT 2022rz） | 无 | mention-only | 过门槛①：逐源光度 CSV（库内检索拿不到的编译光变表），接手者须自行下载核对 |
| AT2022upj | target_AT2022upj_photometry.csv（原文记名 AT 2022upj） | 无 | mention-only | 过门槛①：逐源光度 CSV（库内检索拿不到的编译光变表），接手者须自行下载核对 |
| AT2022wtn | target_AT2022wtn_photometry.csv（原文记名 AT 2022wtn） | 无 | mention-only | 过门槛①：逐源光度 CSV（库内检索拿不到的编译光变表），接手者须自行下载核对 |
| AT2023clx | target_AT2023clx_photometry.csv（原文记名 AT 2023clx） | 无 | mention-only | 过门槛①：逐源光度 CSV（库内检索拿不到的编译光变表），接手者须自行下载核对 |
| AT2023cvb | target_AT2023cvb_photometry.csv（原文记名 AT 2023cvb） | 无 | mention-only | 过门槛①：逐源光度 CSV（库内检索拿不到的编译光变表），接手者须自行下载核对 |
| AT2023kvy | target_AT2023kvy_photometry.csv（原文记名 AT 2023kvy） | 无 | mention-only | 过门槛①：逐源光度 CSV（库内检索拿不到的编译光变表），接手者须自行下载核对 |
| AT2023lli | target_AT2023lli_photometry.csv（原文记名 AT 2023lli） | 无 | mention-only | 过门槛①：逐源光度 CSV（库内检索拿不到的编译光变表），接手者须自行下载核对 |
| AT2023mfm | target_AT2023mfm_photometry.csv（原文记名 AT 2023mfm） | 无 | mention-only | 过门槛①：逐源光度 CSV（库内检索拿不到的编译光变表），接手者须自行下载核对 |
| AT2023mhs | target_AT2023mhs_photometry.csv（原文记名 AT 2023mhs） | 无 | mention-only | 过门槛①：逐源光度 CSV（库内检索拿不到的编译光变表），接手者须自行下载核对 |
| AT2023rvb | target_AT2023rvb_photometry.csv（原文记名 AT 2023rvb） | 无 | mention-only | 过门槛①：逐源光度 CSV（库内检索拿不到的编译光变表），接手者须自行下载核对 |
| AT2023tmq | target_AT2023tmq_photometry.csv（原文记名 AT 2023tmq） | 无 | mention-only | 过门槛①：逐源光度 CSV（库内检索拿不到的编译光变表），接手者须自行下载核对 |
| AT2023ugy | target_AT2023ugy_photometry.csv（原文记名 AT 2023ugy） | 无 | mention-only | 过门槛①：逐源光度 CSV（库内检索拿不到的编译光变表），接手者须自行下载核对 |
| AT2023vto | target_AT2023vto_photometry.csv（原文记名 AT 2023vto） | 无 | mention-only | 过门槛①：逐源光度 CSV（库内检索拿不到的编译光变表），接手者须自行下载核对 |
| AT2023wdb | target_AT2023wdb_photometry.csv（原文记名 AT 2023wdb） | 无 | mention-only | 过门槛①：逐源光度 CSV（库内检索拿不到的编译光变表），接手者须自行下载核对 |
| AT2023xen | target_AT2023xen_photometry.csv（原文记名 AT 2023xen） | 无 | mention-only | 过门槛①：逐源光度 CSV（库内检索拿不到的编译光变表），接手者须自行下载核对 |
| AT2024admt | target_AT2024admt_photometry.csv（原文记名 AT 2024admt） | 无 | mention-only | 过门槛①：逐源光度 CSV（库内检索拿不到的编译光变表），接手者须自行下载核对 |
| AT2024aepd | target_AT2024aepd_photometry.csv（原文记名 AT 2024aepd） | 无 | mention-only | 过门槛①：逐源光度 CSV（库内检索拿不到的编译光变表），接手者须自行下载核对 |
| AT2024agqx | target_AT2024agqx_photometry.csv（原文记名 AT 2024agqx） | 无 | mention-only | 过门槛①：逐源光度 CSV（库内检索拿不到的编译光变表），接手者须自行下载核对 |
| AT2024as | target_AT2024as_photometry.csv（原文记名 AT 2024as） | 无 | mention-only | 过门槛①：逐源光度 CSV（库内检索拿不到的编译光变表），接手者须自行下载核对 |
| AT2024bgz | target_AT2024bgz_photometry.csv（原文记名 AT 2024bgz） | 无 | mention-only | 过门槛①：逐源光度 CSV（库内检索拿不到的编译光变表），接手者须自行下载核对 |
| AT2024doo | target_AT2024doo_photometry.csv（原文记名 AT 2024doo） | 无 | mention-only | 过门槛①：逐源光度 CSV（库内检索拿不到的编译光变表），接手者须自行下载核对 |
| AT2024eqp | target_AT2024eqp_photometry.csv（原文记名 AT 2024eqp） | 无 | mention-only | 过门槛①：逐源光度 CSV（库内检索拿不到的编译光变表），接手者须自行下载核对 |
| AT2024gre | target_AT2024gre_photometry.csv（原文记名 AT 2024gre） | 无 | mention-only | 过门槛①：逐源光度 CSV（库内检索拿不到的编译光变表），接手者须自行下载核对 |
| AT2024gxr | target_AT2024gxr_photometry.csv（原文记名 AT 2024gxr） | 无 | mention-only | 过门槛①：逐源光度 CSV（库内检索拿不到的编译光变表），接手者须自行下载核对 |
| AT2024kt | target_AT2024kt_photometry.csv（原文记名 AT 2024kt） | 无 | mention-only | 过门槛①：逐源光度 CSV（库内检索拿不到的编译光变表），接手者须自行下载核对 |
| AT2024lhc | target_AT2024lhc_photometry.csv（原文记名 AT 2024lhc） | 无 | mention-only | 过门槛①：逐源光度 CSV（库内检索拿不到的编译光变表），接手者须自行下载核对 |
| AT2024mvz | target_AT2024mvz_photometry.csv（原文记名 AT 2024mvz） | 无 | mention-only | 过门槛①：逐源光度 CSV（库内检索拿不到的编译光变表），接手者须自行下载核对 |
| AT2024pvu | target_AT2024pvu_photometry.csv（原文记名 AT 2024pvu） | 本 PR #890（已审核入库） | 已审核（2026-11-05） | 已按 24 列契约入库 9560 行；口径与未收行判读见 info comment |
| AT2024qab | target_AT2024qab_photometry.csv（原文记名 AT 2024qab） | 无 | mention-only | 过门槛①：逐源光度 CSV（库内检索拿不到的编译光变表），接手者须自行下载核对 |
| AT2024rny | target_AT2024rny_photometry.csv（原文记名 AT 2024rny） | 无 | mention-only | 过门槛①：逐源光度 CSV（库内检索拿不到的编译光变表），接手者须自行下载核对 |
| AT2024tvd | target_AT2024tvd_photometry.csv（原文记名 AT 2024tvd） | 无 | mention-only | 过门槛①：逐源光度 CSV（库内检索拿不到的编译光变表），接手者须自行下载核对 |
| AT2024ule | target_AT2024ule_photometry.csv（原文记名 AT 2024ule） | 无 | mention-only | 过门槛①：逐源光度 CSV（库内检索拿不到的编译光变表），接手者须自行下载核对 |
| AT2024vip | target_AT2024vip_photometry.csv（原文记名 AT 2024vip） | 无 | mention-only | 过门槛①：逐源光度 CSV（库内检索拿不到的编译光变表），接手者须自行下载核对 |
| AT2024wsd | target_AT2024wsd_photometry.csv（原文记名 AT 2024wsd） | 无 | mention-only | 过门槛①：逐源光度 CSV（库内检索拿不到的编译光变表），接手者须自行下载核对 |
| AT2024ymu | target_AT2024ymu_photometry.csv（原文记名 AT 2024ymu） | 无 | mention-only | 过门槛①：逐源光度 CSV（库内检索拿不到的编译光变表），接手者须自行下载核对 |
| AT2024yqo | target_AT2024yqo_photometry.csv（原文记名 AT 2024yqo） | 无 | mention-only | 过门槛①：逐源光度 CSV（库内检索拿不到的编译光变表），接手者须自行下载核对 |
| AT2024zau | target_AT2024zau_photometry.csv（原文记名 AT 2024zau） | 无 | mention-only | 过门槛①：逐源光度 CSV（库内检索拿不到的编译光变表），接手者须自行下载核对 |
| LSQ12dyw | target_LSQ12dyw_photometry.csv（原文记名 LSQ12dyw） | 无 | mention-only | 过门槛①：逐源光度 CSV（库内检索拿不到的编译光变表），接手者须自行下载核对 |
| PS1-10jh | target_PS1-10jh_photometry.csv（原文记名 PS1-10jh） | 无 | mention-only | 过门槛①：逐源光度 CSV（库内检索拿不到的编译光变表），接手者须自行下载核对 |
| PTF09djl | target_PTF09djl_photometry.csv（原文记名 PTF09djl） | 无 | mention-only | 过门槛①：逐源光度 CSV（库内检索拿不到的编译光变表），接手者须自行下载核对 |
| PTF09ge | target_PTF09ge_photometry.csv（原文记名 PTF09ge） | 无 | mention-only | 过门槛①：逐源光度 CSV（库内检索拿不到的编译光变表），接手者须自行下载核对 |
| SwiftJ164449.3+573451 | target_Swift_J1644+57_photometry.csv（原文记名 Swift_J1644+57） | 无 | mention-only | 过门槛①：逐源光度 CSV（库内检索拿不到的编译光变表），接手者须自行下载核对 |
| SwiftJ2058+08 | target_Swift J2058+0516_photometry.csv（原文记名 Swift_J2058+08） | 无 | mention-only | 过门槛①：逐源光度 CSV（库内检索拿不到的编译光变表），接手者须自行下载核对 |
| ZTF22aaajecp | target_AT2022cmc_photometry.csv（原文记名 AT 2022cmc） | 无 | mention-only | 过门槛①：逐源光度 CSV（库内检索拿不到的编译光变表），接手者须自行下载核对 |
| iPTF15af | target_iPTF15af_photometry.csv（原文记名 iPTF15af） | 无 | mention-only | 过门槛①：逐源光度 CSV（库内检索拿不到的编译光变表），接手者须自行下载核对 |
| iPTF16axa | target_iPTF16axa_photometry.csv（原文记名 iPTF16axa） | 无 | mention-only | 过门槛①：逐源光度 CSV（库内检索拿不到的编译光变表），接手者须自行下载核对 |

官方数据入口（论文 §3 与 Data availability 节声明）：

- GitHub：https://github.com/dlangis/TDECat（主目录 CSV + 逐源测光/光谱文件 + 本地 App）
- CDS：https://cdsarc.cds.unistra.fr/viz-bin/cat/J/A+A/707/A171（Table 1＝TDE 候选表；2026-11-05 实测 CDS 全站自本机网络不可达，已记 audit/unverified.tsv 通道级行）
- VoR：A&A 官网 HTML/PDF 金 OA；aanda.org 有 DataDome 反爬，curl 403，浏览器路线可过（2026-11-05 实测）

## 增量门槛判读

- 全部 134 源都**过门槛①**（逐源光度 CSV 是库内 GCN/目录检索拿不到的编译测光表），接手任一源时
  应下载对应 `target_<名>_photometry.csv` 自行逐行核对后入库。
- **宿主档案与爆发段混排**：CSV 把宿主档案测光（CRTS 2006-2015、PS1、ALLWISE、NEOWISE、爆发前 ZTF/ATLAS）
  与 TDE 爆发段混在同一文件，入库前必须区分并写明取舍（AT2021qth 取爆发段窗口、AT2024pvu 全档案入库并
  逐段注明口径——两种做法都合法，须在 comment 写清依据）。
- **口径提示（审 AT2024pvu 时确证，预计全样本通用）**：
  1. CSV 行为**总流量（含宿星系核）**，非差分——安静期水平即宿主（AT2024pvu ZTF zg≈17.25）；
     与 TNS 差分星等（纯瞬变）不可互删，§3.4 判非同值；
  2. CSV 保留**各巡天原生星等系统**（AT2024pvu 的 WISE W1≈13.3 为 Vega 可证）：CRTS、
     ASAS-SN V、WISE/NEOWISE、Swift/UVOT＝Vega；ZTF、ATLAS、ASAS-SN g、iPTF、Pan-STARRS、SDSS＝AB
     （论文 §3.1 声明其分析中统一转 AB，但 CSV 值未转）；**UVOT 行已做银消光改正且未扣宿主**
     （论文 §3.3 原文 All magnitudes were corrected for Galactic extinction … not host subtracted）；
  3. CRTS(CL) 为无滤光片 → band=G；
  4. CSV 无非探测标志列；审 AT2024pvu 时发现 ASASSN 行有 Error=-1.0（缺测哨兵）与
     Magnitude=99.99（非探测占位）两类哨兵，ATLAS 有 H/t 两个无法唯一判读的波段标签——
     接手者请按同样规则处理（哨兵不入库或误差留空；无法判读波段在 PR 待决上报）；
  5. CSV 内存在**同历元同值双行**（误差实现不同，§3.4 同值去重保留一行）与**同历元近值双行**
     （不同管线，值差 ~0.02–0.05 mag，均保留）；ZTF 同一曝光最多 4 行＝**双管道×双误差变体**
     （长精度 MJD 行＝ALeRCE magpsf_corr 口径，短精度行＝BHTOM ZTF 编译，系统差 ~0.023 mag），需按曝光去重；
  6. **逐源爆发窗口（Bayesian blocks 的 start/end）未在正文或 GitHub 发布**——若在 CDS 侧，CDS 不可达期间
     无法取得，窗口边界只能由审核者按文献拟合峰值+观测间隙自行约定并在 comment 写明。

## 待决

- TDECat 测光文件中 ATLAS 行存在个别 16-17 mag 离群点（论文自述「some artifacts could be present」）：
  按库规则原样入库、不做清洗，是否需要库级 artifacts 标记约定，请维护者裁定。
- 论文正文仅 2 张表（重复爆发表、候选示例表），主目录与 103 个 flare 的 timescale 参数表只存在于
  GitHub/CDS 机读侧；CDS 恢复可达后建议补查 flare 参数表是否逐源发布。
- ATLAS(H)/(t) 波段标签无法唯一判读（AT2024pvu 8 行未入库），随各源审核时按 PR 待决上报。

## 合并并入的行（同批其它审核 PR）

| 源集合 | 表号 | 源级卡 | status | 增量判读 |
| 上方 `sources` 全部 132 源 | VizieR J/A+A/707/A171 主表 | 无 | mention-only | 不过增量门槛（见下） |
