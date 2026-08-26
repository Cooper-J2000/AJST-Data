# uvot_grb — Swift/UVOT 第二版 GRB 余辉目录（外部数据存档）

## 基本信息

- **目录名称**：A Large Catalog of UV/Optical GRB Afterglows（第二版 Swift/UVOT GRB 余辉目录，HLSP: UVOTGRB）
- **主页 URL**：https://archive.stsci.edu/prepds/uvotgrb/
- **发布机构**：MAST / STScI（HLSP 高质量科学产品）
- **来源文献**：Roming et al. 2017, ApJS, 228, 13（"A Large Catalog of Homogeneous Ultra-Violet/Optical GRB Afterglows: Temporal and Spectral Evolution"，arXiv:1701.03713）
- **获取日期**：2026-07-21
- **数据下载 URL**（主页 "Data Products" 区直接给出的 4 个 FITS 文件，均为 curl 实测下载成功）：
  - https://archive.stsci.edu/missions/hlsp/uvotgrb/hlsp_uvotgrb_swift_uvot_all_multi_v1_grb-cat.fits
  - https://archive.stsci.edu/missions/hlsp/uvotgrb/hlsp_uvotgrb_swift_uvot_all_multi_v1_image-event-3db.fits
  - https://archive.stsci.edu/missions/hlsp/uvotgrb/hlsp_uvotgrb_swift_uvot_all_multi_v1_image-event-5db.fits
  - https://archive.stsci.edu/missions/hlsp/uvotgrb/hlsp_uvotgrb_swift_uvot_all_multi_v1_noc-db.fits

## 文件清单与行数核对

均为 FITS 二进制表（BinTable 在第 1 扩展）。**注意：为减小仓库体积，这 4 个原始 FITS 文件不随本仓库分发**，请从上述 MAST HLSP 下载地址自行下载到本目录后运行 `python3 parse.py` 重新生成 `normalized.jsonl`。下表行数与 MD5 来自发布时的核对，可用于校验下载结果。

| 文件 | 大小 | 实测行数 × 列数 | 论文声称 | MD5 |
|---|---|---|---|---|
| `hlsp_uvotgrb_swift_uvot_all_multi_v1_grb-cat.fits` | 0.9 MB | 626 × 349 | 626 行 / 349 列 ✔ | b9957874d950a984e4a10ae9ef057e92 |
| `hlsp_uvotgrb_swift_uvot_all_multi_v1_image-event-3db.fits` | 45 MB | 119598 × 81 | 119,598 行 / 81 列 ✔ | 582fa85394a5e98e39d86c13a387d286 |
| `hlsp_uvotgrb_swift_uvot_all_multi_v1_image-event-5db.fits` | 45 MB | 120217 × 81 | 120,217 行 / 81 列 ✔ | 5f66e8c7f851cdfe2af5a939f53824a3 |
| `hlsp_uvotgrb_swift_uvot_all_multi_v1_noc-db.fits` | 1.4 MB | 13597 × 20 | 13,597 行 / 20 列 ✔ | 484c9d35b83165eccd8240c32592e065 |

行数用 `astropy.io.fits` 读 `NAXIS2` 实测，与论文（§4）完全一致。

**关于网页上的 "538 GRBs"**：主页简介称目录基于 538 个 GRB 的 12 万次观测。实际 `grb-cat` 有 **626 行（626 个唯一 OBJECT）**。论文明确解释：目录共收录 626 个爆发（2005-01-17 至 2010-12-25，由 Swift/BAT、HETE2、INTEGRAL、IPN、Fermi/LAT、AGILE 首先发现），其中 538 个被 UVOT 实际观测（占比 86%），其余 88 个因亮星邻近等原因未被 UVOT 观测，相应 UVOT 列为 NULL。入库时 OBJECT 去重后应为 626。

## 文件内容概述

1. **grb-cat**（核心目录表，每行一个 GRB）：位置、发现卫星、触发时间、红移、消光、T90、BAT 瞬时辐射参数、XRT 参数、UVOT 首次/峰值观测、7 个 UVOT 滤光片（UVW2/UVM2/UVW1/u/b/v/white）各自的多段幂律光变拟合参数（每滤光片 26 列）、2×10³/2×10⁴/2×10⁵ s 三个时刻的计数率与流量密度、以及三个时刻的消光改正紫外/光学谱指数 β。
2. **image-event-3db / 5db**：原始测光数据库，分别用 3″ 和 5″ 源孔径，每行一次 UVOT 曝光的测量（时间、滤光片、孔径测光、星等、流量等 81 列）。
3. **noc-db**：归一化、最优叠加（NOC, Morgan et al. 2008 方法）光变数据库，每行一个叠加数据点（20 列，扩展名 OPTCOADD）。

## 瞬时辐射（prompt emission）参数 —— 对本项目最重要的列

全部在 `grb-cat` 中，均来自 SGA（Swift GRB Archive，即 Sakamoto et al. BAT 目录系列）或 GCN 通报。**注意：本目录没有 Epeak、没有 Eiso、没有 1–10⁴ keV 静止系 bolometric fluence**——BAT 能段窄（15–150 keV），只给流量、峰值光子流和光子指数。若要 Epeak/Eiso 需另接 Fermi GBM 或 BAT 谱目录。

| 列名 | 物理含义 | 单位 | 误差/备注 |
|---|---|---|---|
| `T90` | T90 持续时间 | s | 观测系；**能段随发现仪器不同**：Swift 爆发为 15–350 keV（Sakamoto et al. 定义），HETE2 爆发为 30–400 keV（个别 80–400 keV），见 T90_REF |
| `T90_REF` | T90 出处 | — | `SGA`（538 个）或 `GCNnnnn` 通报号 |
| `BAT_FL` | BAT 瞬时辐射流量 fluence | erg cm⁻² | **15–150 keV 能段，观测系**；缺失 = -1.0e-07 |
| `BAT_FL_ERR` | BAT fluence 误差 | erg cm⁻² | **90% 置信**（非 1σ！）；缺失 = -1.0e-07 |
| `BAT_PPF` | BAT 1 秒峰值光子流量 | ph cm⁻² s⁻¹ | 15–150 keV；缺失 = -1.00 |
| `BAT_PPF_ERR` | 峰值光子流量误差 | ph cm⁻² s⁻¹ | **90% 置信**；缺失 = -1.00 |
| `BAT_PI` | BAT 能谱光子指数 | 无量纲 | 15–150 keV；缺失 = -1.00 |
| `BAT_PIT` | 光子指数类型（能谱模型） | — | `PL`=简单幂律（468 行）、`CPL`=截断幂律（71 行）；缺失标记混乱，见"坑" |
| `BAT_PI_ERR` | 光子指数误差 | 无量纲 | **90% 置信**；缺失 = -1.00 |

XRT 相关（顺带提供）：`XRT_FLUX`/`XRT_11FLUX`/`XRT_24FLUX` 为 0.3–10 keV 能段流量（erg cm⁻² s⁻¹），`XRT_TI` 初始终态指数、`XRT_SI` 谱指数、`XRT_NH` 柱密度（cm⁻²）。

## grb-cat 全部 349 列分组文档

单位写在 TTYPE 注释里（TUNIT 关键字为空），以下按组说明；误差列除特别注明外均为 **1σ**。

- **标识与位置（列 1–8）**：`OBJECT`（GRB 名，见下节）、`RA`/`DEC`（J2000.0，度）、`POS_ERR`（位置误差，角秒）、`POS_REF`（位置出处：SGA/GCN/Butler/Goad）、`DISC_BY`（发现卫星整数旗标，**0=Swift, 1=HETE2, 2=INTEGRAL, 3=IPN, 4=Fermi, 5=BAT Slew Survey(BATSS), 6=AGILE, 7=Swift 地面分析**；分布：0:522, 1:8, 2:37, 3:7, 4:8, 5:9, 6:14, 7:21）、`TRIGTIME`（触发时刻，Swift MET 秒）、`TRIG_UT`（触发时刻 UTC，格式 `YYYY-DDD-HH:MM:SS`，年积日）。
- **红移与消光（9–11）**：`Z`（红移；**缺失 = -1.0**，201 个有红移）；`E_MW`（银河系平均 E(B-V)）；`E_HOST`（宿主星系 E(B-V)，缺失 = -99.0）。
- **瞬时辐射（12–20）**：见上节。
- **XRT（21–27）**：见上节，缺失 = -1.00。
- **UVOT 首次/峰值观测（28–41）**：`FRST_TSTART`/`PEAK_TSTART`（相对触发的秒数）、`FRST_FILT`/`PEAK_FILT`（滤光片，未见 = `NULL`）、`FRST_MAG`/`PEAK_MAG`（星等，Vega 系统）、`*_MAG_ERR`/`*_FLUX_ERR`（**1σ**）、`FRST_FLUX`/`PEAK_FLUX`（流量密度 erg cm⁻² s⁻¹ Å⁻¹）、`*_SIGMA`（检测显著度）。
- **光变拟合（42–223，每滤光片 26 列 × 7 滤光片）**：后缀 `_W2/_M2/_W1/_UU/_BB/_VV/_WH` 对应 UVW2/UVM2/UVW1/u/b/v/white。`ALP1..ALP4`（第 1–4 段时间幂律指数，F∝t^(-α)）、`TB1..TB3`（拐折时间，s）、`NORM`（首段归一化）、`CHISQ`/`DOF`（拟合优度）；`*N`/`*P` 后缀为负/正方向 **1σ** 误差。约半数源为单幂律（仅 ALP1 有效），其余有 1–3 个拐折。
- **固定时刻流量（224–331）**：`R2_2E3/2E4/2E5_*`（由时间斜率外推的 2×10³/2×10⁴/2×10⁵ s 计数率）及 `F2_*`（换算的流量密度），带负/正误差；`_2E4_`、`_2E5_` 块不含 white 滤光片。
- **谱指数（332–349）**：`BETA_2E3/2E4/2E5`（2×10³/2×10⁴/2×10⁵ s 时刻的红移+消光改正紫外/光学谱指数 β，F∝ν^(-β)，β=Γ-1）、`*_ERR`（1σ）、`NORM_*`（归一化）、`CHISQ_B3/B4/B5`、`DOF_B3/B4/B5`。

## noc-db 20 列（OPTCOADD 扩展）

`OBJECT`、`FILTER`、`TIME`（加权时刻）、`TSTART`/`TSTOP`（MET）、`EXPOSURE`、`CSRC`/`CERR`（源计数及误差）、`RATE`/`RATE_ERR`、`MAG`/`MAG_ERR`、`FLUX`/`FLUX_ERR`（1σ）、`SIGMA`、`FIT_TSTART`/`FIT_TSTOP`、`ALPHA`（段时间斜率）、`SCALE_FACT`（滤光片归一化因子）、`NORM_TO`（归一化到的滤光片）。

## image-event-3db/5db 81 列（摘要）

前 16 列：`OBJECT`、`RA`、`DEC`、`POS_ERR`、`TRIGTIME`（MET）、`TRIG_UT`、`TSTART`/`TSTOP`/`TELAPSE`/`TIME`（MET 秒）、`TSINCE_BUR`（=TSTART-TRIGTIME）、`EXPOSURE`、`FILTER`、`BINNING`、`APERTURE`（源孔径半径）、`SRC_AREA`；后续为多种孔径/背景的计数、率、星等、流量及误差，以及图像质量旗标和观测 ID 字符串（完整 81 列定义见 FITS 头 TTYPE 注释与论文 Table 4）。两个文件除孔径（3″ vs 5″）外结构相同。

## 爆发如何标识

- **名称格式**：`GRByymmdd[x]`，如 `GRB050117`、`GRB051021A`（一日多个爆发加 A/B 后缀）。全部 626 个 OBJECT 唯一、无重复。
- **触发编号**：**没有** BAT trigger number 列；与其他目录（如 HEASARC swiftgrb）交叉证认需用名称或坐标+触发时间。
- **坐标**：有，`RA`/`DEC`（J2000.0，度）+ `POS_ERR`（角秒）+ `POS_REF` 出处。
- **时间**：`TRIGTIME` 为 Swift MET（自 2001-01-01 00:00:00 UTC 起的秒数）；`TRIG_UT` 为 `YYYY-DDD-HH:MM:SS`（年积日，非年月日！如 `2005-017-12:52:36`）。

## 发现的坑（入库前必读）

1. **缺失值记号五花八门，且随列而变**：`BAT_FL/BAT_FL_ERR` 缺失 = `-1.0e-07`（物理上不可能的小负数，容易误当正常值，实测 81 行为负）；`BAT_PPF/BAT_PI` 等缺失 = `-1.00`（99 行 PPF 为负）；`Z` 缺失 = `-1.0`（425 行）；`E_HOST` 缺失 = `-99.0`；滤光片等字符串缺失 = `'NULL'`；T90 有 2 行（GRB090515、GRB100628A）为 0，应视为缺失。入库必须逐列按记号清洗，不能统一按 NULL/NaN 处理。
2. **`BAT_PIT` 缺失标记与文档不符**：论文称缺失为 `NULL`，实际 86 行写的是字符串 `'-1.00'`（对应 BAT_PI=-1）；另有 1 行（GRB060123）为怪值 `'(PL)'`。合法模型只有 PL（简单幂律）和 CPL（截断幂律）。
3. **误差置信度两套体系混在一表**：BAT 四参数误差（FL/PPF/PI 及各自 ERR）是 **90% 置信**；UVOT 测光、光变拟合、谱指数的误差是 **1σ**。入库或比较时务必区分。
4. **能段陷阱**：BAT fluence/峰流/光子指数是 **15–150 keV**（观测系），**不是** bolometric 1–10⁴ keV；T90 的能段随发现仪器变化（Swift 15–350 keV，HETE2 30–400 keV）；XRT 流量是 0.3–10 keV。与 Fermi GBM（常报 10–1000 keV / 50–300 keV）的 fluence 直接比较需谨慎。
5. **网页简介数字过时**：主页写 "538 GRBs"，实际目录 626 行（538 是 UVOT 观测子集）。以 FITS 文件和论文为准。
6. **字符串列带尾随空格**：如 `'GRB071129 '`、`'PL   '`、`'SGA'`，比较/连接前需 strip。
7. **FITS TUNIT 全空**：单位只写在 TTYPE 注释文本里，不能依赖 astropy 自动解析单位。
8. **无 Epeak/Eiso**：本目录只有窄能段流量和光子指数，不提供谱峰能量或各向同性光度；需要时须外部补充（Fermi GBM 目录、BAT 谱目录等）。
9. **MET vs UTC**：TRIGTIME 是 Swift MET 秒（2001 年起算），不是 Unix 时间戳；TRIG_UT 用年积日，解析时注意。
