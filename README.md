# AJST-Data

AJST 暂现源数据库的数据仓库（数据目录 `catadata/`）。本仓库只包含数据与数据说明，配合代码仓库 **AJST** 使用。

## 目录结构

- `info/`：每个暂现源一个 JSON（基本参数、坐标、红移、目录合并数据等），共 1440 个源
- `lc/`：每个暂现源一个 CSV（多波段光变曲线数据点）
- `spectra/`：每个暂现源一个子目录，存放公开光谱（统一 JSON 格式）
- `filters.json`：滤光片/波段定义（银消改正用）
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

- 其余文档：`部分数据说明及导入记录.md`、`数据统一列定义.md`、`external/SCHEMA.md`、`external/统计关系样本添加指南.md`、`external/导入说明_grbcata_source_2.md`

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

**重要**：本数据库的数据批量抓取自已公开发表的文章与 GCN 通告，并继承了某个研究项目（<!-- TODO: 作者补充 -->）的既有数据。目前**尚未完成逐条人工审核**，作者计划用约一年时间完成全部条目的质量审核。**在此之前，请勿将本数据直接用于严肃科学研究。**

## 许可

- 本仓库整体采用 [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) 许可（法律全文见 `LICENSE`）。
- `external/` 各子目录的数据遵从各自原始来源的条款与引用要求。**使用相应子集时请引用原始文献**，出处见各子目录的 `README.md`。
