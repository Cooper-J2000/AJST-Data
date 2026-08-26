# heasarc_grbcat — HEASARC Gamma-Ray Bursts Catalog (GRBCAT)

## 基本信息

- **目录名称**：GRBCAT — Gamma-Ray Bursts Catalog（HEASARC 综合 GRB 目录，收录 1967 年首个 GRB 以来的多卫星探测，汇编自公开发表文献；表作者 Angelini et al.，HEASARC 于 2008 年 6 月收录）
- **主页 URL**：https://heasarc.gsfc.nasa.gov/W3Browse/all/grbcat.html
- **数据文件下载 URL**（HEASARC FTP 镜像，tdat 格式）：
  - 主表：https://heasarc.gsfc.nasa.gov/FTP/heasarc/dbase/tdat_files/heasarc_grbcat.tdat.gz
  - 流量/流量积分表：https://heasarc.gsfc.nasa.gov/FTP/heasarc/dbase/tdat_files/heasarc_grbcatflux.tdat.gz
  - 余辉表：https://heasarc.gsfc.nasa.gov/FTP/heasarc/dbase/tdat_files/heasarc_grbcatag.tdat.gz
  - 对应头文件（列定义）：同目录 `tdat_headers/heasarc_grbcat.hdr.gz` 等
- **获取日期**：2026-07-21（curl 下载，文件原样保存，未做任何修改）
- **数据新鲜度**（文件头 `LAST MODIFIED`）：
  - 主表 2025-10-29（仍在持续更新）
  - **flux 表 2020-09-28（已 5 年未更新，基本静止！）**
  - 余辉表 2025-11-05

## 文件清单

| 文件 | 内容 | 实测数据行数 | 文件头声称 (TOTAL ROWS) | 是否一致 |
|---|---|---|---|---|
| `heasarc_grbcat.tdat.gz` | 主表：每个 GRB×卫星 一行 | **10119** | 10119 | 是 |
| `heasarc_grbcatflux.tdat.gz` | 峰值流量/流量积分，每 GRB×能段 一行 | **12055** | 12055 | 是 |
| `heasarc_grbcatag.tdat.gz` | 余辉观测（含红移） | **2778** | 2778 | 是 |
| `heasarc_grbcat.hdr.gz` | 主表列定义（官方头文件） | — | — | — |
| `heasarc_grbcatflux.hdr.gz` | flux 表列定义 | — | — | — |
| `heasarc_grbcatag.hdr.gz` | 余辉表列定义 | — | — | — |

行数用 `zcat <file> | sed -n '/<DATA>/,/<END>/p'` 抽取数据段实测；整个 `.tdat` 文件总行数（含头）分别为 10196 / 12110 / 2847。W3Browse 网页本身不标注总行数，以文件头 `TOTAL ROWS` 为准，两者完全吻合。

主表 10119 行覆盖 **5831 个唯一 GRB 名**（同一 GRB 被多个卫星探测会有多行）；flux 表覆盖 3781 个 GRB；余辉表仅 213 个 GRB。

## 数据格式说明（HEASARC tdat）

- 纯 ASCII，gzip 压缩。**管道符 `|` 分隔**的定序字段。
- 结构：`<HEADER>` 段（含 `#` 注释 + `field[...]` 列定义）→ `<DATA>` → 数据行 → `<END>`。
- 列顺序以头文件中 `line[1] = ...` 为准（与 `field[]` 声明顺序一致）。
- **缺失值 = 相邻两个管道符之间的空字符串**（如 `||`），没有 `NULL`/`NaN`/`-99` 之类的记号。
- 读取方式示例：`zcat heasarc_grbcat.tdat.gz | sed -n '/<DATA>/,/<END>/p' | grep -v '^<'`。

## 爆发如何标识

- `name`：`GRB YYMMDD`，同一天多个爆发时追加字母，如 `GRB 690703`、`GRB 921112C`（**年份是两位**，解析时注意 19xx/20xx 的世纪判断）。
- `id`：整数，同一 GRB 的所有记录（跨表）共享同一 id，**这才是跨表 join 的可靠键**（name 有少量重名/异名情况，另有 `alt_names` 记录别名）。
- 坐标：`ra`/`dec`（J2000，度）。主表 10119 行中 5943 行有坐标；`coord_flag` 说明坐标质量：`-1` = 无坐标，`0` = 唯一坐标，`0–1` 之间 = 坐标可信度（越接近 1 越好）。
- `time`：**MJD（Modified Julian Day）浮点数**，不是 ISO 字符串，也不是 Unix 时间戳。`time_def` 说明该时刻的定义（如 "Earth Crossing Time"、触发时刻等，定义随观测台而异）。

## 主表 heasarc_grbcat 逐列文档

列序（31 列）：`record_number id name alt_names time time_def observatory ra dec coord_flag region afterglow_flag reference t50_mod t50 t50_error t50_range t50_emin t50_emax t90_mod t90 t90_error t90_range t90_emin t90_emax t_other flux_flag notes flux_notes local_notes class`

| 列 | 含义 | 单位/备注 |
|---|---|---|
| record_number | 每行唯一序号 | int |
| id | GRB 源编号（跨表共享） | int，**join 键** |
| name | 爆发名 | GRB YYMMDD[x] |
| alt_names | 别名 | 字符串，可空 |
| time | 爆发时刻 | **MJD**，定义见 time_def |
| time_def | 时刻定义 | 如 "Earth Crossing Time" |
| observatory | 探测卫星/仪器 | 36 种取值；多仪器写作 `obs-instr`，多台联合写作 `obs1/obs2`（如 `ULYSSES/BATSE-CGRO`） |
| ra, dec | 误差区中心坐标 | 度，J2000；coord_flag=-1 时为空 |
| coord_flag | 坐标质量标志 | -1 无 / 0 唯一 / 0~1 可信度 |
| region | 误差区类型 | circle/annulus/box/dual/annulus intersect/irregular/intersect（具体形状参数在 grbcatcirc/grbcatann 等附属表，本目录未下载） |
| afterglow_flag | 是否有余辉记录 | Y/N |
| reference | 文献来源 | ADS bibcode 格式 |
| t50_mod | T50 修饰符 | `<`、`>`、`~` 等（文献中的近似记号） |
| **t50** | **T50 持续时间** | **秒，观测系（observer frame）**；25%→75% 计数间隔。2033 行非空 |
| t50_error | T50 误差 | 秒；**直接取自原始文献，置信度未统一**（各文不一，可能是 1σ 或 90%，见"坑"） |
| t50_range | T50 能段（字符串） | keV，如 "50-300"；**几乎全空（仅 5 行）** |
| t50_emin / t50_emax | T50 能段数值下/上限 | keV，int；同样大多为空 |
| t90_mod | T90 修饰符 | 同上 |
| **t90** | **T90 持续时间** | **秒，观测系**；5%→95% 计数间隔。**2809 行非空** |
| t90_error | T90 误差 | 秒；置信度随原始文献，未统一 |
| t90_range | T90 能段（字符串） | keV；**仅 63 行非空** |
| t90_emin / t90_emax | T90 能段数值下/上限 | keV；仅 63 行非空。**BATSE 的 T90 一般指 50–300 keV，但本表大多未填能段，不能想当然** |
| t_other | 其他定义的持续时间 | 秒；376 行非空，细节在 notes |
| flux_flag | flux 表是否有该源流量数据 | Y/N |
| notes / flux_notes / local_notes | 各类备注 | 字符串 |
| class | Browse 分类 | 全部为 GRB（1710） |

## flux 表 heasarc_grbcatflux 逐列文档

列序（19 列）：`record_number id name observatory flux_mod flux flux_error flux_units flux_energy flux_emin flux_emax fluence_mod fluence fluence_error fluence_units fluence_energy fluence_emin fluence_emax flux_notes`

| 列 | 含义 | 单位/备注 |
|---|---|---|
| record_number | 行唯一序号 | int |
| id / name | GRB 编号/名称 | 与主表 join |
| observatory | 观测台 | |
| flux_mod | 峰值流量修饰符 | `<`、`>`、`~` |
| **flux** | **峰值流量（peak flux）** | **单位由 flux_units 决定**：`photons` → ph s⁻¹ cm⁻²；`ergs` → erg s⁻¹ cm⁻²；`counts` → counts s⁻¹ cm⁻²（极少）。11581 行非空 |
| flux_error | 峰值流量误差 | 同单位；置信度随文献未统一 |
| flux_units | 流量单位 | 分布：photons 8276、ergs 1082、counts 7、空 2678 |
| flux_energy | 流量能段（字符串） | keV |
| flux_emin / flux_emax | 流量能段数值下/上限 | keV |
| fluence_mod | fluence 修饰符 | `<`、`>`、`~` |
| **fluence** | **流量积分（fluence）** | **单位由 fluence_units 决定**：`ergs` → erg cm⁻²；`photons` → ph cm⁻²。11999 行非空 |
| fluence_error | fluence 误差 | 同单位；置信度随文献未统一 |
| fluence_units | fluence 单位 | 分布：ergs 9789、counts 2、空 2260 |
| fluence_energy | fluence 能段（字符串） | keV |
| fluence_emin / fluence_emax | fluence 能段数值下/上限 | keV；9313 行非空 |
| flux_notes | 备注 | 早期 VELA 源常见 "Fluence energy not specified" |

**注意：每个 GRB 在 flux 表中可能有多行（不同能段/不同文献各一行），取 fluence 时必须按 (flux_emin, flux_emax) 选定能段，不能简单求和或取首行。**

## 余辉表 heasarc_grbcatag 逐列文档（附带下载，主要价值是红移）

列序（27 列）：`record_number id name alt_names telescope observatory band energy_range obs_time ra dec coord_flag local_notes detected intensity_mod intensity intensity_error intensity_error_min intensity_error_max intensity_units redshift_mod redshift redshift_error redshift_min redshift_max reference notes`

- 每行 = 一次余辉观测（某望远镜、某波段）。`band` 为波段字符串（如 "20 cm"、"0.1-2.4 keV"），`energy_range` 为大类代码：**R=射电, I=红外, O=光学, U=紫外, X=X射线, G=伽马**。
- `intensity` + `intensity_units`：单位混杂（mJy、erg cm⁻² s⁻¹、erg s⁻¹、星等等），用前必须看 `intensity_units`。
- `detected`：y/n/p（p=可能）；未探测时 intensity 多为上限（intensity_mod="Limit"）。
- **redshift**：实测红移，**仅 22 行非空**（绝大多数余辉记录没有红移），另有 redshift_mod/redshift_min/redshift_max。红移误差列 redshift_error 是**字符串**（非数值），注意解析。

## 关键参数可用性小结（针对瞬时辐射研究）

| 参数 | 是否有 | 位置/说明 |
|---|---|---|
| T90 | **有** | 主表 `t90`（2809 行非空），观测系，秒；误差 `t90_error`；能段大多未记录 |
| T50 | 有 | 主表 `t50`（2033 行非空） |
| Fluence | **有** | flux 表 `fluence`（11999 行非空），单位看 `fluence_units`（多为 erg cm⁻²），能段见 `fluence_emin/emax` |
| Peak flux | 有 | flux 表 `flux`（11581 行非空），单位看 `flux_units` |
| **Epeak** | **没有** | GRBCAT 不记录任何能谱参数 |
| 能谱模型（Band/CPL/PL） | 没有 | 无 |
| **Eiso** | 没有 | 需结合 fluence + 红移自行计算 |
| 红移 | 极少 | 余辉表 `redshift` 仅 22 行 |

**若需要 Epeak / 能谱模型，应改用 heasarc_batsegrbsp（BATSE 光谱目录）、heasarc_fermilgrb、heasarc_swiftgrb 等表（同在 FTP tdat_files 目录），GRBCAT 本身只有持续时间和流量类参数。**

## 发现的坑（重要）

1. **没有 Epeak/Eiso/能谱模型**——这是最大的预期偏差，GRBCAT 是"高层信息"汇编目录。
2. **误差置信度不统一**：t90_error、fluence_error 等均按原始文献照抄，HEASARC 文档未声明是 1σ 还是 90%；不同 observatory/文献之间混用，做统计样本时需谨慎。
3. **全部是观测系量**：T90、fluence 均为 observer frame，无静止系改正（红移也基本没有）。
4. **一行 ≠ 一个 GRB**：主表按 GRB×探测卫星分行（5831 个 GRB → 10119 行）；flux 表按 GRB×能段×文献分行。聚合时以 `id` 为准。
5. **缺失值是空字符串**（`||`），不是 NULL 记号；时间列是 MJD 浮点。
6. **流量/fluence 单位藏在单位列里**：`flux`/`fluence` 列是纯数值，物理单位由 `flux_units`/`fluence_units` 决定（photons vs ergs 差一个能谱形状因子，绝不能混用）。早期 VELA 源 fluence 甚至未标能段。
7. **T90/T50 能段基本缺失**：`t90_emin/emax` 仅 63 行非空，不能默认 BATSE 源就是 50–300 keV（虽然多数 BATSE-CGRO 记录文献上是该能段）。
8. **flux 表 2020 年后未更新**（主表和余辉表 2025 年仍在更新），新爆发（2020 年后）可能只有主表行而没有 fluence。
9. **tdat 文件头占约 77 行**，直接用 `wc -l` 统计会多算；务必抽取 `<DATA>`–`<END>` 段。
10. 余辉表 `redshift_error` 是字符串类型、`energy_range` 是单字母大类代码，均与直觉不符。

## MD5 校验（下载时）

```
fd9cfbfcbeddd9f5c4c24d3f9e74adc3  heasarc_grbcat.tdat.gz
57a6cfe17e7fde3c293207b16731a860  heasarc_grbcat.hdr.gz
f1bf6f5fb677718ef27ce2a3e3f2f1c2  heasarc_grbcatflux.tdat.gz
cd1e1e63fdf653337b371b7d8b9d2d96  heasarc_grbcatflux.hdr.gz
6698d72e0db1ef960aa08e7a50c2d3f4  heasarc_grbcatag.tdat.gz
653b5ee45c7320478c356a8fac948101  heasarc_grbcatag.hdr.gz
```
