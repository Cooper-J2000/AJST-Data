paper_key: pursiainen2018
paper: Pursiainen M. et al. 2018, MNRAS 481, 894, "Rapidly evolving transients in the Dark Energy Survey", DOI 10.1093/mnras/sty2309（arXiv:1803.04869v2，OA）
date: 2026-11-06
helper: wa1kmoon@zcode
sources: DES13X1hav,DES13X3gms,DES14S2pli,DES15C3mgq,DES15E2nqh,DES15S1fli,DES16C1cbd,DES16C2ggt,DES16E2pv,DES16X1eho,DES16X3cxn

## 为什么是文献级卡

DES-SN 4 年（Y3A2）快演化暂现源（RET）主文：72 个事件（37 个 gold+silver 有光谱红移、35 个 bronze 无），
库内 11 个 DES 源（上表）全部在 gold sample 中。文章的核心增量是**逐源的绝对时间锚点与光变参数**：

- Table 5（arXiv v2 编号，tab:photometric）：g 波段光变参数——**t_peak = 观测 g 波段最亮点日期（整数 MJD）**
  （本库各 DES 源 T0 均为 null，这是目前唯一可用的绝对时间锚点）、M_peak(g)、t_rise、t_decline、t_1/2（rest frame）；
- Table 6（tab:bb_peak）：峰处黑体拟合 T/r/L 与数据点数；
- Table 4（tab:sample）：瞬变体坐标（J2000 六十进制）、z_spec、E(B−V)（Schlafly+2011）；
- Table 7：宿主 SED 拟合 log M*、log sSFR；
- Table 3（tab:z_sources）：宿主巡天、偏移（″/kpc）、DLR、z_spec/z_phot。

**光变本身只有附录图**（lc_all_gold/silver/bronze*.pdf，37+35 事件），无任何数值测光表——按契约不读图入库。

## 涉及源一览（仅列库内源；其余 gold/silver/bronze 事件均 out_of_repo）

| 源 | 表号（arXiv v2 编号） | 源级卡 | status | 增量判读 |
|---|---|---|---|---|
| DES16X3cxn | 表 4/5/6/7 | 无（本源已审，数值入 info comment，PR #921） | extracted | T0 已按 t_peak MJD 57694 入 info |
| DES13X1hav | 表 4/5/6/7 | 有（leads/DES13X1hav.md） | extracted | t_peak MJD 56551 等，T0 待定锚 |
| DES13X3gms | 表 4/5/6/7 | 有（leads/DES13X3gms.md） | extracted | t_peak MJD 56567 |
| DES14S2pli | 表 4/5/6/7 | 有（leads/DES14S2pli.md） | extracted | t_peak MJD 56987 |
| DES15C3mgq | 表 4/5/6/7 | 有（leads/DES15C3mgq.md） | extracted | t_peak MJD 57331 |
| DES15E2nqh | 表 4/5/6/7 | 有（leads/DES15E2nqh.md） | extracted | t_peak MJD 57366 |
| DES15S1fli | 表 4/5/6/7 | 有（leads/DES15S1fli.md） | extracted | t_peak MJD 57276 |
| DES16C1cbd | 表 4/5/6/7 | 有（leads/DES16C1cbd.md） | extracted | t_peak MJD 57660 |
| DES16C2ggt | 表 4/5/6/7 | 有（leads/DES16C2ggt.md） | extracted | t_peak MJD 57756 |
| DES16E2pv | 表 4/5/6/7 | 有（leads/DES16E2pv.md） | extracted | t_peak MJD 57629 |
| DES16X1eho | 表 4/5/6/7 | 有（leads/DES16X1eho.md） | extracted | t_peak MJD 57722 |

库内其余 DES 源（DES13X3gmd、DES14C3tnz、DES17C3gen、DES17S2fee、DES17X3cds）为 Season 5 / 新搜索法发现，
**不在**本文样本中（见 papers/wiseman2020.md）。

## 增量门槛判读

- **过门槛**：上表全部源——t_peak（整数 MJD）/M_peak/t_rise/t_decline/t_1/2 与黑体参数是库内 GCN/目录检索
  拿不到的数值，且 t_peak 是 T0 审核必需的时间锚点；每源一张源级卡（status: extracted，原始行已录）。
- **不过门槛**： bronze 样本 35 个（库内无对应源）。

## 版本与可用性

- VoR（OUP MNRAS 481, 894）Cloudflare 反爬 403 不可达；CDS/VizieR 三镜像超时——已登记
  `audit/unverified.tsv`（DES16X3cxn 行，status=substituted）。全部数值取自 **arXiv:1803.04869v2** 实读 TeX，
  表号均为 arXiv v2 编号，VoR 表号待接手者核对。
- 契约提醒：接手者仍须自行打开原文逐值核对（防转录错误传染），不得直接抄卡。
