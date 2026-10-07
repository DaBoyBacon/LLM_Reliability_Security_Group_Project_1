# LLM_Reliability_Security_Group_Project_1

# Utilized Technologies

## Prisma workflow

https://github.com/CoLRev-Environment/prisma-flow-diagram

# Magron

found papers:
Prompt: RAG && Data poisoning and backdoors (ACM Digital Library)
Prompt: RAG & Data poisoning and backdoors (IEEE Xplore)
RQ: How resistant are RAG systems to data poisoning?
RQ: How effective are different data poisoning attempts at making RAG models more likely to hallucinate?

https://ieeexplore.ieee.org/document/11547227
https://dl.acm.org/doi/10.1145/3733799.3762976

# Divya

RQ1: When does the retrieval actually improve the correctness and factuality of the LLM responses?
RQ2: How can RAG systems avoid unnecessary retrieval while, maintaining answer quality?
RQ3: How does adding external retrieval introduce new attack surfaces for LLM systems?
RQ4: What happens to efficiency and reliability when we introduce security defenses into RAG?

# Bijaya

https://arxiv.org/pdf/2409.10102 (SUPER helpful for upwards/downwards searching)
https://arxiv.org/pdf/2502.06864
https://dl.acm.org/doi/pdf/10.1145/3769082
https://ieeexplore-ieee-org.ezproxy.lib.ou.edu/document/11405858

# Moving on from previous work

## What are our research questions

RQ1: When does the retrieval actually improve the correctness and factuality of the LLM responses?
RQ2: How can RAG systems avoid unnecessary retrieval while, maintaining answer quality?
RQ3: How does adding external retrieval introduce new attack surfaces for LLM systems?
RQ4: What happens to efficiency and reliability when we introduce security defenses into RAG?
RQ5: How resistant are RAG systems to data poisoning?

# More focused paper #Bijaya

RQ1: Does knowledge graph-guided retrieval improve retrieval relevance in RAG?
RQ2: Does RAG reduce hallucinations and remove unnecessary retrieval with Self Evaluation using Supervised Model?
RQ3: Can prediction-powered evaluation predict hallucination risk?
papers like Self-RAG, FactReasoner, GraphEval, are closer.

# Building the PRISMA figure and search log

The PRISMA flow figure, the counts quoted in Section II of the report, and the Appendix A search log are all generated from the **Prisma Info** sheet in `data/pocliteraturematrix.xlsx`. Nobody should type these numbers by hand. Update the sheet, run the script, and the figure and report stay consistent with the search log.

The figure is drawn with the CoLRev package: https://github.com/CoLRev-Environment/prisma-flow-diagram

## Project layout

```
main.tex                       IEEE report (upload to Overleaf)
refs.bib                       references for every included paper
data/pocliteraturematrix.xlsx  team workbook (Literature Matrix + Prisma Info)
data/search_meta.csv           date and limits for each search row
scripts/build_prisma.py        builds the figure, counts and search log
figures/prisma_flow.pdf/.png   generated PRISMA figure
generated/counts.tex           generated count macros used in main.tex
generated/searchlog.tex        generated Appendix A table
```

## One time setup (macOS or Linux)

Run these from the project folder:

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install prisma-flow-diagram openpyxl matplotlib typing_extensions
```

On Windows, activate with `.venv\Scripts\activate` instead.

## Running the script

Every time you open a new terminal:

```bash
source .venv/bin/activate
python3 scripts/build_prisma.py data/pocliteraturematrix.xlsx
```

## What it generates

| File                      | What it is                                           | Used in              |
| ------------------------- | ---------------------------------------------------- | -------------------- |
| `figures/prisma_flow.pdf` | PRISMA 2020 style flow figure                        | Fig. 1 in Section II |
| `figures/prisma_flow.png` | Same figure as an image, for quick viewing           | Preview only         |
| `generated/counts.tex`    | Count macros such as `\nIdentified` and `\nIncluded` | Text of Section II   |
| `generated/searchlog.tex` | Full search log table                                | Appendix A           |

The script also prints every count it used and a list of **rows to fix** for any Prisma Info row whose numbers do not add up.

## How each count is calculated

| Figure box                 | Source in the Prisma Info sheet                                                |
| -------------------------- | ------------------------------------------------------------------------------ |
| Records identified         | Sum of "Amount found (base)" for database rows                                 |
| Removed by database limits | Base minus the last filter count (filter 2, else filter 1, else base)          |
| Records screened           | Sum of the last filter counts                                                  |
| Reports assessed           | "Abstracts read" minus "Abstracts removed"                                     |
| Reports excluded           | Assessed minus included                                                        |
| Included                   | Sum of "Included in literature matrix"                                         |
| Citation lane              | Rows whose Database is "Backward citation search" or "Forward citation search" |

## Rules for the Prisma Info sheet

1. One row per search, with the exact query text in "Search term".
2. Count cells must be numbers only, or `NA` when they do not apply. Do not write text such as `2 (Paper A and Paper B)`.
3. Each row must add up: abstracts read minus abstracts removed equals papers read, and papers read minus papers removed equals included.
4. Count each paper once, under the search where it was first found.
5. Name citation searches exactly `Backward citation search` or `Forward citation search` so they go to the right lane.
6. Add the date and limits for your row to `data/search_meta.csv`, using exactly the same Database and Search term text as the sheet.

## After adding new papers

1. Add the paper row to the **Literature Matrix** sheet and the search row to **Prisma Info**.
2. Add the date and limits for the search to `data/search_meta.csv`.
3. Add a BibTeX entry for each new paper to `refs.bib`.
4. Run the script and fix any rows it reports.
5. In `main.tex`, update the composition sentence in Section II (marked `% UPDATE`) and the theme table (Table II).
6. Upload the updated `figures/`, `generated/`, `main.tex` and `refs.bib` to Overleaf and recompile. Overleaf cannot run Python, so always run the script locally first.
