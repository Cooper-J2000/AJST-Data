# 文献索引：Oates+2009（Swift/UVOT 高红移 GRB 光变统计研究，26 暴）

- paper_key: oates2009
- paper: Oates+2009, MNRAS 395, 490（DOI 10.1111/j.1365-2966.2009.14544.x；arXiv:0901.3597）
- date: 2026-11-03
- helper: Rusty-Harpoon@zcode
- sources: GRB050319A,GRB050525A,GRB050712,GRB050726,GRB050730A,GRB050801A,GRB050802A,GRB050922C,GRB051109A,GRB060206A,GRB060223A,GRB060418A,GRB060512A,GRB060526A,GRB060605A,GRB060607A,GRB060708A,GRB060804,GRB060908A,GRB060912A,GRB061007A,GRB061021A,GRB061121A,GRB070318A,GRB070420,GRB070529A

## 为什么是文献级卡

Oates et al. 2009 对 26 个有红移 Swift/UVOT GRB 做了早期光变统计（上升段/峰值/衰减斜率），是 Dainotti2024
目录 source=Oates 行的上游。**论文正文与在线材料均无逐点星等表**（arXiv:0901.3597 v1 TeX 全文核对，2026-11-03）：
只有峰值星等/峰值时刻/拟合斜率表与相对流量图；其逐点光变数据未随文公开发布。

GRB050730A 审验记录（2026-11-03）：本库 17 行 Dainotti2024;Oates（uvot-v）无法溯源到任何可打开的
Oates 逐点表，且该文自述其 050730 时间零点与 BAT 触发最大差 133.1 s（时间历元存疑），已全部置 discard=y
并登记 audit/unverified.tsv（status=missing，A 档待维护者裁决）。

## 涉及源一览

26 个样本暴全部在库（sources 列）。下表登记已审验源。

| 源 | 表号 | 源级卡 | status | 增量判读 |
|---|---|---|---|---|
| GRB050730A | 无逐点表（正文 Table 3 仅峰值/斜率） | 无（本卡即索引） | mention-only | 论文给出的峰值星等 17.22、峰值时刻 744 s、α>500s=-0.89±0.05 为正文可核值，接手者可抄进 comment；逐点星等不可核 |

## 增量门槛判读

- 该文对任何库内源都**没有可采纳的逐点测光**（图上读数禁止入库）：不开源级卡。
- 若 Dainotti 系 Oates 行在其他源出现，同样应核查其可溯源性（预计同样无出处，需 discard 或维护者裁决）。

## 待决

- Dainotti DB 的 Oates 逐点数值来源（疑为作者私有数据）：需要维护者决定全库 Oates 行的处置（恢复/删除）。
