# 文献级索引卡：Makrygianni+2025

- paper_key: makrygianni2025
- paper: Makrygianni+2025, ApJL 987, L20（DOI 10.3847/2041-8213/ade155；arXiv:2505.16867；A second likely partial tidal disruption event in the repeating TDE candidate AT 2022dbl）
- date: 2026-11-05
- helper: Rusty-Harpoon@zcode
- out_of_repo: AT2019eve（表 6 对比样本库外源；new-source Issue #899）
- sources: PS1-10jh,AT2017eqx,AT2018dyb,AT2018hco,AT2018hyz,AT2018iih,AT2018zr,AT2019azh,AT2019dsg,AT2019ehz,AT2019qiz

## 为什么是文献级卡

AT 2022dbl 第二次耀发（2024）的专文：AT 2022dbl 双耀发的射电/光学跟踪（表 1 guidance、表 2 射电），
并在表 6（tab:intenergy）给出 12 个对比 TDE 的积分 bolometric 能量等派生标量——其中 11 个为库内源
（见 sources 键）。表 6 为派生标量/转引性质，不过源级卡门槛（§3.11 第 7 条），按第 8 条建本索引卡承载。

## 涉及源一览

| 源 | 表号 | 源级卡 | status | 增量判读 |
|---|---|---|---|---|
| AT2022dbl（本卡所审源） | 表 1 guidance（差分 ZTF g 8 行含 2 上限 + LCO r/i 6 行）、表 2 射电 22 行 | 无（已随 PR #896 审核入库） | extracted | 已逐值入库 |
| PS1-10jh | 表 6（积分 bolometric 能量，派生标量） | 无 | mention-only | 派生标量，不过源级门槛；接手者如需可查 VoR 表 6 |
| AT2017eqx | 表 6 | 无 | mention-only | 同上 |
| AT2018dyb | 表 6 | 无 | mention-only | 同上 |
| AT2018hco | 表 6 | 无 | mention-only | 同上 |
| AT2018hyz | 表 6 | 无 | mention-only | 同上 |
| AT2018iih | 表 6 | 无 | mention-only | 同上 |
| AT2018zr | 表 6 | 无 | mention-only | 同上 |
| AT2019azh | 表 6 | 无 | mention-only | 同上 |
| AT2019dsg | 表 6 | 无 | mention-only | 同上 |
| AT2019ehz | 表 6 | 无 | mention-only | 同上 |
| AT2019qiz | 表 6 | 无 | mention-only | 同上 |

## 增量门槛判读

- 表 6 的 11 个库内源条目均为**积分 bolometric 能量等派生标量**（非逐点测光、非口径差异、非新文献引用
  三者皆不沾）——不过 §3.11 第 7 条的源级卡门槛，索引于此即可。
- 表 1/表 2 仅覆盖 AT2022dbl 本身（已随 PR #896 逐值入库）。
- AT2019eve（表 6 库外源）→ new-source Issue #899。

## 待决

无（表 6 为派生标量，不涉维护者数据裁决；表 2 的 MJD 笔误裁决见 PR #896 待决事项）。
