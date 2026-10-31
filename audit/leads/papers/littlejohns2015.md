# 文献索引：Littlejohns+2015（Swift 时代 GRB 光学消光 / RATIR 首夜测光样本）

- paper_key: littlejohns2015
- paper: Littlejohns+2015, MNRAS 449, 2919（DOI 10.1093/mnras/stv479；arXiv:1412.6530。VoR 未通读：OUP 全站反爬 403，按 §3.3 第 3 级以 arXiv TeX 全文 + ADS 元数据三方交叉，已逐值读取 arXiv 源 ms.tex）
- date: 2026-11-01
- helper: Rusty-Harpoon@zcode
- sources: GRB130122A, GRB130215A, GRB130327A, GRB130418A, GRB130420A, GRB130427A, GRB130502A, GRB130504A, GRB130514A, GRB130606A, GRB130609A, GRB130610A, GRB130612A, GRB130626A, GRB130701A, GRB130907A, GRB130925A, GRB131004A, GRB131030A, GRB140114A, GRB140118A, GRB140129A, GRB140215A, GRB140311A, GRB140318A, GRB140331A, GRB140419A, GRB140518A, GRB140614B, GRB140622A, GRB140703A, GRB140709A, GRB140710A

## 为什么是文献级卡

RATIR（1.5m Harold L. Johnson Telescope, OAN-SPM）对 Swift GRB 的光学消光研究（Table 1 快样本 33 暴、Table 4 首夜堆叠测光 30 暴）。
对本库有增量的表：
- **Table 4（tab:first_night_phot）**：30 暴 RATIR **首夜堆叠测光**（r/i/Z/Y/J/H 列，AB 系统、未做银消改正，原文声明）。
  其中 30 个源全部在库内（含上限行如 131004A）。
- **Table 1（tab:fast_sample）**：delay（RATIR 首历元起始，分钟）、首历元 duration（分钟）、RATIR 探测性（M/D/UL）、
  β_X、β_OX（5.5/11 h）、N_H,rest 等样本参数——目录级参数，可作审核时的补充口径，不直接入库。
- SED 图（sed_new_*.eps）与 Table 6 消光拟合结果：图上读数不入库（§3.3）。

## 涉及源一览

| 源 | 表号 | 源级卡 | status | 增量判读 |
|---|---|---|---|---|
| GRB130701A | Table 4 r/i/Z/Y | 无（本 PR 已审核） | extracted | 4 行已入库（PR #715）；历元按 Table 1 delay=300.3 min + duration=21 min 中点±半宽 |
| 其余 32 源（29 源在 Table 4；GRB130122A/GRB130626A/GRB140118A 仅 Table 1） | Table 4 / Table 1 | 无 | mention-only（未提取） | 首夜堆叠 r/i/Z/Y/J/H 测光或上限；历元锚点只有 delay+首历元 duration，接手者按 §3.8 coadd 约定处理 |

## 增量门槛判读

- Table 4 的 RATIR 堆叠测光**过增量门槛**（第 1 条：多数暴无 RATIR GCN 通告，库内拿不到该数值）；
- Table 1 的 β/N_H 等为目录级参数（§3.3「目录级快照不含光变表」同类），只在审核时作 comment 备考，不开卡；
- 30 源规模同 anderson2018 卡的处理：源级卡留给各源审核时按需建立。

## 待决

- Table 4 堆叠历元的锚定方式（本 PR 对 GRB130701A 采用 delay+duration 中点±半宽并在 comment 声明堆叠真实历元不可恢复）
  是否作为该表入库的统一口径，请维护者裁定；
- 部分源的 RATIR 通道记号（Z/Y）与库内 filters.json 键（Z=UKIRT/UKIDSS、Y=UKIRT/UKIDSS）为近似对应，接手者需在 comment 声明。
