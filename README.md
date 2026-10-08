# BestBuy.ca Review Scraper + Sentiment Analysis

Scrapes **publicly visible** product reviews from bestbuy.ca (Selenium + BeautifulSoup), cycles through the
review filters (Most Helpful, Newest, Highest Rating, Lowest Rating, Most Relevant), clicks "Show more" until all
reviews load, then runs sentiment analysis (overall + per-aspect) and produces a CSV/Excel file and a Word report.

## Project layout
```
bestbuy_reviews_scraper_sentiment.ipynb   <- main notebook (scraping + sentiment, commented)
build_report.py                           <- builds the Word report from the notebook's CSV
requirements.txt
sample_data/                              <- SYNTHETIC demo data (offline testing only)
data/                                     <- real outputs land here (CSV, XLSX, charts)
data/demo/                                <- outputs from a demo run (synthetic - never submit these)
debug/                                    <- page HTML saved here if no reviews were parsed
```

## Run it (about 5 minutes)
1. Install Python 3.10+ and Google Chrome.
2. `python -m venv .venv` then activate it (`source .venv/bin/activate`, or `.venv\Scripts\activate` on Windows)
3. `pip install -r requirements.txt`
4. `jupyter notebook` -> open the notebook -> edit `PRODUCT_URL` in the config cell (any product with 50+ reviews)
5. First run: set `HEADLESS = False` so you can watch the browser. Then **Restart & Run All**.
6. Outputs: `data/bestbuy_reviews_sentiment.csv` and `.xlsx`, plus charts.
7. `python build_report.py` -> `Report_BestBuy_Review_Analysis.docx`

Test without the website: set `USE_SAMPLE_DATA = True` (synthetic data, writes to `data/demo/`).

## If it collects 0 reviews (or far fewer than expected)
BestBuy can change its page at any time. The notebook saves the page HTML to `debug/page_*.html`.
1. Re-run with `HEADLESS = False` and watch: is the reviews section showing? Is a CAPTCHA appearing?
2. Open `debug/page_*.html` and search for a review's text. If it is there, the parser needs a tweak (send me the file).
3. If the log says the sort control wasn't found, it still runs using the page's default order.

## Anti-blocking notes
Delays are randomised, one browser session at a time, and the scraper **stops** on a CAPTCHA / access-denied page
(it does not try to bypass it). For larger jobs: rotating residential proxies, lower rate, or a licensed data feed.
Check bestbuy.ca's Terms of Use and robots.txt before running at scale.

## Methodology (short)
- **Parser**: anchors on each review's date, finds the enclosing card, then reads rating/title/text/name by content.
- **Sentiment**: VADER compound score (>= 0.05 Positive, <= -0.05 Negative). Aspect labels come from keyword matching
  per sentence, e.g. `['Design (Pos)', 'Value for Money (Neg)']`.
- Reviews where star rating and text disagree are flagged in `Rating_vs_Text_Flag`.
