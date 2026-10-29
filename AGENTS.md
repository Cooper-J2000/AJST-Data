# AJST-Data — agent 必读（每次开工先读这一页）

本仓库是 AJST 暂现源光变目录的**数据**仓库（`info/*.json` + `lc/*.csv`，GRB / 超新星 / FRB 等）。
**唯一权威是 [`数据审核提示词.md`](数据审核提示词.md)**——本文件只是入口与最常违规项的摘要，
**冲突时以提示词为准**。

## 开工顺序（缺一不可）

0. **先清自己手上的反馈**：`gh pr list --author @me --state open`，逐个 `gh pr view <n> --json comments`。
   维护者在**你自己** open PR 下的评论就是审核意见，**处理完（改数据 + 回复 commit sha，或写明未采纳理由）才允许领新源**
   （提示词 §2 第 2 条 / §5 第 8 项）。已合并/已关闭的不必回看。
1. 通读 `数据审核提示词.md`（尤其 §2 开始之前、§3 单源审核流程、§7 禁止事项、§8 自检清单）；
2. 契约补充：`SCHEMA.md`、`CONTRIBUTING.md`、`audit/README.md`、`audit/leads/README.md`、`filters.json`、`tags.json`；
3. `python3 tools/audit_queue.py --id <源ID>` 查状态：`reserved` = 维护者自留，**不得认领、不得开 claim PR**；
4. 开工第一件事开 `claim: <源ID>` **draft** PR；审核与子代理核查通过后转正式，标题改 `data: 审核 <源ID>（一句话摘要）`；
5. PR 正文按 `.github/PULL_REQUEST_TEMPLATE.md` 填（对应提示词 §5 七要素）；
6. **每交付一个源后**：`git fetch origin main && git log --oneline HEAD..origin/main`。有变动先
   `git pull --rebase origin main` 再挑下一个源；新提交若碰到你刚提交的源、或你下一个要审的源，
   先读改动再动手。维护者会直接改 `info/`、`lc/`、`tools/` 与文档，这条保证**我方改动在你的下一次任务里一定可见**
   （提示词 §2 第 10 条 / §5 第 7 条，2026-10-24 新增）。PR 页面上也会有一条「分支落后」的 CI 警告，落后多少提交、落后哪几个，都在那里。

## 最常被违反的 6 条（细节见提示词）

1. **PR 有评论就要回**（§2 第 2 条 / §5 第 8 项，2026-10-29 新增）：维护者评论＝审核意见。采纳就改数据并在回复里给
   `commit sha`，不采纳就写理由 + 证据；**不得静默重推同一 diff**。有未处理反馈时不领新源。
2. **`lc/` 为空或行数偏少的源必须检索并留证**（§3.3，2026-10-24 新增）。先查仓内
   `gcn/archive`（45 563 篇 Circular 全文）、`external/rssgrbag`、`external/grbsn_webtool`，再查
   GCN 站 / **ADS 或 SciX** / TNS；`comment` 末段按「**检索日期 + 入口与篇数 + 结论 + 补了几行**」留证。
   **只写一句「已检索」不算留证。** 检索到的探测与上限，只要有明确时间锚点（绝对时刻，或 `+26.3 h`
   这类相对触发时长），就要入库，不能只写 comment。
3. **`T0` 只能是触发时刻**（§3.2）：GCN 通告里观测窗口的起止时刻（`from 07:00-09:30 UTC`、
   `through to 04:55:50 UT`、`starting at 13:40 UT`）**不得**写进 `T0`；通告只给「窗口 + 相对触发时长」时，
   用该时长反算触发时刻并在 `T0_ref` 写明依据。见 Issue #84。
4. **X 射线行（`band` 为能量串，如 `10keV`）不改、不删、不新增、不参与去重**（§3.3 / §3.4 / §7）。
5. **一源一 PR**（CI 的 `check_pr_scope.py` 会拦：一个 PR 只能碰一个 `info/lc` 源；§3.7 的源级处置也要拆两个 PR，
   除非维护者在本 PR 下裁定接受）；不动别人的源、不动 `spectra/` `tmplibrary/` `external/` `tools/`；不手改 `audit/state.tsv`；
   库外新源用 `new-source` Issue，不擅自新建 `info/<id>.json`。
6. **提交前 `python3 tools/validate.py` 必须 0 错误**（含新增的「每行 `flux_density` 非空」ERROR）；`--strict` 的告警看「相对基线是否新增」，
   不要用退出码当唯一判据（main 上本来就有历史告警）。

## 最近更新（外部 agent 请注意版本）

- **2026-10-29**：三条契约硬化（本批 155 个 PR 审核暴露）：
  1. **PR 有评论就要回**（§2 第 2 条 / §5 第 8 项）：领新源前先 `gh pr list --author @me --state open` 扫自己 PR 的
     维护者评论，改数据 + 回复 `commit sha`（或不采纳理由）后才允许继续；PR 模板新增「前序 PR 反馈处理」栏。
  2. **一源一 PR 由 CI 强制**：新增 `tools/check_pr_scope.py`（`validate` job 内运行）——`info/lc` 源集合 >1 或改动路径
     越界（如 `filters.json`）即红；维护者 PR 豁免。§3.7 源级处置同样要拆两个 PR。
  3. **`flux_density` 每行必须非空**：`validate.py` 升级为 ERROR。上限行的限度、探测行的测量值都要写进列，
     只写在 `comment` 里不算（本批 5 个 draft PR、94 行犯此错，`main` 上基线是 0 行）。
  另：**空转认领可被提前释放**（§5.6）——认领 72 h 内零提交零更新、维护者留言无回应者，维护者直接关闭并释放源
  （先例 #342–#344 `GRB001019`/`GRB010326A`/`GRB021125`，10-26 → 10-29 释放）。

- **2026-10-26**：三条维护者裁定，已落进契约与校验器：
  1. **`articles[]` 不收 GCN 通告**（§3.5、SCHEMA §2.1）。通告出处只写在 `comment` 的核对记录与 `lc` 行的
     `reference`；`articles[]` 只放研究论文（DOI/arXiv）。`validate.py` 新增警告级普查「articles 含 GCN 通告」
     （存量回扫后应归零）。
  2. **alias 伪形豁免**（§3.10）：伪形在 `comment`/`extra_data` 文本里带证据串 **`<GCN nnn> … 原文用名`**
     （同段内既有通告编号、又出现该别名原文写法）即视为有出处、不计入伪形普查；没有证据串的照旧计入。
     `validate.py` 现已自动豁免并单列「另 N 项豁免」。这条回答了 Issue #69 的白名单申请。
  3. **`sub_tag` 可用来源表的 `t90` 字段判定**（§3.9）：须在 `comment` 写明 `t90=<值>±<误差> s（<目录/通告>）`
     并注明「按目录 t90 判 lgrb/sgrb」；禁止自己从光变曲线现算 T90。冲突时仍留空待决。
- **2026-10-24**：§3.11 线索卡加**增量门槛**（只有「库内 GCN/目录拿不到的量、不同口径、新的正式文献引用」
  才开源级卡；纯汇总表转引 GCN 不开卡），并新增**文献级索引卡** `audit/leads/papers/<paper_key>.md`
  （一篇多源文献一张，覆盖 ≥3 个库内源时先建；契约见 `audit/leads/papers/README.md`）。
  工具同步：`audit_queue.py --paper <key>` / `--check-leads`（PR 守卫，警告级）、`validate.py` 校验文献级卡、
  PR 模板加「多目标文献线索」一栏；历史已合并的源级卡**不追溯回滚**。
- **2026-10-24**：§3.3 新增「零测光 / 测光稀少的源：检索义务与留证」，并同步 §8 自检清单；
  同日 §3.3 写明「历史上限有时间锚点才入库」，检索入口加入 **SciX**（= ADS 升级版，2026-11-16 ADS 并入 SciX）；
  `tools/audit_queue.py --id` 与 `tools/validate.py` 也会就零测光留证给出提示/警告。
- **2026-10-12**：无滤光片 → `band=G` + comment（不新增臆造波段）；`T0_offset` 只记真实爆发时刻相对
  **设备自动触发** T0 的偏移，且要求 `|offset| > 1 s`。

## 不确定时

按提示词 §7 分 A / B 两档：A 档（影响数据对错或源身份）写进 PR 说明的「待决事项」等维护者裁决；
B 档按默认动作处理并写进 `comment`。两档都**不得臆造**；拿不准就停下来问用户。
