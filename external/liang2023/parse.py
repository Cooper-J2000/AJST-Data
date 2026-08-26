#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
liang2023 解析器：Liang et al. 2023 (ApJS 266, 31; arXiv:2211.12187)
LaTeX 源 (arxiv_src/ms.tex) -> normalized.jsonl

153 个带红移的 Fermi-GBM GRB。逐暴数据来自 4 张 deluxetable：
  表1 tab:global     样本基本性质（GRB、z、T90、T90/(1+z)、S_gamma、探测器、
                     背景区间、时间积分谱优选模型、暴分类 Short/S/M）
  表2 tab:Integrated 时间积分谱拟合（COMP=CPL 与 Band 两模型并列；含
                     E_p/E_c、alpha、beta、E_p^rest、E_gamma,iso）
  表3 tab:1sPeak     1-s 峰谱拟合（同上，含 L_p,iso）
  表4 tab:hybrid     需附加黑体分量的暴（Band+BB / CPL+BB 混合拟合）
表5-7 为汇总统计（无逐暴数据），不解析。

按 GRB 合并为一条 normalized 记录（输出契约见 ../SCHEMA.md）：
  params.epeak/ep_rest/eiso/alpha/beta 取表1"优选模型"对应的表2列
  （Band/Band+BB -> Band 列；CPL/CPL+BB -> COMP 列），
  params.lp_iso 取表3对应列；Unconstrained 暴不写 epeak/spec_class。
  表4 混合拟合的关键单元格原样存入 other（键名带 T4 前缀）。
"""
import os
import re
import json
from datetime import datetime, timedelta

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "arxiv_src", "ms.tex")
OUT = os.path.join(HERE, "normalized.jsonl")

# Ep 明显超物理范围的值视为论文排版错误（如 141220252 行 Band 列
# "154150$^{+1}_{-1}$"），移入 other 保留原文
EP_SANITY_KEV = 5e4


def rnd(x):
    """乘 10^n 因子带来的浮点尾数噪声（如 8.4999...e-07）修约到 6 位有效数字。"""
    return float("%.6g" % x)


def parse_val(s):
    """解析 LaTeX 数值单元格 -> (v, err)；err 为 None / 单值 / [pos, neg]。
    支持: 0.1218 ; 0.960$\\pm$0.345 ; 124$^{+24}_{-21}$ ;
          (8.5$^{+0.1}_{-0.1}$)$\\times$10$^{52}$ ; 10$^{+33}_{5}$（下误差漏负号）
    \\nodata / 上限 $<$x -> None。"""
    s = s.strip()
    if not s or "\\nodata" in s:
        return None
    if re.match(r"^\$?<\$?", s):
        return None  # 上限，按缺失处理
    fac = 1.0
    m = re.search(r"\\times\$?\s*10\$\^\{(-?\d+)\}\$", s)
    if m:
        fac = 10.0 ** int(m.group(1))
        s = s[:m.start()] + s[m.end():]
    t = (s.replace("$", "").replace("(", "").replace(")", "")
          .replace("\\rm", "").replace("\\ ", "").strip())
    m = re.match(r"^(-?[\d.]+)\\pm(-?[\d.]+)$", t)
    if m:
        return rnd(float(m.group(1)) * fac), rnd(float(m.group(2)) * fac)
    m = re.match(r"^(-?[\d.]+)\^\{\+?(-?[\d.]+)\}_\{[+-]?([\d.]+)\}$", t)
    if m:
        v = rnd(float(m.group(1)) * fac)
        return v, [rnd(abs(float(m.group(2))) * fac),
                   rnd(abs(float(m.group(3))) * fac)]
    try:
        return rnd(float(t) * fac), None
    except ValueError:
        return None


def clean_cell(s):
    """单元格原样保留用的轻清理：去 $、压缩空白。"""
    return re.sub(r"\s+", " ", s.replace("$", "")).strip()


def iter_tables(tex):
    """产出 (caption, data_segment) 遍历所有含 \\startdata 的 deluxetable。"""
    for m in re.finditer(
            r"\\begin\{deluxetable\*?\}.*?\\end\{deluxetable\*?\}", tex, re.S):
        block = m.group(0)
        cm = re.search(r"\\tablecaption\{(.*?)\}", block, re.S)
        dm = re.search(r"\\startdata(.*?)\\enddata", block, re.S)
        if cm and dm:
            yield cm.group(1), dm.group(1)


def iter_chunks(data):
    """按 \\\\ 切块，剥掉 \\multicolumn 节标题与 \\hline 前缀；
    产出 (section_title_or_None, 剩余行文本)。节标题与其后首个数据行
    常落在同一 \\\\ 分块内，需先提取标题再剥除。"""
    for raw in re.split(r"\\\\", data):
        raw = raw.strip()
        if not raw:
            continue
        sec = None
        m = re.search(r"\\multicolumn\{\d+\}\{.\}\{(.*?)\}\\tabularnewline",
                      raw, re.S)
        if m:
            sec = m.group(1).strip()
        raw = re.sub(r"^.*\\tabularnewline", "", raw, flags=re.S)
        raw = re.sub(r"\\hline|\\noalign\{[^}]*\}", "", raw).strip()
        yield sec, raw


def iter_rows(data):
    """数据段 -> 单元格列表（节标题行剔除）。"""
    for sec, raw in iter_chunks(data):
        if raw and "&" in raw:
            yield [c.strip() for c in raw.split("&")]


NAME_RE = re.compile(r"^(\d{6})([A-Z]*)\((\d{3})\)$")


def iso_from_trigger(yymmdd, nnn):
    """GBM 触发号小数部分 NNN = 当日千分比 -> ISO UTC。"""
    dt = datetime.strptime(yymmdd, "%y%m%d") + timedelta(
        seconds=round(int(nnn) / 1000.0 * 86400))
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")


def main():
    tex = open(SRC, encoding="utf-8").read()
    tables = {}
    for caption, data in iter_tables(tex):
        if caption.startswith("Global Properties"):
            tables["t1"] = list(iter_rows(data))
        elif caption.startswith("Time-integrated Spectral Fit Results for those"):
            tables["t4"] = data  # 含两节标题，后面用 iter_chunks 解析
        elif caption.startswith("Time-integrated Spectral Fit Results"):
            tables["t2"] = list(iter_rows(data))
        elif caption.startswith("(1-s Peak)"):
            tables["t3"] = list(iter_rows(data))
    assert len(tables) == 4, tables.keys()

    # ---------- 表1：主样本 ----------
    records = {}   # key = yymmdd+NNN
    order = []
    for cells in tables["t1"]:
        if len(cells) != 9:
            print("WARN t1 bad row:", cells[:2])
            continue
        m = NAME_RE.match(cells[0])
        if not m:
            print("WARN t1 bad name:", cells[0])
            continue
        yymmdd, letters, nnn = m.groups()
        if letters.endswith("S"):  # 如 101224AS：末尾 S 为 Short 标记
            letters = letters[:-1]
        key = yymmdd + nnn
        zr = parse_val(cells[1])
        t90 = parse_val(cells[2])
        flu = parse_val(cells[4])
        spec = clean_cell(cells[7])      # Band/CPL/Unconstrained/Band+BB/CPL+BB
        klass = clean_cell(cells[8])     # Short/S/M

        params = {"redshift": {"v": float(zr[0])}} if zr else {}
        if cells[1].strip().startswith("$<$"):
            pass  # 上限红移只入 other
        if t90:
            params["t90"] = {"v": float(t90[0]), "err": t90[1],
                             "band": "50-300 keV"}
        if flu:
            params["fluence"] = {"v": float(flu[0]), "err": flu[1],
                                 "band": "8 keV-40 MeV"}
        if spec.startswith("Band"):
            params["spec_class"] = {"v": "Band"}
        elif spec.startswith("CPL"):
            params["spec_class"] = {"v": "CPL"}
        params["grb_type"] = {"v": "I" if klass == "Short" else "II"}

        other = {
            "Detectors": clean_cell(cells[5]),
            "Background intervals": clean_cell(cells[6]),
            "Averaged Spectrum": spec,
            "Classified": klass,
            "T90/(1+z) (s)": clean_cell(cells[3]),
        }
        if not zr:
            other["z_raw"] = clean_cell(cells[1])  # 如 $<$2.2

        records[key] = {
            "cat": "liang2023",
            "name": "GRB " + yymmdd + letters,
            "name_alt": ["GRB %s.%s" % (yymmdd, nnn), "bn" + yymmdd + nnn],
            "trigger_time": iso_from_trigger(yymmdd, nnn),
            "ra": None,
            "dec": None,
            "params": params,
            "other": other,
            "_spec": spec,  # 内部用：优选模型
        }
        order.append(key)

    # ---------- 表2/表3：谱拟合 ----------
    # 列布局见模块 docstring；idx = (K, alpha, Ep/Ec, beta, lik, 导出量)
    def merge_spec(rows, ncol, cpl_cols, band_cols, derived, label):
        """derived: 'eiso'(表2) 或 'lp_iso'(表3)。"""
        n = 0
        for cells in rows:
            if len(cells) != ncol:
                print("WARN %s bad row:" % label, cells[:2])
                continue
            key = cells[0].strip()
            rec = records.get(key)
            if rec is None:
                print("WARN %s id not in t1:" % label, key)
                continue
            spec = rec["_spec"]
            if spec.startswith("Band"):
                cols, model = band_cols, "BAND"
            elif spec.startswith("CPL"):
                cols, model = cpl_cols, "CPL"
            else:
                continue  # Unconstrained：表2/3 中一般也没有该行
            c_k, c_a, c_e, c_b, c_d = cols
            p = rec["params"]
            ep = parse_val(cells[c_e])
            if ep and ep[0] > EP_SANITY_KEV:
                rec["other"]["%s Ep_raw (paper typo?)" % label] = \
                    clean_cell(cells[c_e])
                ep = None
            if label == "t2":
                if ep:
                    p["epeak"] = {"v": float(ep[0]), "err": ep[1],
                                  "model": model, "frame": "obs"}
                if model == "CPL":
                    epz = parse_val(cells[c_d])
                    if epz and epz[0] > EP_SANITY_KEV:
                        rec["other"]["t2 Ep_rest_raw (paper typo?)"] = \
                            clean_cell(cells[c_d])
                        epz = None
                else:
                    # 表2 Band 列的 E_p^rest 印刷值与观测系 E_p 完全相同
                    # （全列未乘 1+z，系论文排版错误，CPL 列已验证为
                    # (2+alpha)*Ec*(1+z)），故 Band 暴用 (1+z)*E_p 自行换算
                    epz = None
                    z = p.get("redshift", {}).get("v")
                    if ep and z is not None:
                        e = ep[1]
                        if isinstance(e, list):
                            e = [rnd(e[0] * (1 + z)), rnd(e[1] * (1 + z))]
                        elif e is not None:
                            e = rnd(e * (1 + z))
                        epz = (rnd(ep[0] * (1 + z)), e)
                if epz:
                    p["ep_rest"] = {"v": float(epz[0]), "err": epz[1],
                                    "frame": "rest"}
                eiso = parse_val(cells[8 if cols is cpl_cols else 15])
                if eiso:
                    p["eiso"] = {"v": float(eiso[0]), "err": eiso[1],
                                 "band": "1-10000 keV", "frame": "rest"}
            else:  # t3
                lp = parse_val(cells[c_d])
                if lp:
                    p["lp_iso"] = {"v": float(lp[0]), "err": lp[1],
                                   "band": "1-10000 keV", "frame": "rest"}
                if ep:
                    rec["other"]["T3 1-s peak Ep or Ec (keV)"] = \
                        clean_cell(cells[c_e])
            # alpha/beta 以时间积分谱（表2）为准；表3 仅对表2 缺失的暴
            # （090902B、160625B、190114C、201216C）补 1-s 峰值
            al = parse_val(cells[c_a])
            if al and "alpha" not in p:
                p["alpha"] = {"v": float(al[0]), "err": al[1]}
                if label == "t3":
                    rec["other"]["alpha_source"] = "1-s peak (no T2 row)"
            if model == "BAND":
                be = parse_val(cells[c_b])
                if be and "beta" not in p:
                    p["beta"] = {"v": float(be[0]), "err": be[1]}
            n += 1
        return n

    # 表2: 0 ID,1 区间,2 S; CPL: 3 K,4 a,5 Ec,6 lik,7 Ep_rest,8 Eiso;
    #      Band: 9 K,10 a,11 Ep,12 beta,13 lik,14 Ep_rest,15 Eiso; 16 dAIC
    n2 = merge_spec(tables["t2"], 17, (3, 4, 5, None, 7), (9, 10, 11, 12, 14),
                    "eiso", "t2")
    # 表3: 0 ID,1 区间,2 S; CPL: 3 K,4 a,5 Ec,6 lik,7 Lp;
    #      Band: 8 K,9 a,10 Ep,11 beta,12 lik,13 Lp; 14 dAIC
    n3 = merge_spec(tables["t3"], 15, (3, 4, 5, None, 7), (8, 9, 10, 11, 13),
                    "lp_iso", "t3")

    # ---------- 表4：Band+BB / CPL+BB 混合拟合，原样存 other ----------
    section = None
    n4 = 0
    for sec, raw in iter_chunks(tables["t4"]):
        if sec:
            if "Time-intergrated" in sec:
                section = "int"
            elif "1-s peak" in sec:
                section = "peak"
        if not raw or "&" not in raw:
            continue
        cells = [c.strip() for c in raw.split("&")]
        if len(cells) != 14 or not re.match(r"^\d{9}$", cells[0]):
            if cells != [""]:
                print("WARN t4 bad row:", cells[:2])
            continue
        rec = records.get(cells[0])
        if rec is None:
            print("WARN t4 id not in t1:", cells[0])
            continue
        pre = "T4 %s" % section
        rec["other"][pre + " model"] = clean_cell(cells[3])
        rec["other"][pre + " Ep or Ec (keV)"] = clean_cell(cells[6])
        if "\\nodata" not in cells[7]:
            rec["other"][pre + " beta"] = clean_cell(cells[7])
        rec["other"][pre + " kT (keV)"] = clean_cell(cells[9])
        n4 += 1

    # ---------- 输出 ----------
    with open(OUT, "w", encoding="utf-8") as f:
        for key in order:
            rec = records[key]
            del rec["_spec"]
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")

    recs = list(records.values())
    cov = lambda k: sum(1 for r in recs if k in r["params"])
    print("records:", len(recs), "(t1 rows)")
    print("t2 merged:", n2, " t3 merged:", n3, " t4 rows:", n4)
    for k in ["t90", "redshift", "fluence", "spec_class", "grb_type",
              "epeak", "ep_rest", "eiso", "alpha", "beta", "lp_iso"]:
        print("params.%-10s %d" % (k, cov(k)))
    print("name:", sum(1 for r in recs if r["name"]), "/",
          len(recs), " trigger_time:",
          sum(1 for r in recs if r["trigger_time"]), " ra/dec:",
          sum(1 for r in recs if r["ra"] is not None))
    print("z upper-limit (no params.redshift):",
          [r["name"] for r in recs if "redshift" not in r["params"]])
    print("sanity-filtered Ep:",
          [r["name"] for r in recs
           if any("typo" in k for k in r["other"])])


if __name__ == "__main__":
    main()
