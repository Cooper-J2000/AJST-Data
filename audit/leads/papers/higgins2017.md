# 文献级索引卡：Higgins+2017

- paper_key: higgins2017
- paper: Higgins+2017, MNRAS 470, 314-323（DOI 10.1093/mnras/stx1163; arXiv:1705.06744）
- date: 2026-11-06
- helper: wa1kmoon@zcode
- sources: GRB091111, GRB121212A, GRB100909A, GRB150831A, GRB110112A, GRB110428A, GRB140219A

## 为什么是文献级卡

Higgins+2017 是 INTEGRAL IBAS WEAK（亚阈值）触发的 Swift ToO 专篇研究：15 个 WEAK 触发
（11 个自选 ToO 命名 IGRWYYMMDD + 4 个此前已有 XRT 观测的候选 GRB），6 个确认为 GRB。
给出每个源的 XRT 观测窗口（表 2）、部分源的 XRT 谱参数（表 3）与 UVOT 多滤光片测光/上限
（表 4），附录三段式表给出 92 个 IBAS GRB 的注量/T90/11 h X 射线流量。覆盖库内 7 个源，
先建索引卡；仅 GRB121212A 过源级卡增量门槛（详见下表）。

## 涉及源一览

| 源 | 表号 | 源级卡 | status | 增量判读 |
|---|---|---|---|---|
| GRB091111 | 表 1/2/4、附录 IBAS 样本表 | —（本 PR（#911）已随源审核入库 UVOT 6 行） | extracted | UVOT v/b/u 探测（作者自注可能非真实）与 uvw1/uvm2/uvw2 3σ 上限、T90=100 s、20-200 keV 注量；库内 GCN/目录检索拿不到 UVOT 值 |
| GRB121212A | 表 2/3/4、附录表 | audit/leads/GRB121212A.md | extracted | UVOT white 23.89±0.38 探测 + 6 滤光片 3σ 上限（多幅叠加口径，库内 GCN/目录无此值）；XRT 谱与衰减参数 |
| GRB100909A | 表 2/4、附录表 | —（不开卡：源已 reviewed，2026-10-31 Rusty-Harpoon@zcode） | extracted | UVOT 6 滤光片 3σ 上限、T90=60 s、注量 21.5(+7.00/-4.70)e-7 erg/cm2（20-200 keV）；供复核参考 |
| GRB150831A | 表 2/3/4、附录表 | —（不开卡：源已 reviewed，2026-11-04 wa1kmoon@zcode） | extracted | UVOT 6 滤光片 3σ 上限、XRT WT/PC 谱参数、T90≈2 s（按 t90 属短暴）、注量 ≈3e-7 erg/cm2（作者注明转引 GCN，Mereghetti+2015） |
| GRB110112A | 正文 §Swift Analysis | —（不开卡） | mention-only | 仅正文一句：XRT 于 6.2(±0.6)e4 s 非探测（X 射线，超范围）；Fermi GBM 同时探测定性为 GRB；无数表 |
| GRB110428A | 表 1（IGRW 110428） | —（不开卡） | mention-only | 仅 XRT 非探测（图无数值表） |
| GRB140219A | 表 1（IGRW 140219） | —（不开卡） | mention-only | 仅 XRT 非探测（图无数值表） |

## 增量门槛判读

- 过门槛（该有源级卡）：GRB121212A（UVOT 值为库内 GCN/目录检索拿不到的多幅叠加测光）——
  卡已随本 PR 提交。
- 不过门槛：GRB110112A/GRB110428A/GRB140219A（仅 XRT 非探测、无数表或超 X 射线范围）。
- 已 reviewed 的 GRB100909A/GRB150831A 按契约不开新卡，判读写在上表供复核。

## 版本状态

VoR（OUP）不可达：academic.oup.com 直连 HTTP 000（连接失败，两次）、CDS VizieR
J/MNRAS/470/314 HTTP 000、archive.org HTTP 000。本卡信息取自 arXiv v2（1705.06744，
2026-06-09 更新的接受后版本；arXiv 元数据确认 DOI），表号为 arXiv v2 编号，VoR 表号未核。
登记见 `audit/unverified.tsv`（GRB091111 行，PR #911）。

## 待决

- 库外源 GRB150305A（本文确认的新 GRB，有 UVOT uvw1/uvm2 上限与 XRT 探测）与 IGRW151019
  （AGN 候选）不在库内：本 PR 范围所限未开 new-source Issue，是否建源由维护者裁定。
- 其余库外 IGRW 触发（160610/150903/150610/130904/110718/110608）仅 XRT 非探测、无增量数值，
  不建议建源。
