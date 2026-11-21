# 文献索引：McBreen+2010（GROND 四 Fermi/LAT 暴光学/NIR 跟测）

- paper_key: mcbreen2010
- paper: McBreen et al. 2010, A&A 516, A71（DOI 10.1051/0004-6361/200913734；arXiv:1003.3885；A&A 全文页 DataDome 反爬 403，2026-11-22 经 arXiv 源码通读）
- date: 2026-11-22
- helper: Rusty-Harpoon@zcode
- sources: GRB090323A, GRB090328A, GRB090510A, GRB090902B
- out_of_repo:

## 为什么是文献级卡

GROND（MPG/ESO 2.2m）对四个 Fermi/LAT 暴（090323/090328/090510/090902B）的光学/NIR 跟测专篇
+ 090323 的 TLS 补充、090328/090510 的 VLT 光谱。**关键限制：全文没有测光表**——四暴的多色
GROND 光变只在图（090323 为 Fig.4，GROND 7 波段 + TLS Rc；090328/090510/090902B 亦为图），
正文明确「Late upper limits are not shown」；表仅 3 张（090328 吸收线表、090510 发射线表、
暴属性汇总表 Table 2 含 z/Eiso/暴参数）。按提示词 §3.3「只有图没有表时不得从图上读数入库」，
本篇**无可提取测光行**，只能用其正文结论（拟合参数、host 检出）与图注数值。

口径要点（接手者核对 GCN 9026 GROND 行时可引）：GROND g'r'i'z' 用 SDSS DR7 定标、JHK 用 2MASS
（090323 场）；典型绝对精度 g'r'i'z' 0.04 / JH 0.06 / Ks 0.08 mag，已平方加入误差；TLS 数据用
6 颗 SDSS 星、Lupton (2005) 转换定标 Rc；090323 GROND 起测 T0+27 h（GCN 9026 的 02:50 UT），
最后一历元 T0+100 d；090323 光变拟合为幂律+拐角成分+host 常数项，alpha=1.90±0.01；
090323 host 在 r'、i' 检出（g'z'JHKs 不定，拟合中固定）；E(B-V)=0.03。

## 涉及源一览

| 源 | 表号 | 源级卡 | status | 增量判读 |
|---|---|---|---|---|
| GRB090323A | 无测光表（Fig.4 光变）；Table 2 含本暴 z/Eiso 汇总行 | 无（本源已审，PR #1163；GROND 行已按 GCN 9026 入库） | mention-only | 不开源级卡（图上无数表）；其 GROND 晚期点与 host 值无法按行入库，待 A&A「data behind figure」或作者数据公开后再议 |
| GRB090328A | 吸收线表 + Table 2 属性行 | 无（该源已 reviewed） | mention-only | 同上（光变仅图） |
| GRB090510A | 发射线表 + Table 2 属性行 | 无（该源已 reviewed） | mention-only | 同上 |
| GRB090902B | Table 2 属性行；光变仅图 | 无 | mention-only | 同上 |

## 增量门槛判读

- 四源均**不过**类型 1 门槛（无测光表可提取；图读数禁止）——只留本索引卡，不写源级卡。
- 类型 3（新正式文献引用）角度：GROND 数据行的 articles[] 若缺本篇，接手者可补引
  （090323 的 GROND 行本 PR 已在 info.comment 引用链注明 GCN 9026→McBreen+2010 无表）。

## 待决

- A&A 官网（DataDome）未取到 VoR 页面，「data behind the figure」是否存在未确认；
  arXiv 源码内无数据表已确认。若维护者能取 A&A 附件，090323 的 GROND 晚期多色点值得入库。
