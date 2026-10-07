"""Build the PRISMA flow figure, LaTeX count macros, and the search log table
from the team's literature matrix workbook.

Usage (from the project root):
    python3 scripts/build_prisma.py data/pocliteraturematrix.xlsx

Outputs:
    figures/prisma_flow.pdf and figures/prisma_flow.png
    generated/counts.tex     (\newcommand macros used in main.tex)
    generated/searchlog.tex  (Appendix A table)

The figure is drawn with the CoLRev prisma-flow-diagram package
(https://github.com/CoLRev-Environment/prisma-flow-diagram).
Rows whose screening arithmetic does not add up are reported on stdout.
"""

from __future__ import annotations

import csv
import sys
import types
from collections import OrderedDict
from pathlib import Path

import openpyxl

# The package imports colrev only for loading .bib records, which we do not use.
for name in ("colrev", "colrev.loader", "colrev.loader.load_utils"):
    sys.modules.setdefault(name, types.ModuleType(name))

from prisma_flow_diagram.prisma import Prisma2020Diagram, PrismaStyle  # noqa: E402

# Larger text than the package default so the figure stays legible at IEEE two column width.
STYLE = PrismaStyle(box_fontsize=12, char_width=0.075, per_line_height=0.27,
                    base_box_height=0.28, min_box_height=0.62, max_width=5.4, comfy_chars=20)

ROOT = Path(__file__).resolve().parents[1]
CITATION_SOURCES = {"backward citation search", "forward citation search"}


def num(value):
    """Return an int for numeric cells, otherwise None (for NA, '-', blanks)."""
    if isinstance(value, (int, float)):
        return int(value)
    if isinstance(value, str):
        digits = value.strip().split(" ")[0].replace(",", "")
        if digits.isdigit():
            return int(digits)
    return None


def canonical_source(name: str) -> str:
    fixed = {"acm digial library": "ACM Digital Library"}
    return fixed.get(name.strip().lower(), name.strip())


def load_rows(xlsx: Path):
    ws = openpyxl.load_workbook(xlsx, data_only=True)["Prisma Info"]
    rows = []
    for r in ws.iter_rows(min_row=2, values_only=True):
        if not r or not r[0]:
            continue
        rows.append(
            dict(
                source=canonical_source(str(r[0])),
                raw_source=str(r[0]).strip(),
                term=str(r[1]).strip() if r[1] else "",
                base=num(r[2]),
                f1=num(r[3]),
                f2=num(r[4]),
                abstracts=num(r[5]),
                abs_removed=num(r[6]),
                read=num(r[7]),
                read_removed=num(r[8]),
                included=num(r[9]),
            )
        )
    return rows


def load_meta(path: Path):
    meta = {}
    if path.exists():
        with path.open(newline="") as fh:
            for rec in csv.DictReader(fh):
                meta[(rec["database"].strip(), rec["search_term"].strip())] = rec
    return meta


def check(rows):
    problems = []
    for i, r in enumerate(rows, start=2):
        a, g, h, i_, j = (r["abstracts"], r["abs_removed"], r["read"],
                          r["read_removed"], r["included"])
        if None in (a, g, h, i_, j):
            problems.append(f"Sheet row {i} ({r['source']}): screening cells missing")
            continue
        if a - g != h:
            problems.append(f"Sheet row {i} ({r['source']}, '{r['term'][:40]}'): "
                            f"abstracts read {a} minus removed {g} = {a - g}, "
                            f"but papers read = {h}")
        if h - i_ != j:
            problems.append(f"Sheet row {i} ({r['source']}, '{r['term'][:40]}'): "
                            f"papers read {h} minus removed {i_} = {h - i_}, "
                            f"but included = {j}")
    return problems


def after_limits(r):
    for key in ("f2", "f1", "base"):
        if r[key] is not None:
            return r[key]
    return 0


class LabelledDiagram(Prisma2020Diagram):
    """Same layout as the package, with labels that describe our process."""

    def _main_right_text(self, lane):
        text = super()._main_right_text(lane)
        removed = lane["removed_before_screening"]
        records = lane["records"]
        text["ident"] = (
            "Records removed before screening:\n"
            f"Duplicate records (n = {removed['duplicates']})\n"
            "Removed by database limits\n"
            f"(year, type) (n = {removed['other']})"
        )
        text["screened"] = (
            "Records excluded at title\nor abstract screening\n"
            f"(n = {records['excluded']})"
        )
        return text

    def _other_left_text(self):
        text = super()._other_left_text()
        rec = self.other_methods.get("records", {})
        text["ident"] += f"\nExcluded on abstract (n = {rec.get('excluded', 0)})"
        return text


def main(xlsx: Path):
    rows = load_rows(xlsx)
    meta = load_meta(ROOT / "data" / "search_meta.csv")

    db_rows = [r for r in rows if r["source"].lower() not in CITATION_SOURCES]
    cit_rows = [r for r in rows if r["source"].lower() in CITATION_SOURCES]

    by_source = OrderedDict()
    for r in db_rows:
        by_source[r["source"]] = by_source.get(r["source"], 0) + (r["base"] or 0)

    identified = sum(by_source.values())
    screened = sum(after_limits(r) for r in db_rows)
    removed_limits = identified - screened
    duplicates = 0  # no cross source duplicates were logged

    abstracts = sum(r["abstracts"] or 0 for r in db_rows)
    abs_removed = sum(r["abs_removed"] or 0 for r in db_rows)
    assessed = abstracts - abs_removed            # derived so the flow adds up
    db_included = sum(r["included"] or 0 for r in db_rows)
    ft_excluded = assessed - db_included
    title_excluded = screened - abstracts

    cit_records = sum(r["abstracts"] or 0 for r in cit_rows)
    cit_abs_removed = sum(r["abs_removed"] or 0 for r in cit_rows)
    cit_assessed = cit_records - cit_abs_removed
    cit_included = sum(r["included"] or 0 for r in cit_rows)
    cit_ft_excluded = cit_assessed - cit_included

    total_included = db_included + cit_included

    db_registers = {
        "identification": {"databases": dict(by_source)},
        "removed_before_screening": {"duplicates": duplicates, "other": removed_limits},
        "records": {"screened": screened, "excluded": screened - assessed},
        "reports": {
            "sought": assessed,
            "not_retrieved": 0,
            "assessed": assessed,
            "excluded_reasons": {"Did not meet the inclusion\ncriteria (Appendix B)": ft_excluded},
        },
    }
    other_methods = {
        "identification": {"Citation searching": cit_records},
        "records": {"screened": cit_records, "excluded": cit_abs_removed},
        "reports": {
            "sought": cit_assessed,
            "not_retrieved": 0,
            "assessed": cit_assessed,
            "excluded_reasons": {"Did not meet the inclusion\ncriteria (Appendix B)": cit_ft_excluded},
        },
    }

    figdir = ROOT / "figures"
    figdir.mkdir(exist_ok=True)
    for ext in ("pdf", "png"):
        LabelledDiagram(
            db_registers=db_registers,
            included={"studies": total_included},
            other_methods=other_methods,
            style=STYLE,
        ).plot(filename=str(figdir / f"prisma_flow.{ext}"), figsize=(14, 9.2),
               validation="warn")

    gen = ROOT / "generated"
    gen.mkdir(exist_ok=True)
    macros = OrderedDict(
        nIdentified=identified, nRemovedLimits=removed_limits, nDuplicates=duplicates,
        nScreened=screened, nTitleExcluded=title_excluded, nAbstracts=abstracts,
        nAbstractExcluded=abs_removed, nAssessed=assessed, nFullTextExcluded=ft_excluded,
        nDbIncluded=db_included, nCitRecords=cit_records, nCitAssessed=cit_assessed,
        nCitExcluded=cit_ft_excluded, nCitIncluded=cit_included, nIncluded=total_included,
        nSearches=len(db_rows), nSources=len(by_source),
    )
    with (gen / "counts.tex").open("w") as fh:
        fh.write("% Generated by scripts/build_prisma.py. Do not edit by hand.\n")
        for k, v in macros.items():
            fh.write(f"\\newcommand{{\\{k}}}{{{v:,}}}\n")

    def tex(s: str) -> str:
        for a, b in (("\\", r"\textbackslash{}"), ("&", r"\&"), ("%", r"\%"),
                     ("_", r"\_"), ("#", r"\#"), ('"', "''")):
            s = s.replace(a, b)
        return s

    def cell(v):
        return "NA" if v is None else f"{v:,}"

    with (gen / "searchlog.tex").open("w") as fh:
        fh.write("% Generated by scripts/build_prisma.py. Do not edit by hand.\n")
        fh.write(
            "\\begin{table*}[!h]\n\\caption{Search Log}\n\\label{tab:log}\n\\centering\n\\scriptsize\n"
            "\\begin{tabularx}{\\textwidth}{@{}>{\\raggedright\\arraybackslash}p{1.9cm}>{\\raggedright\\arraybackslash}p{4.4cm}p{0.7cm}Yrrrrr@{}}\n\\toprule\n"
            "\\textbf{Source} & \\textbf{Exact query} & \\textbf{Date} & \\textbf{Limits} & "
            "\\textbf{Found} & \\textbf{Limited} & \\textbf{Abstr.} & "
            "\\textbf{Full} & \\textbf{Incl.} \\\\\n\\midrule\n"
        )
        for r in rows:
            m = meta.get((r["raw_source"], r["term"]), {})
            fh.write(
                f"{tex(r['source'])} & {tex(r['term'])} & {tex(m.get('date', 'TBC'))} & "
                f"{tex(m.get('limits', 'TBC'))} & {cell(r['base'])} & "
                f"{cell(after_limits(r) if r['source'].lower() not in CITATION_SOURCES else None)} & "
                f"{cell(r['abstracts'])} & {cell(r['read'])} & {cell(r['included'])} \\\\\n"
            )
        fh.write("\\bottomrule\n\\end{tabularx}\n\\end{table*}\n")

    print("PRISMA counts:")
    for k, v in macros.items():
        print(f"  {k:18s} {v}")
    problems = check(rows)
    if problems:
        print("\nRows to fix in the Prisma Info sheet:")
        for p in problems:
            print("  -", p)
    else:
        print("\nAll Prisma Info rows add up.")


if __name__ == "__main__":
    main(Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "data" / "pocliteraturematrix.xlsx")
