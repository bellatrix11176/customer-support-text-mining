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
Setup (Windows)

cd /d "PATH\TO\customer-support-text-mining"

pip install -r requirements.txt
py -c "import nltk; nltk.download('stopwords')"

py src\text_mining.py
```

MIT License

Copyright (c) 2026 Gina Aulabaugh

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

🌐 **PixelKraze Analytics (Portfolio):** https://pixelkraze.com/?utm_source=github&utm_medium=readme&utm_campaign=portfolio&utm_content=homepage


