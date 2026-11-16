# 文献级索引卡：Zhong+2019（短暴前兆性质与 progenitor 探针）

- paper_key: zhong2019
- paper: Zhong, S.-Q., Dai, Z.-G., Cheng, J.-G., Lan, L., & Zhang, H.-M. 2019, ApJ 884, 25「Precursors in Short Gamma-Ray Bursts as a Possible Probe of Progenitors」（DOI 10.3847/1538-4357/ab3e48；arXiv:1909.00577；VoR IOP HTML 已实取：https://doi.org/10.3847/1538-4357/ab3e48 ）
- date: 2026-11-17
- helper: fsy@zcode
- sources: GRB060502B, GRB081024A, GRB100213A, GRB100702A, GRB140209A, GRB160408A, GRB170817A, GRB180402A

## 为什么是文献级卡

短暴前兆样本分析（Swift 与/或 Fermi 观测）：表 1 给每个前兆例的前兆/主暴时窗（since BAT trigger，8 ms 分辨）、平均流量、硬度比、静默期、图像显著性；表 2 给前兆与主暴谱拟合（PL/CPL/BB）。时窗与显著性为作者自算（GCN/目录检索拿不到；Swift 源的 T100_start 已在 swift_bat 快照，本卡增量=前兆/主暴分解窗+显著性）。库内命中 8 源（按 arXiv v1 文本正则普查；表 1 行已见者单列）。
注意：表 1 注 a 逐字 `The SGRBs observed by both Swift and Fermi are GRB 081024A-bn081024245, ...`——A/B 命名与 GBM 触发号配对的 VoR 级证据。

## 涉及源一览

| 源 | 表号 | 源级卡 | 增量判读 |
|---|---|---|---|
| GRB060502B | 表 1（arXiv 文本 L493） | — | 前兆 −0.56～−0.25 s（Swift）；作者自算时窗，接手者按 VoR 表复核后再用 |
| GRB081024A | 表 1（VoR 已逐字核对） | — | 已审（PR #1090，commit 886e6e00）：前兆 −1.65～−1.59 s since BAT trigger（6.7σ）与快照 T100_start=−1.656 s 自洽；本源 T0_offset 证据链已入库 |
| GRB100213A | 表 1（arXiv 文本 L496） | — | 前兆 −0.27～−0.23 s；接手者按 VoR 表复核 |
| GRB100702A | 表 1（arXiv 文本 L497） | — | 表行部分值被 pdftotext 截断；接手者按 VoR 表复核 |
| GRB140209A | 表 1（arXiv 文本 L501） | — | 前兆 −0.94～−0.87 s；Fermi 同测（EE 类候选，正文 L464）；接手者按 VoR 表复核 |
| GRB160408A | 表 1（arXiv 文本 L502） | — | 前兆 +0.29～+0.37 s；接手者按 VoR 表复核 |
| GRB170817A | 正文（L253 谱关联讨论） | — | 仅正文提及（谱关联拟合），无表行 |
| GRB180402A | 表 1（arXiv 文本 L505） | — | 前兆 −0.14～−0.01 s（GBM 基准）；接手者按 VoR 表复核 |

## 增量门槛判读

- 8 源的表 1 时窗/显著性均为作者自算（增量门槛 #1：作者自算 ΔT），但 Swift 源的爆发窗本身可由 swift_bat 快照 T100_start 派生——增量主要在「前兆/主暴分解 + 显著性」，供 T0_offset 与前兆真实性复核；均不开源级卡（索引信息即本卡），接手者审对应源时按 VoR 表行复核。
- 表 2 谱参数（CPL Γ、Ec、kT）不属测光，未逐源登记。

## 待决

1. 库外样本成员（090510、140402A、160726A、160818198、170709334、170726794 等）未逐个核库内映射，不在本卡范围。
