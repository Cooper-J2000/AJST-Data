# 文献级索引卡：Jelinek+2010（BOOTES-1B 四年跟踪汇总）

- paper_key: jelinek2010
- paper: Jelinek+2010, "Four Years of Real-Time GRB Followup by BOOTES-1B (2005-2008)", Advances in Astronomy 2010, 432172（DOI 10.1155/2010/432172；arXiv:1001.2147）；VoR PDF 已实取（Hindawi/Wiley gold OA，dl 存档 3,683,248 B，印刷头/citation meta 核验）
- date: 2026-11-19
- helper: fsy@zcode
- sources: GRB050215B,GRB050509A,GRB050509B,GRB050525A,GRB050922C,GRB051109A,GRB051211B,GRB051221B,GRB060421,GRB061110B

## 为什么是文献级卡

本文是 BOOTES-1B（30 cm，El Arenosillo）2005-2008 四年 GRB 实时跟踪的汇总专篇：正文 §3 按事件逐暴 case 段（(a)-(x)），Table 1 为成功跟踪暴的汇总表（GRB | Tobs-Ttrigger | Tobs-Tnotice | mag），§4.1 另有一张逐暴统计表（GCN notice 号 + 最佳极限引用 + 备注）。覆盖约 24 个暴，其中 **10 个为库内已存在源**（上 sources 键），随 GRB050528 审核（PR #1103）一并读得。GRB050528 自身的 BOOTES 数据已入该 PR 的 lc（V/I 上限 2 行，GCN 3500 + VoR (f) 段），不在本卡范围。

## 涉及源一览

| 源 | 表号/出处 | 源级卡 | status | 增量判读 |
|---|---|---|---|---|
| GRB050215B | 正文 (a) + Table 1 + §4.1 统计表 | 无 | existing | lc 已有 BOOTES-1B(30cm) V>16.5/I>15.0 @1836 s 两行（Dainotti2024;3023 转引）；正文口径为 "22 minutes after the GRB" 起 slew、coadd 600 s 双 20 cm 望远镜得 V>16.5/I>15.0——1836 s 与正文 22 min 的对应关系待接手者核对 |
| GRB050509A | 正文 (c) + Table 1 + §4.1 统计表 | [GRB050509A.md](../GRB050509A.md) | extracted | 单帧 V>14.9 @63.8 min + 112×10 s coadd V>18.1 @88.0 min（作者自算，未见对应 GCN）；lc 无 BOOTES 行 |
| GRB050509B | 正文 (d) + Table 1 + §4.1 统计表 | [GRB050509B.md](../GRB050509B.md) | extracted | 首 10 s V>11.5 + 12×10 s coadd V>12.5（天线遮挡降质）；Table 1 行 mag 与正文不一致 |
| GRB050525A | 正文 (e) + Table 1 + §4.1 统计表 | [GRB050525A.md](../GRB050525A.md) | extracted | BOOTES-1B 首次探测 V 15.0 @383 s（lc 477 行中无 BOOTES 行） |
| GRB050922C | 正文 (k) + Table 1 + §4.1 统计表 | [GRB050922C.md](../GRB050922C.md) | extracted | 228 s 弱探测 R 14.5 + 天气差极限 12.9；正文另给 BAT 触发 19:55:50 UT（该文口径，可交叉 T0） |
| GRB051109A | 正文 (l) + Table 1 + §4.1 统计表 | 无 | existing | lc 已有 BOOTES-1B(30cm) R @59.8 s 一行（Dainotti2024;4227 转引）；正文 "54.8 s after the burst in R and I bands" 双滤光（该文唯一多滤光探测）与 Table 1 印 R 14.5 @54.8 s 的关系待核 |
| GRB051211B | 正文 (m) + Table 1 + §4.1 统计表 | [GRB051211B.md](../GRB051211B.md) | extracted | 42 s 起 30 s R 曝光一帧后相机故障；Table 1 印 R 16.2（正文未给数值，性质待对 GCN 4333） |
| GRB051221B | 正文 (n) + Table 1 + §4.1 统计表 | 无 | existing | lc 已有 GCN 4379（=正文引 [22] BOOTES 观测通告）四行 R 上限 @235/307/353/665 s；Table 1 印 I > 14.0 @234.8 s——I 波段极限未在 lc，接手者若核 GCN 4379 无载可作补充候选 |
| GRB060421 | 正文 (o) + Table 1 + §4.1 统计表 | [GRB060421.md](../GRB060421.md) | extracted | R > 14（首 10 s）+ R > 16（30 图组合，均值时刻 547 s）；Table 1 行 mag 与正文不一致 |
| GRB061110B | 正文 (p) + Table 1 + §4.1 统计表 | [GRB061110B.md](../GRB061110B.md) | extracted | 该文给 BAT T0=21:58:45 UT、notices 延迟 626 s（downlink）；Table 1 印 R > 16.0 @698 s |

## 增量门槛判读

- **7 个过门槛建源级卡**（050509A/050509B/050525A/050922C/051211B/060421/061110B）：lc 均无 BOOTES 行（telescope/reference 列检索确证，2026-11-19）；case 段数值为该文自有（作者自算 coadd、响应时刻 Tobs-Tnotice 列），满足门槛第 1 条（库内 GCN/目录检索拿不到的数值）。
- **3 个不建源级卡**（050215B/051109A/051221B，status=existing）：lc 已有 BOOTES 观测行（2/1/4 行），增量已部分入库；其 case 段与 Table 1 口径差异写在上表"增量判读"列，接手者按行核对即可，不再单开卡。
- 库外源（050505/050520/050730/050805B/050824/050904/071101/071109/080330/080413A/080430/080605/081003B 等）：不建卡、不写 out_of_repo 键（new-source Issue 需 gh 权限，本 lane 未开）——清单在此报备，由维护者决定是否开 Issue。

## 待决

- **Table 1 mag 列错位警示**：VoR Table 1 的 mag 列与正文 case 段系统性错位（050525A 行印 "V > 12.5"、050528 行印 "V 15.0"、050730 行印 "V > 13.8, I > 13.0"——050528 行的 V 15.0 实为 050525A 的探测值、050730 行实为 050528 的上限）；另有 050509A 行印 V > 14.0（正文 V > 14.9）、050509B 行印 V > 18.1（正文 V > 11.5/V > 12.5）、050922C 行印 R > 18.2（正文 228 s 弱探测 R 14.5）、060421 行印 V > 13.3（正文 R > 14 / R > 16）。**取值一律以正文 (a)-(x) case 段为准，Table 1 mag 列不可直接照抄。**
- 库外源是否批量开 new-source Issue 由维护者裁定（清单见上）。
- 双栏排版提示：pdftotext 提取该 VoR 时左右栏交叠（图注插入 case 段），复原原句需按语义接续（本卡与各源级卡已按语义复原处均注明）。
