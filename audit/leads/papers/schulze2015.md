# 文献索引：Schulze+2015（TOUGH Survey VII——宿主光度函数，含 050803/050922B 光测红移与宿主测光）

- paper_key: schulze2015
- paper: Schulze+2015, ApJ 808, 73（DOI 10.1088/0004-637X/808/1/73；arXiv:1503.04246v2；Swift/BAT 目录 GRBlist_redshift_BAT 对 050803 红移值即引此文）
- date: 2026-11-20
- helper: wa1kmoon@zcode
- sources: GRB050315A, GRB050318A, GRB050401A, GRB050406A, GRB050416A, GRB050502B, GRB050525A, GRB050714B, GRB050730A, GRB050801A, GRB050819, GRB050820A, GRB050822, GRB050824A, GRB050904A, GRB050908A, GRB050915A, GRB050922B, GRB050922C, GRB051001, GRB051006A, GRB051016B, GRB051117B, GRB060115A, GRB060218A, GRB060306, GRB060522A, GRB060526A, GRB060604A, GRB060605A, GRB060607A, GRB060614A, GRB060707A, GRB060708A, GRB060714A, GRB060719A, GRB060729A, GRB060805A, GRB060814A, GRB060908A, GRB060912A, GRB060923A, GRB060923B, GRB060927A, GRB061007A, GRB061021A, GRB061110A, GRB061110B, GRB061121A, GRB070103, GRB070110A, GRB070129A, GRB070224A, GRB070306A, GRB070318A, GRB070328, GRB070419B, GRB070506A, GRB070611A, GRB070721B, GRB070802A, GRB050726, GRB050803A, GRB060919, GRB060923C, GRB061004, GRB070330, GRB070621, GRB070808

## 为什么是文献级卡

TOUGH VII 基于 TOUGH 样本（Swift GRB 宿主 69 个）做宿主光度函数：Table 2 逐暴给宿主红移+一个波段的宿主星等+βUV+M1600
（红移多转引自 Hjorth+2012/Perley+2013/Krühler+2015 等）；Table 3 给 8 个 HST 深场宿主（z=3–4）的结构参数与 F775W/F160W 测光；
Table 4 给 GRB 050803 与 050922B 的多波段宿主测光（g'/R/i'/z'/F160W/Ks/IRAC，银消光已改正口径）并新测两暴光测红移。
对 GRB050803A：z=3.5±0.5（phot）已由本源审核（PR #1121）入库（redshift_type=phot，redshift_ref=Schulze+2015），本卡不承载其行。

## 涉及源一览

| 源 | 表号 | 源级卡 | status | 增量判读 |
|---|---|---|---|---|
| GRB050803A | Table 2/4 | 无（本源已审，PR #1121） | extracted（z=3.5±0.5 phot 已入库；Table 4 宿主测光与 host_galaxy 既有 Perley+2016 元组同源异口径，未重复入库） | 已消化 |
| GRB050922B | Table 2/4 | GRB050922B.md | extracted | Table 4 宿主测光为「银消光已改正」口径，与库内 host_galaxy 既有 Perley+2016 Table 4（未改正）成对错位，换口径会真出错 → 开源级卡 |
| GRB050730A, GRB050908A, GRB060115A, GRB060526A, GRB060605A, GRB060607A, GRB061110B, GRB070721B | Table 3 | 无 | mention-only | HST 宿主结构参数（r1/2、r0、pch）与 F775W/F160W 宿主测光；宿主属性数据，接手者比对各自 host_galaxy 是否已覆盖 |
| GRB050726, GRB050922B, GRB060919, GRB060923C, GRB061004, GRB070330, GRB070621, GRB070808 | Table 2（Hosts with Unknown Redshifts + footnote g） | 无 | mention-only | 宿主红移上限（050726 z<5.5、050922B z<6.1、061004 z<10、070330 z<5.5 等，宿主非探测推得）；红移上限级信息，接手者勘酌是否补注 |
| 其余 52 源（TOUGH 已知红移样本） | Table 2 | 无 | mention-only | 宿主星等/βUV/M1600 多转引 Hjorth+2012/Perley+2013/Krühler+2015（库内 host_galaxy 已按各自审核口径处理）；纯汇编转引，不开源级卡 |

## 增量门槛判读

- 过门槛：GRB050922B（Table 4 银消改正口径宿主测光 + Table 2 新光测红移 4.5±0.5，与库内 Perley+2016 z=4.9 并存需接手者判读）→ 已写 `audit/leads/GRB050922B.md`。
- 不过门槛：Table 2 已知红移 52 源的宿主星等系 TOUGH/Hjorth+2012 编译（数值同源），纯汇总转引不开卡；Table 3 HST 参数属宿主属性、非瞬变体测光，索引即可。
- 版本状态：IOP VoR 页 HTTP 403（Cloudflare 人机验证，2026-11-20 实测）；CDS/VizieR 无 J/ApJ/808/73 表；取 arXiv v2 全文核对（已登记 audit/unverified.tsv）。数值均取自 arXiv v2 Table 2/3/4 与脚注，未通读 VoR。

## 待决

- Table 2/3 的宿主测光/结构参数是否值得在各自源被审核时并入 host_galaxy（口径：Table 2 已转 AB 且改正银消光；Table 4 改正银消光；与库内既有「未改正」口径并存时需逐源裁定）——留给接手者，不在本卡批量处理。
