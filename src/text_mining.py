"""
Customer Support Text Mining
----------------------------
Reads a customer support text corpus, tokenizes and cleans it, computes token frequencies,
and saves results (CSV, Excel, TXT summary, and a PNG chart) into the project-level /output folder.

This version does NOT print token tables to IDLE/console.
Instead, it writes a run log (including Top 20 tokens) to:
  output/run_log.txt

Designed to run consistently from:
- IDLE (Run Module)
- Command Prompt / PowerShell
- GitHub / repo clones
- Colab (with minor path adjustments if needed)
"""

from __future__ import annotations

import re
import unicodedata
from collections import Counter
from datetime import datetime
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

import nltk
from nltk.corpus import stopwords


# ---------------------------
# Paths (ALWAYS project-root)
# ---------------------------

SCRIPT_DIR = Path(__file__).resolve().parent          # .../customer-support-text-mining/src
PROJECT_ROOT = SCRIPT_DIR.parent                      # .../customer-support-text-mining
DATA_DIR = PROJECT_ROOT / "data"
OUTPUT_DIR = PROJECT_ROOT / "output"

DEFAULT_INPUT_FILE = "customer_support_text_corpus.txt"


# ---------------------------
# Text processing helpers
# ---------------------------

def normalize_text(text: str) -> str:
    """
    Normalize Unicode and clean common oddities.
    - NFKC normalization makes visually-similar characters consistent.
    - Standardizes curly apostrophes/quotes to plain ones.
    """
    text = unicodedata.normalize("NFKC", text)
    text = text.replace("’", "'").replace("“", '"').replace("”", '"')
    return text


def tokenize(text: str) -> list[str]:
    """
    Tokenize into words with a regex.
    Keeps apostrophes inside words (e.g., don't, it's, can't).
    """
    return re.findall(r"[a-z0-9]+(?:'[a-z0-9]+)?", text.lower())


def ensure_nltk_stopwords() -> None:
    """Ensure NLTK stopwords are available; download once if missing."""
    try:
        _ = stopwords.words("english")
    except LookupError:
        nltk.download("stopwords")


def build_stopword_set() -> set[str]:
    """
    Build stopword set.
    Uses NLTK English stopwords plus extra "support corpus filler" words
    so top tokens are more topic-focused (devices, accounts, orders, etc.).
    """
    ensure_nltk_stopwords()
    sw = set(stopwords.words("english"))

    # Extra high-noise words common in support text (keeps results topic-focused)
    sw.update({
        "would", "like", "also", "still", "really", "just",
        "get", "got", "going", "go", "one", "can", "could",
        "im", "ive", "youre", "theyre", "weve",
        "dont", "doesnt", "didnt",
        "want", "need", "know", "back", "time",
        "thanks", "thank", "please"
    })

    return sw


def filter_tokens(tokens: list[str], sw: set[str], min_len: int = 4) -> list[str]:
    """Remove stopwords and short tokens."""
    return [t for t in tokens if len(t) >= min_len and t not in sw]


def count_tokens(tokens: list[str]) -> pd.DataFrame:
    """Count tokens and return a DataFrame sorted by frequency (desc)."""
    counts = Counter(tokens)
    df = pd.DataFrame(counts.items(), columns=["word", "total"])
    df = df.sort_values("total", ascending=False).reset_index(drop=True)
    return df


# ---------------------------
# Output helpers
# ---------------------------

def write_run_log(
    input_path: Path,
    freq_df: pd.DataFrame,
    threshold: int,
    output_dir: Path,
) -> Path:
    """
    Write a run log file to output/ including:
    - timestamp
    - input file path
    - token counts
    - top 20 tokens table
    - output file list
    """
    log_path = output_dir / "run_log.txt"

    top20 = freq_df.head(20)
    df_ge = freq_df[freq_df["total"] >= threshold]

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    lines: list[str] = []
    lines.append("Customer Support Text Mining - Run Log")
    lines.append("=" * 40)
    lines.append(f"Run timestamp: {now}")
    lines.append(f"Project root: {PROJECT_ROOT}")
    lines.append(f"Input file:    {input_path}")
    lines.append("")
    lines.append(f"Unique tokens (after filtering): {len(freq_df)}")
    lines.append(f"Tokens with total >= {threshold}: {len(df_ge)}")
    lines.append("")
    lines.append("Top 20 tokens:")
    lines.append(top20.to_string(index=False))
    lines.append("")
    lines.append("Generated outputs:")
    lines.append(f"- {output_dir / 'token_frequencies_all.csv'}")
    lines.append(f"- {output_dir / f'token_frequencies_ge_{threshold}.csv'}")
    lines.append(f"- {output_dir / 'text_mining_results.xlsx'}")
    lines.append(f"- {output_dir / 'summary_top20.txt'}")
    lines.append(f"- {output_dir / f'top_tokens_ge_{threshold}.png'}")
    lines.append(f"- {log_path}")

    log_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return log_path


def save_outputs(freq_df: pd.DataFrame, threshold: int = 250) -> None:
    """Save CSVs, Excel workbook, summary text, chart, and a run log to OUTPUT_DIR."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    df_all = freq_df.copy()
    df_ge = freq_df[freq_df["total"] >= threshold].copy()

    # Output paths
    csv_all_path = OUTPUT_DIR / "token_frequencies_all.csv"
    csv_ge_path = OUTPUT_DIR / f"token_frequencies_ge_{threshold}.csv"
    xlsx_path = OUTPUT_DIR / "text_mining_results.xlsx"
    txt_path = OUTPUT_DIR / "summary_top20.txt"
    png_path = OUTPUT_DIR / f"top_tokens_ge_{threshold}.png"

    # Save CSVs
    df_all.to_csv(csv_all_path, index=False, encoding="utf-8")
    df_ge.to_csv(csv_ge_path, index=False, encoding="utf-8")

    # Save Excel
    with pd.ExcelWriter(xlsx_path, engine="openpyxl") as writer:
        df_all.to_excel(writer, index=False, sheet_name="all_tokens")
        df_ge.to_excel(writer, index=False, sheet_name=f"tokens_ge_{threshold}")

    # Save Top-20 summary text (quick human-readable)
    top20 = df_all.head(20)
    summary_lines = [
        "Top 20 tokens:",
        top20.to_string(index=False),
        "",
        f"Tokens with total >= {threshold}: {len(df_ge)}",
        "",
    ]
    txt_path.write_text("\n".join(summary_lines), encoding="utf-8")

    # Save chart (bar chart for filtered set; plot top 50 for readability)
    plot_df = df_ge.head(50) if len(df_ge) > 50 else df_ge
    if len(plot_df) > 0:
        plt.figure(figsize=(14, 7))
        plt.bar(plot_df["word"], plot_df["total"])
        plt.xticks(rotation=60, ha="right")
        plt.xlabel("word")
        plt.ylabel("total")
        plt.title(f"Top tokens (frequency >= {threshold})")
        plt.tight_layout()
        plt.savefig(png_path, dpi=200, bbox_inches="tight")
        plt.close()
    else:
        # If nothing meets the threshold, create a note instead of an empty chart
        (OUTPUT_DIR / "chart_note.txt").write_text(
            f"No tokens met the threshold of {threshold}, so no chart was generated.\n",
            encoding="utf-8",
        )

    # Write a run log (instead of printing to IDLE)
    input_path = DATA_DIR / DEFAULT_INPUT_FILE
    write_run_log(input_path=input_path, freq_df=freq_df, threshold=threshold, output_dir=OUTPUT_DIR)


# ---------------------------
# Main
# ---------------------------

def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    input_path = DATA_DIR / DEFAULT_INPUT_FILE
    if not input_path.exists():
        raise FileNotFoundError(
            f"Input file not found: {input_path}\n"
            f"Make sure your corpus is located at: {DATA_DIR / DEFAULT_INPUT_FILE}\n"
            f"Current project root is: {PROJECT_ROOT}"
        )

    raw_text = input_path.read_text(encoding="utf-8", errors="replace")
    raw_text = normalize_text(raw_text)

    sw = build_stopword_set()
    tokens = tokenize(raw_text)
    tokens = filter_tokens(tokens, sw=sw, min_len=4)

    freq_df = count_tokens(tokens)

    save_outputs(freq_df, threshold=250)
    # No console/IDLE printing. See output/run_log.txt instead.


if __name__ == "__main__":
    main()
