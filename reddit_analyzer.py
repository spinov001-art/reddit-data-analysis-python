"""
Reddit Data Analyzer — Analyze any subreddit without API keys.
Uses Reddit public JSON API. No authentication needed.

Usage:
    python reddit_analyzer.py --subreddit startup --limit 100
    python reddit_analyzer.py --search "best CRM" --limit 50
    python reddit_analyzer.py --subreddit SaaS --keyword "pricing"
"""

import argparse
import json
import sys
import time
from datetime import datetime

try:
    import requests
except ImportError:
    print("Install requests: pip install requests")
    sys.exit(1)

HEADERS = {"User-Agent": "RedditAnalyzer/1.0 (github.com/spinov001-art)"}
BASE_URL = "https://www.reddit.com"


def fetch_subreddit(subreddit: str, sort: str = "hot", limit: int = 25) -> list:
    """Fetch posts from a subreddit."""
    url = f"{BASE_URL}/r/{subreddit}/{sort}.json?limit={limit}"
    resp = requests.get(url, headers=HEADERS, timeout=10)
    resp.raise_for_status()
    children = resp.json()["data"]["children"]
    return [parse_post(c["data"]) for c in children]


def search_reddit(query: str, subreddit: str = None, limit: int = 25) -> list:
    """Search Reddit for posts matching a query."""
    if subreddit:
        url = f"{BASE_URL}/r/{subreddit}/search.json?q={query}&restrict_sr=1&limit={limit}&sort=new"
    else:
        url = f"{BASE_URL}/search.json?q={query}&limit={limit}&sort=new"
    resp = requests.get(url, headers=HEADERS, timeout=10)
    resp.raise_for_status()
    children = resp.json()["data"]["children"]
    return [parse_post(c["data"]) for c in children]


def parse_post(data: dict) -> dict:
    """Extract useful fields from a Reddit post."""
    return {
        "title": data.get("title", ""),
        "subreddit": data.get("subreddit", ""),
        "score": data.get("score", 0),
        "upvote_ratio": data.get("upvote_ratio", 0),
        "num_comments": data.get("num_comments", 0),
        "author": data.get("author", ""),
        "created_utc": datetime.utcfromtimestamp(data.get("created_utc", 0)).isoformat(),
        "url": f"https://reddit.com{data.get('permalink', '')}",
        "selftext": data.get("selftext", "")[:500],
    }


def analyze_sentiment(posts: list) -> dict:
    """Basic sentiment analysis using keyword matching."""
    positive_words = {"great", "awesome", "love", "best", "amazing", "excellent", "good", "perfect", "recommend", "helpful"}
    negative_words = {"bad", "terrible", "worst", "hate", "awful", "horrible", "broken", "useless", "scam", "disappointing"}

    results = {"positive": 0, "negative": 0, "neutral": 0}
    for post in posts:
        text = (post["title"] + " " + post["selftext"]).lower()
        pos = sum(1 for w in positive_words if w in text)
        neg = sum(1 for w in negative_words if w in text)
        if pos > neg:
            results["positive"] += 1
        elif neg > pos:
            results["negative"] += 1
        else:
            results["neutral"] += 1
    return results


def main():
    parser = argparse.ArgumentParser(description="Analyze Reddit data without API keys")
    parser.add_argument("--subreddit", "-s", help="Subreddit to analyze")
    parser.add_argument("--search", help="Search query")
    parser.add_argument("--keyword", "-k", help="Filter posts by keyword")
    parser.add_argument("--limit", "-l", type=int, default=25, help="Number of posts")
    parser.add_argument("--sort", choices=["hot", "new", "top", "rising"], default="hot")
    parser.add_argument("--output", "-o", help="Save results to JSON file")
    parser.add_argument("--sentiment", action="store_true", help="Run sentiment analysis")
    args = parser.parse_args()

    if not args.subreddit and not args.search:
        parser.error("Provide --subreddit or --search")

    print(f"Fetching Reddit data...")
    if args.search:
        posts = search_reddit(args.search, args.subreddit, args.limit)
    else:
        posts = fetch_subreddit(args.subreddit, args.sort, args.limit)

    if args.keyword:
        kw = args.keyword.lower()
        posts = [p for p in posts if kw in p["title"].lower() or kw in p["selftext"].lower()]

    print(f"Found {len(posts)} posts\n")
    print(f"{"Score":>6} | {"Comments":>8} | Title")
    print("-" * 70)
    for p in posts[:20]:
        print(f"{p["score"]:>6} | {p["num_comments"]:>8} | {p["title"][:50]}")

    if args.sentiment:
        sentiment = analyze_sentiment(posts)
        print(f"\nSentiment: +{sentiment["positive"]} / -{sentiment["negative"]} / ~{sentiment["neutral"]}")

    if args.output:
        with open(args.output, "w") as f:
            json.dump(posts, f, indent=2)
        print(f"\nSaved to {args.output}")


if __name__ == "__main__":
    main()
