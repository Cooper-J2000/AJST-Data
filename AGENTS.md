# AJST-Data — agent 必读（每次开工先读这一页）

本仓库是 AJST 暂现源光变目录的**数据**仓库（`info/*.json` + `lc/*.csv`，GRB / 超新星 / FRB 等）。
**唯一权威是 [`数据审核提示词.md`](数据审核提示词.md)**——本文件只是入口与最常违规项的摘要，
**冲突时以提示词为准**。

## 开工顺序（缺一不可）

1. 通读 `数据审核提示词.md`（尤其 §2 开始之前、§3 单源审核流程、§7 禁止事项、§8 自检清单）；
2. 契约补充：`SCHEMA.md`、`CONTRIBUTING.md`、`audit/README.md`、`audit/leads/README.md`、`filters.json`、`tags.json`；
3. `python3 tools/audit_queue.py --id <源ID>` 查状态：`reserved` = 维护者自留，**不得认领、不得开 claim PR**；
4. 开工第一件事开 `claim: <源ID>` **draft** PR；审核与子代理核查通过后转正式，标题改 `data: 审核 <源ID>（一句话摘要）`；
5. PR 正文按 `.github/PULL_REQUEST_TEMPLATE.md` 填（对应提示词 §5 七要素）。

## 最常被违反的 5 条（细节见提示词）

1. **`lc/` 为空或行数偏少的源必须检索并留证**（§3.3，2026-10-24 新增）。先查仓内
   `gcn/archive`（45 563 篇 Circular 全文）、`external/rssgrbag`、`external/grbsn_webtool`，再查
   GCN 站 / **ADS 或 SciX** / TNS；`comment` 末段按「**检索日期 + 入口与篇数 + 结论 + 补了几行**」留证。
   **只写一句「已检索」不算留证。** 检索到的探测与上限，只要有明确时间锚点（绝对时刻，或 `+26.3 h`
   这类相对触发时长），就要入库，不能只写 comment。
2. **`T0` 只能是触发时刻**（§3.2）：GCN 通告里观测窗口的起止时刻（`from 07:00-09:30 UTC`、
   `through to 04:55:50 UT`、`starting at 13:40 UT`）**不得**写进 `T0`；通告只给「窗口 + 相对触发时长」时，
   用该时长反算触发时刻并在 `T0_ref` 写明依据。见 Issue #84。
3. **X 射线行（`band` 为能量串，如 `10keV`）不改、不删、不新增、不参与去重**（§3.3 / §3.4 / §7）。
4. **一源一 PR**；不动别人的源、不动 `spectra/` `tmplibrary/` `external/` `tools/`；不手改 `audit/state.tsv`；
   库外新源用 `new-source` Issue，不擅自新建 `info/<id>.json`。
5. **提交前 `python3 tools/validate.py` 必须 0 错误**；`--strict` 的告警看「相对基线是否新增」，
   不要用退出码当唯一判据（main 上本来就有历史告警）。

## 最近更新（外部 agent 请注意版本）

- **2026-10-24**：§3.3 新增「零测光 / 测光稀少的源：检索义务与留证」，并同步 §8 自检清单；
  同日 §3.3 写明「历史上限有时间锚点才入库」，检索入口加入 **SciX**（= ADS 升级版，2026-11-16 ADS 并入 SciX）；
  `tools/audit_queue.py --id` 与 `tools/validate.py` 也会就零测光留证给出提示/警告。
- **2026-10-12**：无滤光片 → `band=G` + comment（不新增臆造波段）；`T0_offset` 只记真实爆发时刻相对
  **设备自动触发** T0 的偏移，且要求 `|offset| > 1 s`。

## 不确定时

按提示词 §7 分 A / B 两档：A 档（影响数据对错或源身份）写进 PR 说明的「待决事项」等维护者裁决；
B 档按默认动作处理并写进 `comment`。两档都**不得臆造**；拿不准就停下来问用户。
