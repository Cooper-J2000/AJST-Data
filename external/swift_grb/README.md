# swift_grb — Swift Gamma Ray Bursts Catalog (HEASARC SWIFTGRB)

- **目录名称**: SWIFTGRB — Swift Gamma Ray Bursts Catalog
- **主页 URL**: https://heasarc.gsfc.nasa.gov/W3Browse/swift/swiftgrb.html
- **数据文件下载 URL**: https://heasarc.gsfc.nasa.gov/FTP/heasarc/dbase/dump/heasarc_swiftgrb.tdat.gz
- **获取日期**: 2026-07-21
- **参考文献**: Donato D. et al. 2012, ApJS, 203, 2D
- **覆盖范围**: Swift 任务开始（2004-11-20）至 2012-12-31 观测到的所有 GRB（含 Swift 触发及跟进其他卫星发现的 GRB）。W3Browse 页面称数据库最后更新于 2014-10-30；文件头显示 2025-01-07 重新导出（内容未变）。

## 文件清单

| 文件 | 说明 |
|---|---|
| `heasarc_swiftgrb.tdat.gz` | HEASARC 数据库 tdat 格式整表导出（gzip 压缩，305 KB，解压后约 937 KB） |

**格式说明**: tdat 是 HEASARC 的 ASCII 表导出格式。文件分两段：`<HEADER>` 段（表元数据、每个字段的类型/单位/注释、列顺序定义 `line[1] = ...`）和 `<DATA>` 段。数据行为 **管道符 `|` 分隔**，每行末尾还有一个多余的 `|`（解析时去掉末尾空字段）。缺失值为**空字符串**（两个 `|` 相邻）。

**行数核对**: 实测数据行（以 `GRB` 开头）**872 行**，与文件头 `TOTAL ROWS: 872` 一致。网页宣称覆盖 2004-11-20 至 2012-12-31 的全部 Swift GRB，实测首行 GRB 041217、末行 GRB 121229A，相符。每行 178 列。

## 爆发标识

- `name`: 名称格式 `GRB YYMMDD`，同一天多个爆发追加字母 `A/B/C...`（如 `GRB 041219A`）；2010-01-01 之后所有 GRB 名称均带字母。
- `target_id`: Swift 触发编号（整数，最多 8 位）。≥100000 为 BAT 触发；20000–29999 为其他任务触发或 BAT 地面分析发现的 GRB。**注意有 4 行无 target_id**（GRB 070326、GRB 090418B、GRB 110906A、GRB 111126A），联合主键是 `(target_id, name)`。
- 坐标：主坐标 `ra`/`dec`（J2000，度）为"最佳位置"（取自 BAT/XRT/UVOT/地面观测中最优者，`pos_flag` 标明来源：B=BAT, X=XRT, U=UVOT, G=地面等）；各仪器另有独立坐标列（`bat_ra/dec`、`xrt_ra/dec`、`uvot_ra/dec`、`ot_ra/dec`）。872 行全部有主坐标。
- `det_flag`: S=仅 Swift 触发(483)，O=仅其他任务(127)，B=两者(262)。

## 逐列文档（共 178 列）

单位标注在字段定义中（如 `float8:.4f_s` 表示秒，`erg/cm^2` 等）。**除特别注明外，所有物理量均为观测系（observer frame）**。

### 通用信息（1–17）

| 列 | 含义 | 单位/备注 |
|---|---|---|
| name | 源名称（主键之一） | `GRB YYMMDD[x]` |
| target_id | 唯一触发编号 | 整数，4 行缺失 |
| other_id | 其他任务的爆发标识 | 依任务而定 |
| det_flag | 探测标志 | S/O/B |
| slew_info | 跟进延迟原因 | BTS/DIS/EAR/GRN/MOO/OBS/SUN/TOO |
| ra, dec | 最佳位置（赤道坐标，J2000） | 度 |
| pos_err | 最佳位置误差 | **角秒** |
| lii, bii | 银经、银纬 | 度 |
| pos_flag | 位置来源标志 | B(BAT)/X(XRT)/U(UVOT)/G(地面)等 |
| pos_ref | 位置参考文献 | ADS bibcode |
| start_time, stop_time | Swift 首次/末次观测时间 | UTC |
| duration | 观测持续时间 | **天** |
| trigger_time | 触发时间 | UTC，ISO 格式带小数秒 |
| trigger_ref | 触发参考文献 | bibcode |

### BAT 部分（18–96）—— 注意：BAT 能段为 **15–150 keV**

| 列 | 含义 | 单位/备注 |
|---|---|---|
| bat_detection | BAT 是否探测到 | Y/U（**没有 N，未知用 U**） |
| bat_dettype | BAT 探测类型 | R(rate 触发)/I(image 触发) |
| bat_ra, bat_dec | BAT 位置 | 度 |
| bat_pos_err | BAT 位置误差 | **角分**（注意与 pos_err 的角秒不同！） |
| bat_pos_ref | BAT 位置参考 | bibcode |
| bat_theta, bat_phi | BAT 视场内角度 | 度 |
| bat_imagesig | BAT 图像显著性 | σ |
| **bat_t90** | **T90（5%–95% 计数时间间隔）** | 秒，**15–150 keV 能段导出**，708/872 有值 |
| bat_t50 | T50（25%–75%） | 秒，15–150 keV，695/872 有值 |
| bat_start, bat_stop | 事件数据起止时间（相对触发） | 秒 |
| bat_t100_start, bat_t100_stop | T100 区间（流量/能谱测量区间） | 秒 |
| bat_fluence_model | 流量所用能谱模型 | **PL(598)/CPL(109)**，仅这两种，无 Band |
| **bat_fluence** | **T100 区间总流量** | erg/cm²，**15–150 keV**，706/872 有值 |
| bat_fluence_err | 流量误差；**无误差值=该测量是上限** | erg/cm² |
| bat_fluence1..4 + _err | 分能段流量 | erg/cm²；15–25 / 25–50 / 50–100 / 100–150 keV |
| bat_peak_time | 峰流量时刻（相对触发） | 秒 |
| bat_peak_model | 峰流量能谱模型 | PL/CPL |
| bat_peak_flux + _err | 1 秒积分峰流量（能量） | erg/s/cm²，15–150 keV |
| bat_peak_flux1..4 + _err | 分能段峰流量（能量） | erg/s/cm² |
| bat_peakfluxp + _err | 1 秒积分峰流量（光子） | photon/s/cm²，15–150 keV |
| bat_peakfluxp1..4 + _err | 分能段峰流量（光子） | photon/s/cm² |
| bat_plsl + _err | 幂律(PL)拟合光子指数及单侧误差 | T100 区间，15–150 keV |
| bat_pl_chi2, bat_pl_dof | PL 拟合约化 χ²、自由度 | |
| bat_ctslope + _err/_n_err | 截断幂律(CPL)光子指数，低/高不对称误差 | |
| bat_ctezero + _err/_n_err | CPL 截断能量 E₀，低/高不对称误差 | keV |
| bat_ct_chi2, bat_ct_dof | CPL 拟合约化 χ²、自由度 | dof 恒为 56 |
| **bat_epeak** | **νFν 谱峰能量（观测系）** | keV，194/872 有值；来自 BAT 或其他任务 |
| bat_epeak_ref | Epeak 来源参考 | bibcode |
| **bat_eiso** | **各向同性能量，15–150 keV 能段** | 见下方"坑"，61/872 有值，需红移 |
| **bat_eiso1000** | **各向同性能量，1–1000 keV 能段** | 15/872 有值，需红移 |
| bat_eiso_alpha/beta/norm | Eiso 计算所用 Band 谱参数 | α、β、归一化 |
| bat_eiso_dur | Eiso 计算所用持续时间 | 秒 |
| bat_eiso_ref | Eiso 能谱参考 | bibcode |
| bat_redshift | 计算 Eiso 所用的红移 | 134/872 有值 |
| bat_hrd1 + _err | 硬度比 25–50 / 15–25 keV | 注：字段头误标单位为 keV |
| bat_hrd2 + _err | 硬度比 50–100 / 15–25 keV | 同上 |
| bat_comment | BAT 备注 | |

### XRT 部分（97–126）

| 列 | 含义 | 单位/备注 |
|---|---|---|
| xrt_detection | XRT 是否探测到 | Y/N/U |
| xrt_ra, xrt_dec, xrt_pos_err, xrt_pos_ref | XRT 位置及误差（角秒） | 度 |
| xrt_onsource | XRT 在源时间 | 秒 |
| xrt_c100_rate/start/stop/expo/mode | C100（首个 PC 模式段）计数率等 | |
| xrt_e1_rate + _err | E1（首个 WT 段）计数率 | counts/s |
| xrt_e1_rate1..3 + _err | E1 分段计数率 | |
| xrt_e1_start/stop/expo, xrt_e1_mode | E1 区间、模式 | |
| xrt_hrd1/hrd2 + _err | XRT 硬度比 | |
| xrt_lcchange | 光变次数 | 整数 |
| xrt_flare | 是否有耀发 | Y/N |

### UVOT 部分（127–146）

| 列 | 含义 | 单位/备注 |
|---|---|---|
| uvot_detection | UVOT 探测 | Y(245)/N(501)/U(119)/**P(7，部分探测)** |
| uvot_ra, uvot_dec, uvot_pos_err, uvot_pos_ref | UVOT 位置 | 度，误差角秒 |
| uvot_onsource | 在源时间 | 秒 |
| uvot_vv_flux/mag/mag_err/start/stop/expo | V 滤片流量/星等及观测区间 | |
| uvot_w1_* | UVW1 滤片同上 | |

### 红移与后随观测（147–178）

| 列 | 含义 | 单位/备注 |
|---|---|---|
| redshift + _err | 光学余辉红移 | 338/872 有值 |
| redshift_type | 红移类型 | P/PL=测光，S/SL=光谱，G/GL=寄主星系 |
| redshift_line | 发射/吸收线 | E/A |
| redshift_from | 红移来源 | Swift 或其他 |
| redshift_ref | 红移参考 | bibcode |
| galactic_nh | 银河系氢柱密度 | cm⁻² |
| followup | 是否有其他台站探测 | Y/N |
| radio/infra/opt_detection + _ref | 射电/红外/光学探测标志及参考 | Y/N/U |
| ot_ra/dec/pos_err/pos_ref | 光学暂现源(OT)位置 | 度 |
| other_obs..4 + _ref | 其他观测（最多 4 条） | |
| supernova_flag | 是否成协超新星 | Y/N |
| galaxy_flag/name/type/ra/dec/pos_ref/redshift/ref/offset | 寄主星系信息 | galaxy_redshift 为字符串型 |
| ground_counterpart | 地面对应体 | Y/N |
| web_page | 该爆发数据产品网页 | URL |
| comments | 备注 | 自由文本 |

## 关键注意事项（坑）

1. **能段是 15–150 keV**（BAT），不是 Fermi-GBM 的 50–300 keV。T90/T50/fluence/峰流量/硬度比全部基于该能段（或其子段）。跨目录比较 Epeak–fluence 关系时必须注意。
2. **观测系 vs 静止系**：`bat_epeak` 是**观测系** νFν 峰能量（keV）；T90 也是观测系秒数，未做 (1+z) 改正。Eiso 是静止系能量但积分能段标注在列名里（15–150 或 1–1000 keV）。
3. **Eiso 单位矛盾（文档 bug）**：字段头注释写 "BAT Luminosity" 且类型标注 `erg/s`，但网页文档称其为 "isotropic equivalent energy"，数值量级（~1e51–1e53）证实是**能量（erg）而非光度**。入库时按 erg 处理。
4. **能谱模型只有 PL 和 CPL**（`bat_fluence_model`/`bat_peak_model`），无 Band 模型拟合结果；Band 参数仅出现在 Eiso 计算参考列（`bat_eiso_alpha/beta/norm`）。
5. **误差置信度**：网页文档未明确声明 1σ 还是 90%。CPL 参数误差是**不对称的低/高双侧误差**（`_err` 低侧、`_n_err` 高侧）；PL 光子指数误差为单侧。**fluence/峰流量列若误差为空，该值是上限而非测量值**（网页明确说明）。
6. **缺失值**：空字符串；布尔/标志类用 `U` 表示未知（不是空）；`uvot_detection` 还有 `P`（部分）。**bat_detection 只有 Y/U，没有 N**。
7. **行尾多余 `|`**：解析时每行 split('|') 会多出一个空尾字段，需剔除。
8. **单位陷阱**：`pos_err` 是角秒，`bat_pos_err` 是角分；`duration` 是天；`bat_hrd1/2` 字段头误标单位为 keV（实为无量纲比值）；`bat_eiso*` 字段头写 erg/s 实为 erg（见第 3 条）。
9. **tdat 头注释与网页文档不一致**：`bat_t90` 头注释写 "Total Energy Band"，网页明确为 15–150 keV——以网页为准。
10. **4 行无 target_id**（GRB 070326、GRB 090418B、GRB 110906A、GRB 111126A），不能用 target_id 单独做主键。
11. **数据时效**：内容止于 2012-12-31（2014 年最后更新）。需要更新的 Swift GRB 表（如 SWIFTBATGRB / swiftgrbba）应另行调研。
12. `bat_ct_dof` 恒为 56；`trigger_time` 小数秒位数不一。

## 解析示例（Python）

```python
import gzip
cols, rows = None, []
with gzip.open('heasarc_swiftgrb.tdat.gz', 'rt') as f:
    for line in f:
        if line.startswith('line[1] ='):
            cols = line.split('=', 1)[1].split()
        elif line.startswith('GRB'):
            vals = line.rstrip('\n').split('|')[:-1]  # 去掉行尾空字段
            rows.append(dict(zip(cols, vals)))
# rows[i]['bat_t90'], rows[i]['bat_epeak'], rows[i]['bat_fluence'] ...
```
