# guidorzi2025 — Guidorzi et al. (A&A 690, A261) GRB 变异性-光度样本

GRB 瞬时辐射变异性 V 与静止系峰值光度 Liso 相关性研究的合并样本，
约 200 个有光谱红移的长暴（Swift/BAT、Fermi/GBM 光变曲线；Liso 取自
Konus-Wind / Fermi/GBM 宽带谱或文献）。

- 论文：Guidorzi C. et al., "New results on the gamma-ray burst
  variability-luminosity relationship", A&A 690, A261
  （bibcode 2024A&A...690A.261G；注：VizieR 与 ADS 均记为 2024 年卷，
  本目录沿用任务指派的短名 guidorzi2025）
- VizieR 目录：J/A+A/690/A261
  https://vizier.cds.unistra.fr/viz-bin/VizieR?-source=J/A+A/690/A261
- 获取日期：2026-07-21，经 TAP 端点
  `https://tapvizier.cds.unistra.fr/TAPVizieR/tap/sync`（FORMAT=csv）下载

## 原始文件

| 文件 | 内容 |
|---|---|
| `table1.csv` | 216 暴，变异性按 f=0.8 计算（主表） |
| `table3.csv` | 188 暴（table1 的子集），变异性按 f=0.45 计算 |
| `ReadMe.txt` | CDS 标准 ReadMe（列定义来源） |

注意：VizieR 上该目录只有 table1 和 table3（无 table2），与论文表号一致。
每表**最后 4 行**是长时标并合候选（060614、191019A、211211A、230307A），
论文中单独分析，解析时在 `other.long_merger_candidate` 标记。

## 列 -> normalized 键映射

以 table1 为主输出；table3 按暴名合并进 `other`。

| VizieR 列 | 去向 | 说明 |
|---|---|---|
| `GRB` | `name` | 原样（去首尾空格）加前缀 `'GRB '`，如 `050219A` -> `GRB 050219A` |
| — | `other.obs_date` | 由暴名推出的日期（样本均在 2000 年后）；表中没有触发时刻，`trigger_time` 一律为 null |
| `_RA`,`_DE` | `ra`,`dec` | J2000 度；231118A、231215A 两行原始数据即缺坐标，置 null |
| `z` | `params.redshift.v` | 光谱红移 |
| `Vf`,`s_Vf` | `params.variability` | `v=Vf`、`err=s_Vf`（1σ 对称）；`f=0.8` 标注计算份额 |
| `Det` | `params.variability.band` | 按论文摘要：BAT -> `15-150 keV`，GBM -> `8-900 keV`（64ms 背景扣除光变曲线） |
| `Vf05`,`Vf95` | `other.Vf05`/`other.Vf95` | Vf 置信区间 5%/95% 分位对应的负/正误差（原样保留，Vf05 原始为负值），未并入 `err` |
| `logLiso`,`e_logLiso` | `params.lp_iso` | 见下"单位换算"；`frame=rest` |
| `Tf`,`e_Tf` | `other.Tf`/`other.e_Tf` | 收集总净计数份额 f 的时间区间（秒） |
| `Det`,`r_logLiso`,`Npeaks` | `other` | 探测器 / Liso 参考文献编号（refs.dat）/ S/N>5 峰数 |
| table3 的 `Vf`,`s_Vf`,`Tf` | `other.Vf_f0.45`/`s_Vf_f0.45`/`Tf_f0.45` | f=0.45 结果（188 条有） |

本目录没有 eiso、epeak、t90 等量，未输出。

## 单位换算

- `logLiso` 是 Liso（erg/s，静止系各向同性峰值光度）的常用对数：
  `lp_iso.v = 10**logLiso`。
- `e_logLiso` 为 log 空间 1σ 对称误差，换算为线性空间不对称误差
  `[正, 负]`：`正 = v*(10**e - 1)`，`负 = v*(1 - 10**(-e))`。
- `lp_iso` 的静止系能段表中未逐暴给出（不同文献来源不同），故省略
  `band` 键，使用方如需能段请按 `other.r_logLiso` 回查 refs.dat 对应文献。
- Vf、z、Tf 均为无量纲/秒，无需换算。

## 重新解析

```
python3 parse.py    # 读 table1.csv/table3.csv，写 normalized.jsonl
```

## 关键假设

1. 论文年份以 bibcode 为准（2024），短名保留 guidorzi2025。
2. `variability.band` 由 `Det` 列推断（BAT=15-150 keV，GBM=8-900 keV），
   依据论文摘要对 64ms 光变曲线能段的描述。
3. `err` 取 1σ 的 `s_Vf`；90% 置信（5–95 分位）的 Vf05/Vf95 保留在 `other`。
4. 无触发时刻，`trigger_time` 置 null，仅提供 `other.obs_date`。
