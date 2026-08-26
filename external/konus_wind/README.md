# konus_wind — Konus-Wind 带红移 GRB 目录（Tsvetkova+ 2017 & 2021）

- **来源论文**：
  - Paper I：Tsvetkova et al. 2017, ApJ, 850, 161（2017ApJ...850..161T）——
    Konus-Wind（KW）**触发模式**带红移 GRB 目录，1997-02 至 2016-06，150 个暴。
  - Paper II：Tsvetkova et al. 2021, ApJ, 908, 83（2021ApJ...908...83T）——
    KW **等待模式** + Swift/BAT 联合样本，2005-01 至 2018 年底，167 个弱而软的暴。
  - 两年样本**互不重叠**（实测 150+167=317，无同名暴），合并后 317 条记录。
- **VizieR 目录**：J/ApJ/850/161 与 J/ApJ/908/83
- **数据文件下载 URL**（VizieR TAP 同步端点，`SELECT *`，FORMAT=csv）：
  - `https://tapvizier.cds.unistra.fr/TAPVizieR/tap/sync?...QUERY=SELECT * FROM "J/ApJ/850/161/grbs"`
  - 同上 `.../table3`、`.../table5`、`"J/ApJ/908/83/table1"`、`table2`、`table4`、`table5`
- **ReadMe 原文**：`https://cdsarc.cds.unistra.fr/ftp/J/ApJ/850/161/ReadMe`
  和 `https://cdsarc.cds.unistra.fr/ftp/J/ApJ/908/83/ReadMe`（已保存为
  `ReadMe_2017.txt` / `ReadMe_2021.txt`）
- **获取日期**：2026-07-21（UTC）

## 文件清单

| 文件 | 行数 | 说明 |
|---|---|---|
| `J_ApJ_850_161_grbs.csv` | 150 | 2017 合并主表（VizieR 把论文 table1+table2+table4 合并）：名称、KW 触发时刻、z、T100/T90/T50、谱延迟 tlagG2G1/G3G1/G3G2、fluence S、峰流量、Eiso、Liso |
| `J_ApJ_850_161_table3.csv` | 513 | 2017 谱参数：每暴 i（时间积分）/p（峰）两类谱，部分暴多个模型；`f_SMod=yes` 为 BEST 模型 |
| `J_ApJ_850_161_table5.csv` | 41 | 2017 准直改正能量学（32 个暴；无偏好介质时同一暴给 HM/WM 两行） |
| `J_ApJ_908_83_table1.csv` | 167 | 2021 样本主表：名称、BAT 触发号 NumID、BAT 触发时刻 Time、z |
| `J_ApJ_908_83_table2.csv` | 365 | 2021 谱参数（i/p 两类，单一最优模型） |
| `J_ApJ_908_83_table4.csv` | 167 | 2021 能量学：Eiso/Liso 含**上下不对称** 1σ 误差 |
| `J_ApJ_908_83_table5.csv` | 22 | 2021 准直改正能量学（14 个暴，Egamma 含不对称误差） |
| `ReadMe_2017.txt` / `ReadMe_2021.txt` | — | VizieR 官方列说明（单位、误差定义） |
| `parse.py` | — | 解析器（仅标准库），可重跑 |
| `normalized.jsonl` | 317 | 解析输出（契约见 `../SCHEMA.md`） |

行数与 ReadMe 声明的记录数完全一致（150/513/41；167/365/167/22）。

## 字段映射（源表列 -> normalized 键）

### params

| normalized 键 | 来源列 | 换算 / 说明 |
|---|---|---|
| `redshift` | 2017 grbs.`z`；2021 table4.`z` | 原样。红移类型（spectroscopic/photometric）放 `other.z_type` |
| `tlag` | 2017 grbs.`tlagG2G1` ± `e_tlagG2G1` | 观测系谱延迟（正值=软光子延迟），`band="G2/G1 (70-300/20-70 keV)"`，`frame="obs"`，对称 1σ 误差。**只取 G2/G1 一组**进 params；G3/G1、G3/G2 两组原样放 `other` |
| `eiso` | 2017 grbs.`Eiso` ± `e_Eiso`；2021 table4.`Eiso` ± `e_Eiso`/`E_Eiso` | 原始单位 1e44 J = **1e51 erg**，乘以 1e51 输出 erg；`band="1-10000 keV"`，`frame="rest"`。2017 为对称误差，2021 为不对称 `[正,负]` |
| `lp_iso` | 2017 grbs.`Liso` ± `e_Liso`；2021 table4.`Liso` ± `e_Liso`/`E_Liso` | 原始单位 1e44 W = **1e51 erg/s**，乘以 1e51 输出 erg/s；能段/参考系同 eiso |
| `epeak` | 2017 table3 / 2021 table2 中 **i（时间积分）谱**的 `Ep` ± `e_Ep`/`E_Ep` | 观测系 keV，原样；不对称误差 `[E_Ep, e_Ep]`；`model` 取该行谱模型（CPL/BAND/PL），`frame="obs"`。2017 优先取 `f_SMod=yes`（BEST 模型）的 i 谱行；PL 谱无 Ep，该暴省略 epeak |
| `e_gamma` | 2017/2021 table5.`Egamma` ± 误差 | 原始单位 1e42 J = **1e49 erg**，乘以 1e49 输出 erg；`frame="rest"`。同一暴含 HM/WM 两行时按论文做法取**几何平均**（2021 ReadMe note 1；2017 同样处理，见"假设"） |

### 顶层字段

- `name`：`GRB yymmddX`。2017 `GRB` 列是 `YYMMDDA`（字母可缺），2021 `ID` 列是
  `GRByymmddX`，统一加空格。
- `trigger_time`：
  - 2017：grbs.`Trig` 列。VizieR 列描述写的是 "Hour of KW trigger time"，但实际值是
    **当日毫秒数**（DOUBLE）。已对照原始 `table1.dat` 的 h/m/s 分列验证
    （如 GRB 990123 = 35234151 ms = 09:47:14.151 UT；GRB 030329 = 41849254 ms =
    11:37:29.254 UT，与 Konus GCN 通报一致）。日期由暴名推出。
  - 2021：table1.`Time`（`hh:mm:ss.fff`，Swift/BAT 触发时刻 UT）+ 暴名日期。
- `ra`/`dec`：两表 `_RA`/`_DE` 列。**注意：这是 VizieR 从 SIMBAD 补的 J2000 坐标，
  不是论文原始数据**（VizieR 列描述明确注明 "not part of the original data"）。
- `name_alt`：2021 有 Swift/BAT 触发号，记为 `"BAT <NumID>"`；2017 无别名。

### other（原样保留的重要原始列，键名=原列名）

- 2017：`Type`（I/II 型分类）、`Inst`、`Det`、`n_z`、`z_type`、`f_z`、`T100`、
  `T90`±`e_T90`、`T50`±`e_T50`、`Angle`（度）、`tlagG3G1`±err、`tlagG3G2`±err（s）、
  `S`±`e_S`/`E_S`（fluence，**1e-9 J/m² = 1e-6 erg/cm²**）、
  `Fp1024`/`Fp64`±误差（峰流量，**1e-9 W/m² = 1e-6 erg/cm²/s**）、`Flim`、`Zmax`、
  `tjet`（d）、`theta`（度）、`CBM`、`Lgamma_1e49erg_s`、`spec_alpha`/`spec_beta`/
  `spec_tstart`/`spec_DeltaT`（BEST i 谱的指数与积分区间）。
- 2021：`T100`、`t0_T100_start`、`z_type`、`S`±误差（**1e-10 J/m² = 1e-7 erg/cm²**）、
  `Fp1024`/`Fp64`±误差（**1e-10 W/m² = 1e-7 erg/cm²/s**）、`tjet`、`theta`、`CBM`、
  `Lgamma_1e49erg_s`、`spec_dT`。
- 两年同名 other 键冲突时，2021 值保留原名，2017 值改名 `<键>_2017`（本样本无重名暴，
  实际未触发）。

## 单位换算汇总

| 量 | VizieR 单位 | 换算因子 | 输出单位 |
|---|---|---|---|
| Eiso | 1e44 J | ×1e51 | erg |
| Liso | 1e44 W | ×1e51 | erg/s |
| Egamma / Lgamma | 1e42 J / 1e42 W | ×1e49 | erg / erg/s |
| Ep | keV | 1 | keV（obs） |
| tlag / T90 / T100 | s | 1 | s（obs） |
| S（2017 / 2021） | 1e-9 / 1e-10 J/m² | ×1e-6 / ×1e-7 | erg/cm²（仅入 other，未换算） |
| Fp（2017 / 2021） | 1e-9 / 1e-10 W/m² | ×1e-6 / ×1e-7 | erg/cm²/s（仅入 other，未换算） |

Eiso/Liso 的能段 `1-10000 keV` 是**静止系**能段（两篇论文均按 KW 惯例在
rest-frame 1 keV–10 MeV 内计算）。

## 关键假设与处理约定

1. **2017 `Trig` 列编码**：列描述称 "Hour of KW trigger time"，实际为当日毫秒数
   （详见上文 trigger_time 说明），已逐值对照原始 dat 文件验证。
2. **epeak 取 i 谱**：每暴有 i/p 两类谱，params.epeak 统一取时间积分谱（i），
   2017 进一步限定 BEST 模型（`f_SMod=yes`）；p 谱的 Ep 不取。
3. **table5 多介质行几何平均**：同一暴有 HM（均匀介质）和 WM（星风介质）两行时，
   Egamma 及误差取几何平均，`other.CBM` 记为 `"HM/WM(geomean)"`。2021 ReadMe note 1
   明确此做法；2017 无明确说明，沿用同一规则（假设）。
4. **0 值视为缺失**：`Ep=0`、`Eiso/Liso=0`、误差=0 在表中是占位缺测（VizieR 区间
   标注 `?`），解析时按缺失处理（如 GRB 171205A 的 Liso=0 → 省略 lp_iso；
   GRB 080413B 为 PL 谱无 Ep → 省略 epeak）。
5. **谱延迟只入一组**：SCHEMA 的 `tlag` 是单值键，params 只放 G2/G1 延迟
   （最常用的一组），G3/G1 与 G3/G2 原样入 other。KW 通道能段取论文标称值
   G1≈20-70、G2≈70-300、G3≈300-1160 keV（精确边界随探测器增益略有变化）。
6. **合并优先级**：两年目录无重名暴（triggered vs waiting-mode 样本互斥），
   但 parse.py 仍实现"互补键合并、同键 2021 优先"的规则以备后续版本变化。
7. **ra/dec 非论文原始数据**：来自 VizieR/SIMBAD（见上）。
8. 误差均为 1σ；2017 对称、2021 不对称（`[正,负]`）。

## 重跑

```bash
python3 parse.py   # 读同目录 7 个 CSV，生成 normalized.jsonl
```
