# AJST-Data 数据契约（SCHEMA）

> 本文件是 AJST-Data 数据格式的**唯一权威定义**。改动数据格式必须先改本文件。
> 机器校验：`python3 tools/validate.py`（纯标准库，任意环境可跑）。
>
> English summary: every transient is one `info/<id>.json` (metadata) plus an optional
> `lc/<id>.csv` (lightcurve points). Since format version **v2.30**, all canonical
> `info` keys are ALWAYS present — missing values are explicit `null`, never omitted
> keys. Lists (`alias`/`tag`/`sub_tag`/`articles`) are always arrays (possibly empty).
> Times: `T0` is ISO8601 UTC; lc `time` is seconds relative to T0; `mjd` is the
> authoritative absolute time. Bands: every `lc` `band` is either a `filters.json`
> key (optical/UV/IR) or a numeric+unit string — `4.86GHz` (radio frequency) /
> `10keV` (X-ray, monochromatic Fν at 10 keV); see §3.1. Run `tools/validate.py`
> before submitting.

## 1. 目录结构与命名

| 路径 | 内容 | 命名规范 |
|---|---|---|
| `info/<id>.json` | 每个暂现源一份元数据 | `<id>` 只允许字母和数字（1–32 字符），与 JSON 内 `transient_id` 完全一致 |
| `lc/<id>.csv` | 每个暂现源一份光变点 | 同名 `<id>.csv`；纯信息源（无任何光变点）可以没有 CSV |
| `spectra/<id>/` | 每个暂现源一个子目录，公开光谱（统一 JSON） | 同名 `<id>` |
| `filters.json` | 滤光片/波段定义（消光改正、拟合用） | 键 = 波段 id |
| `tags.json` | 主/副标签索引 | 数组 `[{name, kind, description, color}]` |
| `tmplibrary/` | 光变模板库（ChromaShift 派生数据；`library.json` 为目录） | 见 `tmplibrary/` 内说明 |
| `external/<目录>/` | 外部目录与文献样本 | 各含 `README.md` + `parse.py` + `normalized.jsonl`，契约见 `external/SCHEMA.md` |

不进仓库的内容：`gcn/archive/`（可再生成）、`backups/`、本机名单文件。

## 2. `info/<id>.json` 字段契约

顶层对象。**v2.30 起全部规范键恒在**：值为空时显式写 `null`（列表写 `[]`），不省略键。
读取方应把「键缺失」与「键 = null」视为等价（兼容 v2.30 之前的旧文件）。

| 键 | 类型 | 空值 | 说明 |
|---|---|---|---|
| `transient_id` | string | 必填 | 源 id，与文件名一致；只允许字母数字 |
| `alias` | string[] | `[]` | 别名列表 |
| `ra` | number\|null | `null` | 赤经，十进制度，[0, 360]，J2000 |
| `dec` | number\|null | `null` | 赤纬，十进制度，[-90, 90]，J2000 |
| `T0` | string\|null | `null` | 参考时刻（触发/发现/峰值等），ISO8601 UTC（如 `2023-01-22T09:21:36Z`） |
| `T0_ref` | string\|null | `null` | T0 的取值依据（引用） |
| `T0_offset` | number\|null | `null` | T0 偏移量，秒（正 = 向后，负 = 提前）；纯元数据，不改写光变时间轴 |
| `T0_offset_ref` | string\|null | `null` | T0 偏移量的引用 |
| `Trigger_Instrument` | string\|null | `null` | 触发仪器（如 `Swift/BAT`、`IPN`） |
| `redshift` | number\|null | `null` | 红移 |
| `redshift_type` | string\|null | `null` | 红移类型（如 `spec`/`phot`） |
| `redshift_ref` | string\|null | `null` | 红移引用 |
| `pos_error` | number\|null | `null` | 定位误差半径 |
| `pos_error_unit` | string | 默认 `"arcsec"` | 定位误差单位 |
| `pos_ref` | string\|null | `null` | 定位引用 |
| `comment` | string\|null | `null` | 备注 |
| `tag` | string[] | `[]` | 主标签（如 `grb`、`sn`；受控词表见 `tags.json`） |
| `sub_tag` | string[] | `[]` | 副标签（如 `lgrb`、`snii`） |
| `extra_data` | object\|null | `null` | 自由扩展字段（入库来源、抓取标记等），不做 schema 约束 |
| `articles` | object[] | `[]` | 研究文章，见 §2.1 |
| `host_galaxy` | object\|null | `null` | 宿主星系，见 §2.2 |

### 2.1 `articles[]` 元素

| 键 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `name` | string | 是 | 短引用名（如 `Smith+2023`） |
| `url` | string | 是 | 文章链接 |
| `title` | string | 否 | 标题 |
| `bibtex` | string | 否 | BibTeX 条目 |
| `source` | string | 否 | 录入来源（`bot` / 账户名等） |

### 2.2 `host_galaxy` 对象

整个对象为 `null` 表示该源无宿主记录（导入语义：null = 删除库中宿主记录）。
对象内字段为空的键省略不写：

| 键 | 类型 | 说明 |
|---|---|---|
| `ra` / `dec` | number | 宿主坐标，十进制度 J2000 |
| `redshift` / `redshift_err` | number | 宿主红移及误差 |
| `redshift_type` | string | `spec` / `phot` 等 |
| `photometry` | object[] | 宿主测光点 `[{band, mag, mag_err, mag_sys, source}]` |
| `derived` | object | 拟合派生量缓存（M\*、SFR 等） |
| `comment` / `source` | string | 备注 / 来源 |

## 3. `lc/<id>.csv` 列契约

表头恰为下列 **24 列**（顺序固定）。空值一律为空字符串。`time`/`mjd` 语义见 §1 顶部说明。

| 列 | 类型 | 必填 | 允许值 / 说明 |
|---|---|---|---|
| `time` | float | 是 | 观测中心时间，相对 T0 |
| `time_err` | float | 否 | 时间误差（如半曝光时间） |
| `time_unit` | str | 是 | `s`/`sec`、`m`/`min`、`h`/`hour`、`d`/`day` |
| `mjd` | float | 否 | 权威绝对时间（T0 + time 换算；T0 为空时为空） |
| `band` | str | 是 | 波段标识，见 §3.1（`filters.json` 键，或频率 / 能量串） |
| `flux_density` | float | 是 | 原始流量密度值（或星等值） |
| `flux_density_err` | float | 否 | 原始误差（1σ） |
| `flux_density_unit` | str | 是 | `mJy`、`uJy`、`cgs`(erg/cm²/s/Hz)、`magnitude` |
| `mag_system` | str | 条件必填 | `AB`/`Vega`；`flux_density_unit=magnitude` 时必填 |
| `Gext_corr` | str | 否 | `y`/`n`，是否已做银河系消光改正，缺省 `n` |
| `upperlimit` | str | 否 | `y`/`n`，是否上限（非探测），缺省 `n` |
| `Gext_Alambda` | float | 否 | 银河系消光量，由后端消光程序给出 |
| `mag_Gextcor` | float | 否 | 消光改正后 AB 星等（Vega 先转 AB 再减 Aλ） |
| `mag_Gextcor_err` | float | 否 | 改正后星等误差（1σ），等于原星等误差 |
| `flux_density_Gextcor` | float | 否 | 改正后流量密度，单位固定 mJy |
| `flux_density_Gextcor_err` | float | 否 | 改正后流量误差（1σ），mJy |
| `flux_density_Gextcor_unit` | str | 否 | 固定 `mJy` |
| `weights` | float | 否 | 拟合权重，默认 1 |
| `discard` | str | 否 | `y`/`n`，是否弃点，缺省 `n` |
| `telescope` | str | 否 | 望远镜名称 |
| `instrument` | str | 否 | 仪器名称 |
| `reference` | str | 否 | 文献引用或数据源 |
| `comment` | str | 否 | 备注 |
| `source` | str | 否 | 录入来源（账户名 / 管线标识） |

### 3.1 `band` 两条车道

`band` 的值只有两类，解析端用同一个正则识别（代码仓库 `backend/fitting/jobs.py` 的
`_FREQ_BAND_RE`；大小写不敏感，容许内部空格）：

| 车道 | 取值 | 示例 | 进 `filters.json`？ |
|---|---|---|---|
| 一：光学 / UV / IR | `filters.json` 中已有的波段键 | `r`、`V`、`J` | 是（新波段须在同一 PR 中按其现有格式补充定义） |
| 二：射电 / 亚毫米 | 「数字 + 单位」串，单位 `Hz`/`kHz`/`MHz`/`GHz`/`THz` | `4.86GHz`、`250GHz` | 否 |
| 二′：X 射线 | 「数字 + 单位」串，单位 `eV`/`keV`/`MeV`/`GeV`（光子能量） | `10keV` | 否 |

- 库内惯例**无空格**（写 `4.86GHz`，不写 `4.86 GHz`）；同一源内保持一致。
- 同一波段的**不同发表值**（`4.8GHz` / `4.86GHz` / `4.9GHz`）是不同文献的不同测量，
  **不得**互相归一化或合并。
- X 射线行语义：能量串（如 `10keV`）表示 **10 keV 处的单色流量密度 Fν**，**不是**能段
  积分流量；单位由该行 `flux_density_unit` 给出（库内 Swift/XRT 的 `10keV` 行多为 `Jy`，
  来源 UKSSDC Swift Burst Analyser）。
- `tools/validate.py` 逐行检查 `band`：为空、或不在上述两条车道内 → **错误**（见 §5）。

## 4. `filters.json` / `tags.json`

- `filters.json`：对象，键 = 波段 id；每项必备数值 `wavelength`（埃），可选 `type`、`Vega2AB`、`description`、`extra_data`（含透过率曲线等）。
- `tags.json`：数组，元素 `{name, kind, description, color}`；`kind` ∈ `main`/`sub`。

## 5. 校验

```bash
python3 tools/validate.py            # 全量校验，结构性错误 → 退出码 1
python3 tools/validate.py --strict   # 值域警告也算失败
```

- `lc` 的 `band` 逐行检查是否落在 §3.1 的两条车道内、是否为空：越界算**错误**
  （`filters.json` 缺失/损坏时只报根因一次并跳过车道一判定，不逐行报错）。
- GitHub Actions 会对每个 push / PR 自动运行同一脚本（`.github/workflows/validate.yml`），
  跑的是非 `--strict` 模式 —— 因此 band 越界会直接让 PR 变红。
