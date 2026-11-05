paper_key: wiseman2020
paper: Wiseman P. et al. 2020, MNRAS 498, 2575, "The host galaxies of 106 rapidly evolving transients discovered by the Dark Energy Survey", DOI 10.1093/mnras/staa2474（arXiv:2005.08653v1，OA）
date: 2026-11-06
helper: wa1kmoon@zcode
sources: DES13X1hav,DES13X3gmd,DES13X3gms,DES14C3tnz,DES14S2pli,DES15C3mgq,DES15E2nqh,DES15S1fli,DES16C1cbd,DES16C2ggt,DES16E2pv,DES16X1eho,DES16X3cxn,DES17C3gen,DES17S2fee,DES17X3cds

## 为什么是文献级卡

DES 5 年 RET 宿主星系研究（106 个 RET = Pursiainen+2018 样本 + Season 5 + 新搜索法补充）。库内全部 16 个
DES 源（上表）都在其 106 样本中。**宿主研究文章：无瞬变体测光**；增量为宿主层面的量与样本选择口径：

- 表 1（tab:obs）：106 源宿主信息——宿主 RA/Dec（J2000，机读全表仅在线版）、宿主 r 波段 Kron 星等（深 coadd）、
  z、光谱巡天/曝光时间。**库内 DES 源的 ra/dec 即本表宿主坐标**（DES16X3cxn 审核时已做一致性推证，
  见该源 comment；z=0.58464 等精确值来自本表机读版）。
- 表 2（宿主性质）：49 个有光谱宿主的 log M*/log SFR/log sSFR/12+log(O/H)（多标度），在线机读。
- 表 5（tab:fluxes，arXiv v1 表序第 5）：发射线流量（附录）。
- §2 的 RET 选择口径（g−r 色 + r 波段上升时标 cut，Gaussian Process 光变拟合）是各源 tag=[fbot] 的分类依据。

## 涉及源一览（全部 mention-only，未开源级卡）

| 源 | 表号 | 源级卡 | status | 增量判读 |
|---|---|---|---|---|
| 全部 16 个库内 DES 源 | 表 1（机读）、表 2（49 源子集） | 无 | mention-only | 表 1 机读行（宿主坐标/z）未逐行核（OUP 反爬）；表 2 中 DES13C1tgd/DES13C3bcok/…/DES17X3cds 等 49 源行在 arXiv v1 TeX L449–504 已见，接手者审核时可直接取 |
| DES13X3gmd、DES14C3tnz、DES17C3gen、DES17S2fee、DES17X3cds | 表 1 | 无 | mention-only | **仅见于本文**（Season 5 / 新搜索法，不在 Pursiainen+2018 样本）——其 z/宿主信息的唯一文献出处；T0/t_peak 在本文中不提供（无逐源光变参数表） |

## 增量门槛判读

- 不为各源写源级卡：表 1/表 2 的机读行本次不可得（OUP Cloudflare 403，已登记 unverified.tsv），
  arXiv TeX 只印了表 1 前 40 行与表 2 的 49 行；各源接手者需先取 VoR 机读表（或 arXiv TeX 表 2 行）再核。
- DES17C3gen 的 z=0.92（无类型标注）已在建源时按本文表 1 机读版提取，接手者注意该值只有本文出处。

## 版本与可用性

- VoR（OUP）Cloudflare 反爬 403；web.archive.org 超时；SciX 返回 JS 壳。arXiv:2005.08653v1 TeX 已通读：
  表 1 机读全表、表 2 机读全表均不在 arXiv 侧（正文只印节选）。
- 光变：本文无逐源测光表/图（GP 拟合参数只在样本层面）——瞬变体测光仍以 Pursiainen+2018 附录图
  为唯一出处（见 papers/pursiainen2018.md）。
