# 外部数据导入说明（grbcata_source_2.md 批次）

> 日期：2026-07-22
> 执行：Kimi Code（按 SCHEMA.md 契约与既有流程）
> 数据源清单：`grbcata_source_2.md`（项目内部清单文件，未随本仓库发布）

---

## 一、批次内容核对

清单 12 条中 **9 条已在 grbcata_source.md 批次导入过**，本次不重复处理：

| 清单条目 | 状态 |
|---|---|
| FERMILGRB / GRBCAT / GRBCATFLUX / GRBCATAG / SWIFTGRB / FERMIGBRST | 已导入（对应 `fermi_lat` / `heasarc_grbcat` / `swift_grb` / `fermi_gbm`） |
| Swift GRBlist redshift BAT / summary burst durations / General summary | 已导入（`swift_bat` 的组成文件） |
| **SAXGRBMGRB** | **本批新增** |
| **RSSGRBAG** | **本批新增** |
| **SWIFTGRBBA** | **本批新增** |

## 二、三个新源的 Parameters 确认与入库位置

### 2.1 saxgrbmgrb — BeppoSAX/GRBM GRB 目录（1082 行）

- 原始文件：`external/saxgrbmgrb/heasarc_saxgrbmgrb.tdat.gz`（HEASARC FTP 镜像）
- 时间覆盖 1996-07 ~ 2002-04；名称全部唯一（GRB yymmddX）
- 入库参数（→ `extra_data.catalog_data.saxgrbmgrb`）：
  - `t90`（观测系，能段逐源不同）、`fluence`（**40–700 keV**，erg/cm²）、`spectral_index`（PL 光子指数）
  - `other`：Tdet/Ta 两套持续时间定义、**峰值能量流量**（erg/cm²/s，注意不是光子流量，故不放 params.peak_flux）、ref_position
- 无 Epeak/Eiso（GRBM 双通道无法拟合谱峰）
- 坑：GRB 980425 在该目录名为 **GRB 980425B**（同日另有 980425A），跨目录匹配靠名称+触发时刻双重校验

### 2.2 swiftgrbba — Swift Burst Advocate 汇编（2036 行）

- 原始文件：`external/swiftgrbba/heasarc_swiftgrbba.tdat.gz`
- 时间覆盖 2004-12 ~ 2026-02；含 Fermi/INTEGRAL/SVOM 触发的暴
- 入库参数（→ `catalog_data.swiftgrbba`）：
  - `t90`（15–150 keV）、`fluence`（15–150 keV，**90% 置信**，标 `cl:90`）、
    `peak_flux`（1 s 光子流量，15–150 keV）、`spectral_index`（PL/CPL，模型在 other）、`redshift`（460 条）
  - `other`：XRT 初始衰减指数（带符号负值）、XRT Γ/N_H、early/11hr/24hr 流量（0.3–10 keV）
- 362 行为官方无后缀名（如 GRB 060729）→ 按日期+坐标匹配
- 11 行 MJD 仅日期精度 → trigger_time=null

### 2.3 rssgrbag — 射电余辉目录（Chandra & Frail 2012, ApJ 746, 156）（304 行）

- 原始文件：`external/rssgrbag/heasarc_rssgrbag.tdat.gz` + CDS `table4.dat`（交叉校验）
- 入库参数（→ `catalog_data.rssgrbag`）：
  - `t90`、`fluence`（15–150 keV）、`eiso`（静止系 1–10000 keV）、
    `e_gamma`（准直修正能量，61 条）、`redshift`（156 条，含 9 个上限）
- **射电流量密度点（→ `lightcurves` 表）**：`external/rssgrbag/lightcurve.jsonl`，
  每源每频段 1 个**峰值点**（峰时 + mJy 流量密度）。
  ⚠️ 注意：论文汇编的 2995 次逐历元测量未电子化发表，机读版只有峰值表，
  故入库的是"峰值点"而非完整射电光变曲线
  - `method=fit`（87 点，激波公式拟合，有误差）/ `method=data`（53 点，直接取值，无误差）
  - 频段：1.38–43 GHz 共 15 种（主峰 8.46 GHz 66 点、4.86 GHz 34 点）

## 三、匹配与去重规则

1. 沿用 `catalog_merge.py` 的 Matcher：精确名（含 aliases）→ 字母约定差异坐标 ≤1.5° →
   无字母名按日期+坐标（阈值按目录精度）
2. 射电点导入前对 13 个待新建源逐一做最近邻检查，**全部 ≥1.3°，确认非重复**：
   GRB001007/001018/011030/020305/021206/030227/030418/030723/050509C/050713B/100413A/980519/981226
3. 新建源基础信息取自本目录（ra/dec/t0/红移），`comment` 注明来源
4. **GRB100413A 与 GRB981226**：与此前删除的 wang2022 stub 是同一物理事件，
   本次以 rssgrbag 为来源重建（wang2022 数据仍保持删除状态）
5. ⚠️ **wang2022 已从 `catalog_merge.py` 的 CATALOGS 和 Z_PRIORITY 中移除**
   （2026-07-22 用户要求删除其全部数据；重跑合并不会带回）

## 四、导入结果

| 项目 | 数量 |
|---|---|
| catalog_data 新增记录 | 三源合计 873 条（saxgrbmgrb 25 + rssgrbag 171 + swiftgrbba 677） |
| 新建暂现源 | 13 个（射电点所属 GRB） |
| 光变表新增 | 140 个射电峰值点（mJy，1.38–43 GHz） |
| 红移填补 | 2 个 |
| 全库规模 | 944 个暂现源 / 912 个有目录数据 |

- 射电 band 不在 filters 表（非光学），银消改正自动跳过
- 已 `etl.py --dump` 同步；操作前备份 `/tmp/ajst_catalog_backup_20260722_*.sql`

## 五、维护指引

- 重跑流程：`外部表更新 → 该目录 parse.py → catalog_merge.py --apply`（射电点需另跑 `rssgrbag_lc_import.py --apply`，幂等）
- 新增外部目录：按 `external/SCHEMA.md` 写 parse.py 产 normalized.jsonl，
  在 `catalog_merge.py` 的 CATALOGS 加条目（参考 saxgrbmgrb 三行格式；`insert_new` 仅限文献样本类小表）
- 逐列文档：各目录 `README.md`；输出契约：`external/SCHEMA.md`
