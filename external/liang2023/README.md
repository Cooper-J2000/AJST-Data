# liang2023 — Liang et al. 2023 Fermi-GBM 带红移 GRB 谱分类目录

- 来源论文：Liang Y.-W. et al. 2023, ApJS, 266, 31,
  "The Model-wise Properties of the GRB Spectral-Energy Correlations: A Nearly Complete
  Sample of Fermi-detected Gamma-Ray Bursts with Known Redshift"
- arXiv: https://arxiv.org/abs/2211.12187 （e-print: https://export.arxiv.org/e-print/2211.12187）
- 获取日期：2026-07-21（`curl -sL` 下载 gzip tar，解压至 `arxiv_src/`）
- 原始文件：`2211.12187.tar.gz` 与解压目录 `arxiv_src/` **不随本仓库分发**（见下节）
- 样本：153 个带红移的 Fermi-GBM GRB（17 短暴 + 136 长暴，2008-07 至 2022-05）

## 原始数据获取方式

为遵守版权，arXiv 源码包（`2211.12187.tar.gz`）及其解压产物（`arxiv_src/`，含 `ms.tex`、论文图片等）不随本仓库分发。请自行从 arXiv 论文页 https://arxiv.org/abs/2211.12187 下载 e-print 源码包（https://export.arxiv.org/e-print/2211.12187 ；对应期刊版本：Liang Y.-W. et al. 2023, ApJS, 266, 31），解压为 `arxiv_src/` 目录后运行 `python3 parse.py` 重新生成 `normalized.jsonl`。

## 解析

`python3 parse.py` → `normalized.jsonl`（每暴一条，输出契约见 ../SCHEMA.md）。
仅依赖 Python 标准库。

### 使用的表（ms.tex 共 7 张表，后 3 张为汇总统计不解析）

| 表 | label | 内容 | 用途 |
|---|---|---|---|
| 表1 | tab:global | 153 暴基本性质：GRB、z、T90、T90/(1+z)、Sγ、探测器、背景区间、时间积分谱优选模型、暴分类 | 主样本（name/z/t90/fluence/spec_class/grb_type/other） |
| 表2 | tab:Integrated | 110 暴时间积分谱拟合：CPL 与 Band 两模型并列，含 E_p/E_c、α、β、E_p^rest、E_γ,iso | epeak/ep_rest/eiso/alpha/beta |
| 表3 | tab:1sPeak | 97 暴 1-s 峰谱拟合，含 L_p,iso | lp_iso |
| 表4 | tab:BB | 需附加黑体分量的暴（Band+BB/CPL+BB，时间积分 11 行 + 1-s 峰 14 行） | 原样存入 other（T4 前缀键） |

合并键：表1 的 `yymmddX(nnn)` 与表2/3/4 的 9 位 ID（yymmdd+触发小数 nnn）拼接匹配。

### 字段映射

| normalized 键 | 来源 | 说明 |
|---|---|---|
| name | 表1 col.1 | `GRB yymmddX`；末尾的 "S"（如 101224AS）是短暴标记，剥去字母 S |
| name_alt | 派生 | `GRB yymmdd.nnn`（Fermi 小数名）+ `bn...` 触发号 |
| trigger_time | 派生 | GBM 触发号 nnn = 当日千分比，换算为 ISO UTC（秒级取整） |
| params.redshift | 表1 col.2 | 190530A 为上限 `$<$2.2`，不写 params，原文存 other.z_raw |
| params.t90 | 表1 col.3 | 观测系，band 标 "50-300 keV"（假设，见下） |
| params.fluence | 表1 col.5 | Sγ，band 标 "8 keV-40 MeV"（假设，见下） |
| params.spec_class | 表1 col.8 | Band→"Band"、CPL→"CPL"、Band+BB→"Band"、CPL+BB→"CPL"；Unconstrained/\nodata 不写 |
| params.grb_type | 表1 col.9 | Short→"I"（并合），S/M（长暴单峰/多峰）→"II"（坍缩星） |
| params.epeak | 表2 优选模型列 | 观测系 keV；model="BAND"（Band 列 E_p）或 "CPL"（COMP 列 E_c）；优选模型由表1 col.8 决定 |
| params.ep_rest | 表2 优选模型列 / 换算 | 静止系 keV，见"关键假设"3 |
| params.eiso | 表2 优选模型列 | erg，band "1-10000 keV"，frame rest |
| params.alpha / beta | 表2 优选模型列 | 时间积分谱指数；仅 4 个无表2 行的暴（090902B、160625B、190114C、201216C）用表3 的 1-s 峰值，并在 other.alpha_source 注明 |
| params.lp_iso | 表3 优选模型列 | erg/s，band "1-10000 keV"，frame rest，来自 1-s 峰谱 |
| other | 表1 原始列 + 表3/表4 原文 | Detectors、Background intervals、Averaged Spectrum、Classified、T90/(1+z) (s)、T3/T4 原始单元格 |

### 关键假设与已知问题

1. **优选模型取值**：论文对每暴并列给出 CPL 与 Band 两套拟合，params 取表1
   "Averaged Spectrum" 列给出的优选模型对应列（Band/Band+BB 取 Band 列，
   CPL/CPL+BB 取 COMP 列）。附加黑体分量（+BB）的混合拟合参数不覆盖 params，
   原文保留在 other 的 `T4 int/peak *` 键中。
2. **表2 Band 列 E_p^rest 印刷错误**：该列全部与观测系 E_p 完全相同（未乘 1+z），
   而 CPL 列经抽查验证为 (2+α)·E_c·(1+z) 的正确静止系值（如 081121858：
   211×1.21×3.512≈899）。因此对 Band 类暴，ep_rest 用 (1+z)·E_p 自行换算
   （误差同比缩放）；CPL 类暴直接用表中印刷值。
3. **能段标注假设**：t90 标 "50-300 keV"（GBM 通行定义，论文未写明）；fluence 标
   "8 keV-40 MeV"（由 E_iso = 4πd_L²·Sγ·k_c/(1+z) 推断 Sγ 为 GBM 能段流量，
   k_c 为 1–10⁴ keV 改正）。eiso/lp_iso 的 1–10⁴ keV 能段在正文明确给出。
4. **GRB 080905 重名**：当天两个触发（bn080905499 短暴、bn080905705 长暴），
   论文均未给字母后缀，两条记录 name 同为 "GRB 080905"，靠 name_alt /
   trigger_time 区分。
5. **论文其他排版错误（已规避，不影响 params）**：表2 141220252 行 Band 列
   E_p 印为 "154150"（该行优选模型为 CPL，params 取 CPL 列不受影响）；
   161017745 行下误差漏负号（`10$^{+33}_{5}$`，解析时取下误差绝对值）。
6. **表2 行数 110**：正文叙述 "109 GRBs with well-measured E_p"，但 tex 表2
   实际 110 行（含 201221963 短暴等），按表为准。
7. 表5（参数分布高斯拟合）、表6（Amati/Yonetoku 回归）、表7（MCMC）为样本级
   统计，不含逐暴数据，未解析。
8. 表2 中部分 Band β 顶在下界 -5.00（如 -5.00^{+0.59}_{-0.08}），按原文照录。
9. 本目录不含 ra/dec（论文表格未给），留 null。

### 误差约定

- 表1 为 `x$\pm$y` 对称误差（单值）；表2/3/4 为 `x$^{+a}_{-b}$` 不对称误差
  （存 [正, 负]，负误差取绝对值）。
- 文中说明误差为 1σ。
