# minaev2020 — Minaev & Pozanenko 2020 I/II 型暴 Amati 关系样本（Table A1）

- **来源论文**：Minaev P.Y., Pozanenko A.S., "The E_p,i–E_iso correlation: type I
  gamma-ray bursts and the new classification method",
  *MNRAS* 492, 1919–1936 (2020)，bibcode `2020MNRAS.492.1919M`
- **VizieR 目录**：`J/MNRAS/492/1919`（表 `tablea1` 为 GRB 样本，320 条；附表 `refs`
  为 130 条参考文献编号对照）
- **目录页 URL**：https://cdsarc.cds.unistra.fr/viz-bin/cat/J/MNRAS/492/1919
- **数据获取方式**：VizieR TAP 同步查询（CSV）
  `curl -s "https://tapvizier.cds.unistra.fr/TAPVizieR/tap/sync?REQUEST=doQuery&LANG=ADQL&FORMAT=csv&QUERY=SELECT%20*%20FROM%20%22J%2FMNRAS%2F492%2F1919%2Ftablea1%22"`
  （refs 表同理，`FROM "J/MNRAS/492/1919/refs"`）
- **VizieR ReadMe**：https://cdsarc.cds.unistra.fr/ftp/J/MNRAS/492/1919/ReadMe
  （已存为 `vizier_ReadMe.txt`，列定义/单位/脚注以此为准）
- **获取日期**：2026-07-21（UTC）

## 数据内容

320 个已知红移的 GRB（45 个 I 型 + 275 个 II 型，截至 2019 年 1 月），
用于研究静止系峰值能量 E_p,i 与各向同性等效能量 E_iso 的 Amati 关系。
样本来自 Konus-Wind、BeppoSAX、Fermi-GBM、HETE-2、BATSE 等目录及单爆文献；
其中 44 个源（`f_GRB='*'`）的 E_iso/E_p,i 由本文作者用文献谱参数自行计算。
文章还定义了两个分类参数：EH = (E_p,i/100keV)·(E_iso/1e51erg)^-0.4，
EHD = EH·(T_90,i/1s)^-0.5，并给出各自对应的 I/II 分类。

## 文件清单

| 文件 | 说明 |
|---|---|
| `tablea1.csv` | TAP 下载的主表原始 CSV（320 行 × 25 列），原样保留 |
| `refs.csv` | TAP 下载的参考文献表（130 条，Ref 编号 ↔ bibcode/作者） |
| `vizier_ReadMe.txt` | VizieR 官方 ReadMe（列定义、单位、脚注） |
| `parse.py` | 解析器（仅用 Python 标准库），`python3 parse.py` 重跑 |
| `normalized.jsonl` | 输出，320 行，契约见 `../SCHEMA.md` |

## 单位确认（关键）

- **Eiso**：VizieR ReadMe 标注单位为 `10+44J`（1e44 J = **1e51 erg**），
  即表内数值需 ×1e51 得到 erg。抓数据验证：
  GRB 970228 = 12.01 → 1.2e52 erg（Amati 2002 约 1.5e52 ✓）；
  GRB 971214 = 146.3 → 1.46e53 erg ✓；GRB 190114C = 270.3 → 2.7e53 erg ✓；
  GRB 170817A = 4.7e-5 → 4.7e46 erg（GW170817 已知低 E_iso ✓）。
  若误按 1e52 换算，190114C 将达 2.7e54 erg，超出合理范围。
- **Epi**：keV，**静止系**（rest-frame）峰值能量。
- **T90i**：秒，**静止系** T90；`I+EE` 型暴给的是初始脉冲复合体（IPC）的时标
  （VizieR ReadMe Note 2），不是全暴 T90，使用时注意。
- **z**：红移，`f_z='PH'` 表示测光红移（16 条）；10 条有红移误差（E_z/e_z）。

## 字段映射（tablea1 → normalized）

| 原列 | 去向 | 说明 |
|---|---|---|
| `GRB` | `name` | `'970228 '` → `'GRB 970228'`（strip 后加 `GRB ` 前缀；320 条均为 `YYMMDD[A]` 格式，无重复） |
| `SimbadName` | `name_alt` | 仅当与构造的 `name` 不同时放入（13 条，如 `GRB 980425B` ↔ `GRB 980425`） |
| `_RA`/`_DE` | `ra`/`dec` | J2000 度 |
| `T90i` | `params.t90` | `{"v": s, "err": null, "band": null, "frame": "rest"}`；无误差列、能段未知故 band=null |
| `z`,`E_z`,`e_z` | `params.redshift` | `{"v": z}`，有误差时加 `"err": [正, 负]`（10 条） |
| `Eiso`,`E_Eiso`,`e_Eiso` | `params.eiso` | ×1e51 换算成 erg；`{"v","err","band":null,"frame":"rest"}`（各仪器能段不一，band 无法统一标注） |
| `Epi`,`E_Epi`,`e_Epi` | `params.ep_rest` | `{"v": keV, "err": [正,负], "frame": "rest"}` |
| `Type` | `params.grb_type` + `other.Type` | `I`、`I+EE`→`'I'`；`II`、`II+SNph`、`II+SNsp`→`'II'`；原值保留在 `other.Type` |
| `f_GRB` | `other.f_GRB` | `'*'` = Eiso/Epi 由本文计算（44 条）；空白省略 |
| `f_z` | `other.f_z` | `'PH'` = 测光红移（16 条）；空白省略 |
| `Exp` | `other.Exp` | 计算 T90i/Epi/Eiso 所用仪器（Konus-Wind/Swift/Fermi/HETE-2/BeppoSAX/BATSE-CGRO） |
| `Ref` | `other.Ref` | 参考文献编号（逗号分隔），对照 `refs.csv` |
| `EH`,`EHtype`,`EHD`,`EHDtype` | `other` 同名键 | 分类参数及其对应的 I/II 判定（EH/EHD 转 float） |
| `recno` | `other.recno` | 原始行号 |

- `trigger_time`：表中无触发时刻，一律 `null`（name 的日期可兜底）。
- 误差约定：E_E*/e_* 分别为上/下误差，不对称时输出 `[正, 负]` 数组，
  相等时输出单值（如 GRB 970228 的 Eiso 误差 9.3e50 erg）。

## 假设与注意事项

1. **Eiso 单位 = 1e51 erg**（1e44 J）：以 VizieR ReadMe 单位标注为准，
   并用多个已知暴的文献值交叉验证（见上）。
2. **Type 映射**：`II+SNph`（光变曲线证认超新星，19 条）、`II+SNsp`（光谱证认，
   21 条）、`I+EE`（带延展辐射的 I 型，11 条）均归入基本型 I/II，
   细分信息保留在 `other.Type`。注意 VizieR ReadMe Note 3 中 SNph/SNsp 的
   "spectroscopically/photometrically" 描述疑与原论文写反
   （ph=photometric、sp=spectroscopic），不影响本映射。
3. `I+EE` 的 `T90i` 是 IPC 时标而非全暴 T90（11 条）。
4. `I+EE` 映射为 I 型是论文自身的分类（abstract 明确 45 I + 275 II，
   与解析输出计数一致）。
5. 红移误差仅 10 条有值；`redshift.err` 缺失时省略该键（SCHEMA 规则 1）。

## 验证

- `python3 parse.py` 输出 320 条；params 各键覆盖 320/320；
  grb_type I=45、II=275（与论文 abstract 一致）；ra/dec/name 覆盖 100%。
- 抽查 GRB 970228 / 980425B / 050709A / 060614A / 170817A / 190114C，
  Eiso、Epi、z 均与文献值吻合（量级 4.7e46–5.8e54 erg、3.37–7955 keV、
  z 0.0085–8.1），误差方向（上/下）与原表一致。
