"""
Task 1: Review Sentiment and Aspect Analysis
Processes an approved/provided CSV of review records. This script does NOT live-scrape BestBuy.
The supplied 50-row file contains records from Datafiniti whose review source URLs include Best Buy URLs.
The records are for Microsoft Surface Pro 4 Type Cover, not the original DJI Avata 2 target.
"""
import argparse
import hashlib
import os
import pandas as pd
from textblob import TextBlob

ASPECT_KEYWORDS = {
    "Battery": ["battery", "charge", "charging", "flight time"],
    "Performance": ["performance", "fast", "speed", "lag", "works", "work"],
    "Design": ["design", "look", "build", "size", "weight", "light", "thin"],
    "Price": ["price", "expensive", "cheap", "value", "cost"],
    "Quality": ["quality", "durable", "broken", "defect", "reliable", "solid", "sturdy"],
    "Customer Support": ["support", "service", "refund", "replacement"],
    "Delivery": ["delivery", "shipping", "package", "arrived"],
    "Camera": ["camera", "video", "image", "photo", "resolution"],
    "App & Connectivity": ["app", "connection", "connectivity", "bluetooth", "wifi", "fingerprint", "recognition"],
}

def tag_aspects(text):
    text = str(text).lower()
    found = [
        aspect for aspect, keywords in ASPECT_KEYWORDS.items()
        if any(keyword in text for keyword in keywords)
    ]
    return ", ".join(found) if found else "Other"

def classify_sentiment(text):
    score = float(TextBlob(str(text)).sentiment.polarity)
    if score >= 0.05:
        label = "Positive"
    elif score <= -0.05:
        label = "Negative"
    else:
        label = "Neutral"
    return label, score

def main():
    parser = argparse.ArgumentParser(description="Analyze review CSV data with TextBlob and keyword aspect tagging.")
    parser.add_argument("--input", default="bestbuy_reviews_50.csv", help="Input CSV with Review and Rating columns")
    parser.add_argument("--output", default="task1_reviews_with_sentiment.csv", help="Output CSV path")
    parser.add_argument("--min-reviews", type=int, default=50, help="Minimum valid unique reviews required")
    args = parser.parse_args()

    if not os.path.exists(args.input):
        raise FileNotFoundError(f"Input CSV not found: {args.input}")

    df = pd.read_csv(args.input)
    df.columns = df.columns.str.strip()
    if "Review" not in df.columns or "Rating" not in df.columns:
        raise ValueError(f"CSV must contain Review and Rating columns. Found: {df.columns.tolist()}")

    for col in ["Title", "Date", "Reviewer", "Source", "Product_Name", "Brand", "Source_URLs"]:
        if col not in df.columns:
            df[col] = ""

    df["Review"] = df["Review"].fillna("").astype(str).str.strip()
    df["Rating"] = pd.to_numeric(df["Rating"], errors="coerce")
    df = df[(df["Review"] != "") & df["Rating"].between(1, 5)].copy()
    df["Primary_Key"] = df["Review"].str.lower().apply(
        lambda x: hashlib.sha256(x.encode("utf-8")).hexdigest()[:12].upper()
    )
    df = df.drop_duplicates(subset=["Primary_Key"]).reset_index(drop=True)

    if len(df) < args.min_reviews:
        raise ValueError(f"Only {len(df)} valid unique reviews found; at least {args.min_reviews} required.")

    df["Review_Clean"] = df["Review"].str.lower()
    sentiment = df.apply(
        lambda row: classify_sentiment(f"{row['Title']} {row['Review']}"),
        axis=1
    )
    df["Overall_Sentiment"] = [x[0] for x in sentiment]
    df["Polarity_Score"] = [round(x[1], 4) for x in sentiment]
    df["Aspects"] = (df["Title"].fillna("").astype(str) + " " + df["Review"]).apply(tag_aspects)
    df["Sentiment_Tags"] = df["Aspects"]

    df.to_csv(args.output, index=False, encoding="utf-8-sig")
    print(f"Wrote {len(df)} rows to {args.output}")
    print("\\nReview count:", len(df))
    print("\\nSentiment distribution:")
    print(df["Overall_Sentiment"].value_counts())
    print("\\nAspect distribution:")
    print(df["Aspects"].str.split(", ").explode().value_counts())

if __name__ == "__main__":
    main()
