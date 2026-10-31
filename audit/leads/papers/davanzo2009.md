# 文献级索引：D'Avanzo+2009（三个短暴 051227 / 061006 / 071227 的 VLT 光学余辉与宿主）

- paper_key: davanzo2009
- paper: D'Avanzo+2009, A&A 498, 711（DOI 10.1051/0004-6361/200811294；arXiv:0901.4038）
- date: 2026-10-31
- helper: Rusty-Harpoon@zcode
- sources: GRB051227, GRB061006A, GRB071227A

## 为什么是文献级卡

该文是 GRB 051227、061006、071227 三个短/硬暴的 VLT 专篇：每个暴一张「VLT observation log」测光表
（表 1/2/3，`tab_log1`/`tab_log2`/`tab_log3`，含平均时刻 UT、曝光、触发后天数、星等与滤光片），
另含 051227/061006/071227 宿主光谱红移与宿主测光。三个暴均在库内，按 §3.11 先建本索引卡。

## 版本状态

- 本次实际逐表核对用 **arXiv v2 LaTeX 源码**（`3short_AA_v10.tex`，A&A 排版版，2026-10-31 实取解包）。
- **VoR（A&A 498, 711）未获取**：aanda.org 整站 DataDome 反爬（HTML 与 PDF 均 HTTP 403）；
  CDS-VizieR `J/A+A/498/711` 及全部镜像（cfa/nao/iucaa/china-vo）连接失败；archive.org 不可达；
  ADS 元数据（题录/摘要）可达。已按 §3.3 三方交叉口径处理并在 `audit/unverified.tsv` 登记
  （GRB061006A 行，PR #688）；**任何地方不得写成「已核对 VoR」**。
- 注：arXiv 源码中 GRB 061006 表 2 有一行被注释掉的 U>22.8（3σ，2006-11-03，FORS2），
  该行不在现表内，是否曾在 VoR 出现未核，接手 061006 相关工作时留意。

## 涉及源一览

| 源 | 表号 | 源级卡 | status | 增量判读 |
|---|---|---|---|---|
| GRB061006A | 表 2（tab_log2，9 行测光） | 无（本源已随 PR #688 审核） | extracted（9 行已逐值核对入库） | 过门槛(1)(3)：VLT 专篇测光表 + 新 bibcode 引用 2009A&A...498..711D |
| GRB051227 | 表 1（tab_log1） | 无 | mention-only | 过门槛判读：该文自有 VLT R/I 测光与上限（未提取；本文未得该宿主准确红移）——接手者按 §3.3 逐值核对 |
| GRB071227A | 表 3（tab_log3） | 无 | mention-only | 过门槛判读：该文自有 VLT 测光、宿主 z=0.381±0.001（未提取）——接手者按 §3.3 逐值核对 |

## 原文口径要点（接手者换算必读）

- 三张表格式相同：Mean time (UT) / Exposure time (s) / **Time since GRB (days)** / Seeing / Instrument /
  Magnitude / Filter。`Time since GRB` 以**各自 BAT 触发 t0** 为历元（061006 的 t0=16:45:50 UT），
  换算 `time` 需 ×86400 并确认该源 T0；Mean time (UT) 可作互验。
- 表注：「Magnitudes are in the Vega system and are not corrected for Galactic absorption」；
  误差 1σ、上限 3σ。
- GRB 071227 的宿主红移 z=0.381±0.001、GRB 061006 的宿主红移 z=0.436±0.002 均出自本文宿主光谱
  （061006 与 Berger+2007 的 z=0.4377±0.0002 一致）；GRB 051227 本文未获得准确宿主红移。

## 待决

- VoR 与 arXiv v2 是否有差未核（出版社整站反爬 + 本网络不可达 CDS/archive.org）；若后续取到 VoR/VizieR 表，
  应按 §3.3 以 VoR 复核已入库的 061006A 九行。
