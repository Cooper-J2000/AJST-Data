- paper_key: tostamelo2024
- paper: Tosta e Melo+2024, A&A 682, A141（DOI 10.1051/0004-6361/202347938，arXiv:2310.17287）"Ready for O4 II: GRANDMA observations of Swift GRBs over eight weeks in spring 2022"
- date: 2026-11-19
- helper: fsy@zcode
- sources: GRB220319A, GRB220325A, GRB220403B, GRB220408A, GRB220412A, GRB220412B, GRB220427A, GRB220430A, GRB220501A, GRB220514A
- out_of_repo: GRB220404A（不在库；new-source Issue 待开，建议见 PR #1105 待决②）
- pr: #1105

# 为什么是文献级卡

GRANDMA "Ready for O4 II" 训练 campaign 的专篇论文（2022-03-19 至 2022-05-14 共 8 周），覆盖 11 个 Swift/INTEGRAL GRB 触发：3 个探测到余辉（220403B、220427A、220514A，各自有专节 + Table B.1 探测表），6 个仅上限（正文 5.1 节逐源文字 + Table B.2 每望远镜一行上限），2 个未观测（220404A、220412B，正文说明日/月约束）。其中 10 个源在库内；**GRB220404A 不在库内（out_of_repo）**——按《数据审核提示词》§3.11 第 8 条不建线索卡源级条目，建议由维护者/主会话开 `new-source: GRB220404A（来自 DOI 10.1051/0004-6361/202347938 的多目标线索）` Issue（该文对该源无观测数据，仅正文一句"未观测"说明，见下表）。

VoR 状态：已获取并核对（EDP Sciences 出版版 A&A 682, A141, 2024-02-13 在线；HTML 全文 + PDF 双通道读取；DataDome 拦 curl，浏览器通道可得）。表 B.1/B.2 在出版社 HTML 中为图片，逐值经渲染 PDF 第 13/14 页视觉核对 + ar5iv LaTeX 源双重印证（pdftotext 对该表多行单元错位，不可作转录依据）。

## 涉及源一览

| 源 | 表号 | 源级卡 | status | 增量判读 |
|---|---|---|---|---|
| GRB220403B | Table B.1（25 行：21 探测 + 4 上限） | GRB220403B.md | extracted | BJP/ALi-50 系列多数行未单独发 GCN；SNOVA/UBAI-AZT-22/KNC-T-CAT 行 VoR 新口径 |
| GRB220427A | Table B.1（探测 12 行）+ 5.2 节 + 宿主 z_phot | 本 PR 数据行（审核中，无卡） | extracted | 已由本 PR 按 VoR 入库（TAROT/TRE 8 行 + Les Makes/T60 4 行）；宿主光致红移 z=0.82±0.09（GROND） |
| GRB220514A | Table B.1（7 行：3 探测 + 4 上限） | GRB220514A.md | extracted | MOSS 19.9±0.25 未单独发 GCN；TNT/CAHA/AbAO/KNC-HAO/KNC-iT21 行 VoR 口径与 GCN 32058 有差 |
| GRB220319A | 正文 5.1 节（上限 ~20 mag B/R/Clear）+ Table B.2（BJP/ALi-50 0.14 h 20.1 Clear） | 无 | mention-only | 文字级上限，时间锚点粗（"∼11 s after the GRB trigger" 为 campaign 时长截断语义）；待审者核对 GCN 31785/31770 |
| GRB220325A | 正文 5.1 节 + Table B.2（NOWT 4.72 h 20.9 R；KAO 8.11 h 21.5 R；C2PU-Omicron 10.16 h 21.6 r'） | 无 | mention-only | B.2 每望远镜一行上限，δt 有锚点；待审者比对 GCN 31793/31797 等 |
| GRB220404A | 正文 5 节（未观测：距太阳过近） | 无（**out_of_repo，不在库**） | mention-only | 无数据；库外源，见元数据区 out_of_repo 与 PR #1105 待决② |
| GRB220408A | 正文 5.1 节（首图 ~38 min V 17.7 上限）+ Table B.2（TRT-SRO 1.82 h 19.3 R；Xinglong-TNT 4.95 h 20.6 R） | 无 | mention-only | 待审者比对 GCN 31855/31859/31862/31864 |
| GRB220412A | 正文 5.1 节（R 上限 20.8）+ Table B.2（UBAI/AZT-22 33.9 h 21.7 R；GMG-2.4 6.06 h 20.5 r'；VIRT 17.59 h 20.3 R） | 无 | mention-only | 待审者比对 GCN 31870/31881/31882/31898 |
| GRB220412B | 正文 5 节（未观测：距月球过近） | 无 | mention-only | 无数据 |
| GRB220430A | 正文 5.1 节（最深上限 21.0 mag 无滤光片）+ Table B.2（SNOVA 17.74 h 19.3 Clear；MOSS 6.59 h 20.3 Clear；Abatsumani/T70 3.22 h 18.7 R） | 无 | mention-only | 待审者比对 GCN 31974/31976/31977/31980 |
| GRB220501A | 正文 5.1 节（r' 16.0 上限，~30 min 起） | 无 | mention-only | 待审者比对 GCN 31990/31997 |

## 增量门槛判读

- **过门槛（已开源级卡）**：GRB220403B、GRB220514A——Table B.1 含未单独发 GCN 的探测行（220403B 的 BJP/ALi-50 高时间采样序列与 SNOVA/UBAI/KNC-T-CAT 行；220514A 的 MOSS 19.9±0.25）。
- **不过门槛（仅索引）**：GRB220319A/220325A/220408A/220412A/220430A/220501A——正文为文字性最深上限汇总（数值与各自 GCN 大体同源），Table B.2 每望远镜一行上限在接手者比对各自 GCN 后再决定是否入库；GRB220404A/220412B 无观测。
- GRB220427A 为本 PR 审核对象，不写卡（避免自占）。

## 待决

- Table B.2 的"每望远镜一行上限"对 6 个未探测源的增量需逐源比对各自 GCN 后由接手者裁决，本卡不做预判断。
- GRB220514A 的 KNC-T21/KNC-iT21 命名在 GCN 32058（KNC-T21 Rc 19.3 @54202 s）与 VoR Table B.1（KNC-iT21 Rc >19.6 @15.06 h）之间不一致，接手者需裁决（本卡不预判）。
