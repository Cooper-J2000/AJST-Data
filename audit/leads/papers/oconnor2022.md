# 文献索引：O'Connor+2022（短暴宿主星系深像巡天，31 个 hostless 候选）

- paper_key: oconnor2022
- paper: O'Connor+2022, MNRAS 515, 4890–4928（DOI 10.1093/mnras/stac1982；arXiv:2204.09059；VoR PDF 已取并核对——OUP 整站 Cloudflare 403，经浏览器会话取得正式版，6 377 281 B，印刷 DOI/卷页已核、无 arXiv 水印）
- date: 2026-11-13
- helper: fsy@zcode（GRB120630A 审核 PR #1066）
- sources: GRB060121, GRB091109B, GRB101224A, GRB110112A, GRB110402A, GRB120305A, GRB120630A, GRB130822A, GRB130912A, GRB131004A, GRB140129B, GRB140516A, GRB140622A, GRB140930B, GRB150423A, GRB150831A, GRB151229A, GRB160408A, GRB160410A, GRB160525B, GRB160601A, GRB160927A, GRB170428A, GRB170728B, GRB171007A, GRB180618A, GRB180727A, GRB180805B, GRB191031D, GRB200411A

## 为什么是文献级卡

该文对 31 个「无预设宿主」的 Swift 短暴做 Gemini/LDT/Keck/GTC/VLT/HST 深像与部分光谱，
给出 putative host 判定、概率巧合度（Pcc）、投影偏移与（部分源的）红移；正文声明
"All reported magnitudes are in the AB system, and are corrected for Galactic extinction
(Schlafly & Finkbeiner 2011)"。主要表：**Table 1**（成像日志，逐暴逐历元：日期/望远镜/仪器/滤光片/
曝光/该历元 putative host 的 AB 星等与 A_λ——注意是**宿主星系测量**，非瞬变体测光）、**Table 2**
（光谱观测日志）、**Table 3**（宿主性质：σ_xrt/σ_XC/R⊥(arcsec,kpc)/宿主 AB 星等/Host?/Pcc/**z 列**——
z 列混有光谱红移与脚注 e 的 z_phot，接手者须逐行看脚注）、附录 **A2.1–A2.14**（逐暴小节：XRT 定位、
深像 3σ 限值——多数含日期锚、宿主候选逐个判读、由 X 射线光变推的环境密度下限 n_min）。
表格/附录覆盖库内 **30 源**（见 sources），远超 3 源门槛，故开文献级卡。

## 涉及源一览

| 源 | 表号 | 源级卡 | status | 增量判读 |
|---|---|---|---|---|
| GRB120630A | Table 1/3、附录 A2.3 | 无（本 PR 审核对象） | extracted | 提出者已逐值核对并入 PR #1066：z_phot 判 phot、Gemini 深像限值入 lc（详见该源 info comment） |
| GRB060121 | Table 1、正文 | 无 | mention-only | sGRBEE 候选（无宿主）；Table 1 有 Keck 成像行（05-27-2014），限值口径接手者自核 |
| GRB091109B | Table 3、附录 A2.x | 无 | mention-only | Table 3 行（光学定位块）+ 附录深像限值/宿主判读 |
| GRB101224A | Table 3、附录 A2.1 | 无 | mention-only | 附录 A2.1 深像限值（含日期锚）与宿主判读 |
| GRB110112A | Table 3、附录 A2.x | 无 | mention-only | Table 3 行 + 附录深像限值 |
| GRB110402A | Table 1/2/3、附录 A2.x | 无 | mention-only | Table 3 z 列给该暴红移（本文工作）；Table 2 有其光谱行——若库内 z 为空为新正式引用 |
| GRB120305A | Table 1/3、附录 A2.2 | 无 | mention-only | 附录 A2.2：LDT/Keck 深像限值（含日期锚）与 G1 宿主判读 |
| GRB130822A | Table 1/3、附录 A2.4 | 无 | mention-only | 附录 A2.4：Keck 深像限值（含日期锚）与 G7 宿主（SDSS 光谱红移，引 Wiersema+2013）判读 |
| GRB130912A | Table 3、附录 A2.x | 无 | mention-only | Table 3 行 + 附录深像限值 |
| GRB131004A | Table 1/2/3、附录 A2.x | 无 | mention-only | Keck/MOSFIRE 光谱（Table 2）+ 深像限值 |
| GRB140129B | Table 1/3、附录 A2.x | 无 | mention-only | Table 3 z 列给 z_phot（脚注 e）；附录有 UVOT 探测记录与深像限值 |
| GRB140516A | Table 1/3、附录 A2.5 | 无 | mention-only | 附录 A2.5：判 observationally hostless，给 i 波段深像限值（含日期锚） |
| GRB140622A | Table 1/2/3、附录 A2.6 | 无 | mention-only | 附录 A2.6：Keck/LRIS 光谱（本文工作，发射线证认）给宿主红移；G1 判 putative host——若库内 z 为空为新正式引用 |
| GRB140930B | Table 3、附录 A2.x | 无 | mention-only | Table 3 行 + 附录深像限值 |
| GRB150423A | Table 3、附录 A2.x | 无 | mention-only | Table 3 行 + 附录深像限值 |
| GRB150831A | Table 1/3、附录 A2.7 | 无 | mention-only | 附录 A2.7：Integral/Swift 双探测、Gemini i 波段限值（含日期锚） |
| GRB151229A | Table 1/2/3、附录 A2.8 | 无 | mention-only | 附录 A2.8：G1 宿主（多历元多仪器测光）+ z_phot（prospector，Keck 谱无迹）——若库内 z 为空为新正式引用 |
| GRB160408A | Table 3、附录 A2.x | 无 | mention-only | Table 3 行 + 附录深像限值 |
| GRB160410A | Table 1/3、附录 A2.x | 无 | mention-only | 正文称其为例外的余辉光谱 case（Fig. 5）；Table 3 z 列有值（脚注须逐行核对） |
| GRB160525B | Table 3、附录 A2.x | 无 | mention-only | Table 3 行 + 附录深像限值 |
| GRB160601A | Table 1/2/3、附录 A2.x | 无 | mention-only | Keck/MOSFIRE 光谱（Table 2）+ 深像限值 |
| GRB160927A | Table 3、附录 A2.x | 无 | mention-only | Table 3 行 + 附录深像限值 |
| GRB170428A | Table 3、附录 A2.x | 无 | mention-only | Table 3 行 + 附录深像限值 |
| GRB170728B | Table 1/2/3、附录 A2.x | 无 | mention-only | Table 3 z 列给 z_phot（脚注 e）；Table 2 光谱 + 附录深像限值 |
| GRB171007A | Table 1/3、附录 A2.10 | 无 | mention-only | 附录 A2.10：两个候选源判读与深像限值（含日期锚） |
| GRB180618A | Table 1/3、附录 A2.x | 无 | mention-only | Table 3 z 列给 z_phot（脚注 e）；Table 1 多历元成像行 |
| GRB180727A | Table 3、附录 A2.11 | 无 | mention-only | 附录 A2.11：Swift/BAT+Fermi/GBM 双触发、Gemini/VLT 深像限值 |
| GRB180805B | Table 1/3、附录 A2.12 | 无 | mention-only | 附录 A2.12 深像限值与宿主判读 |
| GRB191031D | Table 1/3、附录 A2.x | 无 | mention-only | 附录：两个候选宿主（含 Source A）判读与深像限值（含日期锚） |
| GRB200411A | Table 3、附录 A2.14 | 无 | mention-only | 附录 A2.14：G1 判 putative host + z_phot（prospector）——若库内 z 为空为新正式引用 |

## 正文提及、无表行的库内源（多为样本筛选/著名案例对照，增量有限）

GRB050509B、GRB050724A、GRB051210、GRB060502B、GRB070707、GRB070714B、GRB081024A、GRB090426、
GRB090515、GRB090621B、GRB100206A、GRB100625A、GRB100628A、GRB101219A、GRB111020A、GRB120804A、
GRB121226A、GRB130313A、GRB140320A、GRB140611A、GRB141212A、GRB150120A、GRB150301A、GRB150728A、
GRB160624A、GRB161104A、GRB170524A、GRB170817A、GRB180402A、GRB181123B、GRB200826A、GRB200907B、
GRB201006A、GRB211211A——均未给表行（status 一律 mention-only、不开源级卡），接手者如在本文遇到
请按上下文自核。

## 增量门槛判读

- **提出者仅对 GRB120630A 做了逐值核对与入库**（z_phot 判 phot、Gemini r≳25.0 限值入 lc、宿主候选入
  comment）；其余 29 源均为 mention-only：本卡只给表号/小节定位，**未提取数值、未写源级卡**——按
  §3.11「线索不是核验」，接手者须自行打开原文逐值核对。
- 共性增量（凡库内对应字段为空的源都可能过门槛）：① Table 3 z 列的 z_phot（脚注 e，prospector SED，
  未单独发 GCN）；② 附录 A2.x 的深像 3σ 限值（多数给出观测日期/相对时长锚，属库内 GCN/目录检索
  拿不到的自算值）；③ 附录的 X 射线光变环境密度下限 n_min（非测光，仅备查）。
- 共性非增量：Table 1 的逐历元测光是 **putative host 的宿主星系测量**，不得当瞬变体测光入库
  （§3.10 宿主/瞬变体区分）；Table 2 为光谱观测日志。
- 未写源级卡的原因：逐一核对 29 源的库内现状（redshift 是否已有、lc 是否已有对应限值行）超出本 PR
  范围；已在 PR #1066 待决事项提出，请维护者裁定是否需要补写源级卡或按本卡直接接手。

## 待决

- **库外源 16 个**（正文提及或表行）：GRB 040924、GRB 050709、GRB 050724、GRB 050813、GRB 060614、
  GRB 060801、GRB 061201、GRB 061210、GRB 061217、GRB 070729、GRB 080123、GRB 080426A、GRB 080702A、
  GRB 150101A、GRB 170127B、GRB 170728A——其中 170127B、170728A 有 Table 1/3 行（深像/宿主性质）。
  是否开 `new-source` Issue 由维护者裁定（多为文献充分的著名暴，提出者不建议全开）。
- 源名枚举方法：对 VoR 全文做免前缀暴名正则（YYMMDD+可选字母，月日合法化校验，已剔除授权号
  CEX2019-000920-S 之类伪命中）；Table 1 为横排版，pdftotext 线性化失败，提出者对 GRB120630A 行用
  PyMuPDF 页面渲染逐格核对（其余源未做页面级核对，接手者建议同法避免横排表错位）。提取底稿在
  提出者工作目录 `_conv/lit-GRB120630A/`（oconnor2022_vor.txt）。
