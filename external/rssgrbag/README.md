# 射电遴选 GRB 余辉目录（HEASARC `rssgrbag`）

- **目录名称**：Radio-Selected Gamma-Ray Burst Afterglow Catalog（HEASARC 表名 `rssgrbag`）
- **来源文献**：Chandra P. & Frail D. A. 2012, ApJ, 746, 156（Bibcode `2012ApJ...746..156C`）；HEASARC 于 2013-11 基于 CDS 目录 `J/ApJ/746/156` 的 `table1.dat`（主表）与 `table4.dat`（射电峰值）建表。
- **主页 URL**：https://heasarc.gsfc.nasa.gov/W3Browse/gamma-ray-bursts/rssgrbag.html
- **数据下载 URL**（HEASARC 官方 FTP-over-HTTP 镜像，gzip 压缩 tdat）：
  - 数据：https://heasarc.gsfc.nasa.gov/FTP/heasarc/dbase/tdat_files/heasarc_rssgrbag.tdat.gz
  - 表头：https://heasarc.gsfc.nasa.gov/FTP/heasarc/dbase/tdat_headers/heasarc_rssgrbag.hdr.gz
  - CDS 交叉校验用（补充下载）：https://cdsarc.cds.unistra.fr/ftp/J/ApJ/746/156/table4.dat 及同目录 `ReadMe`
- **获取日期**：2026-07-22（tdat 文件本身为 HEASARC 2022-02-06 导出版本；表创建 2020-07-23，最后修改 2022-02-05）
- **文件状态**：原始下载文件，内容未做任何修改。

## 样本概况

304 个 GRB（1997-01 至 2011-01，外加 2011-04-28 的 Fermi 暴 GRB 110428A），均曾被射电望远镜跟踪：270 个 VLA、15 个 EVLA、19 个 ATCA。其中 95 个有射电余辉探测（`radio_ag_flag=Y`，另有 3 个 `Y?` 未确认）；63 个有完整射电光变曲线（单频段 ≥3 次探测），作者用前向激波公式拟合峰值流量密度与峰时；其余探测源的峰值直接取自数据（无拟合误差）。原文共汇编 2,995 次流量密度测量（含上限），但这些逐历元测量**未以机器可读形式发表**（CDS 仅提供 table1/table4 两个文件）——详见"已知坑"第 1 条。

## 文件清单与格式

| 文件 | 大小 | 说明 | 数据行数（实测） |
|---|---|---|---|
| `heasarc_rssgrbag.tdat.gz` | 19,910 B | 主表（每行一个 GRB，含余辉探测标志、T90、红移、fluence、Eiso、11h X 射线/光学流量、喷流拐折参数、6 个频段的射电峰值） | **304** |
| `heasarc_rssgrbag.hdr.gz` | 2,103 B | 列定义/单位/格式（tdat 表头，`TOTAL ROWS: 304`） | — |
| `table4.dat` | 6,160 B | CDS 原版峰值表（固定宽度，140 行），用于交叉校验 | **140** |
| `ReadMe` | 11,514 B | CDS 目录说明（table1/table4 逐字节格式、标志含义、参考文献码表） | — |
| `normalized.jsonl` | — | 解析输出，每行一个 GRB（契约见 `../SCHEMA.md`） | **304** |
| `lightcurve.jsonl` | — | 解析输出，每行一个射电峰值测光点 | **140** |

tdat 为管道符（`|`）分隔 ASCII：开头 `<HEADER>` 元数据块、结尾 `<END>`，每行末尾有尾置 `|`（按 `|` 分割得 75 个字段，丢弃最后一个空字段后为 74 列）。实测行数命令：`zcat heasarc_rssgrbag.tdat.gz | grep -cE '^GRB'`，与表头 `TOTAL ROWS: 304` 一致。

## 逐列文档（74 列）

缺失值为**空字符串**（两个相邻 `|`），无 `NULL`/`NaN` 记号。坐标为 J2000。误差列除注明外均为拟合 1σ。

| # | 列名 | 含义 | 单位 | 备注 |
|---|---|---|---|---|
| 1 | name | 暴名 `GRB YYMMDD[A-Z]` | — | **唯一主键**（304 行无重复，全部匹配 `^GRB \d{6}[A-Z]?$`） |
| 2 | source_flag | 源注释码 | — | `m`=双喷流拐折；`n`=SN/GRB 成协（20 行）；`o`=短硬暴 SHB（33）；`p`=X 射线闪 XRF（15）；`q`=银河暂现源？（1）；`r`=另被 WSRT 观测（1，HEASARC 注明此值本应放在 radio_telescope_flag）；可组合（如 `m,n`、`n,p`）；229 行为空 |
| 3 | instrument_code | 发现仪器码 | — | `A`=ASM，`B`=BeppoSAX，`F`=Fermi，`H`=HETE，`I`=INTEGRAL，`P`=PCA，`S`=Swift，`sA`=superAGILE，`T`=IPN 三角定位；可多值逗号分隔（如 `S, T` 49 行） |
| 4–5 | ra / dec | 赤经 / 赤纬（J2000） | deg | 1997–2001 年暴精度 0.1 s/1″，2002–2011 年 0.01 s/0.1″（GRB 031111、090328、090902B 例外） |
| 6–7 | lii / bii | 银经 / 银纬 | deg | |
| 8–10 | xray_ag_flag / opt_ag_flag / radio_ag_flag | X 射线/光学/射电余辉探测标志 | — | `Y`=探测，`N`=未探测，`X`=未观测，`Y?`=观测了但探测未确认；射电：Y=95、N=206、Y?=3 |
| 11 | radio_telescope | 主射电望远镜 | — | VLA=270、ATCA=19、EVLA=15 |
| 12 | radio_telescope_flag | 附加射电望远镜码 | — | `l`=WSRT+VLBA+Ryle+ATCA+GMRT 全套，`r`=WSRT，`s`=VLBA，`t`=Ryle，`u`=ATCA，`v`=GMRT；可组合；242 行为空 |
| 13 | t90 | T90 持续时间（观测系） | s | **能段为各发现探测器自身的能段**（如 Swift 为 15–350 keV），表中不给逐源能段；缺 5 行 |
| 14–16 | redshift_limit / redshift / redshift_max | 红移及限值 | — | limit=`<` 表示上限（9 行）；redshift_max 非空时（2 行）redshift 为区间**下限**；缺 148 行 |
| 17 | fluence_15_150_kev | 15–150 keV 流量 fluence（观测系） | erg/cm² | 非 Swift 暴的 fluence 由 Nysewander et al. 2009 方法外推到该能段；缺 6 行 |
| 18 | iso_bol_energy | k 改正热动学各向同性能量 Eiso，**静止系 1–10000 keV** | erg | 缺 160 行（依赖红移） |
| 19–20 | xray_flux_11h_limit / xray_flux_11h | 暴后 11 h X 射线流量 | erg/s/cm² | 能段 0.3–10 keV；**BeppoSAX 暴（instrument_code=B）为 1.6–10 keV** |
| 21–22 | opt_flux_11h_limit / opt_flux_11h | 暴后 11 h 光学 R 波段（0.7 µm）流量密度 | µJy | |
| 23–25 | jet_break_time_limit / jet_break_time / jet_break_time_flag | 喷流拐折时间 t_j（观测系） | d | limit `<`/`>`；flag=`?` 表示拐折时间不确定 |
| 26–27 | cbm_number_density / cbm_number_density_flag | 星周介质数密度 n | cm⁻³ | flag=`i` 表示未测定、**假定 n=1 cm⁻³** |
| 28–29 | coll_angle_limit / coll_angle | 喷流准直半角 θ_j | deg | 由 t_j 按 Frail et al. 2001 / Bloom et al. 2003 估算 |
| 30–31 | true_bol_energy_limit / true_bol_energy | 准直改正能量 E_γ（beaming-corrected） | erg | 即 Ghirlanda 关系的 E_gamma |
| 32 | ref_codes | 参考文献码 | — | 顺序固定：T90, z, fluence, Eiso, F_X(11h), F_R(11h), t_j, n；`[]` = 对应量为空，或该值由本文作者据 GCN 通报自行估计；数字码对照见 CDS `refs.dat`/主页（26=GCN 通报等） |
| 33–39 | radio_freq_1 … rf_peak_time_1_error | 第 1（最低）频段峰值 | 见下 | 7 列一组：频率 / 峰值流量密度 / 误差 / 峰时 t_m / 误差 / 静止系峰时 t_m/(1+z) / 误差 |
| 40–46 | …_2 | 第 2 频段 | 同上 | |
| 47–53 | …_3 | 第 3 频段 | 同上 | |
| 54–60 | …_4 | 第 4 频段 | 同上 | |
| 61–67 | …_5 | 第 5 频段 | 同上 | |
| 68–74 | radio_freq_6 … rf_peak_time_6_error | 第 6（最高）频段 | 同上 | 仅 GRB 030329 用满 6 个频段 |

**射电峰值列组（每频段 7 列）单位与约定**：

- `radio_freq_k`：GHz。取值分布：8.46 GHz 66 点、4.86 GHz 34 点、22.5 GHz 11 点、15 GHz 8 点、1.43 GHz 7 点，其余零星（8.7/4.8/4.5/7.9/4.9/2.5/1.38/43/33.6/8.64 GHz）。
- `peak_flux_freq_k[_error]`：**µJy**（int4/int2）。
- `peak_time_k[_error]`：暴后天数（**观测系**）；`rf_peak_time_k[_error]`：静止系 t_m/(1+z)，仅红移已知时给出。
- 有误差 = 前向激波公式拟合（63 个有光变曲线的源）；无误差 = 峰值直接取自数据（53/140 点无流量误差）。
- 全部 140 点均为**探测**（无上限点）；未探测源在此表中根本没有峰值列。

## 爆发标识

- 唯一标识是 `name`（无重复）；格式 `GRB yymmdd` 或 `GRB yymmddX`（当日多暴加字母后缀，如 `GRB 021004`、`GRB 050509C`、`GRB 071112B`），规范化时原样保留。
- 表中**无触发时刻**（连日期时刻都没有），`trigger_time` 一律缺失，匹配合并时只能用 name + 坐标。

## normalized.jsonl 字段映射

- `params.t90`：`{"v": s, "err": null, "band": null}`（能段逐源而异且未列表，故 band=null）。
- `params.redshift`：`{"v": z}`，附 `"limit": "<"` 或 `"v_max"`（区间上限）。
- `params.fluence`：`{"v": erg/cm², "err": null, "band": "15-150 keV"}`（观测系；非 Swift 暴为外推值）。
- `params.eiso`：`{"v": erg, "err": null, "band": "1-10000 keV", "frame": "rest"}`。
- `params.e_gamma`：`{"v": erg, "err": null, "frame": "rest"}`（true_bol_energy，附 limit）。
- `other`：source_flag、instrument_code、三个余辉探测标志、radio_telescope(_flag)、xray_flux_11h（带 unit/band，BeppoSAX 源标注 1.6–10 keV）、opt_flux_11h、jet_break_time（带 limit/uncertain）、cbm_number_density（带 assumed 标记）、coll_angle、ref_codes、radio_peaks（峰值数组原样保留，µJy/天单位不换算）。

## lightcurve.jsonl 字段

每行一个射电峰值点：`name, ra, dec, time`（峰时，暴后**秒**，观测系，由天×86400 换算）、`time_err`（秒）、`band`（如 `"8.46GHz"`）、`flux_mJy`（µJy÷1000）、`flux_err_mJy`、`upperlimit`（恒 false，均为探测）、`reference`（恒为 Chandra & Frail 2012）、`telescope`（主望远镜）、`method`（`fit`=激波公式拟合，有误差；`data`=直接取自数据，无误差）。

## 已知坑 / 注意事项

1. **没有逐历元光变数据**：论文汇编的 2,995 次流量密度测量（含上限）未机器可读发表，CDS/HEASARC 只有主表+峰值表。`lightcurve.jsonl` 每源每频段只有 1 个峰值点，**不是真正的多历元光变曲线**；要逐点数据只能回论文/GCN 原文。
2. 峰值点中 53/140 无流量/峰时误差（直接取自数据而非拟合），用 `method` 字段区分；无误差≠精确。
3. T90 能段不统一（各发现探测器自身能段），跨目录比较时不能与 BATSE 50–300 keV、Swift 15–350 keV 等混用而不加说明。
4. fluence 统一在 15–150 keV，但非 Swift 暴是从其他能段**外推**的（Nysewander et al. 2009 方法），系统误差不明。
5. xray_flux_11h 能段对 BeppoSAX 源是 1.6–10 keV，其余 0.3–10 keV。
6. 红移有 9 个上限（`<`）、2 个区间值（redshift 为下限、redshift_max 为上限）；148/304 无红移，Eiso/E_gamma/静止系峰时随之缺失。
7. source_flag 的 `r`（GRB 090423）是原表笔误，含义实为"另被 WSRT 观测"，与 radio_telescope_flag 的 `r` 同义。
8. cbm_number_density_flag=`i` 的密度是**假定值** 1 cm⁻³，不是测量值。
9. 样本为**射电跟踪样本**（不是射电探测样本）：206/304 射电未探测，做统计时注意选择效应；射电探测率约 31%。
10. 时间基准：峰时相对于"暴"（burst）时刻，但表中没有触发时刻列，如需绝对时间需外部目录补 trigger_time。

## 校验和（SHA-256）

```
ed83dcd32dea8e4b3e1bd7fd92db8ab638be4d8398be4f2bd46698ff3dd27c9a  heasarc_rssgrbag.tdat.gz
c90cc747f3c31ad293d7b1ff85746f9aa94835811b2da5ed6340f75bc64b8e92  heasarc_rssgrbag.hdr.gz
ca3509b4ae3d1384ca39ed2770834f8d47860ce7a6b5180906b48d13f185d847  table4.dat
5f329bb98e7eb406e2b8aa2ccab06ee26af01eb8771221041877352de2a062a5  ReadMe
```

## 解析与验证

`parse.py`（用 burst_advocate 环境 Python 运行）读 `heasarc_rssgrbag.tdat.gz`，生成 `normalized.jsonl`（304 行）与 `lightcurve.jsonl`（140 行）。已验证：lightcurve 的 140 个点与 CDS `table4.dat` 逐点一致（name/频率/峰值流量/峰时多重集合相等）；抽 GRB 990510、GRB 980425、GRB 110428A 与原始 tdat 行对照 ra/dec/t90/z/fluence/eiso 全部一致。
