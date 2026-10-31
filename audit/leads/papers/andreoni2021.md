# 文献索引：Andreoni+2021（ZTFReST 快暂现源实时/存档分类）

- paper_key: andreoni2021
- paper: Andreoni et al. 2021, ApJ 918, 63（DOI 10.3847/1538-4357/ac0bc7；arXiv:2104.06352——本卡依据 arXiv v1 PDF 实取通读，2026-10-31；VoR 被 IOP/Radware 整站反爬拦截未通读，见 audit/unverified.tsv）
- date: 2026-10-31
- helper: Rusty-Harpoon@zcode（审核 ZTF21aaeyldq 时通读）
- sources: ZTF20aajnksq, ZTF20acozryr, ZTF21aahifke, ZTF21aagwbjr
- out_of_repo: ZTF21aapkbav（new-source Issue #692）

## 为什么是文献级卡

该文是 ZTFReST 管线的巡天+分类文：265 天科学验证 + 3 个新 afterglow 识别。表 2 汇总全部 afterglow/暂现源分类（含衰减率 mag/d），表 3–7 给 5 个目标的 **P48/GIT/LCO 强制 PSF 测光**（ZTF 源的巡天测光，多数不在任何 GCN 里，增量门槛条件 1 满足）。

## 涉及源一览

> `status` 全部 `mention-only`（本卡只做索引，未提取任何行的数值；表 3–7 的测光行数未逐行清点）。

| 源 | 表号 | 源级卡 | status | 增量判读 |
|---|---|---|---|---|
| ZTF20aajnksq（AT2020blt） | 表 3（Forced PSF photometry，P48+ZTF） | 无（该源已 reviewed，PR 内未见引用本表；wa1kmoon@zcode 审核用的是 Ho+2020 表 1） | mention-only | 强制测光 vs Ho+2020 表 1 是否有增量，接手者自行比对 |
| ZTF20acozryr（AT2020yxz） | 表 4（Forced PSF photometry，P48+ZTF）；表 2 分类行（GRB 201103B，衰减 0.75/0.78 mag/d） | 无 | mention-only | 过条件 1（ZTF 巡天测光非 GCN 所载）；该源已 tag=grb/lgrb |
| ZTF21aahifke（AT2021clk） | 表 5（Forced PSF photometry，P48+ZTF、GIT、LCO 1-m Sinistro）；表 2 分类行（Unknown，衰减 0.96 mag/d） | 无 | mention-only | 过条件 1 |
| ZTF21aagwbjr（AT2021buv） | 表 6（Forced PSF photometry，P48+ZTF）；表 2 分类行（GRB 210204A，r 衰减 2.34 mag/d） | 无 | mention-only | 过条件 1；该源已 tag=grb |

## 增量门槛判读

- 表 3–7 为 ZTF/GIT/LCO **强制 PSF 测光**，GCN/目录拿不到 → 四个库内源均过条件 1，接手审核时按表逐行取值（VoR 优先；VoR 被 Radware 拦时按 §3.3 渠道分级处理并登记 unverified.tsv）。
- 表 2 各源分类/衰减率为 GCN 之外的正式文献引用（条件 3），可直接入 `articles[]` 与 comment。
- 本源（ZTF21aaeyldq）不在表 3–7：仅有表 2 一行「Afterglow no GRB、r 17.56 mag/d」，已由 PR #687 吸收进 info comment。

## 待决

无（库外源 ZTF21aapkbav 已开 Issue #692，建源由维护者裁定）。
