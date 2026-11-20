# 文献索引:Perley+2016(SHOALS I,Swift GRB 宿主星系 Legacy Survey I)

- paper_key: perley2016
- paper: Perley et al. 2016, ApJ 817, 7(DOI 10.3847/0004-637X/817/1/7;arXiv:1504.02482)
- date: 2026-11-20
- helper: wa1kmoon@zcode
- sources: GRB050803A, GRB050922B, GRB060204B, GRB061202, GRB070223A, GRB080205A, GRB080319A, GRB081210A

## 为什么是文献级卡

该文 §5「NEW REDSHIFT CONSTRAINTS」§5.1 逐暴注记给出 **8 个此前未发表**("Eight new (not previously
published) redshifts have so far been established by our program")的宿主红移(光谱或 photo-z),
逐一对应下表 8 个库内源;另有 §5.2 的 9 个红移上限源与 Table 1–4 全样本表(119 暴,库内更多 Swift 时代
源在列,未逐表提取)。这些红移多数不在 GCN/GRBCAT 类目录中,对该批源构成增量(新正式文献引用 +
可能的新红移值)。本卡只做索引,不含可采纳数值以外的判读。

## 涉及源一览(§5.1 注记,2026-11-20 经 arXiv v1/v3 PDF 读毕)

| 源 | 位置 | 源级卡 | status | 增量判读 |
|---|---|---|---|---|
| GRB050803A | §5.1 注记 | leads/GRB050803A.md | extracted | 宿主 photo-z ~4.3±0.4(1σ),1.9<z<4.9(95%);与已库 z=3.5(Schulze+2015 同数据异软件)并存待判 |
| GRB050922B | §5.1 注记 | leads/GRB050922B.md | extracted | 宿主 photo-z best-fit z=4.9,4.2<z<5.2;库内 redshift=null,直接增量 |
| GRB060204B | §5.1 注记 | leads/GRB060204B.md | extracted | 宿主 X-shooter 光谱 z=2.3393(多线);库内已有同值无 type/ref,注记为正式引用增量 |
| GRB061202 | §5.1 注记 | leads/GRB061202.md | extracted | 宿主 X-shooter 光谱 z=2.2543;库内已有同值无 type/ref |
| GRB070223A | §5.1 注记 | 无(该源已 reviewed) | mention-only | 宿主 LRIS 光谱 z=1.6295;库内已入库(z=1.6295 spec),仅补引用,不开卡 |
| GRB080205A | §5.1 注记 | 无(随本 PR 入库) | extracted | 宿主 photo-z z=2.71(+0.25/−0.69)、z<3.08;已写入 info.redshift(2026-11-20) |
| GRB080319A | §5.1 注记 | leads/GRB080319A.md | extracted | photo-z 2.43(+0.20/−0.36)+ 新 MOSFIRE 光谱 z=2.0265(库内已存该值,type/ref 缺) |
| GRB081210A | §5.1 注记 | 无(该源已 reviewed) | mention-only | 宿主 X-shooter 光谱 z=2.0631([O III]λ5007 判定);库内已入库,不开卡 |

## 版本状态

- **VoR(IOP,ApJ 817, 7)未取得**(文章页 TLS 握手失败/反爬;VizieR 无 J/ApJ/817/7;INSPIRE 有记录无本地全文)。
  本次取 arXiv:1504.02482 **v1 与 v3 两版 PDF** 对照:GRB080205 注记两版逐字一致(z=2.71+0.25/−0.69),
  其余 7 源注记未做两版逐字比对。已登记 `audit/unverified.tsv`(status=substituted)。
- Table 1–4(样本参数/宿主测光表)、§5.2 红移上限 9 源名单、Figure 2/3,**均未提取**。

## 已核对 / 未核对

- 已核对:GRB080205 注记逐字(v1/v3 一致);上述 8 条注记的原文摘录(见各源级卡)。
- 未核对:各源注记与 Schulze+2015/Krühler+2015 平行发表的重叠关系;各红移是否确属"8 个未发表"之列(论文未逐一指明);
  Table 1–4;后续文献是否更新了这些红移;未做任何数值换算;库外 SHOALS 源一律未开卡。
