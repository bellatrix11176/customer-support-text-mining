# Customer Support Text Mining

This project performs basic **text mining** on a customer support text corpus using Python.  
It turns raw text into measurable token frequencies, then saves clean outputs (CSV/Excel + a chart) for analysis and reporting.

## Project Structure

```
customer-support-text-mining/
├─ data/
│ └─ customer_support_text_corpus.txt
├─ src/
│ └─ text_mining.py
├─ output/ # created automatically when you run the script
├─ requirements.txt
└─ README.md
```

## What the Script Does

- Reads a text corpus from `data/customer_support_text_corpus.txt`
- Normalizes Unicode text for consistent counting
- Tokenizes text into words (tokens)
- Removes English stopwords
- Filters out short tokens
- Counts token frequency
- Saves results to CSV and Excel
- Saves a bar chart for high-frequency tokens

## Setup (Windows)

```bat
cd /d "C:\Users\gigih\OneDrive\School\Week5\Chapter10"
py -m venv .venv
.venv\Scripts\activate

pip install -r requirements.txt
py -c "import nltk; nltk.download('stopwords')"

py src\text_mining.py
```