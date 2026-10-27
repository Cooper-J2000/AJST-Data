# 文献级索引：Roming+2009 (Swift/UVOT GRB afterglow catalog)

- paper_key: roming2009
- paper: Roming+2009, ApJ 690, 163（DOI 10.1088/0004-637X/690/1/163；arXiv:0809.4193；VizieR J/ApJ/690/163）Table 3
- date: 2026-10-27
- helper: Rusty-Harpoon@qoder
- sources: GRB050117, GRB050124, GRB050128, GRB050215B, GRB050219A, GRB050219B, GRB050223A, GRB050306, GRB050315A, GRB050318A, GRB050319A, GRB050326, GRB050406A, GRB050408A, GRB050410, GRB050412, GRB050416A, GRB050416B, GRB050421, GRB050422, GRB050502A, GRB050502B, GRB050504, GRB050505A, GRB050509A, GRB050509B, GRB050509C, GRB050520, GRB050522, GRB050525A, GRB050528, GRB050603A, GRB050607, GRB050701, GRB050709A, GRB050712, GRB050713A, GRB050713B, GRB050714B, GRB050716, GRB050717, GRB050721, GRB050724A, GRB050726, GRB050730A, GRB050801A, GRB050802A, GRB050803A, GRB050813A, GRB050814A, GRB050815, GRB050819, GRB050820A, GRB050820B, GRB050822, GRB050824A, GRB050826A, GRB050827, GRB050904A, GRB050908A, GRB050911, GRB050915A, GRB050915B, GRB050916, GRB050918, GRB050922B, GRB050922C, GRB051001, GRB051006A, GRB051008, GRB051012, GRB051016A, GRB051016B, GRB051021A, GRB051021B, GRB051022A, GRB051028A, GRB051105, GRB051105B, GRB051109A, GRB051109B, GRB051111A, GRB051117A, GRB051117B, GRB051210, GRB051211B, GRB051221A, GRB051221B, GRB051227, GRB060105, GRB060108A, GRB060109, GRB060110, GRB060111A, GRB060111B, GRB060115A, GRB060116A, GRB060117, GRB060121, GRB060124A, GRB060202, GRB060203, GRB060204B, GRB060206A, GRB060210A, GRB060211A, GRB060211B, GRB060213, GRB060218A, GRB060219, GRB060223A, GRB060306, GRB060312, GRB060313, GRB060319A, GRB060323, GRB060403, GRB060413, GRB060418A, GRB060421, GRB060427, GRB060428A, GRB060428B, GRB060501, GRB060502A, GRB060502B, GRB060505A, GRB060507, GRB060510A, GRB060510B, GRB060512A, GRB060515, GRB060522A, GRB060526A, GRB060602A, GRB060604A, GRB060605A, GRB060607A, GRB060614A, GRB060707A, GRB060708A, GRB060712, GRB060714A, GRB060717, GRB060719A, GRB060729A, GRB060801A, GRB060804, GRB060805A, GRB060805B, GRB060807, GRB060813, GRB060814A, GRB060825, GRB060901, GRB060904A, GRB060904B, GRB060906A, GRB060908A, GRB060912A, GRB060919, GRB060923A, GRB060923B, GRB060926A, GRB060927A, GRB060929, GRB061002, GRB061004, GRB061006A, GRB061007A, GRB061019, GRB061021A, GRB061025, GRB061027, GRB061028, GRB061102, GRB061110A, GRB061110B, GRB061121A, GRB061122, GRB061126A, GRB061201A, GRB061202, GRB061210A, GRB061217A, GRB061222A, GRB061222B, GRB070103, GRB070107, GRB070110A, GRB070126, GRB070129A, GRB070208A, GRB070209, GRB070219, GRB070220, GRB070223A, GRB070224A, GRB070227, GRB070306A, GRB070309, GRB070311, GRB070318A, GRB070328, GRB070330, GRB070406, GRB070411A, GRB070412, GRB070419A, GRB070419B, GRB070420, GRB070429A, GRB070429B, GRB070506A, GRB070508, GRB070509, GRB070518, GRB070520A, GRB070520B, GRB070521A, GRB070529A, GRB070531, GRB070611A, GRB070612B, GRB070615, GRB070616

## 为什么是文献级卡

该文是 Swift/UVOT 图像模式 GRB 余辉测光汇编：VizieR Table 3（`J/ApJ/690/163/table3`）有 229 个 GRB 名，逐行给出滤光片、曝光、星等/上限与流量；与本库 `info/` 交集 **226 个源**（见下表）。按 §3.11，覆盖 ≥3 个库内源的多源文献先建本索引卡，不为每个源单独开卡。

**名称映射规则**：VizieR `GRB` 列大小写/后缀不稳定；先精确匹配 `GRB<name>`，无则试 `GRB<name>A`（本库多数源带 A 后缀）；`051105a` 经 alias 对应 `GRB051105`；`060602` 经位置核对（Roming 149.5697/+0.3035 与本库 GRB060602A 149.575/+0.3167 一致，GRB060602B 在 267.368/−28.121）取 `GRB060602A`。3 个名称库内无对应：`051211A`、`060204A`、`060223B`（未列入 `sources`，也未开 new-source Issue，留待维护者决定）。

## 版本状态

- 本次实际使用 arXiv:0809.4193v1（VoR 的 IOP PDF 被 Radware captcha 拦截，未取）；Table 3 通过 VizieR `J/ApJ/690/163/table3` 核到列名与行数。
- Table 2 只列 9 个无 XRT/地面定位的暴的「best reported」位置（OBJECT/RAJ2000/DECJ2000/ERROR/Comments），**不含测光**；它转录的是各暴信息文件里的最佳报告位置（多为 BAT），不是独立测量。
- 本卡只做索引，**不含可采纳数值**；接手者须自行打开 VoR/arXiv 与 VizieR 表逐值核对。

## 涉及源一览

| 源 | 表号 | 源级卡 | status | 增量判读 |
|---|---|---|---|---|
| GRB050117 | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB050124 | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB050128 | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB050215B | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB050219A | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB050219B | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB050223A | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB050306 | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB050315A | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB050318A | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB050319A | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB050326 | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB050406A | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB050408A | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB050410 | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB050412 | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB050416A | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB050416B | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB050421 | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB050422 | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB050502A | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB050502B | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB050504 | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB050505A | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB050509A | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB050509B | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB050509C | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB050520 | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB050522 | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB050525A | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB050528 | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB050603A | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB050607 | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB050701 | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB050709A | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB050712 | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB050713A | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB050713B | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB050714B | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB050716 | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB050717 | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB050721 | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB050724A | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB050726 | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB050730A | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB050801A | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB050802A | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB050803A | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB050813A | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB050814A | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB050815 | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB050819 | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB050820A | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB050820B | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB050822 | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB050824A | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB050826A | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB050827 | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB050904A | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB050908A | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB050911 | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB050915A | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB050915B | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB050916 | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB050918 | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB050922B | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB050922C | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB051001 | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB051006A | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB051008 | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB051012 | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB051016A | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB051016B | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB051021A | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB051021B | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB051022A | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB051028A | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB051105 | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB051105B | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB051109A | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB051109B | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB051111A | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB051117A | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB051117B | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB051210 | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB051211B | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB051221A | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB051221B | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB051227 | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB060105 | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB060108A | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB060109 | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB060110 | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB060111A | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB060111B | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB060115A | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB060116A | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB060117 | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB060121 | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB060124A | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB060202 | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB060203 | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB060204B | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB060206A | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB060210A | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB060211A | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB060211B | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB060213 | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB060218A | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB060219 | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB060223A | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB060306 | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB060312 | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB060313 | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB060319A | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB060323 | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB060403 | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB060413 | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB060418A | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB060421 | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB060427 | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB060428A | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB060428B | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB060501 | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB060502A | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB060502B | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB060505A | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB060507 | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB060510A | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB060510B | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB060512A | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB060515 | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB060522A | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB060526A | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB060602A | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB060604A | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB060605A | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB060607A | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB060614A | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB060707A | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB060708A | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB060712 | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB060714A | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB060717 | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB060719A | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB060729A | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB060801A | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB060804 | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB060805A | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB060805B | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB060807 | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB060813 | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB060814A | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB060825 | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB060901 | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB060904A | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB060904B | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB060906A | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB060908A | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB060912A | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB060919 | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB060923A | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB060923B | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB060926A | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB060927A | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB060929 | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB061002 | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB061004 | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB061006A | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB061007A | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB061019 | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB061021A | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB061025 | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB061027 | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB061028 | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB061102 | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB061110A | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB061110B | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB061121A | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB061122 | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB061126A | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB061201A | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB061202 | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB061210A | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB061217A | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB061222A | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB061222B | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB070103 | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB070107 | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB070110A | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB070126 | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB070129A | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB070208A | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB070209 | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB070219 | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB070220 | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB070223A | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB070224A | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB070227 | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB070306A | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB070309 | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB070311 | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB070318A | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB070328 | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB070330 | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB070406 | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB070411A | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB070412 | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB070419A | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB070419B | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB070420 | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB070429A | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB070429B | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB070506A | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB070508 | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB070509 | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB070518 | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB070520A | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB070520B | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB070521A | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB070529A | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB070531 | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB070611A | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB070612B | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB070615 | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |
| GRB070616 | table3 | 无 | — | 过门槛(3)：正式 UVOT 测光/上限 |

## 增量门槛判读

- 对表内每个源，本文提供了**正式发表的 UVOT 测光/上限**（bibcode `2009ApJ...690..163R`），满足增量门槛第 3 条（新的正式文献引用）；审该源时应把 `Roming+2009` 登记进 `articles[]`，并按 §3.3 逐值核对是否入库。
- 本卡不代替源级卡：若某源在 Table 3 的口径与本库不同（T0 历元、滤光片键、星等系统、co-add 窗口），接手者需另开 `audit/leads/<源ID>.md` 记录差异。
- 纯「GCN 转引」不适用本卡：Table 3 是 UVOT 实测目录，不是 GCN 汇总。

## 待决

- 本卡在 GRB060102 的审核 PR 中建立（该源用 Table 2 交叉核对坐标）。若维护者认为该卡应与 GRB060102 的数据 PR 分离，可另开 docs PR 迁移；卡内容不变。
- `051211A`、`060204A`、`060223B` 三个库外名称是否开 `new-source` Issue，请维护者裁定。
