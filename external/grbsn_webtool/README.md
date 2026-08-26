# grbsn_webtool — GRB-SN 关联多波段数据

来源：**GRBSN webtool** 的开源数据仓库（`SourceData/` 子树原样收录）。

- 上游仓库：https://github.com/GabrielF98/GRBSNWebtool
- 文献：Finneran & Martin-Carrillo 2025, "The GRBSN webtool: An open-source
  repository for gamma-ray burst-supernova associations"
  (arXiv:2411.08866, open access)

## 内容

`SourceData/<事件名>/` 下为每个 GRB-SN 关联事件的标准化多波段数据
（X 射线 / 光学 / 射电 txt 光变、Open SN Catalog 光谱 JSON），
每个事件的 `readme.md` / `readme.yml` 记录了逐文件的数据来源（ADS 链接）、
处理说明与数据契约。数据格式契约见 `SourceData/README.md`。

## 版权说明

本目录**不包含**上游仓库 `OriginalFormats/` 中的期刊网页 HTML 快照与论文
PDF（版权原因未随本仓库分发）；仅保留标准化后的数据文件与逐文件的来源
引用（见各事件 `readme.yml` 的 `sourceurl` 字段）。如需原始发表格式，
请按 `sourceurl` 指向的文献页面自行获取。

使用本目录数据时请引用上游文献（Finneran & Martin-Carrillo 2025）及
`readme.yml` 中列出的各原始文献。
