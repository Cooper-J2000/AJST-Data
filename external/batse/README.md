# BATSE GRB 目录（HEASARC `batsegrb`）

- **目录名称**：CGRO/BATSE Gamma-Ray Burst Catalog（HEASARC 表名 `batsegrb`）
- **主页 URL**：https://heasarc.gsfc.nasa.gov/w3browse/all/batsegrb.html
- **数据下载 URL**（HEASARC 官方 FTP-over-HTTP 镜像，gzip 压缩 tdat）：
  - 主表数据：https://heasarc.gsfc.nasa.gov/FTP/heasarc/dbase/tdat_files/heasarc_batsegrb.tdat.gz
  - 主表表头：https://heasarc.gsfc.nasa.gov/FTP/heasarc/dbase/tdat_headers/heasarc_batsegrb.hdr.gz
  - 能谱表数据（补充）：https://heasarc.gsfc.nasa.gov/FTP/heasarc/dbase/tdat_files/heasarc_batsegrbsp.tdat.gz
  - 能谱表表头（补充）：https://heasarc.gsfc.nasa.gov/FTP/heasarc/dbase/tdat_headers/heasarc_batsegrbsp.hdr.gz
- **获取日期**：2026-07-21（数据文件本身为 HEASARC 2022-02-03 导出版本）
- **文件状态**：原始下载文件，内容未做任何修改。

## 文件清单与格式

| 文件 | 大小 | 说明 | 数据行数（实测） |
|---|---|---|---|
| `heasarc_batsegrb.tdat.gz` | 328,248 B | BATSE GRB 主目录（触发、位置、T50/T90、峰值流量、四通道 fluence、注释） | **2702** |
| `heasarc_batsegrb.hdr.gz` | 1,774 B | 主表列定义/单位/格式（tdat 表头） | — |
| `heasarc_batsegrbsp.tdat.gz` | 28,766 B | 补充：BATSE Complete Spectral Catalog of Bright GRBs（`batsegrbsp`，350 个亮 GRB 的时间积分能谱拟合参数，**含 Epeak**） | **350** |
| `heasarc_batsegrbsp.hdr.gz` | 1,407 B | 能谱表列定义 | — |

tdat 是 HEASARC 的管道符（`|`）分隔 ASCII 格式：文件开头有一段 `<HEADER> ... <DATA>` 元数据块，之后每行一条记录，文件以 `<END>` 结束。实测行数命令：`zcat heasarc_batsegrb.tdat.gz | grep -cE '^[0-9]+\|'`。

**行数核对**：实测 2702 行，与表头内 `TOTAL ROWS: 2702` 及 BATSE 现行目录（MSFC "current catalog"）公认的 2702 个 GRB 一致。能谱表实测 350 行，与其表头 `TOTAL ROWS: 350` 一致。

## 主表 `heasarc_batsegrb.tdat.gz` 逐列文档

共 47 列（每行末尾有尾置 `|`，按 `|` 分割会得到第 48 个空字段，解析时注意丢弃）。缺失值为**空字符串**（两个相邻 `|`），无 `NULL`/`NaN` 记号。

| # | 列名 | 含义 | 单位 | 备注 |
|---|---|---|---|---|
| 1 | trigger_num | BATSE 触发编号（105–8121） | — | **唯一主键** |
| 2 | name | 爆发名称（见"爆发标识"节） | — | 不唯一！ |
| 3 | ra | 赤经（J2000） | deg | |
| 4 | dec | 赤纬（J2000） | deg | |
| 5 | lii | 银经 | deg | |
| 6 | bii | 银纬 | deg | |
| 7 | day_trigger | 触发日的截断儒略日 TJD | d | TJD = JD − 2440000.5 |
| 8 | time | 触发时刻 | MJD | 与 day_trigger+seconds_trigger 冗余 |
| 9 | seconds_trigger | 当日 UT 秒数 | s | |
| 10 | error_radius | 位置误差圆半径 | deg | BATSE 定位误差含统计+系统项，典型几度 |
| 11 | earth_angle | 爆发方向与卫星星下点（地心方向）夹角 | deg | |
| 12 | overwrite | 该爆发是否覆盖了一个更早更弱的触发（Y/N） | — | 117 行为 Y |
| 13 | overwritten | 该触发是否被之后更强的触发覆盖（Y/N） | — | 75 行为 Y |
| 14–18 | max_cts_64 / threshold_64 / flux_64 / flux_64_error / flux_64_time | 64 ms 时标：峰值计数与阈值之比、触发阈值、**峰值流量**及其误差、峰时刻 | photon/cm²/s | 流量能段 **50–300 keV**（与星上触发能段一致）；误差为 **1σ 统计误差**；flux_64_time 为该 64 ms 区间**末端**相对触发时刻的秒数 |
| 19–23 | *_256 | 同上，256 ms 时标 | 同上 | |
| 24–28 | *_1024 | 同上，1024 ms 时标 | 同上 | |
| 29 | t50 | T50 持续时间（25%–75% 计数间隔） | s | 见下方能量范围说明 |
| 30–31 | t50_error / t50_start | T50 误差（1σ）/ T50 起点（相对触发） | s | |
| 32 | t90 | **T90 持续时间**（5%–95% 计数间隔） | s | 见下方能量范围说明 |
| 33–34 | t90_error / t90_start | T90 误差（1σ）/ T90 起点（相对触发） | s | |
| 35–36 | fluence_1 / fluence_1_error | 通道 1 fluence，**20–50 keV** | erg/cm² | 误差 1σ |
| 37–38 | fluence_2 / fluence_2_error | 通道 2 fluence，**50–100 keV** | erg/cm² | |
| 39–40 | fluence_3 / fluence_3_error | 通道 3 fluence，**100–300 keV** | erg/cm² | |
| 41–42 | fluence_4 / fluence_4_error | 通道 4 fluence，**E > 300 keV（积分通道）** | erg/cm² | 对假设能谱形状敏感，官方不建议用于精细能谱分析 |
| 43–47 | comments_quality / comments_otherobs / comments_general / comments_position / comments_duration | 数据质量/其他仪器/一般/位置/持续时间注释（自由文本） | — | 多数为空 |

**能量范围 / 参考系 / 误差约定（重点）**：

- 峰值流量能段固定为 **50–300 keV**；fluence 分四个通道（20–50 / 50–100 / 100–300 / >300 keV）。与 Swift/BAT 的 15–150 keV、Fermi/GBM 的 50–300 keV（峰流常用 10–1000 keV 拟合）不可直接混用，做跨目录比较时需注明。
- T50/T90 按主页文档，用**满足触发条件的探测器、四个 LAD 甄别通道求和**后的计数计算（即大致全 LAD 能量范围，而非仅 50–300 keV）。
- 所有量均为**观测系（observer frame）**；BATSE 时代无红移，库中不存在 rest-frame 量，T90 等未做任何 (1+z) 改正。
- 所有误差列均为 **1σ 统计误差**（主页明确说明），不是 90% 置信。
- 主表**不含 Epeak、不含能谱模型参数、不含 Eiso**。Eiso 需要 fluence（通常取通道 2+3，即 50–300 keV）结合红移自行计算，本目录不提供。

## 能谱表 `heasarc_batsegrbsp.tdat.gz`（补充，含 Epeak）

来源：BATSE Complete Spectral Catalog of Bright GRBs（Kaneko et al. 2006, ApJS 166, 298 一脉），350 个亮 GRB 的时间积分能谱。共 31 列，关键列：

| 列名 | 含义 | 单位/备注 |
|---|---|---|
| trigger_num / name | 触发编号 / 名称（`GRB yymmdd` 格式） | 可与主表 join（用 trigger_num） |
| ra / dec / lii / bii / error_radius / time / seconds_trigger | 位置与触发时刻 | deg / MJD / s |
| lad_data_type / lad_number | 所用 LAD 数据类型与探测器号 | 如 HERB |
| start_spectrum / end_spectrum | 能谱积分区间（相对触发） | s |
| lower_energy / upper_energy | 拟合能段（各源不同，约 30–2000 keV） | keV |
| num_spectra | 时间分辨能谱数目 | |
| spectral_model | 最优拟合模型：**BAND**(124) / **SBPL**(142) / **COMP**(67, 即 CPL 截断幂律) / **PWRL**(17, 单幂律) | 实测取值分布 |
| amplitude / amplitude_error | 归一化 | photon/s/cm²/keV，1σ |
| **peak_energy / peak_energy_error** | **Epeak（νFν 峰能）** | **keV，观测系**，1σ |
| low_pl_index / high_pl_index 及误差 | 低/高能幂律指数 | BAND/SBPL；COMP 无高能指数（空） |
| break_energy / break_energy_error | 谱拐折能量 E0 | keV，1σ |
| sbpl_break_scale | SBPL 拐折锐度 | decades of energy |
| chi_squared / fit_dof | 拟合卡方与自由度 | |
| grb_flag | `W`=弱爆发、`C`=定标爆发、空=正常 | 325 空 / 17 W / 8 C |

注意：Epeak 仅在 BAND 和 SBPL 模型下有物理意义；COMP（CPL）模型拟合的是峰值能量（COMP 模型下 peak_energy 即 CPL 的 Epeak），PWRL 模型无峰能（该列应为空）。所有误差 1σ，观测系。

## 爆发标识

- **唯一标识是 trigger_num**（整数 105–8121，含非 GRB 触发？不——本表只收 GRB，但编号不连续）。
- **名称不唯一**：实测有 **667 个重复名称**（如 `4B 910425-` 对应多个触发），因为同一天多个爆发共用日期名。join/匹配时**必须用 trigger_num**，不能只用名称。
- 名称两种格式：
  - 4B 目录期（触发 ≤5586）：`4B yymmddx`，x 为当日序号字母，多触发且未定序时用 `-` 结尾（如 `4B 940716-`）；
  - 4B 之后：`GRB yymmdd` 或 `GRB yymmdd-`。
- 坐标：ra/dec（J2000）+ error_radius，绝大多数有位置（BATSE 定位误差几度）。

## 已知坑 / 注意事项

1. **缺失值为空字符串**（`||`），无 NULL 记号。缺失量统计（2702 行中）：T50/T90 及其误差缺 665 行（数据间断的爆发无法计算 T90，主页明确说明）；64/256/1024 ms 峰值流量缺 569 行；四通道 fluence 缺 569 行；max_cts/threshold 系列缺 1386 行。
2. tdat 文件开头有 `<HEADER>` 元数据块、结尾有 `<END>` 行，解析时需跳过；每行末尾有尾置 `|`。
3. **通道 4 fluence（>300 keV）是积分通道**，其值对假设的能谱形状敏感，官方明确警告不要用它做精细能谱分析。
4. 流量能段 50–300 keV、fluence 分通道、T90 用全通道计数——三个量的能段定义互不相同的，引用时务必区分。
5. **名称重复**（667 个），唯一键是 trigger_num；名称里 4B 期用 `4B yymmddx` 格式、后期用 `GRB yymmdd`，且部分以 `-` 结尾（当日多触发未定序）。
6. 时间有三套冗余表示（TJD 日数、MJD、当日秒数）；TJD = JD − 2440000.5。
7. overwrite/overwritten 标记的爆发（Y 共约 190 行）是触发系统层面的相互覆盖事件，流量/fluence 可能受另一爆发污染，使用时建议检查。
8. 主表无 Epeak/Eiso；Epeak 需 join `batsegrbsp`（仅 350 个亮源）；Eiso 需红移+fluence 自算。
9. 该表是"current catalog"的持续更新版（4B 之后直到任务结束），与 1996 年发表的 4B 纸版目录（1637 个爆发）不是一回事；HEASARC 另有 `batse4b`、`batse3b` 表。

## 校验和（SHA-256）

```
393054e2e59b5ad72ae7821d0caf7e8f517d290c1cf7700affb55dfa00bc8e5d  heasarc_batsegrb.tdat.gz
b601c61ca881c61e3c23fa94810a55f5cefb0598862d303fd9559ca3b9ade6d0  heasarc_batsegrb.hdr.gz
167d8f85ac0b0148c8d439666a5da15b62f75e1ace43c9dc8f842b41061705ab  heasarc_batsegrbsp.tdat.gz
291b4f06d43f270f083c8fffe675abbfbc61fa9e25c58cd7028dafedddf71008  heasarc_batsegrbsp.hdr.gz
```

## 快速解析示例（Python）

```python
import gzip, csv
with gzip.open("heasarc_batsegrb.tdat.gz", "rt") as f:
    rows = [
        line.rstrip("\n").split("|")[:-1]  # 丢弃尾置空字段
        for line in f
        if line and line[0].isdigit()
    ]
# rows[i][31] = t90, rows[i][38] = fluence_3，空字符串即缺失
```
