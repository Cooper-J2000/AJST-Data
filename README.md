# AJST-Data

AJST 暂现源数据库的数据仓库（数据目录 `catadata/`）。本仓库只包含数据与数据说明，配合代码仓库 **AJST** 使用。

## 目录结构

- `info/`：每个暂现源一个 JSON（基本参数、坐标、红移、目录合并数据等），共 2794 个源（2026-09）
- `lc/`：每个暂现源一个 CSV（多波段光变曲线数据点），共 2514 个（2026-09）；纯信息源可无 CSV
- `spectra/`：每个暂现源一个子目录，存放公开光谱（统一 JSON 格式）
- `filters.json`：滤光片/波段定义（银消改正用）
- `tags.json`：主/副标签索引
- `tmplibrary/`：光变模板库（ChromaShift 派生数据，`library.json` 为其目录）
- `galaxy_extinction.py`：银河系消光改正工具脚本
- `gcn/archive/`：GCN circular 存档（45315 个 JSON，**不随仓库发布**，可自行再生成，见下文）
- `external/`：外部 GRB 目录与文献样本，每个子目录含 `README.md`（来源与逐列说明）、`parse.py`（解析脚本）、`normalized.jsonl`（规范化产物，输出契约见 `external/SCHEMA.md`）：

| 子目录 | 来源 |
|---|---|
| `batse` | BATSE GRB 目录（HEASARC `batsegrb`） |
| `fermi_gbm` | Fermi GBM 爆发目录（FERMIGBRST） |
| `fermi_lat` | Fermi LAT 第二个 GRB 目录（FERMILGRB / 2FLGC） |
| `swift_bat` | Swift/BAT GRB 目录 |
| `swift_xrt_live` | Swift-XRT GRB Catalogue |
| `swift_grb` | Swift GRB 总表（HEASARC SWIFTGRB） |
| `swiftgrbba` | Swift Burst Advocate 汇编表（HEASARC `swiftgrbba`） |
| `uvot_grb` | Swift/UVOT 第二版 GRB 余辉目录（MAST HLSP UVOTGRB，Roming et al. 2017） |
| `konus_wind` | Konus-Wind 带红移 GRB 目录（Tsvetkova+ 2017 & 2021） |
| `agile_mcal` | 第二版 AGILE-MCAL GRB 目录 |
| `heasarc_grbcat` | HEASARC GRB 总目录（GRBCAT） |
| `mpe_greiner` | Greiner GRB 定位总表（MPE） |
| `grbsn_webtool` | GRBSN webtool 的 GRB-超新星多波段标准化数据 |
| `wang2022` | Wang et al. 2022 Eiso-Ep 校准样本（MNRAS 516, 2575） |
| `minaev2020` | Minaev & Pozanenko 2020 I/II 型暴 Amati 关系样本（MNRAS 492, 1919） |
| `guidorzi2025` | Guidorzi et al. GRB 变异性-光度样本（A&A 690, A261） |
| `liang2023` | Liang et al. 2023 Fermi-GBM 带红移 GRB 谱分类目录（ApJS 266, 31） |
| `rssgrbag` | 射电遴选 GRB 余辉目录（Chandra & Frail 2012, ApJ 746, 156） |
| `saxgrbmgrb` | BeppoSAX/GRBM GRB 目录（HEASARC `saxgrbmgrb`） |

- `tools/`：零依赖命令行工具（`validate.py` 数据校验、`audit_queue.py` 审核队列与认领）
- `audit/`：认领快照 `state.tsv`（机器生成，**勿手改**；契约见 `audit/README.md`）
- 其余文档：`数据审核提示词.md`、`部分数据说明及导入记录.md`、`数据统一列定义.md`、`external/SCHEMA.md`、`external/统计关系样本添加指南.md`、`external/导入说明_grbcata_source_2.md`

## 数据契约与贡献

| 文件 | 作用 |
|---|---|
| **`SCHEMA.md`** | 数据格式的唯一权威定义（info JSON 字段契约、lc CSV 24 列契约、命名规范、`null` 约定）。 |
| **`CONTRIBUTING.md`** | 校验 / 扩充 / 提交流程：`python3 tools/validate.py` 零依赖全量校验（CI 自动运行），扩充按 SCHEMA 契约，提交走 Pull Request。 |
| **`数据审核提示词.md`** | **逐源数据审核任务的提示词**：整段发给你的 agent（Claude Code / Cursor / ZCode 等）即可开工，详见下节。 |
| **`audit/README.md`** | 认领快照 `audit/state.tsv` 的契约与读取规则——多方并行审核时的查重依据。 |
| **`tools/audit_queue.py`** | 审核队列工具：挑源（`--limit`）、确定性分片（`--bucket 1/4`）、查单源状态（`--id`）、实时查重（`--live`）。 |

效力：`SCHEMA.md` / `CONTRIBUTING.md` / `audit/README.md`（数据与流程契约）高于 `数据审核提示词.md`（任务提示词）；冲突时以契约文件为准，并欢迎就提示词本身提 Issue / PR。

## 用你自己的 agent 参与数据审核（外部贡献推荐入口）

本库最核心的工作，是把 2794 个源**逐个从「未核实」变成「已核实」**（见文末免责声明）。任何合作者都可以用自己的 agent 来做这件事，不必了解后端代码：

1. clone / fork 本仓库；
2. 把 **`数据审核提示词.md`** 里的「提示词本体」整段发给你的 agent（该文件开头有给人看的使用说明）；
3. 让 agent 先挑源并认领，别和其他合作方撞车：
   ```bash
   python3 tools/audit_queue.py --limit 20     # 可认领队列（小源在前）
   python3 tools/audit_queue.py --bucket 1/4   # 多人并行时用确定性分片，彼此不重叠
   python3 tools/audit_queue.py --live         # 实时查重（判据）
   ```
   开工即开 draft PR（标题 `claim: <源ID>`）。离线时读 `audit/state.tsv`，但它只能**排除已占用**、
   不能**确认空闲**（快照最长滞后 24 小时，超过 3 天即过期）；
4. 按提示词约定完成单源复核，**一个源一个 PR** 回交上游。

agent 会先跟你确认**审核人姓名**，再用队列工具挑源、开 `claim:` draft PR 认领，之后才开工。几个关键约定（完整版见提示词本体）：

- 库中已有数据一律视为「未核实」，不盲目相信；原有行同样逐行核对；
- 每个数值都必须在本次会话中从来源原文实际核对得出，**严禁臆造 / 内插 / 估算 / 凭模型记忆填写**；
- 复核后的整张光变表统一用同一个标准 T0；`T0` 本身不改，真实爆发时刻的偏差写入 `T0_offset`（秒，后移为正、提前为负）；
- 星等就存星等（`flux_density_unit=magnitude`），不做单位换算、不做消光改正，后端派生列（`Gext_*` 系列）一律留空；
- `band` 只有两条车道：光学 / UV / IR 用 `filters.json` 里已有的键；射电 / 亚毫米写物理频率串（如 `4.86GHz`、`250GHz`，**不进** `filters.json`，原文不同发表值不得归一化合并）。**X 射线行（`band` 为能量串，如 `10keV`）暂不在审核范围——不改、不删、不新增，逐行核对时跳过并保持原样**；
- 开工先认领（`claim: <源ID>` draft PR）：一个源同时只应有一个未过期认领，普通源 14 天、`lc` 超 1000 行的巨源 30 天；遇到别人未过期的认领先评论询问并等 48 小时再接手；
- 开 PR 前必须发起一个**无利益关联的独立子代理**核查数据真实性，核查结论写入 PR 说明；
- 提交前 `python3 tools/validate.py` 必须 0 错误（CI 会重跑）。

直链（方便 `curl` 或在 Issue 里贴给别人的 agent）：

```
https://raw.githubusercontent.com/Cooper-J2000/AJST-Data/main/%E6%95%B0%E6%8D%AE%E5%AE%A1%E6%A0%B8%E6%8F%90%E7%A4%BA%E8%AF%8D.md
```

## 接入方法

1. 将本仓库 clone 到 AJST 代码仓库的 `catadata/` 位置：

   ```bash
   git clone <本仓库地址> catadata
   ```

   或放到任意位置后设置环境变量：

   ```bash
   export AJST_DATA_DIR=/path/to/catadata
   ```

2. 运行代码仓库的 `backend/etl.py` 将数据导入 PostgreSQL。

3. GCN 存档不随本仓库分发，用代码仓库的 `scripts/fetch_gcn_archive.sh` 拉取，或手动下载解压：

   ```bash
   curl -sL https://gcn.nasa.gov/circulars/archive.json.tar.gz | tar -xz -C gcn/
   ```

   （解压目标为 `gcn/archive/`，每个 circular 一个 JSON。）

## 数据质量免责声明

**重要**：本数据库的数据批量抓取自已公开发表的文章与 GCN 通告，并继承了 [Dainotti 2024](https://academic.oup.com/mnras/article/533/4/4023/7697178?login=true) 等研究项目的既有数据。目前**尚未完成逐条人工审核**，作者计划用约一年时间完成全部条目的质量审核。**在此之前，请勿将本数据直接用于严肃科学研究。**

欢迎社区对数据的贡献，项目作者不胜感激。想参与逐源审核的合作者（包括让自己的 agent 来做），直接从 [`数据审核提示词.md`](数据审核提示词.md) 开始。

## 许可

- 本仓库整体采用 [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) 许可（法律全文见 `LICENSE`）。
- `external/` 各子目录的数据遵从各自原始来源的条款与引用要求。**使用相应子集时请引用原始文献**，出处见各子目录的 `README.md`。
