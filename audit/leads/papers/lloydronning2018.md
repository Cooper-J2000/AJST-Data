# 文献级索引卡：Lloyd-Ronning+2018（短暴反向激波射电可探测性，含 4 行射电探测汇总表）

- paper_key: lloydronning2018
- paper: Lloyd-Ronning, N. 2018, Galaxies 6, 103「Reverse Shock Emission from Short GRBs」（DOI 10.3390/galaxies6040103；MDPI 开放获取，VoR PDF 已实取通读）
- date: 2026-11-20
- helper: wa1kmoon@zcode
- sources: GRB050724A, GRB051221A, GRB130603B, GRB140903A, GRB150724A

## 为什么是文献级卡

理论短文（反向激波可探测性估算），唯一天文观测内容是**表 1「Radio afterglow detections of short GRBs」（4 行）**，
数值全部转引自其参考文献 [14] = Fong+2015（ApJ 815, 102，已有文献级卡 `fong2015.md`，表 8 射电目录即其来源）。
**建卡主因是一处可能污染库内数据的暴名笔误**：表 1 首行暴名列「150724A」（t_obs=0.57, 1.68 d；Flux=173, 465 μJy），
但其正文原文写明「four individual bursts were detected by Fong et al. [14] in the radio band. These bursts are
**GRB050724A**, GRB051221A, GRB130603B and GRB140903A」；且 Fong+2015 arXiv v1 全文（本卡建卡时独立实查）0 次出现
「150724」、表 8 中 173/465 μJy 探测行属 GRB050724A——表 1 首行系 **050724A → 150724A 笔误**。
GRB150724A 是长暴（t90=280±44 s，GCN 18055），不属于该短暴样本；审 GRB150724A 时（2026-11-20）已甄别、
未采用该行（见其 info comment ⑦）。

## 涉及源一览

| 源 | 表号 | 源级卡 | status | 增量判读 |
|---|---|---|---|---|
| GRB150724A | 表 1（首行，笔误名） | — | mention-only | **笔误行**：数据实属 GRB050724A（正文原文 + Fong+2015 表 8 互证），非本源观测，不采用 |
| GRB050724A | 表 1 | — | mention-only | 汇总表转引 Fong+2015 表 8（见 `fong2015.md`）→ 不开卡 |
| GRB051221A | 表 1 | — | mention-only | 汇总表转引 Fong+2015 表 8（见 `fong2015.md`）→ 不开卡 |
| GRB130603B | 表 1 | — | mention-only | 汇总表转引 Fong+2015 表 8（见 `fong2015.md`）→ 不开卡 |
| GRB140903A | 表 1 | — | mention-only | 汇总表转引 Fong+2015 表 8（见 `fong2015.md`）→ 不开卡 |

## 增量门槛判读

- 全部源**不开源级卡**：表 1 是 4 行汇总转引（数值与 Fong+2015 表 8 同源，且 fong2015.md 已覆盖）；
- 唯一「增量」是否定性的：表 1 首行暴名笔误。任何人在导入/审核 050724A 或 150724A 时若撞见本表，应回到
  Fong+2015 表 8 取原始行（含观测频率），不要直接抄本表。

## 待决

- 无。
