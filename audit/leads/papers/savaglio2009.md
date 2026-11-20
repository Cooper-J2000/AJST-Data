# 文献索引：Savaglio+2009（46 个 GRB 宿主星系性质普查）

- paper_key: savaglio2009
- paper: Savaglio, Glazebrook & Le Borgne 2009, ApJ 691, 182（DOI 10.1088/0004-637X/691/1/182；VoR=IOP 未通读；取值经 arXiv:0803.2718v3 PDF 全文核对，2026-11-21 实取）
- date: 2026-11-21
- helper: wa1kmoon@zcode
- sources: GRB970228A, GRB970508A, GRB970828, GRB971214A, GRB980425A, GRB980613A, GRB980703A, GRB990123A, GRB990506, GRB990705A, GRB990712A, GRB991208A, GRB000210, GRB000418A, GRB000911A, GRB000926A, GRB010222A, GRB010921A, GRB011121A, GRB011211A, GRB020405A, GRB020813A, GRB020819B, GRB020903A, GRB021004A, GRB021211A, GRB030328A, GRB030329A, GRB030528A, GRB031203A, GRB040924A, GRB041006A, GRB050223A, GRB050416A, GRB050509B, GRB050709A, GRB050724A, GRB050826A, GRB050904A, GRB051022A, GRB051221A, GRB060218A, GRB060505A, GRB060614A, GRB061006A, GRB061126A

## 为什么是文献级卡

46 个 GRB 宿主的多波段性质普查：表 1（z/长短型/形态/E(B−V)）、表 2（宿主「伪测光」u'BVR/F814/J/H/K，AB 系统、已做银消改正）、表 3（发射线流量）、表 5（M*/MK/MB）、表 6（SFR）等。库内命中 46 源，故建文献级卡。

## 涉及源一览（按表分组，同表内各源行结构同构）

| 源 | 表号 | 源级卡 | status | 增量判读 |
|---|---|---|---|---|
| 上列 46 源 | 表 1/2/5/6 | 无（见下判读） | extracted（GRB050724A 行已逐值核对；其余源仅编目未逐行） | 见下 |

## 增量门槛判读

- **不开源级卡**（全类）：表 2 是**宿主**伪测光（无时间轴，归 `info.host_galaxy.photometry` 通道），表 1/5/6 为元数据与派生量（params 通道），均无 OT 光变行。接手者在审宿主块时直接查原文表 2 即可。
- 口径注意（接手者必读）：表 2 注明「All magnitudes (corrected for Galactic extinction) are in the AB system」——即该表已做银消改正、系统为 AB；若与未改正的其他宿主测光并列，注意口径差（GRB050724A 的 host_galaxy 内两套来源并存时已分别在条目上区分）。
- GRB050724A 行（表 2）已逐值核对：B=19.82±0.12、V=18.72±0.04、F814=18.03±0.16、J=17.23±0.04、H=16.84±0.05、K=16.65±0.04（z=0.257、short）。

## 待决

- 无。
