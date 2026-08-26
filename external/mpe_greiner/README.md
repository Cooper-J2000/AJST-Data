# mpe_greiner — Greiner GRB 定位总表（Catalog of GRB localizations）

- **目录名称**：Jochen Greiner's GRB page（"GRBs localized with BeppoSAX/BATSE/IPN/HETE/INTEGRAL/Swift/AGILE/Fermi/MAXI/EP/SVOM ..."），维护者 Jochen Greiner（MPE，jcg@mpe.mpg.de）
- **主页 URL**：https://www.mpe.mpg.de/~jcg/grbgen.html
- **数据文件下载 URL**：
  - https://www.mpe.mpg.de/~jcg/grbgen.html （主表，单文件完整 HTML 表格，无分页）
  - https://www.mpe.mpg.de/~jcg/grbrsh.html （附属红移汇总页，含各红移的文献出处）
- **获取日期**：2026-07-21（UTC）
- **页面标注的最后更新**：29-May-2026

## 重要说明（先说结论）

**该目录不包含 T90、Epeak、fluence、Eiso 等瞬时辐射（prompt emission）参数。**
它是一个"已快速定位 GRB"的索引总表：GRB 名称、X 射线/伽马射线位置、定位误差、
定位仪器、是否有 IPN 探测/X 射线余辉/光学余辉/射电余辉、红移。
价值在于作为**权威的外部源清单 + 位置 + 红移**交叉证认基准；
T90/Epeak/fluence 需从其他目录（Fermi-GBM、Swift-BAT、Konus-Wind 等）获取。

**没有官方机器可读下载渠道**：页面源码中无任何 ASCII/FITS/CSV/FTP 下载链接，
目录索引未开放；HEASARC W3Browse/FTP 中也未找到该表的官方镜像（已尝试
table-search / table-list 检索 "greiner"，无结果）。唯一的"完整数据文件"就是
这个单文件 HTML 表格本身（1.4 MB，非分页），已原样保存。

## 文件清单

| 文件 | 格式 | 大小 | 说明 |
|---|---|---|---|
| `grbgen.html` | HTML 4（latin-1 编码） | 1,462,448 B | 主表：2948 个 GRB 条目 + 文末年度统计小表 |
| `grbrsh.html` | HTML | 19,216 B | 附属页：GRB 红移列表及每条红移的文献链接（GCN/astro-ph） |

md5（2026-07-21 下载）：
- `grbgen.html` = `14508e52a3f61af7fd42414f10aa9be9`
- `grbrsh.html` = `5ba80e0bee4bf368ea20b42dc9646330`

## 行数核对

- 主表实测 **2948 行数据**（Python 正则解析 `<TR>...<TD>` 结构，2948 行 × 10 列，
  GRB 名均唯一），其中 **764 行有红移值**。
- 网站年度统计小表自报合计 **2878**（仅覆盖 1997–2025）；主表按年份拆分：
  1996 年 1 个、2026 年 68 个（统计小表尚未计入），2878 + 1 + 68 = 2947，
  与实测 2948 差 1（2025 年主表 224 个 vs 统计表 223 个，统计表滞后 1）。
  结论：实测 2948 与网站口径自洽，差异来自统计小表更新滞后。

## 逐列文档（grbgen.html 主表）

| # | 列名（页面表头） | 物理含义 | 单位 / 取值 |
|---|---|---|---|
| 1 | GRBᵃ | GRB 名称，格式 `yymmddx`（如 `260527A`）。后缀字母见脚注ᵃ | 字符串 |
| 2 | GRB X-ray position | 位置（RA + Dec），**历元未注明（实际为 J2000）**；这是伽马/X 射线探测器给出的位置，与光学/NIR/射电位置可能差几个角分 | `HHhMMmSSs ±DD° MM'`（多数无秒以下精度，Dec 只到角分） |
| 3 | Error | 定位误差半径；椭圆误差框写作 `长轴*短轴`（如 `186*2.6`） | **角分（arcmin）** |
| 4 | Instrument | 提供亚角分定位的仪器（Swift、EP、SVOM、Fermi、MAXI、IPN、INTEGRAL、GOTO、MASTER、ZTF、DDOTI、TESS、LEIA、SRG、HXMT、AGILE、CALET 等）。2023 年起宽视场光学巡天发现对应体时填光学巡天名而非伽马仪器（页面自己承认不一致） | 字符串 |
| 5 | IPNᵇ | 是否有行星际网络（IPN）探测 | `y` / 空（少数 `n`、`?`） |
| 6 | XAᵇ | 是否有 X 射线余辉 | `y` / 空 |
| 7 | OTᵇ | 是否有光学（或红外）暂现源 | `y` / 空（少数 `n`、`?`、`y?`） |
| 8 | RAᵇ | 是否有射电余辉 | `y` / 空 |
| 9 | IAUC | 是否有 IAU Circular | `y` / 空 |
| 10 | zᶜ | 红移（**观测系数值**，静止系量需自行用 1+z 换算）。后缀：`ul`=上限，`<x`=上限，`ph`=测光红移，`h`=宿主星系红移，`phh`=宿主测光红移，范围形如 `1.179-2` | 无量纲 |

页面脚注原文要点：
- (a) 日期后的 "X" = 无伽马探测、X 射线性质类似 GRB 的 XRF；"B" = 当天第二个 GRB；
  **"S" = 短暴（有争议的不标记）**。主表中带 S 后缀共 236 个。
- (b) IPN = 行星际网络探测；XA = X 射线余辉；OT = 光学/IR 暂现源；RA = 射电余辉；z = 红移。
- (c) ul = 上限；ph = 测光红移；h = 宿主星系红移；phh = 宿主测光红移。

**能量范围 / 能谱模型 / 误差置信度：本表不含任何能谱与流量列，故无能量范围、
Band/CPL 模型、1σ/90% 置信度等标注问题。** 定位误差列（第 3 列）的置信度
页面未说明（各仪器 GCN 原始通报惯例不一，通常 90% 半径，使用时需注意）。

## 爆发标识

- 名称格式：`yymmddx`，如 `260527A`；后缀 `S` 表示短暴（合并在名称里，如 `260527AS`）。
- **无触发编号**（无 Swift trigger / Fermi bn 号），如需与触发号关联须借助其他目录。
- 每个名称有超链接指向单爆页面 `grbyymmddx.html`（含 GCN 通报与文献汇编，未抓取）。
- 坐标：有（第 2 列），但精度不一，IPN 条目误差可达数百角分（3σ 误差框）。

## 已发现的坑

1. **HTML 注释中的模板行**：主表开头有被 `<!-- ... -->` 注释掉的占位行
   （如 260501A），解析前必须先剔除注释，否则会多计行。
2. **`<TR>` 未闭合**：HTML 4 风格，行尾没有 `</TR>`，不能用配对正则，应按 `<TR` 切分。
3. **缺失值记号**：空单元格用 `&nbsp;`；红移后缀（ul/ph/h/phh/`<`/范围）混在数值列里，
   解析成 float 前要剥离。
4. **误差列的 `*`**：`长轴*短轴` 是椭圆误差框，不是乘号运算；IPN 条目常见（402 行）。
5. **坐标格式不统一**：RA 有时分秒，Dec 只有度+角分（无秒）；个别行有空格错位
   （如 `+0 5° 19'`）；多行 RA/Dec 之间是换行符。位置不是光学对应体位置，注意页面 NOTE。
6. **Instrument 列口径变化**：2023 年前是 X/γ 仪器，之后可能是光学巡天（ZTF、GOTO、
   MASTER 等），不可直接当作"探测仪器"。
7. **名称后缀 X**（XRF）在近年条目中基本不再使用，主要见于 HETE 时代。
8. 编码为 **latin-1**（`&#176;` 为度符号），按 UTF-8 读可能报错。
9. 年度统计小表在主表之后同一文件内，解析时需以 "GRB and afterglow statistics" 分界，
   避免把统计行当数据行。

## 已尝试但未成功的获取途径

- 页面及页面源码全文检索 ascii/ftp/download/.txt/.dat/.fits/.csv：无任何下载入口。
- `https://www.mpe.mpg.de/~jcg/` 目录索引：未开放（只返回首页）。
- HEASARC W3Browse `table-search.pl` / `table-list.pl` 检索 "greiner"：无对应表。
