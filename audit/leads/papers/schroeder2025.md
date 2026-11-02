---
paper_key: schroeder2025
paper: Schroeder+2025, ApJ 982, 42, DOI 10.3847/1538-4357/ada9e5 (arXiv:2407.13822)
date: 2026-11-02
helper: LHe496@Codex
sources: GRB170428A, GRB170524A, GRB170728B, GRB201006A, GRB210323A, GRB210919A, GRB211023B, GRB230205A, GRB230217A, GRB230228A
---

## 为什么是文献级卡

本文 Table 4 汇总十个库内短暴的 VLA 射电观测，其中包括 previously unpublished VLA reanalysis/observations；本文还明确列出 201006A、230205A、230217A 没有已确定红移（§4 注释 33）。本文的 230205A Table 4 五个射电点已逐项核对并入本 PR；其余源的原始表值已按状态分别交接，其中 GRB230228A 的 CHIME/VLA 数据已由 PR #745 核对并采纳，待接手的源级线索卡现为 7 张。

**版本状态**：VoR = *The Astrophysical Journal* 982, 42 (2025-03-20), DOI 10.3847/1538-4357/ada9e5。IOP 出版社页面在本轮不可直接获取；已取得 Oxford Research Archive 的机构库 PDF（https://ora.ox.ac.uk/objects/uuid:6593ea1e-2cb9-474a-b66b-86c7f0624d27/files/r0z708z01b），首页印刷刊名、卷页、日期和 DOI 与 VoR 一致；按出版社 PDF Retrieval 阶梯属于机构库中的 VoR 镜像。PDF Table 4 与 arXiv:2407.13822 核对。Table 4 注释：δt 是整次观测的中点相对 Swift/BAT trigger；中心频率 GHz；测量误差 1σ、上限 3σ，括号内是图像 rms（μJy）。

## 涉及源一览

| 源 | 表号 | 源级卡 | status | 增量判读 |
|---|---|---|---|---|
| GRB170428A | Table 4 | GRB170428A.md | extracted | 新的 VLA 3σ 上限 |
| GRB170524A | Table 4 | GRB170524A.md | extracted | 新的 VLA 3σ 上限×2 |
| GRB170728B | Table 4 | GRB170728B.md | extracted | VLA 多频检测与上限，GCN/早期资料不能覆盖全部表行 |
| GRB201006A | Table 4 | GRB201006A.md | extracted | VLA 新观测与上限；另列独立 coherent radio source 数据，源关联需接手者核实 |
| GRB210323A | Table 4 | GRB210323A.md | extracted | 新的 VLA 测量及上限 |
| GRB210919A | Table 4 | GRB210919A.md | extracted | VLA 上限与 host-galaxy radio measurement，需区分源/宿主 |
| GRB211023B | Table 4 | 无（已 reviewed；Table 4 仍有待维护者判断的 6.63 d 上限） | mention-only | 此 PR 不新增其源级卡或改动其数据；可能有新观测未被 GCN 覆盖 |
| GRB230205A | Table 4 | 无（本 PR 正在审核） | extracted | 五个 VLA 观测已逐值核入本 PR |
| GRB230217A | Table 4 | GRB230217A.md | extracted | 新的 VLA 测量及上限 |
| GRB230228A | Table 4 | 无（已由 PR #745 核对并采纳，待合并） | handled-in-PR | 新的 VLA 上限×2 已由 #745 采纳；另核入 CHIME 数据 |

## 增量门槛判读

Table 4 是独立重处理/新射电数据，不是单纯 GCN 汇编。除本 PR 正在审核的 GRB230205A、已 reviewed 的 GRB211023B，以及已由 PR #745 核对并采纳的 GRB230228A 外，其余 7 个待接手源保留源级线索卡。此卡只做文献覆盖索引；接手者必须自行打开表 4 核值，不能从线索卡直接抄入光变表。另：该文引用 2024 ApJ 970, 139 的 Figure 8 展示汇编射电光变，但没有提供可直接核录的逐点数表；本 PR 未从图读数。

## 待决

- GRB201006A 的 Table 4 含单独一段 `Coherent Radio (9)` 行；其是否与 VLA 余辉为同一对应体应由该源接手者依原文/Rowlinson+2024 判断，线索卡保留原文分段。
- GRB210919A 的末行明标 `Host Galaxy`，不可自动视作余辉。
- GRB211023B 已有 `extra_data.audit.status=reviewed`，因此本 PR 未新增该源级卡；Table 4 的 6.63 d 上限尚未与该源当前 42 行审查数据逐项去重，需维护者决定是否另开补充审核。
