# HanuAI ML Assessment — Task 1 and Task 2

This submission package includes the Task 1 review sentiment/aspect pipeline and Task 2 EDA/text-mining project.

## Task 1 files
- `Task1_Scraping_Sentiment/Task1_Report.docx`
- `Task1_Scraping_Sentiment/Task1_Scraping_Sentiment.ipynb`
- `Task1_Scraping_Sentiment/scrape_and_analyse.py`
- `Task1_Scraping_Sentiment/bestbuy_reviews_50.csv`
- `Task1_Scraping_Sentiment/task1_reviews_with_sentiment.csv`
- `Task1_Scraping_Sentiment/requirements.txt`

Task 1 processes 50 selected records from the supplied Datafiniti dataset. The records are for **Microsoft Surface Pro 4 Type Cover with Fingerprint ID**; the source URL metadata includes Best Buy review URLs. These records were not live-scraped in this project build, and they are not for the original DJI Avata 2 product. If the assessment requires 50 reviews from that exact product or requires live scraping, that requirement remains unfulfilled and should not be represented as completed.

To reproduce Task 1 (from the Task 1 folder):
```bash
pip install -r requirements.txt
python scrape_and_analyse.py --input bestbuy_reviews_50.csv --min-reviews 50 --output task1_reviews_with_sentiment.csv
```

## Task 2
Task 2 EDA/text-mining notebook, dataset, outputs, charts, and stakeholder report are included in `Task2_EDA_TextMining/`. See the root `VERIFICATION.md` for verification notes and limitations.

## Important
Check the assessment instructions before submitting. Do not describe the Task 1 dataset as live-scraped or as DJI Avata 2 reviews.
