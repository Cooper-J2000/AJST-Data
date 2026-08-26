# fermi_gbm — Fermi GBM Burst Catalog (FERMIGBRST)

## 基本信息

- **目录名称**: Fermi GBM Burst Catalog（HEASARC 表名 `fermigbrst`）
- **主页 URL**: https://heasarc.gsfc.nasa.gov/W3Browse/fermi/fermigbrst.html
- **数据文件下载 URL**: https://heasarc.gsfc.nasa.gov/FTP/heasarc/dbase/dump/heasarc_fermigbrst.tdat.gz
  （HEASARC 全库转储目录 `/FTP/heasarc/dbase/dump/`，所有 Browse 表均有对应 `.tdat.gz`）
- **获取日期**: 2026-07-21
- **数据版本**: 文件头 CREATION DATE = 2026-07-19 03:30:29；主页 Bulletin 称表最后更新于 2026-07-19，两者一致，为当日最新。
- **内容**: Fermi GBM 触发并被分类为 GRB 的爆发的位置、时标（T50/T90）、流量/注量、以及两套能谱拟合（峰流量谱 pflx、注量谱 flnc）× 四种模型（PL/CPL/Band/SBPL）的参数。数据由 GBM 仪器运行中心（GIOC）和 FSSC 提供，新数据处理后约一天内自动更新。

## 文件清单

| 文件 | 大小 | 说明 |
|---|---|---|
| `heasarc_fermigbrst.tdat.gz` | 4,468,607 B (md5: 7cbda2ca5cbcd5db329be6a83ef08d69) | 原始下载文件，未做任何修改 |

**格式**: 解压后为 HEASARC `.tdat` 纯文本转储格式：
- `<HEADER>` 段（含全部 306 列的机器可读定义：`field[名] = 类型_单位 [UCD] // 描述`）；
- `<DATA>` 与 `<END>` 之间为数据区，每行一条记录，字段以竖线 `|` 分隔；
- 总行数实测：`zcat | wc -l` = 4698 行（含表头 351 行 + `<DATA>`/`<END>` 标记各 1 行 + 末行换行）。
- **数据行数实测 4345 行**，与文件头声明 `TOTAL ROWS: 4345` 一致（脚本逐行解析验证）。所有 4345 行 `name` 均以 `GRB` 开头、`trigger_name` 均以 `bn` 开头。

## 逐列文档（关键列详解 + 命名规则 + 完整清单）

共 **306 列**。绝大多数列遵循统一命名规则，先讲规则再列关键列，附录给出全部列的清单。

### 命名规则

- **时标/定位/基础量**：无前缀（`t50`、`t90`、`fluence`、`flux_*` 等），来自 "bcat" 批量拟合文件（8 通道数据、Comptonized 模型），用于确定爆发时长。
- **能谱拟合参数**：`{区间}_{模型}_{参数}` 三段式：
  - 区间前缀：`pflx_` = 峰流量谱（峰流量时间范围内的单段谱）；`flnc_` = 注量谱（覆盖整个爆发时长的单段谱）。
  - 模型：`plaw`（幂律 PL）、`comp`（Comptonized，即指数截断幂律 CPL）、`band`（Band 函数）、`sbpl`（平滑折线幂律 SBPL）。
  - 参数：`ampl`（幅度）、`index`/`alpha`/`beta`/`indx1`/`indx2`（谱指数）、`epeak`（νFν 峰能量，keV，仅 comp/band）、`pivot`（支点能量）、`brken`/`brksc`（SBPL 转折能量/转折尺度）、`phtflux`/`ergflux`（光子/能量通量）、`phtflnc`/`ergflnc`（光子/能量注量）、以上加 `b` 后缀（`phtfluxb` 等）表示 **50-300 keV（BATSE 标准带）** 版本、不加 b 为 **10-1000 keV** 标称带；`redchisq`、`redfitstat`、`dof`、`statistic` 为拟合优度。
- **误差列**：基础量用 `_error`（对称 1σ）；谱拟合参数用 `_pos_err` / `_neg_err`（非对称正负 1σ 统计误差；**误差 = 0.0 表示该参数在拟合中被固定**，不是误差为零）。
- `*_best_fitting_model` 给出该区间的最优模型名（取值如 `flnc_comp`、`pflx_plaw` 等），配合 `*_best_model_redchisq`。

### 关键列详解

| 列 | 单位 | 说明 |
|---|---|---|
| `trigger_name` | - | Fermi 触发编号，格式 `bnyymmddfff`（fff=当日 UTC 小数），主键 |
| `name` | - | 源名，初为 `GRByymmddfff`，人工确认后改为 `GRByymmddx`（x 为空/A/B…，区分同日多个爆发） |
| `ra`, `dec` | degree | J2000 赤道坐标 |
| `lii`, `bii` | degree | 银道坐标 |
| `error_radius` | degree | 定位误差半径。统计 1σ（误差椭圆平均，GBM 误差不对称）。**0 = 由外部仪器（Swift/XMM/Chandra 等）定位；50 = 定位很差** |
| `trigger_time` | MJD | 触发时刻（由 Fermi MET 转换为 UTC/MJD） |
| `duration_energy_low/high` | keV | T50/T90 积分能段，实测全表为 **50–300 keV** |
| `t50`, `t50_error`, `t50_start` | s | 积累 25%→75% 注量所需时间（T50），观测系；start 为相对触发时刻的起点 |
| `t90`, `t90_error`, `t90_start` | s | 积累 5%→95% 注量所需时间（T90），观测系 |
| `bcat_detector_mask` | - | 14 位 0/1 标志：前 12 位 NaI 探测器、后 2 位 BGO，1=用于时长计算 |
| `flu_low`, `flu_high` | keV | 流量/注量积分能段，标称 10–1000 keV（逐源给出实际值） |
| `fluence`, `fluence_error` | erg/cm² | 整个爆发（100% 水平）**10-1000 keV** 注量，来自 bcat 批量拟合（Comptonized 模型，8 通道数据）；1σ 对称误差 |
| `fluence_batse`, `fluence_batse_error` | erg/cm² | 同上但 **50-300 keV**（BATSE 标准带），便于与 BATSE 目录比较 |
| `flux_64/256/1024`, `*_error`, `*_time` | photon/cm²/s, s | **10-1000 keV** 峰流量（64/256/1024 ms 三种时间尺度）及对应区间起点 |
| `flux_batse_64/256/1024` 等 | photon/cm²/s | 同上但 **50-300 keV** |
| `actual_64/256/1024ms_interval` | s | 名义时间尺度的实际长度（短爆发边界处会截断） |
| `scat_detector_mask` | - | 14 位 0/1 标志：用于能谱拟合的探测器 |
| `pflx_spectrum_start/stop` | s | 峰流量谱拟合区间（相对触发时刻） |
| `pflx_comp_epeak` ± pos/neg | keV | **峰流量谱 CPL 模型 Epeak（观测系）** |
| `pflx_band_epeak` ± pos/neg | keV | 峰流量谱 Band 模型 Epeak（观测系） |
| `flnc_comp_epeak` ± pos/neg | keV | **注量谱（时间积分谱）CPL 模型 Epeak（观测系）** |
| `flnc_band_epeak` ± pos/neg | keV | 注量谱 Band 模型 Epeak（观测系） |
| `{pflx,flnc}_{model}_ergflnc(b)` | erg/cm² | 谱拟合导出的能量注量（10-1000 keV；带 b 为 50-300 keV） |
| `{pflx,flnc}_best_fitting_model` | - | 最优模型名（空 = 无有效谱拟合） |
| `bcatalog`, `scatalog` | - | bcat/scat 文件所属目录版本号（详见"坑"一节） |
| `last_modified` | MJD | 该行最后修改时间 |

### 能量范围与参考系（重要）

- **T50/T90**：在 **50–300 keV** 能段计算（`duration_energy_low/high` 逐源给出，本版全表均为 50/300）。
- **`fluence`/`flux_*`（bcat 产物）**：主列为 **10–1000 keV**；`*_batse` 列为 **50–300 keV**。
- **谱拟合通量/注量（pflx_/flnc_）**：不带 `b` 后缀为 **10–1000 keV**；带 `b` 后缀为 **50–300 keV**。
- **参考系**：所有量均为**观测系（observer frame）**。GBM 目录不含红移，**没有静止系 Epeak、没有 Eiso/Liso**；如需 Eiso 需自行结合红移计算。
- **能谱模型**：PL（plaw）、CPL（comp，指数截断幂律）、Band、SBPL 四种；Epeak 只有 comp 和 band 模型有（SBPL 用 `brken` 转折能量）。
- **误差**：全部为 **1σ 统计误差**。基础量（T90、fluence、flux）为对称 `_error`；谱参数为非对称 `_pos_err`/`_neg_err`。**不存在 90% 置信误差**。

### 爆发标识

- 主键 `trigger_name` = `bnyymmddfff`（Fermi 触发编号）。
- `name` = `GRByymmddfff`（管线初命名）或人工改名后的 `GRByymmddx`（x 为空或 A/B…）。本表中两种格式并存，做跨表关联时建议用 `trigger_name` 或用 `GRByymmdd` 前缀匹配。
- 有坐标：`ra`/`dec`（度）+ `error_radius`（度，注意 0 和 50 的特殊含义）。

### 坑与注意事项（实测发现）

1. **行尾多一个 `|`**：每条数据行以竖线结尾，split 后得到 307 个字段（最后一个为空字符串），解析时按 306 列截取或丢弃末元素。
2. **缺失值 = 空字符串**（两个 `|` 相邻），无 `NULL`/`-999` 之类的哨兵值。但注意 **`_pos_err`/`_neg_err` = 0.0 有特殊含义：参数被固定**，不是误差为零。
3. **缺失规模实测**（4345 行中）：`t90`/`fluence` 等 bcat 量仅 1 行缺失；`flnc_comp_epeak` 缺 725 行、`flnc_band_epeak` 缺 727 行、`pflx_band_epeak` 缺 822 行（弱爆发复杂模型拟合不收敛，字段留空）；`flnc_best_fitting_model` 缺 682 行、`scatalog` 缺 659 行（无谱拟合条目）。
4. **两套 fluence 不要混淆**：`fluence`（bcat，8 通道批量拟合，官方称可靠性低于谱拟合）vs `flnc_{model}_ergflnc`（128 通道谱拟合产物）。精确工作建议用谱拟合值并参考 `flnc_best_fitting_model` 选模型。
5. **网页文档过时**：主页说 `scatalog` "2 为当前目录"，但实测数据版本分布为 3（2169 行）、5（1382）、4（132）、2（3）、空（659）；`bcatalog` 为 0/1/2/3/4 混合。即表已更新到第四版目录（von Kienlin et al. 2020）之后仍在滚动更新，文档描述停留在第二版。
6. **主页声称数量核对**：网页本身未直接给出行数；其 Bulletin（表更新于 2026-07-19）与转储文件 CREATION DATE（2026-07-19）一致，文件头 `TOTAL ROWS: 4345` 与实测数据行数一致。
7. **`redchisq` 在第二版目录中未使用**（既不用于参数优化也不用于模型比较），少数 GRB 缺 chi 方为已知软件问题，不代表拟合坏。模型选择判据在第一版（Goldstein+2011）与第二版（Gruber+2014）间不同。
8. **无 Eiso / 无红移 / 无静止系量**；`trigger_time` 是 MJD 不是 UTC 字符串，转换时注意。
9. 时间积分谱（flnc）区间由值班科学家选取（`flnc_spectrum_start/stop`），与 T90 区间不一定相同；峰流量谱（pflx）区间对应峰流量时段。
10. 谱拟合可能在弱爆发上产生非物理的流量/注量值且误差留空——官方原样保留了这些坏拟合，使用前应检查 `redfitstat`/误差是否为空。

## 参考文献

- 第四版（当前）总目录：von Kienlin et al. 2020, ApJ, 893, 46
- 第三版：Bhat et al. 2016, ApJS, 223, 28
- 第二版总目录：von Kienlin et al. 2014, ApJS, 211, 13；第二版谱目录：Gruber et al. 2014, ApJS, 211, 12
- GBM Caveats: http://fermi.gsfc.nasa.gov/ssc/data/analysis/GBM_caveats.html

## 附录：完整列清单（306 列，单位与描述提取自文件 HEADER 段）

| 列名 | 单位 | 描述 |
|---|---|---|
| trigger_name | - | Fermi Trigger Designation (Assigned for Each New Trigger Detected) |
| name | - | Source Designation |
| ra | degree | Right Ascension |
| dec | degree | Declination |
| lii | degree | Galactic Longitude |
| bii | degree | Galactic Latitude |
| error_radius | degree | Uncertainty in the Position (degrees) |
| trigger_time | mjd | Observation Trigger Time |
| duration_energy_low | keV | Lower Limit of Duration Integration (keV) |
| duration_energy_high | keV | Upper Limit of Duration Integration (keV) |
| back_interval_low_start | s | Start Time for Lower Background Selection Interval Relative to the Trigger Time |
| back_interval_low_stop | s | Stop Time for Lower Background Selection Interval Relative to the Trigger Time |
| back_interval_high_start | s | Start Time for Upper Background Selection Interval Relative to the Trigger Time |
| back_interval_high_stop | s | Stop Time for Upper Background Selection Interval Relative to the Trigger Time |
| t50 | s | 50% Burst Duration (s) |
| t50_error | s | Uncertainty in T50 Duration |
| t50_start | s | Start of T50 Interval (s) Relative to Trigger Time |
| t90 | s | 90% Burst Duration (s) |
| t90_error | s | Uncertainty in T90 Duration |
| t90_start | s | Start of T90 Interval (s) Relative to Trigger Time |
| bcat_detector_mask | - | Flags [01] Indicate Included Detectors by Position // (0-11: 12 NaI Detectors; 12-13: 2 BGO Detectors) |
| flu_low | keV | Lower Limit of Flux/Fluence Integration (keV) |
| flu_high | keV | Upper Limit of Flux/Fluence Integration (keV) |
| fluence | erg/cm^2 | 10-1000 keV Fluence |
| fluence_error | erg/cm^2 | Uncertainty in the 10-1000 keV Fluence |
| fluence_batse | erg/cm^2 | 50-300 keV Fluence (BATSE Standard) |
| fluence_batse_error | erg/cm^2 | Uncertainty in the 50-300 keV Fluence |
| flux_1024 | photon/cm^2/s | 10-1000 keV Peak Flux (1024ms Timescale) |
| flux_1024_error | photon/cm^2/s | Uncertainty in the 10-1000 keV Peak Flux (1024ms Timescale) |
| flux_1024_time | s | Start Time for Peak Flux Interval (1024ms Timescale) Relative to Trigger Time |
| flux_64 | photon/cm^2/s | 10-1000 keV Peak Flux (64ms Timescale) |
| flux_64_error | photon/cm^2/s | Uncertainty in the 10-1000 keV Peak Flux (64ms Timescale) |
| flux_64_time | s | Start Time for Peak Flux Interval (64ms Timescale) Relative to Trigger Time |
| flux_256 | photon/cm^2/s | 10-1000 keV Peak Flux (256ms Timescale) |
| flux_256_error | photon/cm^2/s | Uncertainty in the 10-1000 keV Peak Flux (256ms Timescale) |
| flux_256_time | s | Start Time for Peak Flux Interval (256ms Timescale) Relative to Trigger Time |
| flux_batse_1024 | photon/cm^2/s | 50-300 keV Peak Flux (1024ms Timescale) |
| flux_batse_1024_error | photon/cm^2/s | Uncertainty in the 50-300 keV Peak Flux (1024ms Timescale) |
| flux_batse_1024_time | s | Start Time for Peak Flux Interval (1024ms Timescale) Relative to Trigger Time |
| flux_batse_64 | photon/cm^2/s | 50-300 keV Peak Flux (64ms Timescale) |
| flux_batse_64_error | photon/cm^2/s | Uncertainty in the 50-300 keV Peak Flux (64ms Timescale) |
| flux_batse_64_time | s | Start Time for Peak Flux Interval (64ms Timescale) Relative to Trigger Time |
| flux_batse_256 | photon/cm^2/s | 50-300 keV Peak Flux (256ms Timescale) |
| flux_batse_256_error | photon/cm^2/s | Uncertainty in the 50-300 keV Peak Flux (256ms Timescale) |
| flux_batse_256_time | s | Start Time for Peak Flux Interval (256ms Timescale) Relative to Trigger Time |
| actual_64ms_interval | s | Actual Length of Nominal 64ms Timescale for Peak Flux Measurement |
| actual_256ms_interval | s | Actual Length of Nominal 256ms Timescale for Peak Flux Measurement |
| actual_1024ms_interval | s | Actual Length of Nominal 1024ms Timescale for Peak Flux Measurement |
| scat_detector_mask | - | Flags [01] Indicate Detectors Included in Model Fits by Position // (0-11: 12 NaI Detectors; 12-13: 2 BGO Detectors) |
| pflx_spectrum_start | s | Start Time for Peak Flux Spectrum Fits Relative to Trigger Time |
| pflx_spectrum_stop | s | End Time for Peak Flux Spectrum Fits Relative to Trigger Time |
| pflx_plaw_ampl | photon/cm^2/s/keV | Power Law Model Amplitude for Peak Flux Spectrum |
| pflx_plaw_ampl_pos_err | photon/cm^2/s/keV | Power Law Model Amplitude Positive Error for Peak Flux Spectrum |
| pflx_plaw_ampl_neg_err | photon/cm^2/s/keV | Power Law Model Amplitude Negative Error for Peak Flux Spectrum |
| pflx_plaw_pivot | keV | Power Law Model Pivot Energy for Peak Flux Spectrum |
| pflx_plaw_pivot_pos_err | keV | Power Law Model Pivot Energy Positive Error for Peak Flux Spectrum |
| pflx_plaw_pivot_neg_err | keV | Power Law Model Pivot Energy Negative Error for Peak Flux Spectrum |
| pflx_plaw_index | - | Power Law Model Index for Peak Flux Spectrum |
| pflx_plaw_index_pos_err | - | Power Law Model Index Positive Error for Peak Flux Spectrum |
| pflx_plaw_index_neg_err | - | Power Law Model Index Negative Error for Peak Flux Spectrum |
| pflx_plaw_phtflux | photon/cm^2/s | Power Law Model Photon Flux for Peak Flux Spectrum |
| pflx_plaw_phtflux_error | photon/cm^2/s | Power Law Model Photon Flux Error for Peak Flux Spectrum |
| pflx_plaw_phtflnc | photon/cm^2 | Power Law Model Photon Fluence for Peak Flux Spectrum |
| pflx_plaw_phtflnc_error | photon/cm^2 | Power Law Model Photon Fluence Error for Peak Flux Spectrum |
| pflx_plaw_ergflux | erg/cm^2/s | Power Law Model Energy Flux for Peak Flux Spectrum |
| pflx_plaw_ergflux_error | erg/cm^2/s | Power Law Model Energy Flux Error for Peak Flux Spectrum |
| pflx_plaw_ergflnc | erg/cm^2 | Power Law Model Energy Fluence for Peak Flux Spectrum |
| pflx_plaw_ergflnc_error | erg/cm^2 | Power Law Model Energy Fluence Error for Peak Flux Spectrum |
| pflx_plaw_phtfluxb | photon/cm^2/s | Power Law Model 50-300 keV (BATSE) Photon Flux for Peak Flux Spectrum |
| pflx_plaw_phtfluxb_error | photon/cm^2/s | Power Law Model 50-300 keV (BATSE) Photon Flux Error for Peak Flux Spectrum |
| pflx_plaw_phtflncb | photon/cm^2 | Power Law Model 50-300 keV (BATSE) Photon Fluence for Peak Flux Spectrum |
| pflx_plaw_phtflncb_error | photon/cm^2 | Power Law Model 50-300 keV (BATSE) Photon Fluence Error for Peak Flux Spectrum |
| pflx_plaw_ergflncb | erg/cm^2 | Power Law Model 50-300 keV (BATSE) Energy Fluence for Peak Flux Spectrum |
| pflx_plaw_ergflncb_error | erg/cm^2 | Power Law Model 50-300 keV (BATSE) Energy Fluence Error for Peak Flux Spectrum |
| pflx_plaw_redchisq | - | Power Law Model Reduced Chi-Squared for Peak Flux Spectrum |
| pflx_plaw_redfitstat | - | Power Law Model Reduced Fitting Statistic for Peak Flux Spectrum |
| pflx_plaw_dof | - | Power Law Model Degrees of Freedom for Peak Flux Spectrum |
| pflx_plaw_statistic | - | Power Law Model Statistical Merit Function for Peak Flux Spectrum |
| pflx_comp_ampl | photon/cm^2/s/keV | Comptonized Model Amplitude for Peak Flux Spectrum |
| pflx_comp_ampl_pos_err | photon/cm^2/s/keV | Comptonized Model Amplitude Positive Error for Peak Flux Spectrum |
| pflx_comp_ampl_neg_err | photon/cm^2/s/keV | Comptonized Model Amplitude Negative Error for Peak Flux Spectrum |
| pflx_comp_epeak | keV | Comptonized Model Peak Energy for Peak Flux Spectrum |
| pflx_comp_epeak_pos_err | keV | Comptonized Model Peak Energy Positive Error for Peak Flux Spectrum |
| pflx_comp_epeak_neg_err | keV | Comptonized Model Peak Energy Negative Error for Peak Flux Spectrum |
| pflx_comp_index | - | Comptonized Model Index for Peak Flux Spectrum |
| pflx_comp_index_pos_err | - | Comptonized Model Index Positive Error for Peak Flux Spectrum |
| pflx_comp_index_neg_err | - | Comptonized Model Index Negative Error for Peak Flux Spectrum |
| pflx_comp_pivot | keV | Comptonized Model Pivot Energy for Peak Flux Spectrum |
| pflx_comp_pivot_pos_err | keV | Comptonized Model Pivot Energy Positive Error for Peak Flux Spectrum |
| pflx_comp_pivot_neg_err | keV | Comptonized Model Pivot Energy Negative Error for Peak Flux Spectrum |
| pflx_comp_phtflux | photon/cm^2/s | Comptonized Model Photon Flux for Peak Flux Spectrum |
| pflx_comp_phtflux_error | photon/cm^2/s | Comptonized Model Photon Flux Error for Peak Flux Spectrum |
| pflx_comp_phtflnc | photon/cm^2 | Comptonized Model Photon Fluence for Peak Flux Spectrum |
| pflx_comp_phtflnc_error | photon/cm^2 | Comptonized Model Photon Fluence Error for Peak Flux Spectrum |
| pflx_comp_ergflux | erg/cm^2/s | Comptonized Model Energy Flux for Peak Flux Spectrum |
| pflx_comp_ergflux_error | erg/cm^2/s | Comptonized Model Energy Flux Error for Peak Flux Spectrum |
| pflx_comp_ergflnc | erg/cm^2 | Comptonized Model Energy Fluence for Peak Flux Spectrum |
| pflx_comp_ergflnc_error | erg/cm^2 | Comptonized Model Energy Fluence Error for Peak Flux Spectrum |
| pflx_comp_phtfluxb | photon/cm^2/s | Comptonized Model 50-300 keV (BATSE) Photon Flux for Peak Flux Spectrum |
| pflx_comp_phtfluxb_error | photon/cm^2/s | Comptonized Model 50-300 keV (BATSE) Photon Flux Error for Peak Flux Spectrum |
| pflx_comp_phtflncb | photon/cm^2 | Comptonized Model 50-300 keV (BATSE) Photon Fluence for Peak Flux Spectrum |
| pflx_comp_phtflncb_error | photon/cm^2 | Comptonized Model 50-300 keV (BATSE) Photon Fluence Error for Peak Flux Spectrum |
| pflx_comp_ergflncb | erg/cm^2 | Comptonized Model 50-300 keV (BATSE) Energy Fluence for Peak Flux Spectrum |
| pflx_comp_ergflncb_error | erg/cm^2 | Comptonized Model 50-300 keV (BATSE) Energy Fluence Error for Peak Flux Spectrum |
| pflx_comp_redchisq | - | Comptonized Model Reduced Chi-Squared for Peak Flux Spectrum |
| pflx_comp_redfitstat | - | Comptonized Model Reduced Fitting Statistic for Peak Flux Spectrum |
| pflx_comp_dof | - | Comptonized Model Degrees of Freedom for Peak Flux Spectrum |
| pflx_comp_statistic | - | Comptonized Model Statistical Merit Function for Peak Flux Spectrum |
| pflx_band_ampl | photon/cm^2/s/keV | Band Model Amplitude for Peak Flux Spectrum |
| pflx_band_ampl_pos_err | photon/cm^2/s/keV | Band Model Amplitude Positive Error for Peak Flux Spectrum |
| pflx_band_ampl_neg_err | photon/cm^2/s/keV | Band Model Amplitude Negative Error for Peak Flux Spectrum |
| pflx_band_epeak | keV | Band Model Peak Energy for Peak Flux Spectrum |
| pflx_band_epeak_pos_err | keV | Band Model Peak Energy Positive Error for Peak Flux Spectrum |
| pflx_band_epeak_neg_err | keV | Band Model Peak Energy Negative Error for Peak Flux Spectrum |
| pflx_band_alpha | - | Band Model Alpha for Peak Flux Spectrum |
| pflx_band_alpha_pos_err | - | Band Model Alpha Positive Error for Peak Flux Spectrum |
| pflx_band_alpha_neg_err | - | Band Model Alpha Negative Error for Peak Flux Spectrum |
| pflx_band_beta | - | Band Model Beta for Peak Flux Spectrum |
| pflx_band_beta_pos_err | - | Band Model Beta Positive Error for Peak Flux Spectrum |
| pflx_band_beta_neg_err | - | Band Model Beta Negative Error for Peak Flux Spectrum |
| pflx_band_phtflux | photon/cm^2/s | Band Model Photon Flux for Peak Flux Spectrum |
| pflx_band_phtflux_error | photon/cm^2/s | Band Model Photon Flux Error for Peak Flux Spectrum |
| pflx_band_phtflnc | photon/cm^2 | Band Model Photon Fluence for Peak Flux Spectrum |
| pflx_band_phtflnc_error | photon/cm^2 | Band Model Photon Fluence Error for Peak Flux Spectrum |
| pflx_band_ergflux | erg/cm^2/s | Band Model Energy Flux for Peak Flux Spectrum |
| pflx_band_ergflux_error | erg/cm^2/s | Band Model Energy Flux Error for Peak Flux Spectrum |
| pflx_band_ergflnc | erg/cm^2 | Band Model Energy Fluence for Peak Flux Spectrum |
| pflx_band_ergflnc_error | erg/cm^2 | Band Model Energy Fluence Error for Peak Flux Spectrum |
| pflx_band_phtfluxb | photon/cm^2/s | Band Model 50-300 keV (BATSE) Photon Flux for Peak Flux Spectrum |
| pflx_band_phtfluxb_error | photon/cm^2/s | Band Model 50-300 keV (BATSE) Photon Flux Error for Peak Flux Spectrum |
| pflx_band_phtflncb | photon/cm^2 | Band Model 50-300 keV (BATSE) Photon Fluence for Peak Flux Spectrum |
| pflx_band_phtflncb_error | photon/cm^2 | Band Model 50-300 keV (BATSE) Photon Fluence Error for Peak Flux Spectrum |
| pflx_band_ergflncb | erg/cm^2 | Band Model 50-300 keV (BATSE) Energy Fluence for Peak Flux Spectrum |
| pflx_band_ergflncb_error | erg/cm^2 | Band Model 50-300 keV (BATSE) Energy Fluence Error for Peak Flux Spectrum |
| pflx_band_redchisq | - | Band Model Reduced Chi-Squared for Peak Flux Spectrum |
| pflx_band_redfitstat | - | Band Model Reduced Fitting Statistic for Peak Flux Spectrum |
| pflx_band_dof | - | Band Model Degrees of Freedom for Peak Flux Spectrum |
| pflx_band_statistic | - | Band Model Statistical Merit Function for Peak Flux Spectrum |
| pflx_sbpl_ampl | photon/cm^2/s/keV | Smoothly Broken Power Law Model Amplitude for Peak Flux Spectrum |
| pflx_sbpl_ampl_pos_err | photon/cm^2/s/keV | SBPL Amplitude Positive Error for Peak Flux Spectrum |
| pflx_sbpl_ampl_neg_err | photon/cm^2/s/keV | SBPL Amplitude Negative Error for Peak Flux Spectrum |
| pflx_sbpl_pivot | keV | Smoothly Broken Power Law Model Pivot Energy for Peak Flux Spectrum |
| pflx_sbpl_pivot_pos_err | keV | SBPL Pivot Energy Positive Error for Peak Flux Spectrum |
| pflx_sbpl_pivot_neg_err | keV | SBPL Pivot Energy Negative Error for Peak Flux Spectrum |
| pflx_sbpl_indx1 | - | Smoothly Broken Power Law Model Index 1 for Peak Flux Spectrum |
| pflx_sbpl_indx1_pos_err | - | SBPL Index 1 Positive Error for Peak Flux Spectrum |
| pflx_sbpl_indx1_neg_err | - | SBPL Index 1 Negative Error for Peak Flux Spectrum |
| pflx_sbpl_brken | keV | Smoothly Broken Power Law Model Break Energy for Peak Flux Spectrum |
| pflx_sbpl_brken_pos_err | keV | SBPL Break Energy Positive Error for Peak Flux Spectrum |
| pflx_sbpl_brken_neg_err | keV | SBPL Break Energy Negative Error for Peak Flux Spectrum |
| pflx_sbpl_brksc | keV | Smoothly Broken Power Law Model Break Scale for Peak Flux Spectrum |
| pflx_sbpl_brksc_pos_err | keV | SBPL Break Scale Positive Error for Peak Flux Spectrum |
| pflx_sbpl_brksc_neg_err | keV | SBPL Break Scale Negative Error for Peak Flux Spectrum |
| pflx_sbpl_indx2 | - | Smoothly Broken Power Law Model Index 2 for Peak Flux Spectrum |
| pflx_sbpl_indx2_pos_err | - | SBPL Index 2 Positive Error for Peak Flux Spectrum |
| pflx_sbpl_indx2_neg_err | - | SBPL Index 2 Negative Error for Peak Flux Spectrum |
| pflx_sbpl_phtflux | photon/cm^2/s | SBPL Photon Flux for Peak Flux Spectrum |
| pflx_sbpl_phtflux_error | photon/cm^2/s | SBPL Photon Flux Error for Peak Flux Spectrum |
| pflx_sbpl_phtflnc | photon/cm^2 | SBPL Photon Fluence for Peak Flux Spectrum |
| pflx_sbpl_phtflnc_error | photon/cm^2 | SBPL Photon Fluence Error for Peak Flux Spectrum |
| pflx_sbpl_ergflux | erg/cm^2/s | SBPL Energy Flux for Peak Flux Spectrum |
| pflx_sbpl_ergflux_error | erg/cm^2/s | SBPL Energy Flux Error for Peak Flux Spectrum |
| pflx_sbpl_ergflnc | erg/cm^2 | SBPL Energy Fluence for Peak Flux Spectrum |
| pflx_sbpl_ergflnc_error | erg/cm^2 | SBPL Energy Fluence Error for Peak Flux Spectrum |
| pflx_sbpl_phtfluxb | photon/cm^2/s | SBPL 50-300 keV (BATSE) Photon Flux for Peak Flux Spectrum |
| pflx_sbpl_phtfluxb_error | photon/cm^2/s | SBPL 50-300 keV (BATSE) Photon Flux Error for Peak Flux Spectrum |
| pflx_sbpl_phtflncb | photon/cm^2 | SBPL 50-300 keV (BATSE) Photon Fluence for Peak Flux Spectrum |
| pflx_sbpl_phtflncb_error | photon/cm^2 | SBPL 50-300 keV (BATSE) Photon Fluence Error for Peak Flux Spectrum |
| pflx_sbpl_ergflncb | erg/cm^2 | SBPL 50-300 keV (BATSE) Energy Fluence for Peak Flux Spectrum |
| pflx_sbpl_ergflncb_error | erg/cm^2 | SBPL 50-300 keV (BATSE) Energy Fluence Error for Peak Flux Spectrum |
| pflx_sbpl_redchisq | - | SBPL Reduced Chi-Squared for Peak Flux Spectrum |
| pflx_sbpl_redfitstat | - | SBPL Reduced Fitting Statistic for Peak Flux Spectrum |
| pflx_sbpl_dof | - | SBPL Degrees of Freedom for Peak Flux Spectrum |
| pflx_sbpl_statistic | - | SBPL Statistical Merit Function for Peak Flux Spectrum |
| pflx_best_fitting_model | - | Peak Flux Spectrum Model Which Best Fits the Data |
| pflx_best_model_redchisq | - | Reduced Chi-Squared for Peak Flux Spectrum Model Which Best Fits the Data |
| flnc_spectrum_start | s | Start Time for Fluence Spectrum Fits Relative to Trigger Time |
| flnc_spectrum_stop | s | End Time for Fluence Spectrum Fits Relative to Trigger Time |
| flnc_plaw_ampl | photon/cm^2/s/keV | Power Law Model Amplitude for Fluence Spectrum |
| flnc_plaw_ampl_pos_err | photon/cm^2/s/keV | Power Law Model Amplitude Positive Error for Fluence Spectrum |
| flnc_plaw_ampl_neg_err | photon/cm^2/s/keV | Power Law Model Amplitude Negative Error for Fluence Spectrum |
| flnc_plaw_pivot | keV | Power Law Model Pivot Energy for Fluence Spectrum |
| flnc_plaw_pivot_pos_err | keV | Power Law Model Pivot Energy Positive Error for Fluence Spectrum |
| flnc_plaw_pivot_neg_err | keV | Power Law Model Pivot Energy Negative Error for Fluence Spectrum |
| flnc_plaw_index | - | Power Law Model Index for Fluence Spectrum |
| flnc_plaw_index_pos_err | - | Power Law Model Index Positive Error for Fluence Spectrum |
| flnc_plaw_index_neg_err | - | Power Law Model Index Negative Error for Fluence Spectrum |
| flnc_plaw_phtflux | photon/cm^2/s | Power Law Model Photon Flux for Fluence Spectrum |
| flnc_plaw_phtflux_error | photon/cm^2/s | Power Law Model Photon Flux Error for Fluence Spectrum |
| flnc_plaw_phtflnc | photon/cm^2 | Power Law Model Photon Fluence for Fluence Spectrum |
| flnc_plaw_phtflnc_error | photon/cm^2 | Power Law Model Photon Fluence Error for Fluence Spectrum |
| flnc_plaw_ergflux | erg/cm^2/s | Power Law Model Energy Flux for Fluence Spectrum |
| flnc_plaw_ergflux_error | erg/cm^2/s | Power Law Model Energy Flux Error for Fluence Spectrum |
| flnc_plaw_ergflnc | erg/cm^2 | Power Law Model Energy Fluence for Fluence Spectrum |
| flnc_plaw_ergflnc_error | erg/cm^2 | Power Law Model Energy Fluence Error for Fluence Spectrum |
| flnc_plaw_phtfluxb | photon/cm^2/s | Power Law Model 50-300 keV (BATSE) Photon Flux for Fluence Spectrum |
| flnc_plaw_phtfluxb_error | photon/cm^2/s | Power Law Model 50-300 keV (BATSE) Photon Flux Error for Fluence Spectrum |
| flnc_plaw_phtflncb | photon/cm^2 | Power Law Model 50-300 keV (BATSE) Photon Fluence for Fluence Spectrum |
| flnc_plaw_phtflncb_error | photon/cm^2 | Power Law Model 50-300 keV (BATSE) Photon Fluence Error for Fluence Spectrum |
| flnc_plaw_ergflncb | erg/cm^2 | Power Law Model 50-300 keV (BATSE) Energy Fluence for Fluence Spectrum |
| flnc_plaw_ergflncb_error | erg/cm^2 | Power Law Model 50-300 keV (BATSE) Energy Fluence Error for Fluence Spectrum |
| flnc_plaw_redchisq | - | Power Law Model Reduced Chi-Squared for Fluence Spectrum |
| flnc_plaw_redfitstat | - | Power Law Model Reduced Fitting Statistic for Fluence Spectrum |
| flnc_plaw_dof | - | Power Law Model Degrees of Freedom for Fluence Spectrum |
| flnc_plaw_statistic | - | Power Law Model Statistical Merit Function for Fluence Spectrum |
| flnc_comp_ampl | photon/cm^2/s/keV | Comptonized Model Amplitude for Fluence Spectrum |
| flnc_comp_ampl_pos_err | photon/cm^2/s/keV | Comptonized Model Amplitude Positive Error for Fluence Spectrum |
| flnc_comp_ampl_neg_err | photon/cm^2/s/keV | Comptonized Model Amplitude Negative Error for Fluence Spectrum |
| flnc_comp_epeak | keV | Comptonized Model Peak Energy for Fluence Spectrum |
| flnc_comp_epeak_pos_err | keV | Comptonized Model Peak Energy Positive Error for Fluence Spectrum |
| flnc_comp_epeak_neg_err | keV | Comptonized Model Peak Energy Negative Error for Fluence Spectrum |
| flnc_comp_index | - | Comptonized Model Index for Fluence Spectrum |
| flnc_comp_index_pos_err | - | Comptonized Model Index Positive Error for Fluence Spectrum |
| flnc_comp_index_neg_err | - | Comptonized Model Index Negative Error for Fluence Spectrum |
| flnc_comp_pivot | keV | Comptonized Model Pivot Energy for Fluence Spectrum |
| flnc_comp_pivot_pos_err | keV | Comptonized Model Pivot Energy Positive Error for Fluence Spectrum |
| flnc_comp_pivot_neg_err | keV | Comptonized Model Pivot Energy Negative Error for Fluence Spectrum |
| flnc_comp_phtflux | photon/cm^2/s | Comptonized Model Photon Flux for Fluence Spectrum |
| flnc_comp_phtflux_error | photon/cm^2/s | Comptonized Model Photon Flux Error for Fluence Spectrum |
| flnc_comp_phtflnc | photon/cm^2 | Comptonized Model Photon Fluence for Fluence Spectrum |
| flnc_comp_phtflnc_error | photon/cm^2 | Comptonized Model Photon Fluence Error for Fluence Spectrum |
| flnc_comp_ergflux | erg/cm^2/s | Comptonized Model Energy Flux for Fluence Spectrum |
| flnc_comp_ergflux_error | erg/cm^2/s | Comptonized Model Energy Flux Error for Fluence Spectrum |
| flnc_comp_ergflnc | erg/cm^2 | Comptonized Model Energy Fluence for Fluence Spectrum |
| flnc_comp_ergflnc_error | erg/cm^2 | Comptonized Model Energy Fluence Error for Fluence Spectrum |
| flnc_comp_phtfluxb | photon/cm^2/s | Comptonized Model 50-300 keV (BATSE) Photon Flux for Fluence Spectrum |
| flnc_comp_phtfluxb_error | photon/cm^2/s | Comptonized Model 50-300 keV (BATSE) Photon Flux Error for Fluence Spectrum |
| flnc_comp_phtflncb | photon/cm^2 | Comptonized Model 50-300 keV (BATSE) Photon Fluence for Fluence Spectrum |
| flnc_comp_phtflncb_error | photon/cm^2 | Comptonized Model 50-300 keV (BATSE) Photon Fluence Error for Fluence Spectrum |
| flnc_comp_ergflncb | erg/cm^2 | Comptonized Model 50-300 keV (BATSE) Energy Fluence for Fluence Spectrum |
| flnc_comp_ergflncb_error | erg/cm^2 | Comptonized Model 50-300 keV (BATSE) Energy Fluence Error for Fluence Spectrum |
| flnc_comp_redchisq | - | Comptonized Model Reduced Chi-Squared for Fluence Spectrum |
| flnc_comp_redfitstat | - | Comptonized Model Reduced Fitting Statistic for Fluence Spectrum |
| flnc_comp_dof | - | Comptonized Model Degrees of Freedom for Fluence Spectrum |
| flnc_comp_statistic | - | Comptonized Model Statistical Merit Function for Fluence Spectrum |
| flnc_band_ampl | photon/cm^2/s/keV | Band Model Amplitude for Fluence Spectrum |
| flnc_band_ampl_pos_err | photon/cm^2/s/keV | Band Model Amplitude Positive Error for Fluence Spectrum |
| flnc_band_ampl_neg_err | photon/cm^2/s/keV | Band Model Amplitude Negative Error for Fluence Spectrum |
| flnc_band_epeak | keV | Band Model Peak Energy for Fluence Spectrum |
| flnc_band_epeak_pos_err | keV | Band Model Peak Energy Positive Error for Fluence Spectrum |
| flnc_band_epeak_neg_err | keV | Band Model Peak Energy Negative Error for Fluence Spectrum |
| flnc_band_alpha | - | Band Model Alpha for Fluence Spectrum |
| flnc_band_alpha_pos_err | - | Band Model Alpha Positive Error for Fluence Spectrum |
| flnc_band_alpha_neg_err | - | Band Model Alpha Negative Error for Fluence Spectrum |
| flnc_band_beta | - | Band Model Beta for Fluence Spectrum |
| flnc_band_beta_pos_err | - | Band Model Beta Positive Error for Fluence Spectrum |
| flnc_band_beta_neg_err | - | Band Model Beta Negative Error for Fluence Spectrum |
| flnc_band_phtflux | photon/cm^2/s | Band Model Photon Flux for Fluence Spectrum |
| flnc_band_phtflux_error | photon/cm^2/s | Band Model Photon Flux Error for Fluence Spectrum |
| flnc_band_phtflnc | photon/cm^2 | Band Model Photon Fluence for Fluence Spectrum |
| flnc_band_phtflnc_error | photon/cm^2 | Band Model Photon Fluence Error for Fluence Spectrum |
| flnc_band_ergflux | erg/cm^2/s | Band Model Energy Flux for Fluence Spectrum |
| flnc_band_ergflux_error | erg/cm^2/s | Band Model Energy Flux Error for Fluence Spectrum |
| flnc_band_ergflnc | erg/cm^2 | Band Model Energy Fluence for Fluence Spectrum |
| flnc_band_ergflnc_error | erg/cm^2 | Band Model Energy Fluence Error for Fluence Spectrum |
| flnc_band_phtfluxb | photon/cm^2/s | Band Model 50-300 keV (BATSE) Photon Flux for Fluence Spectrum |
| flnc_band_phtfluxb_error | photon/cm^2/s | Band Model 50-300 keV (BATSE) Photon Flux Error for Fluence Spectrum |
| flnc_band_phtflncb | photon/cm^2 | Band Model 50-300 keV (BATSE) Photon Fluence for Fluence Spectrum |
| flnc_band_phtflncb_error | photon/cm^2 | Band Model 50-300 keV (BATSE) Photon Fluence Error for Fluence Spectrum |
| flnc_band_ergflncb | erg/cm^2 | Band Model 50-300 keV (BATSE) Energy Fluence for Fluence Spectrum |
| flnc_band_ergflncb_error | erg/cm^2 | Band Model 50-300 keV (BATSE) Energy Fluence Error for Fluence Spectrum |
| flnc_band_redchisq | - | Band Model Reduced Chi-Squared for Fluence Spectrum |
| flnc_band_redfitstat | - | Band Model Reduced Fitting Statistic for Fluence Spectrum |
| flnc_band_dof | - | Band Model Degrees of Freedom for Fluence Spectrum |
| flnc_band_statistic | - | Band Model Statistical Merit Function for Fluence Spectrum |
| flnc_sbpl_ampl | photon/cm^2/s/keV | Smoothly Broken Power Law Model Amplitude for Fluence Spectrum |
| flnc_sbpl_ampl_pos_err | photon/cm^2/s/keV | SBPL Amplitude Positive Error for Fluence Spectrum |
| flnc_sbpl_ampl_neg_err | photon/cm^2/s/keV | SBPL Amplitude Negative Error for Fluence Spectrum |
| flnc_sbpl_pivot | keV | Smoothly Broken Power Law Model Pivot Energy for Fluence Spectrum |
| flnc_sbpl_pivot_pos_err | keV | SBPL Pivot Energy Positive Error for Fluence Spectrum |
| flnc_sbpl_pivot_neg_err | keV | SBPL Pivot Energy Negative Error for Fluence Spectrum |
| flnc_sbpl_indx1 | - | Smoothly Broken Power Law Model Index 1 for Fluence Spectrum |
| flnc_sbpl_indx1_pos_err | - | SBPL Index 1 Positive Error for Fluence Spectrum |
| flnc_sbpl_indx1_neg_err | - | SBPL Index 1 Negative Error for Fluence Spectrum |
| flnc_sbpl_brken | keV | Smoothly Broken Power Law Model Break Energy for Fluence Spectrum |
| flnc_sbpl_brken_pos_err | keV | SBPL Break Energy Positive Error for Fluence Spectrum |
| flnc_sbpl_brken_neg_err | keV | SBPL Break Energy Negative Error for Fluence Spectrum |
| flnc_sbpl_brksc | keV | Smoothly Broken Power Law Model Break Scale for Fluence Spectrum |
| flnc_sbpl_brksc_pos_err | keV | SBPL Break Scale Positive Error for Fluence Spectrum |
| flnc_sbpl_brksc_neg_err | keV | SBPL Break Scale Negative Error for Fluence Spectrum |
| flnc_sbpl_indx2 | - | Smoothly Broken Power Law Model Index 2 for Fluence Spectrum |
| flnc_sbpl_indx2_pos_err | - | SBPL Index 2 Positive Error for Fluence Spectrum |
| flnc_sbpl_indx2_neg_err | - | SBPL Index 2 Negative Error for Fluence Spectrum |
| flnc_sbpl_phtflux | photon/cm^2/s | SBPL Photon Flux for Fluence Spectrum |
| flnc_sbpl_phtflux_error | photon/cm^2/s | SBPL Photon Flux Error for Fluence Spectrum |
| flnc_sbpl_phtflnc | photon/cm^2 | SBPL Photon Fluence for Fluence Spectrum |
| flnc_sbpl_phtflnc_error | photon/cm^2 | SBPL Photon Fluence Error for Fluence Spectrum |
| flnc_sbpl_ergflux | erg/cm^2/s | SBPL Energy Flux for Fluence Spectrum |
| flnc_sbpl_ergflux_error | erg/cm^2/s | SBPL Energy Flux Error for Fluence Spectrum |
| flnc_sbpl_ergflnc | erg/cm^2 | SBPL Energy Fluence for Fluence Spectrum |
| flnc_sbpl_ergflnc_error | erg/cm^2 | SBPL Energy Fluence Error for Fluence Spectrum |
| flnc_sbpl_phtfluxb | photon/cm^2/s | SBPL 50-300 keV (BATSE) Photon Flux for Fluence Spectrum |
| flnc_sbpl_phtfluxb_error | photon/cm^2/s | SBPL 50-300 keV (BATSE) Photon Flux Error for Fluence Spectrum |
| flnc_sbpl_phtflncb | photon/cm^2 | SBPL 50-300 keV (BATSE) Photon Fluence for Fluence Spectrum |
| flnc_sbpl_phtflncb_error | photon/cm^2 | SBPL 50-300 keV (BATSE) Photon Fluence Error for Fluence Spectrum |
| flnc_sbpl_ergflncb | erg/cm^2 | SBPL 50-300 keV (BATSE) Energy Fluence for Fluence Spectrum |
| flnc_sbpl_ergflncb_error | erg/cm^2 | SBPL 50-300 keV (BATSE) Energy Fluence Error for Fluence Spectrum |
| flnc_sbpl_redchisq | - | SBPL Reduced Chi-Squared for Fluence Spectrum |
| flnc_sbpl_redfitstat | - | SBPL Reduced Fitting Statistic for Fluence Spectrum |
| flnc_sbpl_dof | - | SBPL Degrees of Freedom for Fluence Spectrum |
| flnc_sbpl_statistic | - | SBPL Statistical Merit Function for Fluence Spectrum |
| flnc_best_fitting_model | - | Fluence Spectrum Model Which Best Fits the Data |
| flnc_best_model_redchisq | - | Reduced Chi-Squared for Fluence Spectrum Model Which Best Fits the Data |
| bcatalog | - | Catalog Version of the Burst Catalog Entry File |
| scatalog | - | Catalog Version of the Spectral Catalog Entry File |
| last_modified | mjd | Last Modified Time |
