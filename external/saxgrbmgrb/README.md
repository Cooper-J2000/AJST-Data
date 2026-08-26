# BeppoSAX/GRBM GRB 目录（HEASARC `saxgrbmgrb`）

- **目录名称**：BeppoSAX/GRBM Gamma-Ray Burst Catalog（HEASARC 表名 `saxgrbmgrb`）
- **主页 URL**：https://heasarc.gsfc.nasa.gov/W3Browse/gamma-ray-bursts/saxgrbmgrb.html
- **数据下载 URL**（HEASARC 官方 FTP-over-HTTP 镜像，gzip 压缩 tdat）：
  - 数据：https://heasarc.gsfc.nasa.gov/FTP/heasarc/dbase/tdat_files/heasarc_saxgrbmgrb.tdat.gz
  - 表头：https://heasarc.gsfc.nasa.gov/FTP/heasarc/dbase/tdat_headers/heasarc_saxgrbmgrb.hdr.gz
- **获取日期**：2026-07-22（数据文件本身为 HEASARC 2020-09-28 导出版本，源自 CDS 目录 J/ApJS/180/192 的 table2.dat，HEASARC 2010 年 1 月建表）
- **参考文献**：Frontera et al. 2009, ApJS 180, 192（bibcode `2009ApJS..180..192F`）
- **文件状态**：原始下载文件，内容未做任何修改。

## 文件清单与格式

| 文件 | 大小 | 说明 | 数据行数（实测） |
|---|---|---|---|
| `heasarc_saxgrbmgrb.tdat.gz` | 54,103 B | GRBM GRB 主目录（名称、位置、T90/Tdet、40–700 keV fluence 与峰值流量、幂律光子指数） | **1082** |
| `heasarc_saxgrbmgrb.hdr.gz` | 1,453 B | 列定义/单位/格式（tdat 表头） | — |

tdat 是 HEASARC 的管道符（`|`）分隔 ASCII 格式：文件开头有 `<HEADER> ... <DATA>` 元数据块，之后每行一条记录（以 `GRB` 开头），文件以 `<END>` 结束。实测行数命令：`zcat heasarc_saxgrbmgrb.tdat.gz | grep -cE '^GRB'`。

**行数核对**：实测 1082 行，与表头内 `TOTAL ROWS: 1082` 及主页宣称的 1082 个 GRB 一致。时间覆盖 **1996-07-03 – 2002-04-26**（BeppoSAX 在轨期）。

## 逐列文档

共 27 列（每行末尾有尾置 `|`，按 `|` 分割会得到第 28 个空字段，解析时注意丢弃）。缺失值为**空字符串**（两个相邻 `|`），无 `NULL`/`NaN` 记号。

| # | 列名 | 含义 | 单位 | 备注 |
|---|---|---|---|---|
| 1 | name | 爆发名称 `GRB yymmdd[X]`（同日多暴加字母后缀） | — | **唯一主键**（表头 `unique_key = name`），实测全部唯一 |
| 2–3 | ra / dec | 赤经/赤纬（J2000） | deg | 缺 245 行；原始精度 0.01°，但真实定位精度由 error_radius 决定，通常远大于此 |
| 4–5 | lii / bii | 银经/银纬 | deg | |
| 6 | error_radius | 平均位置误差圆半径 | deg | GRBM 自定位的误差很大（几十度），WFC/IPN 位置可小至 0.1° |
| 7 | earth_limb_elevation | 爆发方向相对地球临边的仰角 | deg | 仅对位置已知的源给出 |
| 8 | ref_position | 最佳坐标来源（见下"位置来源代码"） | — | 245 行为空（无可靠位置） |
| 9 | time | GRB 触发时刻（UT） | MJD | 精度 1 s；全部 1082 行有值 |
| 10 | high_res_flag | 是否有高时间分辨率数据（Y/N） | — | Y=675 / N=407 |
| 11–12 | t_other / t_other_error | **Tdet**：从最早冒出 2σ 阈值到最后落回 2σ 之下的总时长 | s | 即 Frontera+2009 的持续时间定义之一 |
| 13–14 | t_above_fraction / t_above_fraction_error | **Ta**：发射高于 2σ 的累计时间 | s | |
| 15 | t_above_num_intervals | 发射高于 2σ 的时间区间数 | — | 多峰暴 >1 |
| 16–17 | t90 / t90_error | **T90**（5%–95% 积分计数间隔，BATSE 定义） | s | 缺 79 行 |
| 18–19 | fluence / fluence_error | **40–700 keV fluence** | erg/cm² | 缺 308 行；全表范围 1.3e-7 – 4.5e-4 |
| 20–21 | peak_flux / peak_flux_error | **40–700 keV 峰值流量** | **erg/cm²/s** | 缺 318 行；⚠️ 是**能量流量**不是光子流量，详见"坑" |
| 22–23 | photon_index / photon_index_error | 幂律谱光子指数 Γ（40–700 keV 与 >100 keV 两通道拟合） | — | 缺 368 行；单幂律假设，无 Epeak |
| 24–26 | detection_unit_1 / _2 / _3 | 所用 GRBM 探测单元（1–4） | — | unit_1 用于时标参数（信噪比最好的单元）；unit_2(+3) 用于 fluence/峰流/硬度 |
| 27 | rebinning_factor | 默认光变曲线重bin因子 | — | 长暴（T90>2s）用 1 s 光变、短暴用 7.8125 ms 光变，再乘此因子；实测取值 1–14 |

**能段 / 参考系 / 误差约定（重点）**：

- GRBM 工作能段 **40–700 keV**；fluence、峰值流量均为该能段，光子指数由 40–700 keV 和 >100 keV 两通道拟合。与 BATSE 的 50–300 keV（20 keV 起四通道）、Swift/BAT 的 15–150 keV 不可直接混用。
- 所有量均为**观测系（observer frame）**；目录不含红移、无 rest-frame 量，T90 未做 (1+z) 改正。
- 误差列为目录给出的**平均误差（mean error）**，Frontera+2009 未明确区分 1σ/90% 置信；按惯例视为 ~1σ 量级使用，做精细误差传播时需留意。
- **不含 Epeak、不含 Band/CPL 谱拟合参数、不含 Eiso**。只有单幂律光子指数。Epeak 需查其它 BeppoSAX 文献/目录。

**位置来源代码（ref_position 实测分布）**：

| 代码 | 来源 | 行数 |
|---|---|---|
| G | BeppoSAX GRBM 自定位 | 351 |
| W | BeppoSAX WFC | 52 |
| A | RXTE/ASM | 7 |
| C | （主页未文档化；实测 1 行：GRB 980706B） | 1 |
| H | HETE-2 | 1 |
| I | IPN（行星际网络） | 28 |
| K | Kommers 目录 | 18 |
| P | RXTE/PCA | 2 |
| S | Stern 目录 | 68 |
| 4B 或 4B_NNNN | BATSE 4B 目录（NNNN=BATSE 触发号） | 309 |
| 空 | 无可靠位置 | 245 |

## 爆发标识

- **唯一标识是 name**（`GRB yymmdd` 或 `GRB yymmddX`，X∈A–E；实测字母后缀最多到 E，如 GRB 960916E 当日 5 暴）。1082 个名称全部唯一、全部符合该格式，且名称日期与触发时刻日期逐行核对无误（parse.py 内置校验，0 个不匹配）。
- **注意**：本目录的同日字母后缀**不一定与通用命名一致**。典型例子：与 SN 1998bw 成协的著名暴 GRB 980425（1998-04-25 21:49 UT，WFC 定位）在本目录中叫 **GRB 980425B**（当天早些时候 10:42 UT 还有一个 GRBM 探测的暴记为 980425A）。跨目录匹配时**必须同时用名称+触发时刻校验**，不能只用名称。
- 坐标：837/1082 行有 ra/dec；其余 245 行无位置（GRBM 是全天监视器，定位依赖其他仪器/目录）。

## 已知坑 / 注意事项

1. **peak_flux 是能量流量（erg/cm²/s），不是光子流量**。SCHEMA 的 `params.peak_flux` 定义为光子峰流量，因此解析时把本目录的 peak_flux 放在 `other` 里（保留原列名），**不要**误当光子流量入库或与 BATSE/GBM 的 photon peak flux 直接比较。峰流的积分时标目录未单列（由 rebinning 后的光变取得）。
2. **缺失值为空字符串**（`||`）。缺失统计（1082 行中）：ra/dec 缺 245；t90 缺 79；fluence 缺 308；peak_flux 缺 318；photon_index 缺 368；error_radius/earth_limb_elevation/ref_position 缺 245（即无位置的行）。
3. tdat 文件开头有 `<HEADER>` 元数据块、结尾有 `<END>` 行；每行末尾有尾置 `|`。数据行以 `GRB` 开头（不是数字），按行首过滤时别沿用 BATSE 表的 `^[0-9]` 规则。
4. **photon_index 是两通道单幂律拟合**（40–700 keV + >100 keV），不是 Band 拟合；对谱拐折在该能段内的暴会有偏差，且与 Band 的 α 不可等同。
5. **同日字母后缀与通用命名可能不一致**（见"爆发标识"节的 GRB 980425B 例子）。
6. ref_position 存在主页未列出的代码：实测有 `C`（1 行，GRB 980706B）和大量 `4B_NNNN`（带 BATSE 触发号的 4B 位置），主页只列了 `4B`。
7. 时间用 MJD 浮点给出（精度 1 s）；GRBM 触发时刻与星上触发逻辑相关，和其他卫星的 trigger_time 可有秒级差异。
8. detection_unit_3 经常为空（仅部分暴加入第三个单元提高统计）；rebinning_factor 的基准光变长/短暴不同（1 s / 7.8125 ms），比较时标相关量时注意。

## normalized.jsonl 字段映射（parse.py）

- `name`：原样（全部符合 `GRB yymmddX`，1082/1082 解析成功）；`name_alt` 为空（目录无其他命名）。
- `trigger_time`：由 `time`（MJD）转 ISO UTC。
- `params.t90`：`t90`/`t90_error`，band=`40-700 keV`。
- `params.fluence`：`fluence`/`fluence_error`，band=`40-700 keV`。
- `params.spectral_index`：`photon_index`/`photon_index_error`，附加 `model: "PL"`（单幂律）。
- `other`：lii、bii、error_radius、earth_limb_elevation、ref_position、high_res_flag、t_other(±err)、t_above_fraction(±err)、t_above_num_intervals、**peak_flux(±err，能量流量)**、detection_unit_1/2/3、rebinning_factor（原样保留原列名）。

输出统计（1082 行）：t90 有值 1003、fluence 774、spectral_index 714、peak_flux(other) 764、有坐标 837。

## 校验和（SHA-256）

```
17dee43cb84900052b25ece2e26beef008b3a09344420650b76defb34d12cf74  heasarc_saxgrbmgrb.tdat.gz
0d8b03a83249195204f4a0859529fc684eb25c624bdba073260813044d89b346  heasarc_saxgrbmgrb.hdr.gz
```

## 快速解析示例（Python）

```python
import gzip
with gzip.open("heasarc_saxgrbmgrb.tdat.gz", "rt") as f:
    rows = [
        line.rstrip("\n").split("|")[:-1]  # 丢弃尾置空字段
        for line in f
        if line.startswith("GRB")
    ]
# rows[i][15] = t90, rows[i][17] = fluence, rows[i][19] = peak_flux(能量流量)，空字符串即缺失
```
