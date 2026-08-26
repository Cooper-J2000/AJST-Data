# Swift GRB Burst Advocate 汇编表（HEASARC `swiftgrbba`）

- **目录名称**：Swift Gamma Ray Burst Compilation by Burst Advocate（HEASARC 表名 `swiftgrbba`）
- **主页 URL**：https://heasarc.gsfc.nasa.gov/W3Browse/swift/swiftgrbba.html
- **数据下载 URL**（HEASARC 官方 FTP-over-HTTP 镜像，gzip 压缩 tdat）：
  - 数据表：https://heasarc.gsfc.nasa.gov/FTP/heasarc/dbase/tdat_files/heasarc_swiftgrbba.tdat.gz
  - 表头（列定义）：https://heasarc.gsfc.nasa.gov/FTP/heasarc/dbase/tdat_headers/heasarc_swiftgrbba.hdr.gz
- **获取日期**：2026-07-22（数据文件为 HEASARC 2026-03-16 导出版本，表头 `EXGEST DATE: 2026-03-17`）
- **文件状态**：原始下载文件，内容未做任何修改。
- **参考 bibcode**：2004ApJ...611.1005G（表头 `catalog_bibcode`，Gehrels et al. 2004，Swift 任务本身；该表由 Swift 项目组 / Burst Advocate 持续维护，无单独发表文献）。

## 文件清单与格式

| 文件 | 大小 | 说明 | 数据行数（实测） |
|---|---|---|---|
| `heasarc_swiftgrbba.tdat.gz` | 346,094 B | Burst Advocate 汇编主表：每个 GRB 一行，BAT/XRT/UVOT 摘要参数 + 红移 + 参考文献 | **2036** |
| `heasarc_swiftgrbba.hdr.gz` | 1,923 B | 列定义/单位/描述（tdat 表头） | — |

tdat 是 HEASARC 的管道符（`|`）分隔 ASCII 格式：文件开头有 `<HEADER> ... <DATA>` 元数据块，之后每行一条记录（以 `GRB ` 开头），文件以 `<END>` 结束，每行末尾有尾置 `|`。实测行数命令：`zcat heasarc_swiftgrbba.tdat.gz | grep -c '^GRB '`。

**行数核对**：实测 2036 行，与表头内 `TOTAL ROWS: 2036` 一致。**时间覆盖 2004-12-17 ~ 2026-02-08**（MJD 53356.31 ~ 61079.21），即 Swift 时代全程；该表为持续更新表（与 `swiftgrb` 等静态表不同）。

**表与网页一致性**：hdr 中 49 个 field 与 W3Browse 网页列出的 Parameters 一一对应（name、trigger_time、time、trigger_obs、target_id、BAT 位置/流量/谱、XRT 位置/流量/衰减/谱、UVOT 位置/星等、红移、参考文献、advocate），已逐列核对。

## 逐列 Parameters 文档

共 49 列（按 `|` 分割后丢弃末尾空字段）。缺失值为**空字符串**（两个相邻 `|`），无 `NULL`/`NaN`/`-99` 记号（已全表核查数值列无哨兵值）。

### 标识与触发（1–5）

| # | 列名 | 含义 | 单位/格式 | 备注 |
|---|---|---|---|---|
| 1 | name | GRB 名称 | `GRB yymmddX` 或 `GRB yymmdd` | **唯一主键**（表头 `unique_key = name`，已验证无重复）。362 行无字母后缀（见"爆发标识"节） |
| 2 | trigger_time | 触发时刻（**仅当日时分秒**） | UTC `HH:MM:SS(.ss)`，char12 | 不含日期！完整时刻须由第 3 列 MJD 重建；11 行为空 |
| 3 | time | 触发时刻 | MJD（float8） | 全覆盖；11 行为整数 MJD（只有日期精度，对应 trigger_time 为空的那 11 行） |
| 4 | trigger_obs | 记录触发的天文台/仪器 | 自由文本 | 实测分布：Swift 1631、Fermi 105、INTEGRAL 60、SVOM 47、Ground Analysis 29、BAT/GUANO 27、MAXI 22、AGILE 20、IPN 15、BATSS 9、HETE 5、BAT/GUNAO 5（源数据拼写如此）等。**本表不只收 Swift 触发的暴** |
| 5 | target_id | Swift 触发编号（target ID） | 整数 | 365 行缺失（非 Swift 触发的暴无此编号） |

### BAT 参数（6–18）

| # | 列名 | 含义 | 单位 | 备注 |
|---|---|---|---|---|
| 6–7 | ra / dec | BAT 位置（J2000） | deg | 18 行缺失 |
| 8–9 | lii / bii | 银经/银纬（J2000） | deg | 与 ra/dec 同缺 |
| 10 | error_radius | BAT 位置误差半径 | arcmin | **90% 置信**；276 行缺失 |
| 11 | bat_t90 | **T90 持续时间** | s | 能段 **15–150 keV**，观测系；406 行缺失 |
| 12–13 | bat_fluence / bat_fluence_error | **BAT fluence** 及误差 | erg/cm² | 能段 **15–150 keV**，观测系；误差为 **90% 置信**（非 1σ）；383/391 行缺失 |
| 14–15 | bat_1s_peak_flux / bat_1s_peak_flux_error | **BAT 1 秒峰光子流量**及误差 | photon/cm²/s | 能段 **15–150 keV**，时标 1 s；误差 **90% 置信**；429/433 行缺失 |
| 16 | bat_spectral_model | BAT 能谱拟合模型 | `PL` / `CPL` | 实测 PL 1396、CPL 249、缺失 391。**只给这两个模型，不给 Band** |
| 17–18 | bat_photon_index / bat_photon_index_error | BAT 光子指数及误差 | — | 观测系；误差 **90% 置信**（15–150 keV 拟合）；379/387 行缺失。**注意：本表无 Epeak！** CPL 拟合的 Epeak 未收录 |

### XRT 余辉参数（19–28）

| # | 列名 | 含义 | 单位 | 备注 |
|---|---|---|---|---|
| 19–20 | xrt_ra / xrt_dec | XRT 位置（J2000） | deg | 精度远高于 BAT（角秒级），344 行缺失 |
| 21 | xrt_error_radius | XRT 位置误差半径 | arcsec | **90% 置信** |
| 22 | xrt_first_obs | XRT 首次观测延迟（相对触发） | s | 435 行缺失 |
| 23 | xrt_early_flux | XRT 早期流量 | erg/cm²/s | 能段 **0.3–10 keV**；1276 行缺失 |
| 24–25 | xrt_11hr_flux / xrt_24hr_flux | XRT **11 小时 / 24 小时流量** | erg/cm²/s | 能段 **0.3–10 keV**；余辉光变采样的两个标准点，452/429 行缺失 |
| 26 | xrt_lc_index | **XRT 初始时间衰减指数** | — | **带符号**（F ∝ t^index，即衰减时指数为负，如 −1.5；实测范围约 −5.3 ~ −0.1）。388 行缺失。本表**只给初始衰减指数，不给拐折时间/拐折后指数** |
| 27 | xrt_gamma | XRT 谱指数（光子指数 Γ） | — | 0.3–10 keV；348 行缺失 |
| 28 | xrt_nh | XRT 吸收柱密度 NH | cm⁻² | 348 行缺失 |

### UVOT 参数（29–35）

| # | 列名 | 含义 | 单位 | 备注 |
|---|---|---|---|---|
| 29–30 | uvot_ra / uvot_dec | UVOT 位置（J2000） | deg | 1546 行缺失 |
| 31 | uvot_error_radius | UVOT 位置误差半径 | arcsec | 90% 置信 |
| 32 | uvot_first_obs | UVOT 首次观测延迟 | s | |
| 33 | uvot_vmag_flag | V 星等是否为上限 | 0/1 | **1 = 上限** |
| 34 | uvot_vmag | UVOT V 星等 | mag | 配合 flag 判断是否上限 |
| 35 | uvot_mag | 其他滤光片星等 | 文本 | 形如 `B=18.3; U=17.3; UVW1=17.4; ...`，上限用 `>` 号 |

### 红移与寄主星系（36–40）

| # | 列名 | 含义 | 备注 |
|---|---|---|---|
| 36 | other_obs | 其他天文台探测情况 | 自由文本 |
| 37 | redshift | **红移** | float；460 行有值（2036−1576） |
| 38 | redshift_comment | 红移注释（测量方法/来源） | 文本 |
| 39 | other_redshift | 其他红移报道 | 文本 |
| 40 | host_galaxy | 寄主星系标识 | 文本 |

### 参考文献与维护者（41–49）

| # | 列名 | 含义 |
|---|---|---|
| 41 | comment | 一般注释（自由文本） |
| 42–48 | ref_bat / ref_xrt / ref_uvot / ref_radio / ref_redshift / ref_host / ref_other | 各类参考文献（多为 GCN 编号，自由文本；**ref_radio 只是射电观测的文献引用，本表不含射电流量数值**） |
| 49 | advocate | 当值 Burst Advocate 姓名 |

## 爆发标识

- **唯一主键是 name**（表头声明 `unique_key = name`，已全表验证无重复）。
- 名称两种格式：
  - `GRB yymmddX`（1674 行）：带当日序号字母后缀的标准名；
  - `GRB yymmdd`（362 行）：**无字母后缀的官方命名**（当日无第二个公认暴时 Swift 时代常不赋后缀，如 GRB 091026、GRB 060729）。解析时**不要臆造后缀**：这些行在 normalized.jsonl 中 `name=null`、原名进 `name_alt`，并给 trigger_time + 坐标兜底（SCHEMA 规则 4）。
- 坐标优先级建议：BAT ra/dec（角分级，18 行缺）→ XRT xrt_ra/xrt_dec（角秒级）→ UVOT uvot_ra/uvot_dec。parse.py 顶层 ra/dec 按此顺序回填。

## 已知坑 / 注意事项

1. **trigger_time 列只有时分秒**（char12），不含日期；完整触发时刻必须用第 3 列 MJD 重建。有 **11 行** trigger_time 为空且 MJD 为整数（如 GRB 120701A、GRB 070125），只有日期精度，解析时 trigger_time 置 null（不能拿整数 MJD 当成 00:00:00，那是假的）。
2. **缺失值为空字符串**（`||`），无数值哨兵；行首标志是 `GRB `（非数字），文件头有 `<HEADER>` 块、尾有 `<END>`，行末有尾置 `|`。
3. **所有 BAT 量的误差都是 90% 置信**（fluence、1s 峰流、光子指数），位置误差也是 90%——与 BATSE（1σ）不同，跨目录比较时务必注意；解析输出按 SCHEMA 加 `"cl": 90`。
4. **本表无 Epeak、无 Eiso、无 T50**。BAT 谱拟合只有 PL/CPL 模型 + 光子指数（CPL 的 Epeak 未收录）；Epeak 需 join `swift_bat`（swiftbatgrb 等）或文献目录。
5. **无射电流量数值**：`ref_radio` 列只是射电观测的 GCN 文献引用文本。
6. xrt_lc_index 是**带符号**的初始衰减指数（负值=衰减），且只有初始段，无拐折时间/拐折后指数；要完整光变拟合需查 Swift XRT 官网光变库（本项目的 `swift_xrt_live`）。
7. 三套坐标精度差异巨大：BAT 角分级（error_radius 单位 arcmin）、XRT/UVOT 角秒级（arcsec），单位不同，混用时注意换算。
8. **本表是"Swift 参与/跟踪的暴"的汇编，不限于 Swift 触发**：105 个 Fermi 触发、60 个 INTEGRAL、47 个 SVOM 触发的暴也在内（这些行通常 target_id 缺失、BAT 参数缺失）。按"Swift 探测样本"做统计时须按 trigger_obs 过滤。
9. 时间有三套冗余表示（name 里的 yymmdd、时分秒、MJD）；MJD 最可靠。已验证带后缀名的日期与 MJD 日期全部一致（0 个不匹配）。
10. trigger_obs 有源数据拼写不一致（`BAT/GUANO` 27 行 vs `BAT/GUNAO` 5 行），原样保留。
11. 该表持续更新（本次导出 2026-03-16，覆盖到 2026-02-08）；重复下载会得到更多行，行数以表头 `TOTAL ROWS` 为准。

## 校验和（SHA-256）

```
ee8242b5cd265800985e3802460ba3c7c7d59bfc9f1f555ef18eec59606a38c5  heasarc_swiftgrbba.tdat.gz
a2cf9549c162ddddd3694180b3f111fd9aaf8322d573fe7243c894651b2fcdf7  heasarc_swiftgrbba.hdr.gz
```

## 快速解析示例（Python）

```python
import gzip
with gzip.open("heasarc_swiftgrbba.tdat.gz", "rt") as f:
    rows = [
        line.rstrip("\n").split("|")[:-1]  # 丢弃尾置空字段
        for line in f
        if line.startswith("GRB ")
    ]
# rows[i][0] = name, rows[i][2] = MJD, rows[i][10] = bat_t90,
# rows[i][25] = xrt_lc_index，空字符串即缺失；共 49 列
```
