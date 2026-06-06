# 🇳🇵 Nepal Government Budget Analyzer 2083/84

A civic tech web app that makes Nepal's federal budget accessible to ordinary citizens. Ask questions in plain English, explore sector-wise allocations, and visualize where public money goes.

**Live data from:** Nepal Ministry of Finance — Budget Speech 2083/84 (FY 2026/27)

---

## What It Does

Nepal's federal budget is public but buried in 93-page Nepali PDF documents. This app:
- Parses the budget speech PDF using an LLM pipeline (Groq Llama 3.3)
- Extracts and structures budget allocations by sector
- Lets citizens ask questions like *"how much for education?"* or *"health budget?"*
- Shows verified amounts with breakdowns and charts

---

## Features

**Tab 1 — Ask the Budget**
Type any question in plain English. The app maps keywords to sectors and returns the official allocation with a breakdown chart.
> Example: "how much for education" → Rs. 21,830 crore allocated to Education sector

**Tab 2 — Sector Explorer**
Select any sector from a dropdown. See the official sector total, percentage of captured budget, and all named sub-allocations with amounts.

**Tab 3 — Budget Overview**
Full pie chart and bar chart of all sectors. Complete sector summary table sorted by allocation size.

---

## Data Coverage

| Metric | Value |
|--------|-------|
| Sectors captured | 17 |
| Total entries | 86 |
| Budget captured | Rs. 1,10,403 crore |
| Actual total budget | Rs. 2,12,434 crore |
| Coverage | ~52% |

The remaining ~48% covers staff salaries, debt service, and general administration — figures not stated in the budget speech text.

---

## Sector Totals (Verified)

| Sector | Allocation (Crore NPR) | Source |
|--------|----------------------|--------|
| Roads & Urban | 28,648 | Para 41 |
| Education | 21,830 | Para 47 |
| Social Security | 12,000 | Para 49 |
| Health | 10,195 | Para 48 |
| Security | 9,196 | Annex 3 |
| Energy | 8,554 | Para 43 |
| Defense | 6,496 | Annex 4 |
| Agriculture | 4,692 | Para 50 |
| Water | 3,717 | Para 42 |
| Forest | 1,231 | Para 51 |
| Industry | 831 | Para 56 |
| Culture & Tourism | 734 | Para 52-53 |
| ICT | 593 | Para 45 |
| Sports | 403 | Para 46 |
| Science & Tech | 400 | Para 57 |
| Labor | 363 | Para 54 |
| Aviation | 293 | Para 53 |
| Women & Children | 227 | Para 49 |

All figures verified against the official Nepali PDF text.

---

## How Search Works

- Keyword matching maps query words to sectors
- Returns the official sector total as the answer
- Shows named sub-allocations as breakdown (not additive)
- Does not search specific staff salaries or line items not named in speech

---

## Tech Stack

| Component | Technology |
|-----------|-----------|
| PDF parsing | pdfplumber |
| Data extraction | Groq API (Llama 3.3 70B) |
| Data processing | pandas |
| Web app | Streamlit |
| Charts | Plotly |
| Data pipeline | Python + JSON caching |
# 🇳🇵 Nepal Government Budget Analyzer 2083/84

A civic tech web app that makes Nepal's federal budget accessible to ordinary citizens. Ask questions in plain English, explore sector-wise allocations, and visualize where public money goes.

**Live data from:** Nepal Ministry of Finance — Budget Speech 2083/84 (FY 2026/27)

---

## What It Does

Nepal's federal budget is public but buried in 93-page Nepali PDF documents. This app:
- Parses the budget speech PDF using an LLM pipeline (Groq Llama 3.3)
- Extracts and structures budget allocations by sector
- Lets citizens ask questions like *"how much for education?"* or *"health budget?"*
- Shows verified amounts with breakdowns and charts

---

## Features

**Tab 1 — Ask the Budget**
Type any question in plain English. The app maps keywords to sectors and returns the official allocation with a breakdown chart.
> Example: "how much for education" → Rs. 21,830 crore allocated to Education sector

**Tab 2 — Sector Explorer**
Select any sector from a dropdown. See the official sector total, percentage of captured budget, and all named sub-allocations with amounts.

**Tab 3 — Budget Overview**
Full pie chart and bar chart of all sectors. Complete sector summary table sorted by allocation size.

---

## Data Coverage

| Metric | Value |
|--------|-------|
| Sectors captured | 17 |
| Total entries | 86 |
| Budget captured | Rs. 1,10,403 crore |
| Actual total budget | Rs. 2,12,434 crore |
| Coverage | ~52% |

The remaining ~48% covers staff salaries, debt service, and general administration — figures not stated in the budget speech text.

---

## Sector Totals (Verified)

| Sector | Allocation (Crore NPR) | Source |
|--------|----------------------|--------|
| Roads & Urban | 28,648 | Para 41 |
| Education | 21,830 | Para 47 |
| Social Security | 12,000 | Para 49 |
| Health | 10,195 | Para 48 |
| Security | 9,196 | Annex 3 |
| Energy | 8,554 | Para 43 |
| Defense | 6,496 | Annex 4 |
| Agriculture | 4,692 | Para 50 |
| Water | 3,717 | Para 42 |
| Forest | 1,231 | Para 51 |
| Industry | 831 | Para 56 |
| Culture & Tourism | 734 | Para 52-53 |
| ICT | 593 | Para 45 |
| Sports | 403 | Para 46 |
| Science & Tech | 400 | Para 57 |
| Labor | 363 | Para 54 |
| Aviation | 293 | Para 53 |
| Women & Children | 227 | Para 49 |

All figures verified against the official Nepali PDF text.

---

## How Search Works

- Keyword matching maps query words to sectors
- Returns the official sector total as the answer
- Shows named sub-allocations as breakdown (not additive)
- Does not search specific staff salaries or line items not named in speech

---

## Tech Stack

| Component | Technology |
|-----------|-----------|
| PDF parsing | pdfplumber |
| Data extraction | Groq API (Llama 3.3 70B) |
| Data processing | pandas |
| Web app | Streamlit |
| Charts | Plotly |
| Data pipeline | Python + JSON caching |

---

## Project Structure
app.py                    ← Streamlit web app (3 tabs)
build_dataset.py          ← Verified budget dataset builder
Nepal_Budget_Parser.ipynb ← PDF extraction notebook
nepal_budget_clean.csv    ← Structured budget data (86 rows)
sector_list.json          ← All sector names
budget_raw_text.txt       ← Raw extracted PDF text

---

## Known Limitations

- Search returns sector total, not specific line items
- ~48% of budget (salaries, debt) not captured
- Irrigation has no official sector total in speech
- Percentages shown are % of captured budget, not total budget

---

## Data Source

Nepal Ministry of Finance  
Budget Speech 2083/84 — presented by Finance Minister Dr. Swarnim Wagle  
[mof.gov.np](https://www.mof.gov.np)
