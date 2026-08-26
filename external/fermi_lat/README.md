# fermi_lat — FERMILGRB（Fermi LAT 第二个 GRB 目录，2FLGC）

## 基本信息

- 目录名称：FERMILGRB — Fermi LAT Second Gamma-Ray Burst Catalog（简称 2FLGC）
- 主页 URL：https://heasarc.gsfc.nasa.gov/W3Browse/fermi/fermilgrb.html
- 参考文献：Ajello et al. 2019, ApJ, 878, 52（"A Decade of Gamma-Ray Bursts Observed by Fermi-LAT: The Second GRB Catalog", arXiv:1906.11403）
- 数据出处：Fermi Science Support Center (FSSC)，HEASARC 于 2022 年 4 月更新入库，表最后更新 2022-06-22
- 获取日期：2026-07-21
- 覆盖时段：2008-08-04 起，原始目录覆盖前 10 年（至 2018-08-04），后续用相同流程补充了新 GRB（当前最晚到 GRB220527）

## 数据文件与下载 URL

| 文件 | 下载 URL | 格式 | 行数（实测） |
|---|---|---|---|
| `gll_2flgc_dr1.fits` | https://heasarc.gsfc.nasa.gov/FTP/fermi/data/lat/catalogs/burst/gll_2flgc_dr1.fits | FITS 二进制表（FSSC 官方 DR1 发布文件） | **228 行** × 116 列 |
| `fermilgrb_w3browse_full.txt` | https://heasarc.gsfc.nasa.gov/db-perl/W3Browse/w3table.pl?tablehead=name%3Dfermilgrb&Action=Default+Search&displaymode=BatchDisplay&Fields=All+Fields&ResultMax=10000 | HEASARC BatchDisplay ASCII（管道分隔，含全部 107 列） | **231 行** × 107 列 |

两个文件均原样保存，未做修改。

### 行数核对说明（重要）

- W3Browse 页面声明表于 **2022-06-22** 最后更新、会定期补充新 GRB；实测其完整表为 **231 个 GRB**（最晚 GRB220527387，2022-05-27）。
- FSSC 的 FITS 文件（`VERSION = 'v02-DR1'`，PRIMARY 头）为 **228 行**（最晚 GRB220210998，2022-02-10），即 DR1 发布时点的快照，比 W3Browse 在线表少 3 个 2022 年的 GRB（GRB220228438、GRB220408311、GRB220527387）。
- 两者主体内容一致，但 **W3Browse 全表（231 行）更新**；FITS 文件独有 97 个时间 bin 的光变曲线矢量列（`LC_*`），W3Browse 表没有。若需要光变曲线用 FITS，若需要最全的 GRB 列表用 ASCII 表。
- 论文（2019ApJ...878...52A）原始目录为 186 个 GRB（前 10 年），后来的行是"same procedure"补充的。

## 爆发标识

- `name` / `GRBNAME`：主标识，格式 **GRByymmddfff**（fff 为当天 UTC 小数，3 位，如 GRB080916009）。注意不是 GRB 常见的 yymmddx 字母后缀格式。
- `gcn_name` / `GCNNAME`：GCN 通报中的名称（通常为 GRB yymmddA 格式，可与其他目录交叉）。
- `gbm_cat_name` / `GBM_assoc_key`：对应的 Fermi GBM 目录名（GRByymmddfff 格式），可用于和 GBM 触发目录（fermigbrst）做关联键。
- `trigger_met` / `GRBMET`：Fermi 任务历经秒（MET, s）。
- 坐标：`ra`、`dec`（J2000，度），`error_radius`（LAT transient factory 定位误差，度）；另有银经银纬 `lii`、`bii`。

## 关键参数速查（对接项目需求）

- **T90**：有。`gbm_cat_t90`（GBM，s）为主；另有 `lle_t90`（LLE 数据，s）和 `tl100`（LAT 100 MeV–100 GeV 持续时长，s）。**没有 15–150 keV 等其它能段的 T90**。
- **Epeak**：**没有**。本目录 LAT 分析只用幂律模型（光子指数），不做 Band/CPL 拟合，无 Epeak、alpha、beta。需要 Epeak 请关联 fermigbrst（GBM 触发目录）。
- **Fluence**：有两套——`gbm_cat_fluence`（GBM 10 keV–1 MeV，erg/cm²）和 `like_*_fluence`（LAT 似然分析，erg/cm²）。
- **Eiso**：有。`like_{best,lat,gbm,ext}_eiso_rf`，**静止系（rest frame）100 MeV–10 GeV**，单位 **10^52 erg**（列名里的 52 就是这个意思，见"坑"一节）。

## 逐列文档（以 W3Browse 全表 107 列为准；FITS 列名对应关系见末尾）

### 标识与时间
| 列名 | 含义 | 单位 |
|---|---|---|
| name | GRB 名称，GRByymmddfff（yymmdd=年月日，fff=当天小数） | — |
| gcn_name | GCN 分发列表中的名称 | — |
| gbm_cat_name | Fermi GBM GRB 目录中的名称 | — |
| time | 触发时间（UTC） | — |
| trigger_met | 触发时间（Fermi MET） | s |

### 位置
| 列名 | 含义 | 单位 |
|---|---|---|
| ra / dec | 测得的赤经/赤纬（指定历元，J2000） | deg |
| lii / bii | 银经/银纬 | deg |
| error_radius | LAT transient factory 分析的定位误差半径 | deg |
| theta | 触发时刻离轴角 | deg |
| zenith | 触发时刻天顶角 | deg |
| arr_flag | 是否触发自主重新指向请求（ARR），1/0 | — |
| distance_to_closest | 与最近 3FGL 源的距离 | deg |

### 红移与距离
| 列名 | 含义 | 单位 |
|---|---|---|
| redshift | 红移（若已知）；**未知=0**（228 行 FITS 中 184 行为 0） | — |
| luminosity_distance | 由红移计算的光度距离；未知=0 | cm |

### LLE（LAT Low Energy）探测
| 列名 | 含义 | 单位 |
|---|---|---|
| lle_bbbd_sig | LLE 数据贝叶斯块爆发检测（BBBD）显著性 | sigma |
| lle_bbbd_sig_detected | LLE 是否探测到（1/0） | — |
| lle_t05 | LLE 起始时间（相对触发；负值=早于触发） | s |
| lle_t90 | LLE 时长，5%–95% 计数区间；HEASARC 文档称其计数取自 **50–300 keV**（见"坑"）；未探测=0 | s |
| lle_t95 | LLE 结束时间 | s |

### LAT 光子计时（100 MeV–100 GeV）
| 列名 | 含义 | 单位 |
|---|---|---|
| tl0 | 第一个关联概率 p>0.9 的光子到达时刻（100 MeV–100 GeV） | s |
| tl1 | 最后一个 p>0.9 光子的到达时刻 | s |
| tl0_lower | LAT 发射起始时间下限估计 | s |
| tl1_upper | LAT 发射结束时间上限估计 | s |
| tl100 | LAT 发射持续时长 = tl1−tl0 | s |
| tl100_error | 上述时长的估计误差 | s |

### 似然分析（四组时间窗 × 8 参数；LAT 能段为 100 MeV–100 GeV）
对 4 个时间窗各做似然分析，前缀分别为：
- `like_best_*`：TS 最高的时间窗（best）
- `like_lat_*`：LAT 时间窗
- `like_gbm_*`：GBM 时间窗（GBM T90 区间）
- `like_ext_*`：EXT（extended/延展发射）时间窗

每组包含（`{p}` 为前缀）：
| 列名 | 含义 | 单位 |
|---|---|---|
| {p}_t0 / {p}_t1 | 似然分析时间窗起/止 | s |
| {p}_ts / like_best_ts | 似然分析检验统计量 TS | — |
| {p}_flux (± _error) | 光子流量 | ph/cm²/s |
| {p}_flux_ene (± _error) | 能量流量 | erg/cm²/s |
| {p}_fluence (± _error) | 能量流量积分（fluence） | erg/cm² |
| {p}_grbindex (± _error) | 拟合幂律的**光子指数**（能谱模型：单一幂律 PL，无 Band/CPL） | — |
| {p}_eiso_rf (± _error) | **静止系**各向同性能量，**100 MeV–10 GeV（rest frame）**，单位 **10^52 erg** | 10^52 erg |

注：仅 `like_best_*` 时间窗有 TS 列名写作 `like_best_ts`（FITS 中为 `LIKE_BEST_TS_GRB`）。

### 延展发射高能光子
| 列名 | 含义 | 单位 |
|---|---|---|
| ext_emission_max_ene | 时间分辨分析中关联概率 >90% 的最高能光子能量 | MeV |
| ext_emission_max_ene_p | 该最高能光子的关联概率 | — |
| ext_emission_max_ene_t | 该光子的到达时间 | s |
| ext_emission_n | 关联概率 >90% 的光子总数 | — |

### LAT 光变曲线时间拟合（注意：是**流量随时间**的幂律，非能谱）
| 列名 | 含义 | 单位 |
|---|---|---|
| lat_spl_chi2 | 单一幂律（SPL）拟合 χ² | — |
| lat_f0 (± _error) | SPL 归一化 | — |
| lat_spl_index1 (± _error) | SPL 时间衰减指数 | — |
| lat_bpl_chi2 | 折幂律（BPL）拟合 χ² | — |
| lat_bpl_f0 (± _error) | BPL 归一化 | — |
| lat_bpl_index1 / lat_bpl_index2 (± _error) | BPL 前/后时间指数 | — |
| lat_bpl_timebreak (± _error) | 折点时刻 | s |
| late_index (± _error) | 晚期行为最佳描述指数（依 χ² 取 BPL 第二指数或 SPL 指数） | — |

### 其它
| 列名 | 含义 | 单位 |
|---|---|---|
| irfs | 分析所用仪器响应函数 | — |
| su_tsinput | LAT transient factory 探测算法的 TS 输入值 | — |

### 附带的 GBM 目录参数（交叉引入自 Fermi GBM GRB 目录）
| 列名 | 含义 | 单位 |
|---|---|---|
| gbm_cat_t05 | GBM T05；**不可得时置 0** | s |
| gbm_cat_t90 | GBM T90；不可得时为估计的瞬时辐射时长 | s |
| gbm_cat_t90_error | GBM T90 误差 | s |
| gbm_cat_t95 | = T90 + T05 | s |
| gbm_cat_fluence (± _error) | GBM 目录 fluence，**10 keV–1 MeV** 能段（erg/cm²；文档与 FITS TUNIT 误写为 erg/cm²/s，见"坑"） | erg/cm² |

### FITS 文件独有列（116 列中超出上表的部分）
- 命名差异：FITS 用 `GCNNAME/GRBNAME/GRBDATE/GRBMET/ERR`、`LLET05/LLET90/LLET95`、`TL0_L/TL1_U`、`EXTENDED_*`、`GBMT05/GBMT90/GBMT95`、`GBM_assoc_key`、`T90_ERROR`、`FLUENCE/FLUENCE_ERROR` 等，与上表一一对应。
- **光变曲线矢量列**（每行 97 个时间 bin，P 格式变长数组）：`LC_START`、`LC_END`、`LC_MEDIAN`（bin 起/止/中位，s）、`LC_TS`（bin 内 TS）、`LC_FLUX(±_ERR)`（ph/cm²/s）、`LC_ENE_FLUX(±_ERR)`（erg/cm²/s）、`LC_FLUENCE`（erg/cm²）、`LC_INDEX(±_ERR)`（bin 内幂律光子指数）。
- FITS 的 `LIKE_LAT_FLUX_ENE`/`LIKE_LAT_FLUENCE_ENE` 等个别 TUNIT 写成 `ph/cm^2/s` 或 `erg/cm^2/s`，应为 erg 系单位（见"坑"）。

## 参考系 / 能段 / 模型 / 误差约定汇总

- **能段**：LAT 光子计时与似然分析均为 **100 MeV–100 GeV（观测系）**；Eiso 为**静止系 100 MeV–10 GeV**；GBM fluence 为 **10 keV–1 MeV**；`lle_t90` 文档称计数取自 50–300 keV。**没有 15–150 keV（那是 Swift/BAT）**。
- **观测系 vs 静止系**：所有 flux/fluence 为观测系；仅 `*_eiso_rf` 为静止系（列名 `_RF` = rest frame），依赖红移，无红移者为 0。
- **能谱模型**：LAT 分析全部用**单一幂律（PL）**，参数为光子指数（`grbindex`）。无 Band、无 CPL、无 Epeak。`lat_bpl/spl` 系列是**光变曲线**的时间幂律，勿当能谱模型。
- **误差置信度**：网页文档只写 "estimated error"，未标注 1σ/90%。按目录论文（Ajello et al. 2019）惯例为 **1σ 统计误差**；GBM 引入参数随 GBM 目录亦为 1σ。若需严格置信度请回查论文对应章节。

## 已发现的坑（务必注意）

1. **Eiso 单位是 10^52 erg，不是 erg**：FITS 列名 `LIKE_*_EISO52_RF`（52 = 指数），TUNIT 写 `erg` 但数值量级为 0–256（如 256 → 2.56×10^54 erg）。入库时必须 ×10^52。
2. **缺失值记号不统一**：
   - 红移未知 → `redshift = 0`、`luminosity_distance = 0`、`*_eiso_rf = 0`（FITS 228 行中 184 行如此）。**0 不是合法物理值，必须当 NULL 处理**。
   - `lle_t90 = 0` 表示 LLE 未探测（117/228 行）；`gbm_cat_t05 = 0` 表示不可得（文档明示）。
   - GBM 关联参数（`FLUENCE`、`T90_ERROR` 等）在无 GBM 对应源时为 FITS NaN（11 行），`GBM_assoc_key` 为空字符串。
   - BatchDisplay ASCII 中缺失值为**空字段**（实测 408 个空格单元）。
3. **单位标注笔误**：FITS 中 `FLUENCE`/`FLUENCE_ERROR`（GBM fluence）TUNIT 标为 `erg/cm^2/s`，实为 **erg/cm²**（fluence 非 flux）；`LIKE_LAT_FLUX_ENE` 标 `ph/cm^2/s` 实为 erg/cm²/s；`LIKE_BEST_FLUENCE_ENE_ERR` 标 `erg/cm^2/s` 实为 erg/cm²。以物理量名为准，勿盲信 TUNIT。
4. **`lle_t90` 能段描述存疑**：HEASARC 文档称其 5–95% 计数区间取自 "50–300 keV"，但 LLE 本身是 30 MeV–100 MeV 的 LAT 低能数据。引用时建议注明出处歧义或回查论文。
5. **GRB 名称格式**：`name` 为 GRByymmddfff（当天小数），与其他目录常用的 GRB yymmddx（字母后缀）不同；交叉匹配优先用 `gbm_cat_name` 或 `trigger_met`。
6. **两个文件行数不同**（228 vs 231）：FITS 为 DR1 快照，W3Browse 在线表多 3 个 2022 年 GRB；但 FITS 独有 97-bin 光变曲线列。按需求选用或合并。
7. **BatchDisplay ASCII 格式**：首行 `BatchStart`、末行 `BatchEnd`，第 2 行为管道分隔表头，第 3 行为 `+---` 分隔线，数据行以 `|GRB` 开头；坐标为 `hh mm ss.s` / `±dd mm ss` 字符串而非十进制度。
8. **TS 与显著性**：`like_*_ts` 是似然比检验统计量（TS≈σ²），不是 σ；`lle_bbbd_sig` 才是 σ。
