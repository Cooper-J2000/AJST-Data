# 文献索引：Vielfaure+2021（LAE-LGRB 普查：GRB 宿主 Lyα 发射样本）

- paper_key: vielfaure2021
- paper: Vielfaure et al. 2021, A&A 653, A83（DOI 10.1051/0004-6361/202140355；arXiv:2105.09314）
- date: 2026-11-08
- helper: Rusty-Harpoon@zcode
- sources: GRB060926A,GRB061222A,GRB071031A,GRB081222A,GRB100424A,GRB121201A,GRB150915A,GRB151021A,GRB170202A,GRB191004B

## 为什么是文献级卡

该文是 LAE-LGRB（宿主具 Lyα 发射的长暴）普查：29 个 LAE-LGRB，其中 5 个为新发表的
VLT/X-shooter 宿主光谱（GRB 060926、070110、081121、081222、100424A，此前未发表）。
覆盖库内 **10 个源**（上表），给出各源宿主 Lyα 流量/光度和（附录属性表）M_UV/logM*/SFR 等
宿主参量——这些量在 GCN/目录中拿不到，也不属于测光转引，故开文献级卡收敛索引。

## 涉及源一览

表号说明：普查表＝附录「List of the LGRBs from the literature (other than TOUGH and XHG
samples) and this work with Lyα-emission detection」（landscape 表，列＝GRB/z/宿主谱仪器/OA
谱仪器/Lyα宿主/LyαOA/EW/F(Lyα)/L(Lyα)/文献号；F 单位 1e-17 erg/s/cm2，已作银消与狭缝损失
改正）；属性表＝附录宿主属性表（M_UV、log M*、SFR 等）。GRB 060926A 另有正文 golden-sample
四张表（观测日志、Balmer/氧线流量、Lyα 线性质、壳模型拟合）。

| 源 | 表号 | 源级卡 | status | 增量判读 |
|---|---|---|---|---|
| GRB060926A | 普查表（EW 37.0±7.0 Å、F 5.30±0.40、L 5.05±0.38）＋golden-sample 4 表 | 有（leads/GRB060926A.md） | extracted | 宿主 Lyα 流量/光度＋宿主谱性质（X-shooter，未发表数据），新增正式引用 |
| GRB061222A | 普查表（F 16.80、L 5.39±0.00）＋属性表（log M*=9.55） | 有（leads/GRB061222A.md） | extracted | 宿主 Lyα 与宿主质量，新增正式引用 |
| GRB071031A | 普查表（F 2.36±0.27、L 1.41±0.16）＋属性表（M_B 22.15±0.05） | 无（源已 reviewed，其审核早于本卡；宿主 Lyα 增量留此备查，是否采纳由维护者裁断） | extracted | 宿主 Lyα，新增正式引用 |
| GRB081222A | 普查表（z=2.7700、F 1.60±0.40、L 1.07±0.27）＋属性表（M 20.80±0.20、log M*=9.61） | 无（本源随 PR #996 同批审核，宿主 Lyα 已写入该源 comment） | extracted | 宿主 X-shooter Lyα 确认 z=2.7700（未发表数据） |
| GRB100424A | 普查表（z=2.4656、F 3.4±0.5）＋属性表（log M*=7.93+0.25−0.18 等行） | 有（leads/GRB100424A.md） | extracted | 宿主 Lyα（X-shooter 未发表数据；正文另给 F=3.4±0.5e-17），新增正式引用 |
| GRB121201A | 普查表（F 2.14±0.36、L 2.31±0.39）＋属性表（M_B 22.00±0.20） | 有（leads/GRB121201A.md） | extracted | 宿主 Lyα，新增正式引用 |
| GRB150915A | 普查表（F 5.00±1.10、L 1.46±0.32）＋属性表（M_B 21.20±0.30、SFR 13.0±0.6） | 有（leads/GRB150915A.md） | extracted | 宿主 Lyα，新增正式引用 |
| GRB151021A | 普查表（F 10.50±0.90、L 4.63±0.40）＋属性表（M_B 22.20±0.20） | 有（leads/GRB151021A.md） | extracted | 宿主 Lyα，新增正式引用 |
| GRB170202A | 普查表（F 2.70±0.60、L 3.49±0.78）＋属性表（M_B 21.55±0.10） | 有（leads/GRB170202A.md） | extracted | 宿主 Lyα，新增正式引用 |
| GRB191004B | 普查表（EW 7.4±2.6 Å、F 1.00±0.10、L 1.18±0.18）＋属性表（M_B 17.20±0.15、log M*=…） | 有（leads/GRB191004B.md） | extracted | 宿主 Lyα，新增正式引用 |

## 增量门槛判读

- 10 个库内源均过门槛（判据 1：宿主 Lyα 流量/光度为 GCN/目录拿不到的量，其中 5 暴为未发表
  X-shooter 数据；判据 3：为各源提供新的正式文献引用 2021A&A...653A..83V）。
- 库外源（011211、021004、030323、030429、070110、081121、090205、971214、000926、050714B、
  050819、050915A、051001、060204B、060604、060707、060805A、060814、061202、070103、070129、
  070224、070328、070419B、070521、070802、071021、080207 等样本成员）不在库内，本卡不展开；
  如需入库请由维护者开 `new-source` Issue。

## 待决

- 无（本卡仅索引与口径记录）。
