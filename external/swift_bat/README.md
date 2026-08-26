# Swift/BAT GRB 目录（swift_bat）

- **目录名称**：The Swift/BAT Gamma-Ray Burst Catalog（在线版，基于第三版 BAT GRB 目录，Lien et al. 2016, ApJ, 829, 7，并持续更新）
- **主页 URL**：https://swift.gsfc.nasa.gov/results/batgrbcat/
- **汇总表索引页**：https://swift.gsfc.nasa.gov/results/batgrbcat/index_tables.html
- **数据下载根目录**：https://swift.gsfc.nasa.gov/results/batgrbcat/summary_cflux/ （"Download all tables" 即指向该目录列表，无打包文件，需逐文件下载）
- **获取日期**：2026-07-21
- **获取方式**：`wget -r -np -nH --cut-dirs=3 -R "index.html*" https://swift.gsfc.nasa.gov/results/batgrbcat/summary_cflux/`，原样镜像，未修改任何文件内容。

注意：HEASARC FTP 镜像 `https://heasarc.gsfc.nasa.gov/FTP/swift/results/batgrbcat/` 已 404（不存在），官方数据以 swift.gsfc.nasa.gov 上述目录为准。HEASARC W3Browse 另有 `swiftbatgrb` 表，但本目录的在线版更新更及时、列更全。

## 数据规模与核对

- 快照覆盖 **GRB 041217（2004-12-17）至 GRB 250605A（2025-06-05）**。
- 主表 `summary_general.txt` 共 **1668 个爆发数据行**（全文件 1691 行，其余为 `#` 表头），与主页逐暴网页列表的 1668 个 "Webpage" 条目**完全一致**。
- 全目录共 65 个文件，约 15 MB。

## 文件清单

所有表均为**管道符 `|` 分隔的 ASCII 文本**，表头为 `#` 开头的多行注释（含官方逐列英文说明），数据行以 `|` 分列。

### summary_general_info/（一般信息）
| 文件 | 数据行数 | 内容 |
|---|---|---|
| `summary_general.txt` | 1668 | 主表：名称、触发 ID、触发时间、坐标、T90/T50、事件数据范围等 |
| `summary_burst_durations.txt` | 1667 | T100/T90/T50/1s 峰的起止时间（相对触发时刻） |
| `summary_trigger_index.txt` | 1549 | 触发判据编号、触发能段、入射角等（仅 rate/image 触发的暴） |
| `GRBlist_redshift_BAT.txt` | 531 | BAT GRB 红移列表（含测定方法与文献） |
| `summary_general_copy.txt` | ~1260 | ⚠️ 服务器遗留的旧版副本，**勿用** |

### summary_T100/、summary_1s_peak/、summary_20ms_peak/（能谱分析，三个时段各一套）
每个目录 9 个文件（T100 时段各表均 1668 数据行；1s/20ms 峰行数相近）：

| 文件 | 内容 |
|---|---|
| `best_model.txt` | 最佳拟合模型：PL（简单幂律）或 CPL（截断幂律），N/A 表示不适用 |
| `summary_pow_parameters.txt` | 简单幂律（PL）拟合参数：光子指数 alpha、归一化等 |
| `summary_cutpow_parameters.txt` | 截断幂律（CPL）拟合参数：alpha、**Epeak**、归一化等 |
| `summary_pow_photon_flux.txt` / `summary_cutpow_photon_flux.txt` | 分能段光子流量 |
| `summary_pow_energy_flux.txt` / `summary_cutpow_energy_flux.txt` | 分能段能量流量 |
| `summary_pow_energy_fluence.txt` / `summary_cutpow_energy_fluence.txt` | 分能段能量流量积分（**fluence**） |

⚠️ `summary_1s_peak/` 下有两个遗留副本：`summary_cutpow_energy_flux_20220519.txt`、`summary_pow_energy_flux_copy20220519.txt`，与正式文件**不同**（旧快照），**勿用**。

### summary_GRBlist/（33 个特殊注释列表）
纯文本小列表（`GRBname trigid` 两列），标记各类特殊情况，如：`GRBlist_short_GRB_with_EE.txt`（带延展辐射的短暴）、`GRBlist_possible_GRB.txt`、`T100_might_be_lower_limits.txt`、`Data_gap_in_T100.txt`、`GRBlist_no_spec_analysis.txt`、`spectral_analysis_failed.txt` 等。用于质量筛选。

## 逐列文档

### 1. summary_general.txt（主表）

| 列 | 含义 | 单位/备注 |
|---|---|---|
| GRBname | GRB 名称 | 格式 `GRB yymmddx`；早期无字母后缀（如 `GRB041217`） |
| Trig_ID | BAT 触发编号 | 事件数据 obsID 为 `00<Trig_ID>000`；地面分析发现的暴用失败事件数据的触发 ID 或完整 obsID |
| Trig_time_met | 触发时间（Swift MET） | s |
| Trig_time_UTC | 触发时间（UTC） | ISO 格式 |
| RA_ground / DEC_ground | BAT 精化位置（J2000） | deg；**有坐标** |
| Image_position_err | BAT 位置误差 | arcmin |
| Image_SNR | BAT 图像探测信噪比 | — |
| **T90 / T90_err** | 爆发时长 T90 及误差 | s；**观测系**，由 15–350 keV 掩模加权光变（battblocks）测得（依据 Lien et al. 2016；表头未注明误差置信水平） |
| T50 / T50_err | 爆发时长 T50 及误差 | s；同上（⚠️ 表头注释把 T50 误写成 "Burst duration T90"，是官方笔误） |
| Evt_start_sincetrig / Evt_stop_sincetrig | 事件数据起止（相对触发时刻） | s |
| pcode | 部分编码因子 | 0–1（个别行 >1，如 1.0156，为已知现象） |
| Trigger_method | 触发方式 | rate trigger / image trigger / ground detected / ground detected during slew |
| XRT_detection | 是否有 XRT 探测 | Yes/No |
| comment | 特殊注释 | 多为空 |

### 2. summary_burst_durations.txt
GRBname, Trig_ID, Trig_time_met, T100_start/stop, T90_start/stop, T50_start/stop, 1s_peak_start/stop —— 均为相对触发时刻的秒数（观测系）。T100 = T90 区间两端外推至 0%/100% 流量的总时长。

### 3. summary_trigger_index.txt
trigger_index（触发判据编号，image 触发为 20000）、energy_band（**触发能段**，如 `25-100 keV`、`50-350 keV`、`15-50 keV`，因暴而异）、foreground/background_exposure（s）、theta/phi（入射角，deg）、imx/imy（探测器平面坐标）。

### 4. GRBlist_redshift_BAT.txt
GRBname, z, Method（ba=吸收线光谱 / he=宿主星系光谱 / bp=测光 / hp=宿主测光）, Uncertainty（主要为测光红移；**各文献置信区间不统一**）, Ref.（GCN 文献，`*` 标记取值来源）。⚠️ 该表按红移测量排序、非时间排序。

### 5. 能谱参数表（summary_{T100,1s_peak,20ms_peak}/）

**best_model.txt**：GRBname, Trig_ID, 最佳模型（PL / CPL / N/A）。

**summary_pow_parameters.txt（PL 模型）**：
- 模型：`f = norm * (E/enorm)^alpha`，`enorm` 固定为 **50 keV**。
- alpha（光子指数，注意符号约定见下）、alpha_low/hi（**90% 置信区间**上下限）、norm（photons/cm²/s/keV）、norm_low/hi（90% 置信）、chi2、dof、reduced_chi2、null_prob（XSPEC 输出）、Exposure_time（s）、Spectrum_start/stop（相对触发时刻，s）、comment。

**summary_cutpow_parameters.txt（CPL 模型）**：
- 模型：`f = norm * (E/enorm)^alpha * exp(-E*(2+alpha)/Epeak)`，`enorm` 固定 50 keV。
- 多出 **Epeak**（keV，**观测系峰值能量**）及 Epeak_low/hi（**90% 置信**）；其余列同上。
- ⚠️ 表头注释把 norm 描述写了两遍、enorm 拼成 "enrom"，为官方笔误。

**fluence / flux / photon_flux 表（pow 与 cutpow 各一套）**：
- 分能段列：`15_25kev, 25_50kev, 50_100kev, 100_150kev, 100_350kev, 15_150kev, 15_350kev`，每个能段三列（值、`_low`、`_hi`，**90% 置信**）。
- 单位：energy_fluence = **erg/cm²**；energy_flux = erg/cm²/s；photon_flux = photons/cm²/s。
- **能段均为观测系（observer frame）**；常用总能段为 15–150 keV 和 15–350 keV。
- 后附 Exposure_time、Spectrum_start/stop、comment。

## 关键参数可用性小结

- **T90**：✅（`summary_general.txt`，观测系，15–350 keV 光变）
- **Epeak**：✅（`summary_cutpow_parameters.txt`，CPL 模型，观测系，90% 置信；无 Band 模型拟合）
- **fluence**：✅（`summary_{pow,cutpow}_energy_fluence.txt`，7 个观测系能段）
- **Eiso**：❌ 目录不直接提供；有红移表（531 个 z）+ fluence，可自行推算。

## 已发现的坑（重要）

1. **缺失值记号为字符串 `N/A`**（坐标、误差、整行拟合结果均可能出现），不是空值或 NaN；解析时需显式处理。主表含 N/A 的行约 71 行。
2. **90% vs 1σ**：能谱拟合所有 `_low/_hi` 误差均为 **90% 置信区间**，不是 1σ；T90/T50 误差的置信水平表头未注明。红移表 Uncertainty 各文献置信区间不统一。
3. **多行 `#` 表头 + `|` 分隔**：跳过所有 `#` 行后按 `|` split，注意行尾可能有多余的 `|` 产生空列。
4. **观测系 vs 静止系**：所有能段、Epeak、T90 均为**观测系**，未做 (1+z) 修正。
5. **CPL 拟合的 Epeak 可能打边界**：Epeak ≈ 9999–10000 keV 或 low/hi = 0 表示拟合未约束（打到参数边界），应视为无效约束；best_model.txt 为 N/A 的行表示该时段无可用拟合。
6. **fluence=1.0 陷阱**：表头注明 XSPEC 原始输出为 log10(flux)，**数值 1.0 实际表示 log10(flux)=0.0 的拟合失败/占位情况**，不能直接当物理量用。
7. **幂律指数符号约定**：数据产品文件夹内 `*.log` 用 XSPEC 约定 E^(-alpha)，而汇总表和论文用 E^(alpha)，两者**符号相反**；混用数据产品目录的 log 时注意。
8. **遗留副本文件**：`summary_general_copy.txt`、`summary_1s_peak/*_20220519.txt`、`*_copy20220519.txt` 是旧快照，与正式文件内容不同，务必用无后缀的正式文件。
9. **无 Band 模型**：只有 PL 和 CPL 两种模型，Epeak 仅在 CPL 下给出（CPL 的 Epeak 与 Band 的 Epeak 定义不同，跨目录对比时注意）。
10. **GRB 041219A 的 Trig_ID 为 N/A**（用 obsID 分析），联表时建议以 GRBname 为主键、Trig_ID 为辅。
11. T90 对个别暴可能是下限或受数据缺口影响，见 `summary_GRBlist/T100_might_be_lower_limits.txt`、`Data_gap_in_T100.txt` 等列表。
12. 该在线目录持续更新，本快照截至 GRB 250605A；后续复采会得到更多行。
