---
paper_key: kumar2025
paper: Kumar+2025, "Discovery and Analysis of Afterglows from Poorly Localised GRBs with the Gravitational-wave Optical Transient Observer (GOTO) All-sky Survey", MNRAS 544, 1541, DOI 10.1093/mnras/staf1689（arXiv:2509.09827）
date: 2026-10-31
helper: Rusty-Harpoon@zcode
sources: GRB240122A, GRB240225B, GRB240619A, GRB240910A, GRB240916A, GRB241002B, GRB241228B
---

## 为什么是文献级卡

GOTO 协作的 LGRB 余辉样本文章，覆盖 7 个库内源（240122A、240225B、240619A、240910A、240916A、241002B、241228B，
均触发自 Fermi/GBM 或 MAXI）。表 A1 给出 7 源的 UV/光学/NIR 测光汇编（「This work」重测 + GCN 转引），
表 A2 给出射电跟踪（ATCA/VLA/AMI-LA/e-MERLIN/RT1/AMI 等），表 2/3/4 给出触发时刻、定位、红移等目录级参数。

**版本状态**：VoR = MNRAS 544, 1541–1587 (2025)，DOI 10.1093/mnras/staf1689。OUP 原站 Cloudflare 403
（HTML 与 PDF 均拦，2026-10-31 实测）；实际取值用 LJMU 机构库排版 VoR 副本
（https://researchonline.ljmu.ac.uk/id/eprint/28158/ ，页眉即「MNRAS 544, 1541–1587 (2025)」），
与 arXiv:2509.09827v1 HTML 交叉核对一致。取值走「补充入口（机构库）」渠道，未直接打开 OUP 原站。

**原文口径（全表通用）**：T0 = 触发卫星触发时刻（表 A1 各源行首给出 T0，JD 形式）；
表 A1 标题声明「All the tabulated magnitudes are in AB system」；§6.2 称种群分析光变做了银消改正
（Schlafly & Finkbeiner 2011），但表 A1 各行与 GCN 原值逐一相同，判表 A1 本身未做银消改正。
GRB 240619A 各行已由本卡建卡人逐值核对入库（见该源 PR）。

## 涉及源一览

| 源 | 表号 | 源级卡 | status | 增量判读 |
|---|---|---|---|---|
| GRB240619A | 表 A1（14 行）、表 A2（1 行 AMI-LA）、表 4（z=0.3960±0.0001） | 无（已审核） | extracted | UVOT white/u/v、NOT r′/z′×4、X-shooter 采集像 r′、ATLAS FP×2 为 GCN 检索拿不到的重测值，已直接入库（GRB240619A PR） |
| GRB240122A | 表 A1、表 A2 | 无 | extracted | 表 A1 含大量「This work」测光（LT/NOT/X-shooter/AZT-33IK 等，MAXI 触发源），多数未单独发 GCN → 过增量门槛，接手者应逐值核对 |
| GRB240225B | 表 A1、表 A2 | 无 | extracted | 同上（MAXI 触发源，「This work」行多）→ 过增量门槛 |
| GRB240910A | 表 A1、表 A2（VLA 9 行） | 无 | extracted | 「This work」UVOT 上限序列、OSIRIS/GTC、LBC/LBT、VLA 多频 → 过增量门槛；部分行转引 SVOM/VT、Giarratana |
| GRB240916A | 表 A1、表 A2 | 无 | extracted | 「This work」GOTO/UVOT/ALT/X-shooter/NOT → 过增量门槛 |
| GRB241002B | 表 A1、表 A2 | 无 | extracted | 「This work」GOTO/UVOT/LBT 等；含 GCN 转引（Torreiro Martínez、Durbak 等）→ 过增量门槛 |
| GRB241228B | 表 A1、表 A2 | 无 | extracted | 「This work」行（Mephisto im 上限、UVOT u 上限等）→ 过增量门槛 |

## 增量门槛判读

7 个库内源的表 A1 均含「This work」重测/新增测光（非纯 GCN 转引），均过增量门槛；但本文只建文献级索引，
**不为各源预写源级卡**——接手者须自己打开 VoR/机构库副本逐值核对（本卡不承载可采纳数值）。
GRB240619A 已由建卡人完整审核并入库，其行值不再留卡。

## 待决

- 无源级卡随本 PR 交付（本文覆盖的其余 6 源均未认领，接手者按上表逐值核对后自建/删除）。
- OUP 原站被 Cloudflare 全站拦截：如需逐字节比对 VoR 与机构库副本，须走浏览器路线；本轮以排版版
  页眉（MNRAS 544, 1541–1587 + DOI）与 arXiv v1 交叉核对，判为 VoR 内容一致。
