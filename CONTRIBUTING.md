# 贡献指南（CONTRIBUTING）

> 本仓库欢迎任何人 / 任何外部 agent 校验、扩充、提交数据。
> English: Anyone — human or automated agent — may validate, extend, and submit data
> to this repository. The data contract is [SCHEMA.md](SCHEMA.md); validate with
> `python3 tools/validate.py` (stdlib-only) and submit via pull request.

## 1. 四种工作方式（审核 / 校验 / 扩充 / 提交）

### 1.1 审核（audit）——外部贡献推荐入口

当前最有价值的贡献形式。库中已有数据一律视为「未核实」，逐源复核、把源从「未核实」变成「已核实」是项目最核心的工作。

把 [`数据审核提示词.md`](数据审核提示词.md) 里的「提示词本体」整段发给你的 agent（Claude Code / Cursor / ZCode 等），它会先与你确认**审核人姓名**与**本批源列表**，然后按约定完成单源复核：

身份核验 → T0 口径统一 → 逐行溯源核对与补充 → 去重 → 元数据与 `extra_data.audit` 标记 → `tools/validate.py` → **独立子代理真实性核查** → 单源 Pull Request。

要点：一源一 PR；数值必须本次从来源原文实际核对得出，严禁臆造/内插/估算；派生列（`Gext_*`）一律留空；拿不准就停下来问。契约（`SCHEMA.md` 与本文件）效力高于该提示词。

### 1.2 校验（validate）

```bash
git clone https://github.com/Cooper-J2000/AJST-Data.git
cd AJST-Data
python3 tools/validate.py
```

零第三方依赖，任意 Python 3 环境可跑。发现错误请提 Issue 或直接 PR 修复。
`--strict` 模式把值域警告（如非法 `y/n` 取值）也算失败。

### 1.3 扩充（extend）

新增一个暂现源 = 新增一对文件：

1. `info/<id>.json`：按 [SCHEMA.md](SCHEMA.md) §2 的字段契约。**全部规范键都要写**，
   无值的写 `null`（列表写 `[]`）；`<id>` 只允许字母数字，且与 `transient_id` 一致。
2. `lc/<id>.csv`（可选）：按 SCHEMA.md §3 的 24 列契约，表头顺序固定。
3. 数据必须可溯源：`articles` 填文献（`name`/`url`），光变行 `reference` 列填出处。
   抓取/整理自其它目录时在 `extra_data` 注明来源（如 `{"src": "..."}`）。
4. 提交前本地跑 `tools/validate.py`，必须 0 错误。

修改已有条目同理：直接改对应文件，保证改完仍过校验。

### 1.4 提交（submit）

1. Fork 本仓库，在分支上提交，发起 Pull Request。
2. Commit 信息格式：`data: <中文或英文简述>`，例如
   `data: 新增 SN2024xyz 光变（来源 Li+2024）`。
3. PR 描述里写清：**数据来源**（文献/目录/通告）、**涉及源列表**、**校验结果**
   （`tools/validate.py` 输出末尾一行）。
4. CI（GitHub Actions）会自动重跑校验；红了请修好再请求 review。

## 2. 不要提交的内容

- `gcn/archive/`（GCN 存档，体积大且可再生成，见 README 接入方法）
- `backups/`、任何数据库 dump
- 未获授权的私有/内审数据；仅提交**已公开发表或公开通告**的数据
- 大体积二进制（光谱请用统一 JSON 文本格式放 `spectra/<id>/`）

## 3. 数据质量与引用

- 本库数据批量汇集自已发表文献与公开通告，质量审核仍在进行（见 README 免责声明）。
  贡献者对自己提交数据的准确性负责；拿不准的字段留 `null`，并在 `comment` 说明。
- 使用本库数据请遵循 CC BY 4.0（署名）；`external/` 子目录数据还需引用各自原始文献。
