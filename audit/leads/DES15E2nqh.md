# 线索：DES15E2nqh（DES RET / FBOT， Pursiainen+2018 gold sample）

- source_id: DES15E2nqh
- status: extracted
- paper: Pursiainen+2018, MNRAS 481, 894（DOI 10.1093/mnras/sty2309；arXiv:1803.04869v2）表 3/4/5/6/7；另 Ho+2023, ApJ 949, 120（DOI 10.3847/1538-4357/acc533；arXiv:2105.08811）表 3
- pr: #921
- helper: wa1kmoon@zcode
- date: 2026-11-06

## 版本状态

- VoR（OUP）Cloudflare 反爬 403 不可达，CDS/VizieR 三镜像超时（见 audit/unverified.tsv，DES16X3cxn 行）；
  本卡数值全部取自 **arXiv:1803.04869v2 TeX 实读**，表号为 arXiv v2 编号（VoR 表号待核）：
  表 3 = tab:z_sources（宿主基本信息）、表 4 = tab:sample（坐标/z/E(B−V)）、表 5 = tab:photometric
  （g 波段光变参数）、表 6 = tab:bb_peak（峰处黑体）、表 7 = tab:host_gal_mass_sfr（宿主 M*/sSFR）。
- Ho+2023 表 3 行为文献汇编（ref [7] = Pursiainen+2018；脚注「DES light curves were provided by M. Pursiainen」），
  取自 arXiv:2105.08811 PDF 实读；i/r/z 波段值与 Pursiainen g 波段表口径不同（不同波段的汇编），仅并列备查。
- 文献级索引卡：`audit/leads/papers/pursiainen2018.md`。

## 原文口径（原样记录，**未做任何换算**）

- 时间口径：t_peak = 观测 **g 波段最亮点日期（整数 MJD）**——唯一绝对时间锚点；t_rise/t_decline/t_1/2 均为
  **rest frame、相对各自峰值**，t_rise 是 last non-detection 到峰的间隔（上限性质）。DES-SN ~7 天 cadence。
- 波段/单位：M_peak(g) 为绝对星等（无银消外 k 改正口径见原文 §4.1）；黑体 T(1000 K)、r(10^14 cm)、L(10^43 erg/s)。
- 坐标：瞬变体 J2000 六十进制；E(B−V) 取 Schlafly+2011。

## 已核对 / 未核对

- 已核对：本卡各行逐字段对照 arXiv v2 TeX 表行（DES16X3cxn 审核时同批提取）。
- 未核对：未换算到本库 T0 口径、未读图提取光变（原文光变仅附录图，禁止读图入库）、
  未查其他文献、未判断星等系统、未做去重；t_peak 的 VoR 表号与数值未对 VoR 复核。

## 原始行（原样）

**表 5（g 波段光变参数）**：t_peak(MJD) = 57366；M_peak = -19.74 ± 0.06 mag；t_rise = 6.5 d；t_decline = 16.30 +3.34/−2.44 d；t_1/2 = 11.57 d

**表 6（峰处黑体）**：T = 22.00 +4.12/−2.81 kK；r = 5.53 +1.03/−0.9 ×10^14 cm；L = 5.10 +1.91/−1.07 ×10^43 erg/s；拟合点数 = 4

**表 4（瞬变体坐标）**：RA = 00:38:55.59, Dec = −43:05:13.14（J2000）；z_spec = 0.52；E(B−V) = 0.0076（Schlafly+2011）

**表 3（宿主）**：巡天 OzDES；偏移 0.517″/3.22 kpc；DLR 1.41；z_spec 0.52；z_phot 0.46

**表 7（宿主）**：log(M*/M☉) = 8.96 +0.33/−0.29；log(sSFR/yr⁻¹) = −9.32

**Ho+2023 表 3**（i 波段）：Mmax = −19.22 ± 0.24 mag；t_b1/2,rise = 3.04–7.34 d；t_b1/2,fade = 5.86 ± 2.17 d；ref [7]

## 备注

同批 DES 源线索另见 papers/pursiainen2018.md（文献级索引卡）与 papers/wiseman2020.md（宿主样本文章卡）；
本源 info 的 tag=[fbot]（Wiseman+2020 RET / Ho+2023 文献 FBOT，class Unknown，无光谱分类，sub_tag 留空）。
