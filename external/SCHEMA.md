# 外部 GRB 目录解析输出契约（normalized.jsonl）

每个目录的解析器输出一个 `normalized.jsonl`（JSON Lines，每行一条记录），保存在
`catadata/external/<目录短名>/normalized.jsonl`。

## 顶层字段

| 字段 | 类型 | 说明 |
|---|---|---|
| `cat` | str | 目录短名（与目录名一致，如 `fermi_gbm`） |
| `name` | str\|null | 标准化暴名 `GRB yymmddX`（含空格、含字母后缀；无法确定则 null） |
| `name_alt` | [str] | 其他可用名（如触发编号 `"BATSE 7975"`、Fermi 小数名 `"GRB 080916.652"`） |
| `trigger_time` | str\|null | 触发时刻 ISO UTC（`2024-03-15T20:10:44Z`），用于按日期校验匹配 |
| `ra` / `dec` | float\|null | J2000 度 |
| `params` | obj | 规范化参数（见下），只放该目录实际有的量 |
| `other` | obj | 目录特有的重要原始列（原样保留，键名=原列名） |

## params 内字段（统一键名；每个量是一个对象）

- `t90`: `{"v":秒, "err":秒|null, "band":"50-300 keV"}` — 观测系；必须标注能段（目录未给能段就写 `null`）
- `t50`: 同 t90
- `epeak`: `{"v":keV, "err":[pos,neg]|单值|null, "model":"BAND|CPL|COMP|SBPL|PL|null", "frame":"obs"}` — 观测系
- `fluence`: `{"v":erg/cm², "err":..|null, "band":"10-1000 keV"}` — 观测系，必须标注能段
- `peak_flux`: `{"v":ph/cm²/s, "err":..|null, "band":"15-150 keV", "dt":"1s|64ms|256ms|1024ms"}` — 光子峰流量，标注时标与能段
- `eiso`: `{"v":erg, "err":..|null, "band":"1-10000 keV", "frame":"rest"}` — 静止系；注意 Fermi LAT 的 eiso 原始单位是 1e52 erg，解析时换算成 erg
- `redshift`: `{"v":float}` — 仅当该目录自带红移
- `spectral_index` / `alpha` / `beta`: `{"v":float, "err":..|null}` — 谱指数（观测系）
- `ep_rest`: `{"v":keV, "err":..|null, "frame":"rest"}` — 静止系峰值能量（Epi，文献发表值）
- `lp_iso`: `{"v":erg/s, "err":..|null, "band":"1-10000 keV", "frame":"rest"}` — 静止系峰值光度
- `tlag`: `{"v":s, "err":..|null, "band":"如 25-50/100-300 keV", "frame":"rest"|"obs"}` — 谱延迟，注明频道与参考系
- `variability`: `{"v":float, "err":..|null, "band":..|null}` — 变异性度量 V
- `e_gamma`: `{"v":erg, "err":..|null, "frame":"rest"}` — 喷流准直修正能量（Ghirlanda 关系用）
- `grb_type`: `{"v":"I"|"II"}` — I 型（短暴/并合）/ II 型（长暴/坍缩星）分类
- `spec_class`: `{"v":"Band"|"CPL"}` — 谱型分类（Liang+2023 等）
- 误差约定：对称误差用单值；不对称用 `[正,负]` 两元素数组；目录若是 90% 置信而非 1σ，在该量对象里加 `"cl": 90`

## 规则

1. 缺失值一律省略该键（不要写 null 占位），`err` 缺失才用 null。
2. 所有时间一律 UTC ISO（`...Z`）。
3. 数值一律转成 float；无法解析的（`N/A`、空串、`-99`、`-1.0e-07` 等缺失记号）视为缺失。
4. `name` 无法可靠确定时置 null 并尽量提供 `trigger_time` + `ra`/`dec`，由合并程序兜底。
5. 只读 `catadata/external/<目录短名>/` 下的原始文件；解析器脚本也保存在该目录（`parse.py`），可重跑。
