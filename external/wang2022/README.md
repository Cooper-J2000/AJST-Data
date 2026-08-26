# wang2022 — Wang et al. 2022 Eiso-Ep 校准样本

## 来源

- 论文：Wang et al. 2022, MNRAS, 516, 2575（用 221 个长 GRB 的 Eiso-Ep（Amati）关系校准 GRB 并限制宇宙学参数）
- 数据：arXiv:2208.09272 e-print 源码包（gzip tar），附录 longtable（caption: "221 GRBs with redshifts, peak energy in cosmological rest frame and isotropic-equivalent energy"）
- URL：https://arxiv.org/e-print/2208.09272
- 获取日期：2026-07-21
- 原始文件：`wang2022.tar` 及解压产物（`ms.tex` 等）**不随本仓库分发**（见下节）

## 原始数据获取方式

为遵守版权，arXiv 源码包（`wang2022.tar`）及其中解压出的 `ms.tex`、模板、bib、论文图片 PDF 等原始文件不随本仓库分发。请自行从 arXiv 论文页 https://arxiv.org/abs/2208.09272 下载 e-print 源码包（https://arxiv.org/e-print/2208.09272 ，对应期刊版本：Wang et al. 2022, MNRAS, 516, 2575），解压后将其中的 `ms.tex` 放到本目录，然后运行 `python3 parse.py` 重新生成 `normalized.jsonl`。

## 解析

运行 `python3 parse.py`，从 `ms.tex` 的附录 longtable 提取 221 行数据，输出 `normalized.jsonl`（契约见 ../SCHEMA.md）。仅用 Python 标准库，可重复运行。

## 字段映射

| 表中列 | normalized 键 | 说明 |
|---|---|---|
| GRB（如 `060218`、`130427A`） | `name` | 加前缀与空格 → `GRB yymmddX`（无字母后缀则只到 6 位日期） |
| Redshift | `params.redshift.v` | 表中红移无误差，故无 `err` 键 |
| $E_{\rm p}$ (keV) | `params.ep_rest` | 论文 caption 明确为宇宙学静止系峰值能量；`frame: "rest"`；1σ 对称误差 |
| $E_{\rm iso}$ ($10^{52}$ erg) | `params.eiso` | 原始值 ×1e52 换算为 erg；`frame: "rest"`；1σ 对称误差 |
| Refs. `(1)`–`(5)` | `other["Refs"]` | 数据来源引用编号，原样保留（含括号），对应论文 caption 脚注 (b) 的文献列表 |

## 单位与假设

- Eiso：表中单位 1e52 erg，解析时乘 1e52；论文脚注 (a) 说明 Eiso 用 $H_0=67.4$, $\Omega_M=0.315$, $\Omega_\Lambda=0.685$ 的平坦 ΛCDM 计算。表中未给 Eiso 能段，故 `band` 键省略。
- 所有误差均为 1σ 对称误差（表中均为 `$\pm$` 单值，无不对称误差、无 \nodata、无跨行）。
- 全部 221 个均为长 GRB（论文用于 Eiso-Ep 校准），表中无坐标和触发时刻，`trigger_time`/`ra`/`dec` 为 null，`name_alt` 为空。
- 表内 `080916`（z=0.689）与 `080916C`（z=4.35）为两个不同条目，按原表照录。
