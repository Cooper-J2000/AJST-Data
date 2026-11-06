# 文献索引：Cenko+2009（P60-Swift 早期光学余辉目录，29 暗暴/29 暴样本）

- paper_key: cenko2009
- paper: Cenko et al. 2009, ApJ 693, 1484（DOI 10.1088/0004-637X/693/2/1484；arXiv:0808.3983 为同文预印本）
- date: 2026-11-07
- helper: wa1kmoon@zcode
- sources: GRB050412, GRB050416A, GRB050607, GRB050713A, GRB050820A, GRB050908A, GRB050915A, GRB060110, GRB060210A, GRB060502A, GRB060510B, GRB060805A, GRB060906A, GRB060908A, GRB060923A, GRB061222A, GRB070208A, GRB070419A, GRB070521A, GRB071003A, GRB071010A, GRB071011, GRB071020A, GRB071122A, GRB080310A, GRB080319A, GRB080319B, GRB080319C, GRB080320
- out_of_repo:

## 为什么是文献级卡

P60（Palomar 60-inch）对 29 个 Swift 暗暴/早期暴的**原始**测光目录（表1，非 GCN 转引——多数 P60 观测
未单独发 GCN，属增量类型 1）。表1 共 6 列：GRB / UT Date（曝光开始）/ Time Since Burst（**曝光中点**
相对 BAT 触发，表注 b）/ Filter / Exposure / Observed Magnitude。机读版在
CDS J/ApJ/693/1484/table1（MRT，本次已用 CFA 镜头逐值核对 GRB080320 的 10 行，与 arXiv 表1 一致）。
星等系统按 §3 显式声明：Rc/Ic 为 Vega，i'/z'/g（Gunn g 定标到 SDSS g）为 AB；数值未做银消改正。
表3 为样本属性表（β_OX、A_V 等，派生量）。来源名为 YYMMDD，映射到库内 id 按日期进行，
字母后缀（A/B）需接手者按坐标/T0 自行核验（如 071010 → GRB071010A）。

## 涉及源一览

| 源 | 表号 | 源级卡 | status | 增量判读 |
|---|---|---|---|---|
| GRB080320 | table1 | 无（本卡即索引） | extracted（10 行已逐值核对并入 PR #960 lc） | 原始 P60 测光（2 探测 + 8 上限），GCN 未发布，已入库 |
| 其余 28 源 | table1 | 无 | mention-only | 同一 MRT 可程序化提取（CDS J/ApJ/693/1484/table1），接手者逐值回核即可 |

## 增量门槛判读

- 对 GRB080320：类型 1（P60 表1 未单独发 GCN）→ 已由本 PR 直接入库，不再开源级卡。
- 对其余 28 源：同为类型 1 候选，但需逐源核对该源是否已有同数据（P60 行可能与后续已入库的
  文献行同源），接手者用 CDS MRT 提取后逐值回核再定去重。

## 待决

无（GRB080320 部分已处置完毕；其余源无卡规模问题——数据全部集中在同一 CDS MRT）。
