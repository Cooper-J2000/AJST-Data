# 文献级索引卡：Pélangeon+2008（HETE-2 完整样本谱参数汇编）

- paper_key: pelangeon2008
- paper: Pélangeon, A., Atteia, J.-L., Nakagawa, Y. E., et al. 2008, A&A 491, 157「Intrinsic properties of a complete sample of HETE-2 gamma-ray bursts. A measure of the GRB rate in the Local Universe」（DOI 10.1051/0004-6361:200809709；arXiv:0811.3304；VoR aanda.org 403 不可达——2026-10-29 两次尝试含浏览器 UA，数值取自 arXiv 版）
- date: 2026-10-29
- helper: wa1kmoon@zcode
- sources: GRB010213, GRB010629, GRB011019, GRB011130, GRB011212, GRB020127, GRB020305, GRB020317, GRB020331, GRB020625, GRB020801, GRB020812, GRB021016, GRB021104, GRB021112, GRB030324, GRB030416, GRB030418, GRB030723, GRB030725, GRB030823, GRB030824, GRB030913, GRB031026, GRB031111B, GRB031220, GRB040511, GRB040825A, GRB040825B, GRB040916, GRB041016, GRB041211, GRB050123, GRB050209, GRB050807, GRB060121

## 为什么是文献级卡

HETE-2 全部 250 事件筛选出的 88 暴完整样本（长暴、SNR 截断）之谱参数汇编。表 2 逐暴给出 α/β/E_obs_peak(keV)/S_X(2-30 keV，10^-7 erg/cm²)/T90,B(FREGATE 6-80 keV)/SNR/伪红移；表 3 给内禀量 log Epeak_intra/log T90_B(静止系)/log Eiso,52/zmax/V/Vmax。表 2 收录 82 暴（含 040912A/B、031109A/B 等成对事件）、其中 36 个为库内已存在源。GRB040825B 审核（本 PR）中实际使用了该文表 2 的行（E_obs_peak=25.1(+15.6/-8.2) keV 等）佐证 XRF 软谱分类，并已登记进该源 articles[]。

## 涉及源一览

| 源 | 表号 | 源级卡 | status | 增量判读 |
|---|---|---|---|---|
| GRB010213 | 表2、表3 | — | mention-only | 谱参数汇总、无测光表 → 不开卡 |
| GRB010629 | 表2、表3 | — | mention-only | 同上 |
| GRB011019 | 表2、表3 | — | mention-only | 同上 |
| GRB011130 | 表2、表3 | — | mention-only | 同上 |
| GRB011212 | 表2、表3 | — | mention-only | 同上 |
| GRB020127 | 表2、表3 | — | mention-only | 同上 |
| GRB020305 | 表2、表3 | — | mention-only | 同上 |
| GRB020317 | 表2、表3 | — | mention-only | 同上 |
| GRB020331 | 表2、表3 | — | mention-only | 同上 |
| GRB020625 | 表2、表3 | — | mention-only | 同上 |
| GRB020801 | 表2、表3 | — | mention-only | 同上 |
| GRB020812 | 表2、表3 | — | mention-only | 同上 |
| GRB021016 | 表2、表3 | — | mention-only | 同上 |
| GRB021104 | 表2、表3 | — | mention-only | 同上 |
| GRB021112 | 表2、表3 | — | mention-only | 同上 |
| GRB030324 | 表2、表3 | — | mention-only | 同上 |
| GRB030416 | 表2、表3 | — | mention-only | 同上 |
| GRB030418 | 表2、表3 | — | mention-only | 同上 |
| GRB030723 | 表2、表3 | — | mention-only | 同上 |
| GRB030725 | 表2、表3 | — | mention-only | 同上 |
| GRB030823 | 表2、表3 | — | mention-only | 同上 |
| GRB030824 | 表2、表3 | — | mention-only | 同上 |
| GRB030913 | 表2、表3 | — | mention-only | 同上 |
| GRB031026 | 表2、表3 | — | mention-only | 同上 |
| GRB031111B | 表2、表3 | — | mention-only | 同上 |
| GRB031220 | 表2、表3 | — | mention-only | 同上 |
| GRB040511 | 表2、表3 | — | mention-only | 同上 |
| GRB040825A | 表2、表3 | — | mention-only | 同上（该源已审、审核未引用此文） |
| GRB040825B | 表2、表3 | — | extracted（本 PR 已核对表 2 该行并登记 articles[]） | 佐证 XRF 软谱；无测光行 |
| GRB040916 | 表2、表3 | — | mention-only | 谱参数汇总 → 不开卡 |
| GRB041016 | 表2、表3 | — | mention-only | 同上 |
| GRB041211 | 表2、表3 | — | mention-only | 同上 |
| GRB050123 | 表2、表3 | — | mention-only | 同上 |
| GRB050209 | 表2、表3 | — | mention-only | 同上 |
| GRB050807 | 表2、表3 | — | mention-only | 同上 |
| GRB060121 | 表2、表3 | — | mention-only | 同上 |

## 增量门槛判读

表 2/表 3 皆为谱参数与内禀参数汇总（Epeak/T90/fluence/Eiso），属 comment 级量、无测光表、无 T0 锚点/滤光片/星等系统等口径风险、亦非独立定标——对表列各源均不满足 §3.11 增量门槛，不开源级卡。

## 待决

无。
