# agile_mcal — The Second AGILE-MCAL GRB Catalog

- **目录名称**：The Second AGILE-MCAL GRB Catalog（AGILE 小型量能器 MCAL 第二版 GRB 目录）
- **主页 URL**：https://www.ssdc.asi.it/mcal2grbcat/
- **对应论文**：Ursi A. et al., ApJ 925, 152 (2022)，DOI: 10.3847/1538-4357/ac3df7（=2022ApJ...925..152U）
- **CDS/VizieR 编号**：J/ApJ/925/152
- **获取日期**：2026-07-21
- **数据覆盖**：2007-11 至 2020-11，AGILE MCAL 触发的 503 个爆发

## 下载 URL（均已于 2026-07-21 用 curl 实际下载验证）

| 文件 | URL | 说明 |
|---|---|---|
| `mcal2grbcat.html` | https://www.ssdc.asi.it/mcal2grbcat/ | 官方主页原始 HTML。**完整 503 行数据内嵌其中**（第 35 行起，每行一个 `new catEntry(...)` JS 调用） |
| `mcal2grbcat.js` | https://www.ssdc.asi.it/mcal2grbcat/mcal2grbcat.js | 上述内嵌表的列定义与逐列说明（官方） |
| `cds_ReadMe` | https://cdsarc.cds.unistra.fr/ftp/J/ApJ/925/152/ReadMe | CDS 机读表官方说明（逐字节格式定义） |
| `cds_table2.dat` | https://cdsarc.cds.unistra.fr/ftp/J/ApJ/925/152/table2.dat | 主表：503 个 GRB 的触发信息与 T50/T90 |
| `cds_table3.dat` | https://cdsarc.cds.unistra.fr/ftp/J/ApJ/925/152/table3.dat | 258 个定位 GRB 的单幂律（PL）谱拟合 |
| `cds_table4.dat` | https://cdsarc.cds.unistra.fr/ftp/J/ApJ/925/152/table4.dat | 43 个定位 GRB 的 Band 模型谱拟合 |

注意：SSDC 主页**没有**单独的 "download full table" 链接，全部数据以 JS 形式内嵌在主页 HTML 里；`mcal2grbcat.html` 即为官方完整机器可读数据（原样保存）。CDS 三个 `.dat` 为论文发表的定宽 ASCII 机读表，两套来源并存、互有出入（见"坑"一节）。

## 文件清单与行数核对

| 文件 | 实测行数 | 网站/论文声称 | 核对 |
|---|---|---|---|
| `mcal2grbcat.html` 内嵌表 | 503 条 `catEntry` | 页面文字："The catalog consists of 503 bursts" | ✅ 一致 |
| `cds_table2.dat` | 503 | ReadMe：503（476 确认 GRB + 27 未确认候选） | ✅ 一致（实测 476 行以 `GRB` 开头，27 行无前缀） |
| `cds_table3.dat` | 258 | ReadMe：258 | ✅ 一致 |
| `cds_table4.dat` | 43 | ReadMe：43 | ✅ 一致 |
| 网页内嵌表 PL 拟合行数 | 258 | — | ✅ 与 table3 一致 |
| 网页内嵌表 Band 拟合行数 | 43 | — | ✅ 与 table4 一致 |
| 网页内嵌表已定位（LOC 非空） | 363 | 页面文字："363 of which have been localized" | ✅ 一致 |
| MCAL 完整获取标志 Y | **393** | 论文摘要写 394 | ⚠️ 差 1（网页表与 CDS table2 均为 393） |
| 部分获取（I+F） | 110 | 论文摘要写 109 | ⚠️ 差 1 |

## 仪器与能段背景（重要）

- MCAL 是非成像闪烁量能器，灵敏能段 **0.4–100 MeV**（400 keV–100 MeV）。
- AGILE 科学计数率计（RM）覆盖 **20 keV–100 MeV**。
- 谱拟合按论文在 **0.4–50 MeV** 能段进行；但网页内嵌表逐行标注的 `PL_RANGE`/`BAND_RANGE` 实际为 **0.4–10 MeV（多数）或 0.4–50 MeV（少数）**，两者不一致，见"坑"。
- 所有时间（T50/T90）和谱参数均为**观测系（observer frame）**；目录不含红移，无静止系量。

## 爆发标识

- 名称格式：`GRB YYMMDDx`（如 `GRB071125A`），x 为当日序号字母（含小写，如 `GRB080413c`）。
- **27 个未被其他仪器确认的候选没有 `GRB` 前缀**，名字仅为 `YYMMDD`（如 `100707`），仅见于 MCAL 数据、无 IPN 匹配。
- 无独立触发编号；辅助标识有 AGILE MET（Mission Elapsed Time，秒）和轨道号（Orbit）。
- 坐标：网页内嵌表含 RA/Dec（J2000，度）+ 银经银纬 l/b（仅 363 个已定位源有值）；CDS table3/table4 只给银道坐标 GLON/GLAT。
- 定位来源（LOC / Obs）：GBM、XRT、IPN、LAT、BAT、SA（SuperAGILE）、INT/ISG（INTEGRAL）。

## 逐列文档

### A. 网页内嵌表（`mcal2grbcat.html` 中 `catEntry`，每行 44 个逗号分隔的引号字段）

字段顺序由 `mcal2grbcat.js` 的 `catEntry(...)` 定义（官方说明照录并翻译）：

| # | 列名 | 含义 | 单位 |
|---|---|---|---|
| 0 | NAME | GRB 名称 | — |
| 1 | RA | 赤经 J2000（度；页面另显示 hh mm ss） | deg |
| 2 | Dec | 赤纬 J2000 | deg |
| 3 | l | 银经 | deg |
| 4 | b | 银纬 | deg |
| 5 | T0 | 触发时间 UTC（`YYYY-MM-DDThh:mm:ss`） | — |
| 6 | MET | AGILE Mission Elapsed Time | s |
| 7 | Orbit | AGILE 轨道号 | — |
| 8 | RM_SA | SuperAGILE 计数率计探测类型 | Y/N/I/F/n |
| 9 | RM_AC | 反符合（AC）计数率计探测类型 | Y/N/I/F/n |
| 10 | RM_MCAL | MCAL 计数率计探测类型 | Y/N/I/F/n |
| 11 | MCAL | MCAL 探测类型：Y=完整，I=不完整，F=碎片化，N=未探测，n=无数据 | 标志 |
| 12 | BKG | MCAL 平均本底计数率 | Hz |
| 13 | T50 | 50% 持续时间（观测系） | s |
| 14 | err_T50 | T50 误差（置信度未在页面注明，见"坑"） | s |
| 15 | BKGSUB_CTS_T50 | T50 内 MCAL 去本底计数 | counts |
| 16 | T90 | 90% 持续时间（观测系） | s |
| 17 | err_T90 | T90 误差 | s |
| 18 | BKGSUB_CTS_T90 | T90 内 MCAL 去本底计数 | counts |
| 19 | LOC | 定位设施（GBM/XRT/IPN/LAT/BAT/SA/INT/ISG），空=未定位 | — |
| 20 | THETA | T0 时刻 AGILE 天顶角 | deg |
| 21 | PHI | T0 时刻 AGILE 方位角（与 CDS 的 phi 不一致，见"坑"） | deg |
| 22 | PL_RANGE | 幂律谱拟合能段（`0.4-10MeV` 或 `0.4-50MeV`） | — |
| 23 | PL_BETA | 幂律**光子指数**（负值，注意符号） | — |
| 24 | PL_BETA_emin | 光子指数下误差 | — |
| 25 | PL_BETA_emax | 光子指数上误差 | — |
| 26 | PL_RED_CHI_SQ | 幂律拟合约化 χ² | — |
| 27 | PL_DOF | 自由度 | — |
| 28 | PL_FLUX | 幂律模型流量 | erg cm⁻² s⁻¹ |
| 29 | PL_FLUENCE | 幂律模型 T90 内流量积分（fluence） | erg cm⁻² |
| 30 | BAND_RANGE | Band 模型拟合能段（`0.4-10MeV` 或 `0.4-50MeV`） | — |
| 31 | BAND_ALPHA | Band 低能光子指数 α | — |
| 32/33 | BAND_ALPHA_emin / emax | α 下/上误差 | — |
| 34 | BAND_BETA | Band 高能光子指数 β | — |
| 35/36 | BAND_BETA_emin / emax | β 下/上误差 | — |
| 37 | Ec | Band 模型"临界能量"（数值上 ≈ 折断能量 E₀，见"坑"） | keV |
| 38 | Ep | Band 模型**峰值能量**（观测系；均值 642 keV，与论文 ⟨Ep⟩=640 keV 一致） | keV |
| 39 | Eb | Band 模型"break energy"（定义不明，见"坑"） | keV |
| 40 | BAND_RED_CHI_SQ | Band 拟合约化 χ² | — |
| 41 | BAND_DOF | 自由度 | — |
| 42 | BAND_FLUX | Band 模型流量 | erg cm⁻² s⁻¹ |
| 43 | BAND_FLUENCE | Band 模型 fluence | erg cm⁻² |

### B. `cds_table2.dat`（定宽 ASCII，503 行，Lrecl=90）

| 字节(1-based) | 列名 | 含义 | 单位 |
|---|---|---|---|
| 1–3 | C | "GRB"=已被其他仪器确认；空=未确认候选（27 个） | — |
| 4–10 | GRB | 标识符 YYMMDDx | — |
| 12–33 | Obs.Y/M/D/h/m/s | 触发时间 UTC（年月日时分秒） | — |
| 35–36 | Conf | 星上配置 C1–C4（触发逻辑/灵敏度时期标志） | — |
| 38/40/42/44 | RM-SA / RM-AC / RM-MCAL / MCAL | 各探测器探测标志：Y=完整，N=无，I=不完整，F=碎片化，n=无数据 | — |
| 46–48 | Bkg | MCAL 能段平均本底率 [139/856] | Hz |
| 50–53 | l_T50 | T50 限值标志（`>=` 表示下限） | — |
| 55–61 | **T50** | 50% 持续时间 [0.007/128]，观测系 | s |
| 63–67 | e_T50 | T50 不确定度 [0.001/3] | s |
| 69 | f_T50 | `*`=基于不完整数据获取评估 | — |
| 71–74 | l_T90 | T90 限值标志（`>=`） | — |
| 76–82 | **T90** | 90% 持续时间 [0.012/213]，观测系 | s |
| 84–88 | e_T90 | T90 不确定度 [0.001/3] | s |
| 90 | f_T90 | `*`=不完整获取 | — |

### C. `cds_table3.dat`（258 行，单幂律 PL 拟合）

| 字节 | 列名 | 含义 | 单位 |
|---|---|---|---|
| 1–10 | C+GRB | 名称 | — |
| 12–14 | Obs | 定位设施 | — |
| 16–28 | GLON / GLAT | 银经 / 银纬 | deg |
| 30–42 | theta / phi | 爆发相对 AGILE 指向的 θ/φ 角 | deg |
| 44–49 | stat | 拟合统计量（cstat/pgstat 等） | — |
| 51–55 | **beta** | 幂律**光子指数**（负值） | — |
| 57–65 | e_beta / E_beta | β 的下/上 **1σ** 误差 | — |
| 67–71 | chi2 | 约化 χ² | — |
| 73–89 | **Flux** / e_Flux | 0.4–50 MeV 流量及误差（CDS 单位写作 mW/m²，**数值上等于 erg cm⁻² s⁻¹**） | erg cm⁻² s⁻¹ |
| 91–107 | **Flue** / e_Flue | 0.4–50 MeV fluence 及误差（CDS 单位 mJ/m² = erg cm⁻²） | erg cm⁻² |

### D. `cds_table4.dat`（43 行，Band 模型拟合）

| 字节 | 列名 | 含义 | 单位 |
|---|---|---|---|
| 1–10 | C+GRB | 名称 | — |
| 12–16 | stat | 拟合统计量 | — |
| 18–32 | alpha, e_alpha, E_alpha | Band 低能光子指数及下/上 **1σ** 误差 | — |
| 34–48 | beta, e_beta, E_beta | Band 高能光子指数及下/上 **1σ** 误差 | — |
| 50–62 | **Ep**, e_Ep, E_Ep | Band 峰值能量及下/上 **1σ** 误差 [428/1963]，观测系（**与网页表 Ep 列不一致，见"坑"**） | keV |
| 64–67 | chi2 | 约化 χ² | — |
| 69–94 | Flux/Flue 及误差 | 0.4–50 MeV 流量、fluence | erg cm⁻² s⁻¹ / erg cm⁻² |

## 误差置信度

- CDS table3/table4 的谱参数误差**明确为 1σ**（ReadMe 写明 "Lower/Upper 1σ uncertainty"），且为不对称双侧误差。
- T50/T90 的不确定度在网页和 CDS ReadMe 中均未注明置信度；按论文惯例应视为 1σ，使用论文结论前建议回查原文 Section 3。

## 发现的坑（务必阅读）

1. **网页表 Ep ≠ CDS 表 Ep**：对 43 个 Band 拟合源逐一比对，CDS `table4.dat` 的 Ep 与网页内嵌表的 Ep 列**全部不同**（17 个等于网页的 Eb 列，26 个三者都不等）。网页表 Ep 均值 642 keV 与论文摘要 ⟨Ep⟩=640 keV 吻合 → **建议采用网页表（mcal2grbcat.html）的 Ep 作为峰值能量**，CDS table4 的 Ep 使用前先回查论文 Table 4 定义。
2. **网页表的 Ec/Ep/Eb 三能量定义不透明**：以 GRB080407A 为例 Ec=237、Ep=420、Eb=686 keV，数值上满足 Ep≈(2+α)·Ec，即 Ec 像 Band 折断能量 E₀、Ep 是 νFν 峰值；Eb 含义不明。CDS 表只有一个 Ep。
3. **谱拟合能段逐行不同**：网页表 `PL_RANGE`/`BAND_RANGE` 为 `0.4-10MeV`（PL 201 行、Band 36 行）或 `0.4-50MeV`（PL 57 行、Band 7 行）；而 CDS ReadMe 声称 table3/table4 的 Flux/Fluence 均为 0.4–50 MeV。跨目录比较 fluence 时务必逐行确认能段。
4. **网页 PHI 与 CDS phi 不一致**：θ 角两者一致，但 φ 角多数源不同且无固定偏移（仅 23/258 完全相同），原因不明；需要仪器坐标系角度时建议用 CDS table3 的 theta/phi 并回查论文定义。
5. **缺失值记号**：网页内嵌表用空字符串 `""` 表示缺失（未定位源 RA/Dec/l/b/LOC/谱参数全为空）；CDS 定宽表中限值用 `>=` 前缀标志列（l_T50/l_T90，共 110 行为下限，对应不完整获取），不完整获取另有 `*` 标志列。
6. **名称陷阱**：27 个未确认候选无 `GRB` 前缀（纯 `YYMMDD`），做名称匹配/连接时会被漏掉；另有小写字母后缀（`GRB080413c`）。
7. **数量小出入**：论文摘要称完整获取 394、部分获取 109，网页表与 CDS table2 实测均为 393（Y）和 110（I=97 + F=13）。
8. **网页数据无独立下载端点**：完整表只能从内嵌 JS 解析（每行 `this[N] = new catEntry(...)`，44 个引号分隔字段），我们已原样保存 HTML 与列定义 JS。
9. **CDS 单位标注**：`mW/m2`、`mJ/m2` 只是 CDS 标准单位写法，数值上分别等于 erg cm⁻² s⁻¹ 和 erg cm⁻²，无需换算。
10. **光子指数符号**：`PL_BETA`/`BAND_BETA` 为负值（光子指数，dN/dE ∝ E^β）；与某些目录（如 GBM 用正能量子谱指数）习惯不同，跨库合并时注意。
