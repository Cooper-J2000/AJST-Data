# 文献级索引卡：Bolmer+2018（GRB z>4 尘埃消光样本，附 GROND 测光表 D.1）

- paper_key: bolmer2018
- paper: Bolmer, Krühler, Greiner, et al. 2018, A&A 609, A62（DOI 10.1051/0004-6361/201731255；arXiv:1709.06867v2）；逐暴测光见附录 D 表 D.1「GROND photometry of the GRB afterglows」（T_GROND=曝光中点、s；g′r′i′z′JHKs AB 星等、未银消改正、上限 3σ；虚线下为 stacked 观测）
- date: 2026-11-07
- helper: wa1kmoon@zcode（PR #949，审 GRB090516A 时顺手建卡）
- sources: GRB071025A, GRB080825B, GRB080913A, GRB080916C, GRB090205A, GRB090423A, GRB090429B, GRB090516A, GRB100205A, GRB100219A, GRB100518A, GRB100905A, GRB111008A, GRB120712A, GRB120923A, GRB130606A, GRB131117A, GRB140311A, GRB140428A, GRB140515A, GRB140614A, GRB151027B, GRB151112A

注：表 D.1 覆盖 22 暴段，逐一与库内 info T0/MJD 比对全部在库；其中 GRB100205A 段在 TeX 中被注释、成文表无数据。

## 版本状态

arXiv:1709.06867v2 e-print（TeX 源 phot.tex + PDF 互证）实取；VoR（A&A 609, A62）aanda.org PDF 403（DataDome）、cdsarc.cds.unistra.fr 超时、VizieR CFA 镜像查无 J/A+A/609/A62 目录、MPG.PuRe API 404——**未通读 VoR**，已在 `audit/unverified.tsv` 登记（GRB090516A 行，pr=949）。表值以 arXiv v2 TeX 为准。

## 原文口径（原样记录，未做换算）

- 各暴一段，段头给该暴 T0（UT + MJD，来源引用 GCN 通告编号）；T_GROND 列为「曝光中点、相对 T0 的秒数」，附 1σ 误差。
- 星等：AB；未做银河系前景消光改正；上限为 3σ；空缺（…）系技术问题/反射环/改用堆叠值。
- 虚线（\hdashline）下为 stacked 观测行（多个单次曝光的合并值）。

## 涉及源一览（表 D.1 覆盖 22 暴段，逐一与库内 info T0/MJD 比对全部在库；其中 GRB100205A 段被注释、无数据）

| 源 | 表号 | 源级卡 | 增量判读 |
|---|---|---|---|
| GRB090516A | 表 D.1（9 历元×7 波段=63 行） | 无卡——**已随 PR #949 直接入库**（63 行，AB、未银消改正；同暴 GCN 9382 初步 GROND 7 行被本表精化值取代删除） | 已逐值核对（arXiv v2 TeX；VoR 不可得已登记） |
| GRB071025A | 表 D.1（Bolmer 用名 "GRB 071025B"，T0/MJD 比对确认为库内 GRB071025A） | 无 | 未逐值核对 |
| GRB080913A | 表 D.1（Bolmer 用名 "GRB 080913"） | 无 | 未逐值核对 |
| GRB090205A | 表 D.1（Bolmer 用名 "GRB 090205"） | 无 | 未逐值核对 |
| GRB090423A | 表 D.1（Bolmer 用名 "GRB 090423"） | 无 | 未逐值核对 |
| GRB100518A | 表 D.1（Bolmer 用名 "GRB 100518"） | 无 | 未逐值核对 |
| GRB140311A | 表 D.1（Bolmer 用名 "GRB 140311"） | 无 | 未逐值核对 |
| GRB080825B | 表 D.1（5 行 + 1 stacked 行） | 无 | 未逐值核对；GROND 多历元测光+g′ 带上限，接手者自行取值 |
| GRB080916C | 表 D.1（1 行） | 无 | 未逐值核对 |
| GRB090429B | 表 D.1（2 行，全上限） | 无 | 未逐值核对 |
| GRB100205A | 表 D.1 段被注释掉（phot.tex 内 %GRB 100205A 行未发表） | 无 | 该段在 TeX 中被注释、成文表无此暴，**无数据可取** |
| GRB100219A | 表 D.1（5 行） | 无 | 未逐值核对 |
| GRB100905A | 表 D.1（1 行） | 无 | 未逐值核对 |
| GRB111008A | 表 D.1（7 行） | 无 | 未逐值核对 |
| GRB120712A | 表 D.1（9 行 + 2 stacked 行） | 无 | 未逐值核对 |
| GRB120923A | 表 D.1（1 行，全上限） | 无 | 未逐值核对 |
| GRB130606A | 表 D.1（3 行） | 无 | 未逐值核对 |
| GRB131117A | 表 D.1（1 行） | 无 | 未逐值核对 |
| GRB140428A | 表 D.1 | 无 | 未逐值核对 |
| GRB140515A | 表 D.1 | 无 | 未逐值核对 |
| GRB140614A | 表 D.1 | 无 | 未逐值核对 |
| GRB151027B | 表 D.1 | 无 | 未逐值核对 |
| GRB151112A | 表 D.1（3 行，含 225119 全上限行） | 无 | 未逐值核对 |

库内/库外判定更正（2026-11-07 核查）：表 D.1 全部 22 个暴段**均已在库内**（初版卡误判 4 源为「库外」——系 Bolmer 用名无 A 后缀所致，如 "GRB 071025B"→GRB071025A、"GRB 080913"→GRB080913A，已逐源以 T0/MJD 与 info/*.json 比对确认同事件）；无库外源、无需开 new-source Issue。GROND 团队同批暴另见 `audit/leads/papers/greiner2024.md`（GROND 样本 I），两卡可互为路由。

## 已核对 / 未核对

- 已核对：GRB090516A 段 9 历元×7 波段 63 值逐值对照 phot.tex，并随 PR #949 入库；表注（AB、未银消改正、3σ、T_GROND=中点）逐条核对。
- 未核对：其余 21 个库内源的表 D.1 行**均未逐值核对、未提取、未换算 T0、未查该源其他文献**——接手者须自己打开原文（arXiv v2 TeX `table/phot.tex`）逐值核对；表值与各源 GCN 初步值可能不同（GROND 精化定标），替换/并存由各源审核员按 §3.3/§3.4 裁定。
