# Swift-XRT GRB Catalogue（swift_xrt_live）

- **目录名称**：The Swift-XRT GRB Catalogue（UKSSDC，莱斯特大学；Evans et al. 2009, MNRAS, 397, 1177 的在线实时更新版）
- **主页 URL**：https://www.swift.ac.uk/xrt_live_cat/
- **文档页**：https://www.swift.ac.uk/xrt_live_cat/docs.php（本目录已保存副本 `docs.html`）
- **获取日期**：2026-07-21

## 数据文件下载 URL

主页表格由 JavaScript 动态加载，其背后的**机器可读 ASCII 端点**（页面 "Select columns and formatting options" → Output: ASCII 所调用的官方接口）为：

```
https://www.swift.ac.uk/xrt_live_cat/getTable_txt.php?ascii=2&sumcols=,ra,dec,poserr,numbreaks,lctype,gal,z&acols=,1,1e,2,2e,3,3e,4,4e,5,5e,6,6e&bcols=,1,1e,2,2e,3,3e,4,4e,5,5e&nhwtcols=,1,1e,2,2e,3,3e,4,4e,5,5e,6,6e&gwtcols=,1,1e,2,2e,3,3e,4,4e,5,5e,6,6e&fwtcols=,1,1e,1u,2,2e,2u,3,3e,3u,4,4e,4u,5,5e,5u,6,6e,6u&nhpccols=,1,1e,2,2e,3,3e,4,4e,5,5e,6,6e&gpccols=,1,1e,2,2e,3,3e,4,4e,5,5e,6,6e&fpccols=,1,1e,1u,2,2e,2u,3,3e,3u,4,4e,4u,5,5e,5u,6,6e,6u&tavwtcols=,nh,nhe,gamma,gammae,flux,fluxe,fluxu&tavpccols=,nh,nhe,gamma,gammae,flux,fluxe,fluxu&fcols=,flux11,flux24&sex=&sex=0
```

即 `getTable_txt.php` 选择全部列、坐标用十进制（`sex=0`）。该 URL 已用 curl 实际下载验证（HTTP 200，内容完整）。

> 注意：这是 **X 射线余辉** 目录，**不含 T90、Epeak、γ 射线 fluence、Eiso 等瞬时辐射参数**。需要这些参数请用 BAT 侧目录（如 HEASARC 的 `swiftgrb` / swiftbat 表）。本目录可提供的相关量是：XRT 位置、红移、银心 N_H、X 射线光变衰减指数/拐折时间、各阶段 X 射线能谱（N_H、光子指数 Γ、0.3–10 keV 流量）以及 11/24 小时 X 射线流量。

## 文件清单

| 文件 | 说明 | 行数 |
|---|---|---|
| `swift_xrt_live_cat_full.txt` | 完整目录 ASCII 表（管道符 `|` 分隔，原样保存未修改） | 1730 行 = 1 行 `<pre>` 标签 + 1 行表头 + **1727 行数据** + 1 行空行 |
| `docs.html` | 官方在线文档页（docs.php）原样副本，供查阅 | — |

**行数核对**：实测数据行 1727（其中 1725 行以 `GRB ` 开头，另有 2 个特殊命名源：`Swift J164449.3+573451`、`SGR 1830-0645`），覆盖 2004-12-18 至 2026 年 1 月。网站未在页面上声称总数（文档仅说明 Evans et al. 2009 原始论文含 327 个 GRB，此后持续自动更新），因此 1727 即为本快照实测值；该目录是 "live" 的，重新下载行数会变化。每行均为 130 列（129 个 `|` 分隔符），各行列数一致。

## 逐列文档（共 130 列）

通用约定：

- **所有误差均为 90% 置信水平**（页面与文档明确声明，不是 1σ）。
- 误差为**双边不对称误差**，在同一字段内写成 `+上, -下`（例：`+0.20, -0.19`）；缺失时该字段为 `, `。
- 数值中嵌有 HTML 实体：`1.75&times;10<sup>-2</sup>` 表示 1.75×10⁻²，解析时必须先做 HTML 反转义/清洗。
- 缺失值记号为 `N/A`。
- 能谱模型：均为**吸收幂律**（phabs_银河 × phabs 或 zphabs_本征） × powerlaw，XRT **0.3–10 keV** 能段；Γ 为光子指数（N(E)∝E^−Γ，注意图中用的能量指数 β=Γ−1）。**没有 Band/CPL 模型，没有 Epeak**。
- 银心吸收 N_H 固定为 Kalberla et al. (2005) 的值；已知红移时本征吸收用 zphabs（红移固定），否则用 phabs（z=0）。
- 时间均为**观测系**、自 BAT 触发时刻起算的秒数（observer frame；本目录不做静止系改正）。
- 流量单位 erg cm⁻² s⁻¹，能段 0.3–10 keV；"Obs" 为观测流量（未改正吸收），"Unabs" 为吸收改正后流量。

| # | 列名 | 物理含义 | 单位 |
|---|---|---|---|
| 1 | GRB | 爆发名称（见下节） | — |
| 2 | RA | XRT 最佳位置赤经（J2000，优先 enhanced position，否则 PSF 拟合位置） | deg |
| 3 | Dec | XRT 最佳位置赤纬（J2000） | deg |
| 4 | Err90 | 位置误差半径（90% 置信） | arcsec |
| 5 | #breaks | 最佳拟合光变曲线中幂律拐折个数（0–5） | — |
| 6 | lc type | 光变分类：Canonical / One-break / No breaks / Oddball / TBD | — |
| 7 | NH_gal | 视线方向银河 N_H（Kalberla et al. 2005），谱拟合中固定 | **10²² cm⁻²** |
| 8 | Redshift | 已发表光谱红移（无则 N/A） | — |
| 9–15 | Ave_NH_wt, Ave_dNH_Wt, Ave_Gamma_WT, Ave_dgamma_WT, Ave_obs_flux_WT, d_Ave_obs_flux_WT, Ave_unabs_flux_WT | **时间平均谱（WT 模式）**：本征 N_H（10²² cm⁻²）、光子指数 Γ、观测流量、吸收改正流量及各自 90% 误差 | 见上 |
| 16–22 | Ave_NH_PC … Ave_unabs_flux_PC | 同上，**PC 模式** | 见上 |
| 23 | Flux_11 | 最佳拟合光变模型在 **触发后 11 小时**的 0.3–10 keV 流量（E09 Table 6 定义） | erg cm⁻² s⁻¹ |
| 24 | Flux_24 | 同上，触发后 **24 小时**（网站后来新增，E09 原文只有 F11） | erg cm⁻² s⁻¹ |
| 25 起，按 phase i=1..6 循环 | alpha_i, D_alpha_i | 第 i 段幂律衰减指数（F∝t^−α，正值为衰减）及 90% 误差 | 无量纲 |
| | break_i, D_break_i（i=1..5） | 第 i 个拐折时间（自触发起算，**观测系**）及 90% 误差 | s |
| | NH_i (wt/pc), D_NH_i (wt/pc) | 第 i 段时间分辨谱本征 N_H（WT/PC 模式分别给出） | 10²² cm⁻² |
| | Gamma_i (wt/pc), D_Gamma_i (wt/pc) | 第 i 段光子指数 | 无量纲 |
| | Obs Flux_i (wt/pc), D_Obs Flux_i (wt/pc) | 第 i 段 0.3–10 keV 观测流量 | erg cm⁻² s⁻¹ |
| | Unabs Flux_i (wt/pc) | 第 i 段 0.3–10 keV 吸收改正流量（无误差列） | erg cm⁻² s⁻¹ |

phase i 的列块结构（i=1..5）：`alpha_i, D_alpha_i, break_i, D_break_i, NH_i(wt), D_NH_i(wt), NH_i(pc), D_NH_i(pc), Gamma_i(wt), D_Gamma_i(wt), Gamma_i(pc), D_Gamma_i(pc), ObsFlux_i(wt), D_ObsFlux_i(wt), UnabsFlux_i(wt), ObsFlux_i(pc), D_ObsFlux_i(pc), UnabsFlux_i(pc)`；i=6 无 break 列。绝大多数源只有 0–2 个拐折，后续 phase 列全为 N/A。

## 爆发标识

- 名称格式为 `GRB yymmddx`（如 `GRB 260127A`），与 BAT 触发命名一致；个别非典型源用专名（`Swift J164449.3+573451`、`SGR 1830-0645`）。
- 表中**没有触发编号（trigger ID）列**，但官网按源查询接口 `getBurst.php?name=` 同时接受 GRB 名和触发号，可逐源映射（E09 论文表中给过 target ID / T90，在线表已移除）。
- 坐标：每源给出 RA/Dec（本快照为十进制 J2000）和 90% 误差半径。

## 已发现的坑

1. **首行是 HTML**：第 1 行为 `<pre id='indexPre'>`，表头在第 2 行，解析时需跳过。
2. **HTML 实体混入数值**：科学计数法写作 `&times;10<sup>-2</sup>`，必须清洗后才能转 float（如 `4.07&times;10<sup>-2</sup>` → 4.07e-2）。银河 N_H 因此实际是 ×10²² cm⁻² 单位下的数值（例：4.07×10⁻² = 4.07×10²⁰ cm⁻²）。
3. **误差与数值同列且不对称**：误差列内容形如 `+0.20, -0.19`，需拆成两列；缺失误差是 `, `（逗号+空格）而非 N/A。
4. **N_H 单位陷阱**：所有 N_H 列单位是 10²² cm⁻²，且**拟合值可能为 0 或极小**（如 1.79×10⁻⁷，即拟合打到下界），此时上误差仍有意义、下误差等于值本身。
5. **lc type = TBD**：新爆发（触发未满 ~24 小时或光变形态不明）分类为 TBD，相关列可能全 N/A；该表是 live 的，同一源重新下载参数可能更新（官方说明新爆发在触发 24 小时后才会入库）。
6. **无 T90/Epeak/fluence/Eiso**：本目录纯 X 射线余辉参数；瞬时辐射参数需另接 BAT 目录。
7. **Flux_11/Flux_24 无误差列**，且只有光变覆盖/可外推到该时刻的源才有值；E09 未明确说明是否改正吸收（XRT 光变曲线库的惯例是吸收改正后的 0.3–10 keV 流量），如需严格使用请核对 xrt_curves 文档。
8. **WT/PC 列成对出现且互不覆盖**：同一 phase 可能只有 WT 或只有 PC 数据（取决于观测模式），合并时不能假设两列都有值。
9. `alpha` 为观测系衰减指数；跨 phase 的 "steep-to-shallow" 等分类判据见 docs.html，自动化拟合可能有误（官方自称耀发识别假阳性/假阴性约 3%）。
