# 文献索引：Ershova+2020（MASTER 全球机器人望远镜网络 GRB 早期光学观测汇编）

- paper_key: ershhova2020
- paper: Ershova+2020, Astronomy Reports 64, 126（DOI 10.1134/S1063772920020018）
- date: 2026-10-24
- helper: Rusty-Harpoon@zcode（原始 45 张源级卡）；Cooper-J2000（2026-10-24 转文献级卡）
- sources: GRB110422A, GRB110801A, GRB120106A, GRB120404A, GRB120811C, GRB120907A, GRB121011A, GRB130122A, GRB130907A, GRB131030A, GRB131125A, GRB140103A, GRB140108A, GRB140129B, GRB140206A, GRB140304A, GRB140311B, GRB140508A, GRB140512A, GRB140629A, GRB140801A, GRB140907A, GRB140930B, GRB141028A, GRB141225A, GRB150211A, GRB150301B, GRB150323C, GRB150403A, GRB150413A, GRB150518A, GRB150627A, GRB151021A, GRB151027B, GRB151215A, GRB160104A, GRB160117B, GRB160131A, GRB160227A, GRB160425A, GRB160625B, GRB160804A, GRB160910A, GRB161017A, GRB161117A
- out_of_repo: GRB091020, GRB060926, GRB150404A

## 为什么是文献级卡

该文是 MASTER 网络 2011–2017 年约 130 个暴的观测汇编，**表 20 覆盖 ~120 行**（逐暴观测日志：
γ 探测器与时标、MASTER 站点、ΔT_notice / ΔT_trigger、m_OT、OT 位置、GCN 引用、首帧上限）；
表 2–19 只给少数暴的专篇测光表。按「一源一卡」机械执行会产出 100+ 张卡，而其中绝大多数只是
**逐行转引各自 GCN**，数值与 GCN 同源、可直接检索到——这正是 2026-10-24 定为「不开源级卡」的典型。

本卡把已经产生的 45 张源级卡压成一张索引：源 / 表号 / 有无源级卡 / 增量判读。历史卡不追溯回滚，
但**新审核任一源时按本卡判断**：只有专篇表（表 2–19）里的源才需要重新评估是否过增量门槛，
仅出现在表 20 的源直接读本卡、删掉源级卡即可。

## 涉及源一览

> 45 张源级卡均来自 PR #120（GRB160611A）与 #126（GRB160709A）两次审核顺带留卡；
> 两 PR 在 12 个源上重复留卡，已按冲突规则把两份内容并列保留（见各卡「合并说明」）。
> `status` 全部为 `mention-only`（只是看到、未逐值提取）。

| 源 | 表号 | 源级卡 | status | 增量判读 |
|---|---|---|---|---|
| GRB110422A | 表 7、表 20 | `audit/leads/GRB110422A.md`（#126） | mention-only | **过门槛候选**：有专篇测光表（表 7），接手者须核专篇表是否含 GCN 拿不到的量 |
| GRB110801A | 表 16、表 20 | `audit/leads/GRB110801A.md`（#126（同源另见 #120，按 audit/leads/README.md「冲突处理」合并保留）） | mention-only | **过门槛候选**：有专篇测光表（表 16），接手者须核专篇表是否含 GCN 拿不到的量 |
| GRB120106A | 表 17、表 20 | `audit/leads/GRB120106A.md`（#126（同源另见 #120，按 audit/leads/README.md「冲突处理」合并保留）） | mention-only | **过门槛候选**：有专篇测光表（表 17），接手者须核专篇表是否含 GCN 拿不到的量 |
| GRB120404A | 表 10、表 20 | `audit/leads/GRB120404A.md`（#126（同源另见 #120，按 audit/leads/README.md「冲突处理」合并保留）） | mention-only | **过门槛候选**：有专篇测光表（表 10），接手者须核专篇表是否含 GCN 拿不到的量 |
| GRB120811C | 表 3、表 6、表 20 | `audit/leads/GRB120811C.md`（#126（同源另见 #120，按 audit/leads/README.md「冲突处理」合并保留）） | mention-only | **过门槛候选**：有专篇测光表（表 3、表 6），接手者须核专篇表是否含 GCN 拿不到的量 |
| GRB120907A | 表 20 | `audit/leads/GRB120907A.md`（#120） | mention-only | 转引型：仅表 20 汇总行 → 按新门槛不开卡，接手时删卡读本卡 |
| GRB121011A | 表 19、表 20 | `audit/leads/GRB121011A.md`（#126（同源另见 #120，按 audit/leads/README.md「冲突处理」合并保留）） | mention-only | **过门槛候选**：有专篇测光表（表 19），接手者须核专篇表是否含 GCN 拿不到的量 |
| GRB130122A | 表 20 | `audit/leads/GRB130122A.md`（#120） | mention-only | 转引型：仅表 20 汇总行 → 按新门槛不开卡，接手时删卡读本卡 |
| GRB130907A | 表 2、表 20 | `audit/leads/GRB130907A.md`（#126（同源另见 #120，按 audit/leads/README.md「冲突处理」合并保留）） | mention-only | **过门槛候选**：有专篇测光表（表 2），接手者须核专篇表是否含 GCN 拿不到的量 |
| GRB131030A | 表 20 | `audit/leads/GRB131030A.md`（#120） | mention-only | 转引型：仅表 20 汇总行 → 按新门槛不开卡，接手时删卡读本卡 |
| GRB131125A | 表 20 | `audit/leads/GRB131125A.md`（#120） | mention-only | 转引型：仅表 20 汇总行 → 按新门槛不开卡，接手时删卡读本卡 |
| GRB140103A | 表 20 | `audit/leads/GRB140103A.md`（#120） | mention-only | 转引型：仅表 20 汇总行 → 按新门槛不开卡，接手时删卡读本卡 |
| GRB140108A | 表 20 | `audit/leads/GRB140108A.md`（#120） | mention-only | 转引型：仅表 20 汇总行 → 按新门槛不开卡，接手时删卡读本卡 |
| GRB140129B | 表 13、表 20 | `audit/leads/GRB140129B.md`（#126（同源另见 #120，按 audit/leads/README.md「冲突处理」合并保留）） | mention-only | **过门槛候选**：有专篇测光表（表 13），接手者须核专篇表是否含 GCN 拿不到的量 |
| GRB140206A | 表 20 | `audit/leads/GRB140206A.md`（#120） | mention-only | 转引型：仅表 20 汇总行 → 按新门槛不开卡，接手时删卡读本卡 |
| GRB140304A | 表 20 | `audit/leads/GRB140304A.md`（#120） | mention-only | 转引型：仅表 20 汇总行 → 按新门槛不开卡，接手时删卡读本卡 |
| GRB140311B | 表 11、表 20 | `audit/leads/GRB140311B.md`（#126（同源另见 #120，按 audit/leads/README.md「冲突处理」合并保留）） | mention-only | **过门槛候选**：有专篇测光表（表 11），接手者须核专篇表是否含 GCN 拿不到的量 |
| GRB140508A | 表 12、表 20 | `audit/leads/GRB140508A.md`（#126） | mention-only | **过门槛候选**：有专篇测光表（表 12），接手者须核专篇表是否含 GCN 拿不到的量 |
| GRB140512A | 表 14、表 20 | `audit/leads/GRB140512A.md`（#126（同源另见 #120，按 audit/leads/README.md「冲突处理」合并保留）） | mention-only | **过门槛候选**：有专篇测光表（表 14），接手者须核专篇表是否含 GCN 拿不到的量 |
| GRB140629A | 表 20 | `audit/leads/GRB140629A.md`（#120） | mention-only | 转引型：仅表 20 汇总行 → 按新门槛不开卡，接手时删卡读本卡 |
| GRB140801A | 表 20 | `audit/leads/GRB140801A.md`（#120） | mention-only | 转引型：仅表 20 汇总行 → 按新门槛不开卡，接手时删卡读本卡 |
| GRB140907A | 表 20 | `audit/leads/GRB140907A.md`（#120） | mention-only | 转引型：仅表 20 汇总行 → 按新门槛不开卡，接手时删卡读本卡 |
| GRB140930B | 表 20 | `audit/leads/GRB140930B.md`（#120） | mention-only | 转引型：仅表 20 汇总行 → 按新门槛不开卡，接手时删卡读本卡 |
| GRB141028A | 表 20 | `audit/leads/GRB141028A.md`（#120） | mention-only | 转引型：仅表 20 汇总行 → 按新门槛不开卡，接手时删卡读本卡 |
| GRB141225A | 表 15、表 20 | `audit/leads/GRB141225A.md`（#126（同源另见 #120，按 audit/leads/README.md「冲突处理」合并保留）） | mention-only | **过门槛候选**：有专篇测光表（表 15），接手者须核专篇表是否含 GCN 拿不到的量 |
| GRB150211A | 表 20 | `audit/leads/GRB150211A.md`（#120） | mention-only | 转引型：仅表 20 汇总行 → 按新门槛不开卡，接手时删卡读本卡 |
| GRB150301B | 表 20 | `audit/leads/GRB150301B.md`（#120） | mention-only | 转引型：仅表 20 汇总行 → 按新门槛不开卡，接手时删卡读本卡 |
| GRB150323C | 表 20 | `audit/leads/GRB150323C.md`（#120） | mention-only | 转引型：仅表 20 汇总行 → 按新门槛不开卡，接手时删卡读本卡 |
| GRB150403A | 表 20 | `audit/leads/GRB150403A.md`（#120） | mention-only | 转引型：仅表 20 汇总行 → 按新门槛不开卡，接手时删卡读本卡 |
| GRB150413A | 表 20 | `audit/leads/GRB150413A.md`（#120） | mention-only | 转引型：仅表 20 汇总行 → 按新门槛不开卡，接手时删卡读本卡 |
| GRB150518A | 表 20 | `audit/leads/GRB150518A.md`（#120） | mention-only | 转引型：仅表 20 汇总行 → 按新门槛不开卡，接手时删卡读本卡 |
| GRB150627A | 表 20 | `audit/leads/GRB150627A.md`（#120） | mention-only | 转引型：仅表 20 汇总行 → 按新门槛不开卡，接手时删卡读本卡 |
| GRB151021A | 表 4、表 20 | `audit/leads/GRB151021A.md`（#126（同源另见 #120，按 audit/leads/README.md「冲突处理」合并保留）） | mention-only | **过门槛候选**：有专篇测光表（表 4），接手者须核专篇表是否含 GCN 拿不到的量 |
| GRB151027B | 表 5、表 20 | `audit/leads/GRB151027B.md`（#126） | mention-only | **过门槛候选**：有专篇测光表（表 5），接手者须核专篇表是否含 GCN 拿不到的量 |
| GRB151215A | 表 20 | `audit/leads/GRB151215A.md`（#120） | mention-only | 转引型：仅表 20 汇总行 → 按新门槛不开卡，接手时删卡读本卡 |
| GRB160104A | 表 20 | `audit/leads/GRB160104A.md`（#120） | mention-only | 转引型：仅表 20 汇总行 → 按新门槛不开卡，接手时删卡读本卡 |
| GRB160117B | 表 20 | `audit/leads/GRB160117B.md`（#120） | mention-only | 转引型：仅表 20 汇总行 → 按新门槛不开卡，接手时删卡读本卡 |
| GRB160131A | 表 20 | `audit/leads/GRB160131A.md`（#120） | mention-only | 转引型：仅表 20 汇总行 → 按新门槛不开卡，接手时删卡读本卡 |
| GRB160227A | 表 18、表 20 | `audit/leads/GRB160227A.md`（#126（同源另见 #120，按 audit/leads/README.md「冲突处理」合并保留）） | mention-only | **过门槛候选**：有专篇测光表（表 18），接手者须核专篇表是否含 GCN 拿不到的量 |
| GRB160425A | 表 20 | `audit/leads/GRB160425A.md`（#120） | mention-only | 转引型：仅表 20 汇总行 → 按新门槛不开卡，接手时删卡读本卡 |
| GRB160625B | 表 20 | `audit/leads/GRB160625B.md`（#120） | mention-only | 转引型：仅表 20 汇总行 → 按新门槛不开卡，接手时删卡读本卡 |
| GRB160804A | 表 20 | `audit/leads/GRB160804A.md`（#120） | mention-only | 转引型：仅表 20 汇总行 → 按新门槛不开卡，接手时删卡读本卡 |
| GRB160910A | 表 20 | `audit/leads/GRB160910A.md`（#120） | mention-only | 转引型：仅表 20 汇总行 → 按新门槛不开卡，接手时删卡读本卡 |
| GRB161017A | 表 20 | `audit/leads/GRB161017A.md`（#120） | mention-only | 转引型：仅表 20 汇总行 → 按新门槛不开卡，接手时删卡读本卡 |
| GRB161117A | 表 20 | `audit/leads/GRB161117A.md`（#120） | mention-only | 转引型：仅表 20 汇总行 → 按新门槛不开卡，接手时删卡读本卡 |

## 增量门槛判读（对全表）

- **15 个源有专篇测光表**（表 2–19）：这些是真正值得留卡的对象，但「值不值得」仍取决于专篇表
  是否含 GCN 检索不到的量——本次只记录了表号、**未逐值提取**，接手者须开 VoR 自行判断。
- **30 个源只有表 20 行**：纯转引型。按 `audit/leads/papers/README.md` 的增量门槛
  这类不该开源级卡；历史卡保留但只作索引，接手该源时直接删卡。
- 表 20 的表头语义（原文）：(1) GRB；(2) γ-Detector；(3) MASTER WF/VWF；(4) ΔT notice（s）；
  (5) ΔT trigger（s）；(6) m_OT；(7) OT R.A., Dec.（2000）；(8) GCN；(9) MASTER 站点；
  (10) Limit on first frame（星等（曝光 s））。W=white、P=偏振片、C=clear（原文未正式定义）。

## 已核对 / 未核对

- 已核对：VoR 可获取（Springer，DOI 10.1134/S1063772920020018，2026-10-24）；表 2–20 的划分与
  各源对应关系（各源级卡分别记录）；45 张源级卡的元数据（表号、status、PR）由脚本从卡本身汇总。
- 未核对：表 20 全表 ~120 行的逐值内容（本卡只汇总已有卡的 45 个源，**不是该文的完整源表**）；
  各专篇表（表 2–19）的数值；星等系统、T0/历元口径、与 GCN 的一致性；库内其他约 75 个可能的源未建卡。

## 已知坑

- **该文部分表 20 行的 m_OT 来自事后被撤回的 GCN 通告**：GRB 160611A 行 m_OT=14.7 / P 14.67 出自
  GCN 19525，而 GCN 19526（Lipunov 本人）撤回该 OT（known star、false identification）。
  任何从表 20 直接抄 m_OT 的做法都会读到已撤回值——必须回查对应 GCN 是否被撤回。
- 该文自称覆盖 44 个暴，实际点名的不同暴数更多（约 46，PR #120 审核时更正）；表 20 的规模以
  原表行数为准，勿引用正文自述数字。

## 待决

① **表 20 全表（~120 行）是否整表不入库**：本表的行全是 GCN 转引，逐行迁移等于把 GCN 抄进库；
  建议维持「不作为独立测光来源」，仅在发现某行**未被对应 GCN 覆盖**时才单独评估（涉及维护者裁定）。
② **剩余 ~75 个源要不要建索引**：本卡只覆盖被人读到过的 45 个源。若将来有人通读表 20，
  应把新发现的源补进本卡 `sources:` 与表格，**而不是**新开 100 张源级卡。
③ `out_of_repo` 的三个库外源已开 Issue：#123（GRB 150404A）、#127（GRB 091020）、#128（GRB 060926）。
