# 文献索引：Urata+2026（JCMT/SCUBA-2 中微子对应体亚毫米巡天 + HerBS/Planck PHZ 星表关联）

- paper_key: urata2026
- paper: Urata+2026, arXiv 2609.07863（Submitted to PASJ；Crossref 按标题检索无命中、无 DOI，VoR 不可得）
- date: 2026-10-29
- helper: wa1kmoon@zcode
- sources: IceCube-160731A, IceCube-190331A, IceCube-200926A, IceCube-200929A, IceCube-201007A, IceCube-210922A, IceCube-220624A, IceCube-221223A, IceCube-230707A, IceCube-230724A, IceCube-240105A, IceCube-260115A, IceCube-260712A

## 为什么是文献级卡

该文两部分内容各自覆盖多个库内 IceCube 源，合计 **13 个**（`sources` 所列；已逐个与 `info/` 文件名核对），
远超「≥3 个库内源」门槛：

- **第一部分：JCMT/SCUBA-2 触发观测**（Table 1 = 9 个场：IC200926A、IC200929A、IC210922A、IC220115A、
  IC220624A、IC221223A、IC230707A、IC230724A、IC240105A，逐场给 850 µm rms 灵敏度；§3.1–§3.3 对
  IC210922A / IC220115A / IC240105A 三场给出候选源与光变）；Table 2 = 3 个场（IC190331A、IC201007、
  IC220306）的 850 µm rms 上限。
- **第二部分：与 Herschel HerBS、Planck PHZ 星表的位置关联**（Table 4 = 4 个场 IC160731A、IC180125A、
  IC180410A、IC141221A 的 HerBS 源 `S850`；Table 3 = IC260712A、IC260115A 两个场的 Planck PHZ 源与
  545 GHz 流量；Table 5/6 为统计汇总与稳健性，非逐源数值）。

两部分的逐源量都是**亚毫米测光/上限与星表关联**，属库内 GCN 检索拿不到的量（JCMT 观测未以 GCN 形式
发布），因此多数库内源过 §3.11.7 增量门槛，宜建源级卡；本卡只做索引，不抄录任何可采纳数值。

命名口径：原文写 `IC 200926A`、`IC201007`（无字母后缀）等，本卡一律映射到库内 ID；`IC201007` 的映射
依据是库内唯一的 2020-10-07 事件 `IceCube-201007A`（名字主干一致，未做任何数值合并）。

## 涉及源一览

> `status` 一律为 `mention-only`（本卡未提取任何逐源行；`IceCube-260115A` 例外，见末行）。
> `源级卡` 一列全部为「无」——本 PR 未新建任何源级卡。
> 本卡不记载任何源的 `free/claimed/reviewed` 状态（契约硬性禁令）。

| 源 | 表号 | 源级卡 | status | 增量判读 |
|---|---|---|---|---|
| IceCube-160731A | Table 4（HerBS 场表，含 `S850`）、§5.1 | 无 | mention-only | 过门槛：给出该场 HerBS 源的 SCUBA-2 `S850` 与位置偏移，库内 GCN 无此量 → 宜建源级卡（未建） |
| IceCube-190331A | Table 2（850 µm rms 行） | 无 | mention-only | 过门槛：该场 850 µm rms 上限为新观测值 → 宜建源级卡（未建） |
| IceCube-200926A | Table 1（首轮触发观测） | 无 | mention-only | 过门槛：首轮 JCMT 850 µm rms 灵敏度 → 宜建源级卡（未建） |
| IceCube-200929A | Table 1 | 无 | mention-only | 同上 |
| IceCube-201007A | Table 2（原文作 `IC201007`） | 无 | mention-only | 过门槛：850 µm rms 上限 → 宜建源级卡（未建） |
| IceCube-210922A | Table 1、§3.1（JCMT0402−0424「Shadow Blaster」光变与 `S850`） | 无 | mention-only | 过门槛且增量最大：该场候选对应体的多历元 850/450 µm 测光，库内无同源数据 → 宜建源级卡（未建） |
| IceCube-220624A | Table 1 | 无 | mention-only | 过门槛：首轮 rms 灵敏度 → 宜建源级卡（未建） |
| IceCube-221223A | Table 1 | 无 | mention-only | 同上 |
| IceCube-230707A | Table 1 | 无 | mention-only | 同上 |
| IceCube-230724A | Table 1 | 无 | mention-only | 同上 |
| IceCube-240105A | Table 1、§3.3（两已知耀变体的 850/450 µm 测光） | 无 | mention-only | 过门槛：耀变体多历元亚毫米测光，库内无 → 宜建源级卡（未建） |
| IceCube-260712A | Table 3（PHz G109.82+68.15 关联与 545 GHz 流量） | 无 | mention-only | 过门槛（新正式文献引用 + 新口径）：可作为 `articles[]`/comment 依据 → 宜建源级卡（未建） |
| IceCube-260115A | Table 3（PHz G221.53+43.23 关联） | 无（本源即本 PR 审核对象） | extracted | 本源已核：Table 3 的分离角/A90/积可信度已逐项核入 `info/IceCube-260115A.json` 的 comment；无需另建源级卡 |

## 增量门槛判读

- **过门槛（宜有源级卡，本 PR 未建）**：13 个源中 12 个给出库内 GCN/目录拿不到的观测（JCMT `rms`/上限、
  HerBS `S850`、Planck PHZ 545 GHz 流量），并顺带提供新的正式文献引用。按源级卡契约，这些卡应由
  **接手该源审核的人随其数据 PR 提交**（每源一张 `audit/leads/<源ID>.md`），本卡仅登记位置。
- **不过门槛的**：Table 5/Table 6 属统计检验汇总（场计数、p 值），无逐源数值，不产生源级卡线索；
  §4.2 的 `ρ`、`A_box,90` 等为作者定义的统计量，不属测光数据。
- **禁用提醒**：本卡所有「表号」只用于定位。接手者必须自行打开原文逐值核对（含 `S850` 是否转引
  Bakx+2020、`z` 的 phot/spec 归属），并自行完成 T0 换算、去重与口径判断；本卡不做任何换算或采纳。

## 待决

1. **`out_of_repo` 暂缺（未开 Issue）**：本文还涉及库内不存在的 IC220115A、IC180125A、IC180410A、
   IC141221A（Table 4）、IC220306（Table 2）、IC200921A 与 IC161125A（§4 统计场列表）。按契约这些应各开
   `new-source` Issue 后才写进 `out_of_repo` 元数据键；本 PR 未开（属维护者权限），请裁定是否补开并回填。
2. **源级卡批量缺口**：12 个库内源过门槛但无源级卡。若维护者希望在本批统一补卡，建议按
   `audit/leads/papers/README.md` 的工具守卫（一个 PR 新增 ≥5 张源级卡须先有文献级卡——本卡已满足）
   分批提交，避免与各源认领冲突。
3. **VoR 追踪**：本文状态为「Submitted to PASJ」，Crossref 无 DOI。待正式发表后，本卡 `paper:` 与各源
   `articles[]` 需按 VoR 的卷/页/DOI 更新，并核对表号是否随排版变动（当前表号依 arXiv v1 PDF 第 9 页图注
   与正文自引「(Table 3)」逐字核定）。
