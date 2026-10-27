# 文献索引：Besson+2007（RICE 冰切伦科夫实验 GRB 超高能中微子流量上限汇编）

- paper_key: besson2007
- paper: Besson+2007, Astropart. Phys. 26, 367–377（DOI 10.1016/j.astropartphys.2006.07.008）
- date: 2026-10-27
- helper: Cooper-J2000@zcode（PR #359 定向修补：按独立核查意见为 Besson+2007 补文献级卡）
- sources: GRB020124A, GRB020813A, GRB020903A, GRB030323A, GRB030429A, GRB030528A, GRB050219A, GRB050219B, GRB050223A, GRB050318A, GRB050406A, GRB050416A, GRB050509C, GRB050603A, GRB050709A, GRB050713A, GRB050724A, GRB050801A, GRB050813A, GRB050826A, GRB050908A, GRB050910A, GRB050915A, GRB050915B, GRB051021A, GRB051109B, GRB051111A

## 为什么是文献级卡

该文用 RICE（Radio Ice Cherenkov Experiment，南极冰切伦科夫实验）数据对一批 GRB 设超高能
（$E_\nu>10^{15}$ eV）中微子流量上限，逐暴名清点共覆盖 **107 个真实 GRB 名**（提取方法见
「已核对/未核对」）。结构上分两层：

- **5 个有红移的暴做逐暴专篇分析**（正文：020813、020124、050603、050730、050908）：4 张带
  `\label` 的表——`tab:grb-parameters`（Sγ/t90/z/dL/Epeak/Eγ,iso/Lγ,iso/RICE〈Live T〉）、
  `tab:burst-parameters`（暴中微子谱参数）、`tab:afterglow-parameters`（余辉中微子谱参数）、
  `tab:limits`（逐暴中微子流量上限及与理论预期之比）——另给 SGR 1806-20 巨耀发上限（非 GRB）。
- **其余约 106 个暴只出现在南天 livetime 阈值表**（caption「GRBs recorded in southern hemisphere,
  with incomplete spectral or redshift information」及两个续 tabular，共 107 行：GRB 名/赤纬/〈Livetime〉/判别
  阈值 V；其中 1 行 `052726B` 为 `050726A` 误植，见「已知坑」）。

按「一源一卡」机械执行会产出 100+ 张卡，其中 100 张左右只是 livetime 阈值表行——无测光、
无定位、无数值增量。按 §3.11.8 一篇多源文献只写一张文献级卡。

**与 GRB 050910A（本 PR 审核源）的关系**：该文只给 livetime 表一行（赤纬 −29.775、〈Livetime〉 0.928、
判别阈值 −0.45 V），无测光、无定位、无数值增量。**其余源在本卡仅为文献覆盖枚举，未动其任何数据。**

## 涉及源一览（论文点名 × 库内精确同名 ID，27 个）

> 「覆盖」按**论文用名与库内 ID 精确一致**判定（逐个 `git show origin/main:info/<ID>.json` 确认存在）；
> 论文中出现但无精确同名 ID 的 80 个名单列在下一节，未计入 `sources:`。
> 「表号」列以 arXiv e-print tex 源的 `\label`/caption 为准（出版稿表号未核，见「已核对/未核对」）。

| 源 | 表号 | 源级卡 | status | 增量判读 |
|---|---|---|---|---|
| GRB020124A | 专篇表×4 + livetime 表 | 无 | mention-only | 有专篇数值（Sγ/T90/z/Eγ,iso/中微子上限，四张 `\label` 表）+ tex 草稿数据行；**无光学测光无定位**；中微子量是否过门槛见「待决」① |
| GRB020813A | 专篇表×4 + livetime 表 | 无 | mention-only | 有专篇数值（同 GRB020124A 行）；**无光学测光无定位**；见「待决」① |
| GRB020903A | livetime 表 + tex 草稿数据行 | 无 | mention-only | livetime 阈值表；草稿行含坐标/Epeak/T90/fluence（「/」分隔的非正式表格，出版稿是否保留未核）；无光学测光 |
| GRB030323A | livetime 表 | 无 | mention-only | mention-only/livetime 阈值表，无测光无定位，无数值增量 |
| GRB030429A | livetime 表 + tex 草稿数据行 | 无 | mention-only | livetime 阈值表；草稿行含坐标/Epeak/T90/fluence（同 GRB020903A 行）；无光学测光 |
| GRB030528A | livetime 表 | 无 | mention-only | mention-only/livetime 阈值表，无测光无定位，无数值增量 |
| GRB050219A | livetime 表 | 无 | mention-only | mention-only/livetime 阈值表，无测光无定位，无数值增量 |
| GRB050219B | livetime 表 | 无 | mention-only | mention-only/livetime 阈值表，无测光无定位，无数值增量 |
| GRB050223A | livetime 表 | 无 | mention-only | mention-only/livetime 阈值表，无测光无定位，无数值增量 |
| GRB050318A | livetime 表 | 无 | mention-only | mention-only/livetime 阈值表，无测光无定位，无数值增量 |
| GRB050406A | livetime 表 | 无 | mention-only | mention-only/livetime 阈值表，无测光无定位，无数值增量 |
| GRB050416A | livetime 表 | 无 | mention-only | mention-only/livetime 阈值表，无测光无定位，无数值增量 |
| GRB050509C | livetime 表 | 无 | mention-only | mention-only/livetime 阈值表，无测光无定位，无数值增量 |
| GRB050603A | 专篇表×4 + livetime 表 | 无 | mention-only | 有专篇数值（同 GRB020124A 行）；**无光学测光无定位**；见「待决」① |
| GRB050709A | livetime 表 | 无 | mention-only | mention-only/livetime 阈值表，无测光无定位，无数值增量 |
| GRB050713A | livetime 表 | 无 | mention-only | mention-only/livetime 阈值表，无测光无定位，无数值增量 |
| GRB050724A | livetime 表 | 无 | mention-only | mention-only/livetime 阈值表，无测光无定位，无数值增量 |
| GRB050801A | livetime 表 | 无 | mention-only | mention-only/livetime 阈值表，无测光无定位，无数值增量 |
| GRB050813A | livetime 表 | 无 | mention-only | mention-only/livetime 阈值表，无测光无定位，无数值增量 |
| GRB050826A | livetime 表 | 无 | mention-only | mention-only/livetime 阈值表，无测光无定位，无数值增量 |
| GRB050908A | 专篇表×4 + livetime 表 | 无 | mention-only | 有专篇数值（同 GRB020124A 行）；**无光学测光无定位**；见「待决」① |
| GRB050910A | livetime 表 | 无 | mention-only | mention-only/livetime 阈值表，无测光无定位，无数值增量。**本 PR 审核源**：该文仅此一处（赤纬 −29.775、〈Livetime〉 0.928、判别阈值 −0.45 V） |
| GRB050915A | livetime 表 | 无 | mention-only | mention-only/livetime 阈值表，无测光无定位，无数值增量 |
| GRB050915B | livetime 表 | 无 | mention-only | mention-only/livetime 阈值表，无测光无定位，无数值增量 |
| GRB051021A | livetime 表 | 无 | mention-only | mention-only/livetime 阈值表，无测光无定位，无数值增量 |
| GRB051109B | livetime 表 | 无 | mention-only | mention-only/livetime 阈值表，无测光无定位，无数值增量 |
| GRB051111A | livetime 表 | 无 | mention-only | mention-only/livetime 阈值表，无测光无定位，无数值增量；另见 tex 源 `\end{document}` 后的草稿备注（「已知坑」） |

## 论文中出现、库内无精确同名 ID 的源（80 个，单列说明，不建档）

按 README 契约，`sources:` 只收精确同名 ID；下列名字**未**登记，也未开 new-source Issue（`out_of_repo`
键留空），仅在此枚举备查。

- **同日异写（33 个）**——库内有同日 ID 但写法不同（多为库内无后缀、论文带后缀），极可能同暴，
  对应关系待核：020305A→GRB020305、020801A→GRB020801、020812A→GRB020812、030418A→GRB030418、
  030723A→GRB030723、030725A→GRB030725、040223A→GRB040223、040228A→GRB040228、040730A→GRB040730、
  041223A→GRB041223、041224A→GRB041224、050129A→GRB050129、050202A→GRB050202、050326A→GRB050326、
  050326B→GRB050326、050331A→GRB050331、050331B→GRB050331、050412A→GRB050412、050412B→GRB050412、
  050418A→GRB050418、050626A→GRB050626、050701A→GRB050701、050701B→GRB050701、050714A→GRB050714
  （库内同日另有 GRB050714B，对应关系待核）、050721A→GRB050721、050721B→GRB050721、050726A→GRB050726、
  050730→GRB050730A（论文全篇用裸名、库内带 A；该暴在论文中有专篇表×4 分析）、050817A→GRB050817、
  050822A→GRB050822、050911A→GRB050911、050916A→GRB050916、051001A→GRB051001。
  注意 050326A/050326B、050331A/050331B、050412A/050412B、050701A/050701B、050721A/050721B 是论文里
  **同日两个不同触发**，库内只有一个无后缀 ID，无法判定对应哪一个。
- **同日但后缀不同（2 个）**——库内 ID 为另一触发，非同暴：050813B（库内为 GRB050813A）、
  051006B（库内为 GRB051006A）。
- **库内同日无任何 ID（45 个）**：020629B、021021A、030629A、030706A、030716A、030821A、031015A、
  040309A、040330A、050107A、050107B、050108A、050121A、050121B、050130A、050203A、050211A、050213A、
  050217A、050222A、050226A、050322A、050323A、050323B、050402A、050602A、050612A、050614B、050623A、
  050703A、050715B、050725A、050727A、050728A、050818A、050830B、050907A、050917A、050917B、050921A、
  050927A、051004A、051004B、051007A、051013A。

## 增量门槛判读（对全表）

- **23/27 不过门槛**：只有 livetime 阈值表行（GRB020903A/GRB030429A 另有 tex 草稿行，但非正式表格）
  ，无测光、无定位、无数值增量 → 不开源级卡，读本卡即可。
- **4 个五暴分析对象（GRB020124A、GRB020813A、GRB050603A、GRB050908A）**：论文给出 GCN 拿不到的
  专篇数值（γ 流量/T90/红移/Eγ,iso/RICE 中微子流量上限），字面满足 README 门槛第 1 条；但这些是
  中微子/γ 物理量，本库数据模型（`lc/` 光学测光）没有承载位 → 建议不开源级卡（「待决」①）。
- 全部 27 个源目前**均无源级卡**（`audit/leads/` 下无对应文件），历史欠账为零。

## 已核对 / 未核对

- 已核对：全文 GRB 名逐个从 tex 源提取（正则 + 月/日合法性过滤；剔除 6 个文献编号形伪命中：
  Phys. Rev. D 65, 016003 / 69, 023001 / 61, 023001 / D68, 043001 / D69, 047101 / PRL 91, 071102；
  及 1 个 `052726B` 误植）；27 个精确同名 ID 逐个 `git show origin/main:info/<ID>.json` 确认存在；
  GRB 050910A 全文仅 livetime 表 1 处（tex line 1151）；livetime 表 107 行逐行核对行首名。
- 未核对：**出版稿（Astropart. Phys. 26, 367–377，Elsevier VoR）未获取**——本卡基于审核代理抓取的
  arXiv e-print tex 源（`D:/AIGen/AJDATA/GRB050910A-src/besson/grb06r.tex`），表号/行号/措辞以出版稿为准；
  各表数值未逐值提取（livetime 表只记行存在性）；草稿数据行与出版稿的异同未核。

## 已知坑

- **`052726B`（livetime 表一行）疑为 `050726A` 误植**：紧邻上一行即 050726A；不存在 GRB 052726
  （月 27 非法）。本卡未将其计为源，引用该表时勿把此行当独立暴。
- **tex 源含草稿残留**：`\end{document}` 之后有一行备注 `GRB51111A <Livefrac>=0.81
  D1threshold=-0.351166`（即 GRB 051111A 的草稿数值，出版稿未必收录）；另有 5 个暴（020124A、
  020813A、020903A、030429A、030723A）的「/」分隔非正式数据行（HETE 官网数据格式，含坐标/Epeak/
  T90/fluence）。接手者引用任何数值前必须对出版稿核实。
- **同一暴两种写法**：正文与专篇表对 5 个分析对象用裸名（020813、020124、050603、050730、050908），
  livetime 表用带后缀名（020813A、020124A、050603A、050908A）；050730 全篇无后缀而库内为 GRB050730A。
- 该文还给 **SGR 1806-20**（2004-12-27 巨耀发）设了中微子上限——非 GRB、库内无此源，本卡不涉及。

## 待决

① **五暴专篇数值要不要为 GRB020124A/GRB020813A/GRB050603A/GRB050908A 开源级卡**：数值真实存在且
  GCN 检索不到，但量纲是中微子/γ 物理量，本库 `lc/` 测光模型无承载位；建议不开卡、以本卡为索引
  （涉及维护者裁定）。
② **「同日异写」33 个是否算「本文覆盖」**：若算，应把对应库内 ID（GRB020305、GRB050129、GRB050326、
  GRB050730A 等）补进本卡 `sources:`；建议接手相应源时先核库内 ID 的坐标/触发时间再定（涉及维护者裁定）。
