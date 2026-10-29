# 文献索引：Soderberg+2005（SN 2003L 的 VLA/VLBA 射电专篇）

- paper_key: soderberg2005
- paper: Soderberg, Kulkarni, Berger, Chevalier, Frail, Fox, Walker 2005, ApJ 621, 908, "The Radio and X-Ray-Luminous Type Ibc Supernova 2003L"（DOI 10.1086/427649，bibcode 2005ApJ...621..908S；VoR 不可达——IOP/stacks 被 bot 验证码拦截、ADS 扫描页 articles.adsabs.harvard.edu 403，实读 arXiv astro-ph/0410163 v1）
- date: 2026-10-29
- helper: wa1kmoon@zcode
- sources: SN2003L

> **注意区分同名论文**：本卡是 ApJ **621, 908**（SN 2003L 射电专篇，库内只覆盖 SN2003L 一源）。同作者同年另一篇 ApJ **627, 877**（HST 搜寻 XRF 伴随超新星，库内覆盖 4 源）见 `papers/soderberg2005b.md`。库内 `articles[]` 两者都写作「Soderberg+2005」，检索/引用时须以 title、DOI、bibcode 区分，勿把两篇的覆盖范围混在一起。

## 为什么是文献级卡

本文是 SN 2003L 的观测专篇：表 1 为 VLA 在 4.9 / 8.5 / 15.0 / 22.5 GHz 四个频率上的通量密度测量（含表 1 注 a 的 VLBA 一行），§2.2 给 VLBA 单次观测，§3 给 Chandra ACES-S 的 X 射线结果，§4–§7 为 SSA/FFA 建模，§8 结论。**全篇只有 SN 2003L 一个库内源**。

严格按《数据审核提示词》§3.11.8 的触发条件（一篇文献覆盖 ≥3 个库内源）本文并不触发文献级卡；本卡因审核 SN2003L 时实际取数而建，作用是把这个常被简写为「Soderberg+2005」的名字锚定到具体 DOI/bibcode，并与同年同作者的另一篇（ApJ 627, 877）划清界限。

## 涉及源一览

> 只做索引：不含可采纳数值、不做单位/T0/消光换算、不判去重。

| 源 | 表号 | 源级卡 | status | 增量判读 |
|---|---|---|---|---|
| SN2003L | 表 1（VLA 四频段通量密度，含注 a 的 VLBA 一行）；另 §2.2 VLBA 位置、§3 Chandra X 射线 | 无（本源即审核对象，不另开源级卡） | extracted | 过门槛（条件 1）：射电光变是本库该源唯一的正式测光表，已在其审核 PR 内逐行取数入 lc；X 射线按 §3.3 不入 lc，只记 comment |

## 增量门槛判读

- **过门槛并已落地**：SN2003L 的表 1（条件 1：正式论文表，GCN 只有单点且含宿主流量）→ 已由本源审核直接写入 `lc/SN2003L.csv`，无需源级卡。
- **不进 `sources` 的**：文中出现的 SN 1998bw、SN 1994I、SN 2002ap 只作比较对象；相关数值要么转引他人文献、要么是模型合成曲线，没有这些源的原始测光表——按增量门槛「纯比较/转引不开卡、不列 sources」处理。
- 本卡未做的动作：未换算任何值、未查其他文献、未对任何目标源的状态表态。

## 待决

1. VoR（ApJ 621, 908）不可达，表 1 数值取自 arXiv v1（submittedVersion，自标「submitted to ApJ」）；建议有 IOP / ADS 权限者复核全表（本卡不重复列值）。
2. 表 1 的 Δt 历元是论文自述的「近似爆炸日」，与库内 T0（发现时刻）不同口径；换算规则已在 `info/SN2003L.json` 的 comment 写明，此处不再展开。
3. **工具侧（供维护者参考，本卡未改 `tools/`）**：`tools/audit_queue.py` 的 `load_paper_cards()` 先把 `sources` 初始化为 `[]`、再用 `key not in meta` 判重，导致元数据里的 `sources:` 永不被读入，只能退回解析「涉及源一览」表首列的 `[A-Za-z]{2,6}\d{6}[A-Za-z]?` 正则；该正则要求 6 位日期，`SN2003L`（4 位）因此无法被 `--paper` 反查索引（`tools/validate.py` 的解析不受影响，本卡校验通过；同类现象在 `curtin2023` 等存量卡上也存在——其 34 个 sources 只显示出 1 个）。
