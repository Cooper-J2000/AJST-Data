- paper_key: langis2026
- paper: Langis+2026, A&A 707, A171（2026A&A...707A.171L，TDECat：optical TDE 汇编目录；机读表 VizieR J/A+A/707/A171，2026-11-06 实取）
- date: 2026-11-06
- helper: wa1kmoon@zcode
- sources: AT2016fnl, AT2017eqx, AT2017gge, AT2018bsi, AT2018dyb, AT2018fyk, AT2018hco, AT2018hyz, AT2018iih, AT2018jbv, AT2018lna, AT2018lni, AT2018mli, AT2018zr, AT2019ahk, AT2019azh, AT2019bhf, AT2019cho, AT2019dsg, AT2019ehz, AT2019gte, AT2019lwu, AT2019meg, AT2019mha, AT2019qiz, AT2019teq, AT2019vcb, AT2020acka, AT2020afhd, AT2020ddv, AT2020ksf, AT2020mbq, AT2020mot, AT2020neh, AT2020nov, AT2020ocn, AT2020opy, AT2020pj, AT2020qhs, AT2020riz, AT2020ukj, AT2020vdq, AT2020vwl, AT2020wey, AT2020ysg, AT2020yue, AT2020zso, AT2021ack, AT2021axu, AT2021blz, AT2021crk, AT2021ehb, AT2021gje, AT2021jjm, AT2021jsg, AT2021lo, AT2021mhg, AT2021nwa, AT2021qth, AT2021qxv, AT2021sdu, AT2021uqv, AT2021utq, AT2021uvz, AT2021yte, AT2021yzv, AT2022adm, AT2022aee, AT2022agi, AT2022arb, AT2022bdw, AT2022csn, AT2022czy, AT2022dbl, AT2022dsb, AT2022dyt, AT2022emf, AT2022exr, AT2022fpx, AT2022gdw, AT2022gri, AT2022hvp, AT2022ibq, AT2022lri, AT2022pna, AT2022rz, AT2022upj, AT2022wtn, AT2023clx, AT2023cvb, AT2023kvy, AT2023lli, AT2023mfm, AT2023mhs, AT2023rvb, AT2023tmq, AT2023ugy, AT2023vto, AT2023wdb, AT2023xen, AT2024admt, AT2024aepd, AT2024agqx, AT2024as, AT2024bgz, AT2024doo, AT2024eqp, AT2024gre, AT2024gxr, AT2024kt, AT2024lhc, AT2024mvz, AT2024pvu, AT2024qab, AT2024rny, AT2024tvd, AT2024ule, AT2024vip, AT2024wsd, AT2024ymu, AT2024yqo, AT2024zau

## 为什么是文献级卡

TDECat（Langis+2026）是全天地光 TDE 汇编目录：VizieR J/A+A/707/A171 主表 132 行（AT 名、ZTF/Gaia/eRASS/别名、J2000 坐标、红移、宿主名、发现时刻/星等/滤光片），附 Notes 表（少数对象的备注，本批库内源均无）。2026-11-04 批次（commit e33ba93f，v2.38）已按本表为 **132 个 TDE 源建源**（`ingest_source=scix_tdecat_20261104`），其中 122 个在库内（见上方 `sources`）；其余 10 行（AT 2022cmc、AT_2019eve、AT_2019fdr、AT_2019aalc、AT_2019baf、AT_2019cmw、AT_2021lwx、AT_2020abri、AT_2023adr、AT_2024kmq）不在库内，**未**开 new-source Issue（如需入库请走 new-source 流程）。

## 涉及源一览

全部 122 个库内源在同一张表（主表 catalog.dat，每源 1 行），处置完全同构，故用统一判读代替 122 行同值表格：

| 源集合 | 表号 | 源级卡 | status | 增量判读 |
|---|---|---|---|---|
| 上方 `sources` 全部 122 源 | VizieR J/A+A/707/A171 主表 | 无 | mention-only | 不过增量门槛（见下） |
| AT2022aee | 同上 | 无（本源已随 PR #923 直接审核） | reviewed | 见 PR #923 |

## 增量门槛判读

- **不过门槛（不开源级卡）**：主表各列（坐标、红移、DiscDate/Discmag/DiscFilter、宿主名）即 2026-11-04 建源批次的唯一数据来源——库内 info 已完整承载，属「目录已有的量」，无源级卡增量。发现时刻/星等与 TNS 发现报告同源（TDECat 的 DiscDate 即 TNS/各发现组报告值的秒级取整）。
- **Notes 表**：仅 3 行备注（OGLE16aaa、AT_2019eve、AT_2021lwx），均不在库内，无库内源增量。
- 本目录**不含测光表**：各源光变须另行检索（TNS phot. / 各发现组公开流 / 专篇文献）。先例：AT2022aee 的光变来自 TNS phot. 表 + ALeRCE 对象 API（PR #923），非本目录。
- 审核 TDE 批次各源时：元数据以 TNS 对象页逐源核对（多数已含 ALeRCE/ZTF 分类报告），测光义务按 §3.3 走 TNS phot. 表与 ALeRCE API。

## 待决

- 10 个库外目录行是否入库由维护者裁定（本卡只登记，未开 Issue）。
- `sources` 由 VizieR 表与 `info/` 程序化交叉匹配得出（2026-11-06）；后续若 ETL 增删 TDE 源，此表可能滞后。
