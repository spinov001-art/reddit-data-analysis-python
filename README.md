# Reddit Data Analysis with Python 📊

Analyze Reddit posts, comments, and trends using Python. No Reddit API key needed — uses Reddit's public JSON endpoints.

## What You Can Do

- **Sentiment Analysis** — Track positive/negative sentiment in any subreddit
- **Trend Detection** — Find emerging topics before they go viral
- **Keyword Monitoring** — Track mentions of your brand, product, or competitors
- **Community Analysis** — Understand subreddit demographics and posting patterns

## Quick Start

```bash
pip install requests pandas textblob
python reddit_analyzer.py --subreddit startup --limit 100
```

## How It Works

Reddit exposes a JSON API at `reddit.com/r/{subreddit}.json`. No authentication needed for public data.

```python
import requests

def get_subreddit_posts(subreddit, limit=25):
    """Fetch posts from any subreddit — no API key needed."""
    url = f"https://www.reddit.com/r/{subreddit}/hot.json?limit={limit}"
    headers = {"User-Agent": "RedditAnalyzer/1.0"}
    response = requests.get(url, headers=headers)
    posts = response.json()["data"]["children"]
    return [{"title": p["data"]["title"],
             "score": p["data"]["score"],
             "comments": p["data"]["num_comments"],
             "author": p["data"]["author"],
             "url": p["data"]["url"]} for p in posts]

# Example: get hot posts from r/startup
posts = get_subreddit_posts("startup", limit=50)
for post in posts[:5]:
    print(f"{post[\"score\"]:>5} | {post[\"title\"][:60]}")
```

## Sentiment Analysis

```python
from textblob import TextBlob

def analyze_sentiment(posts):
    """Analyze sentiment of Reddit posts."""
    for post in posts:
        blob = TextBlob(post["title"])
        post["sentiment"] = blob.sentiment.polarity
        post["label"] = "positive" if post["sentiment"] > 0.1 else \
                        "negative" if post["sentiment"] < -0.1 else "neutral"
    return posts

results = analyze_sentiment(posts)
positive = sum(1 for r in results if r["label"] == "positive")
negative = sum(1 for r in results if r["label"] == "negative")
neutral = sum(1 for r in results if r["label"] == "neutral")
print(f"Positive: {positive} | Negative: {negative} | Neutral: {neutral}")
```

## Keyword Tracking

```python
def track_keyword(subreddit, keyword, limit=100):
    """Find posts mentioning a specific keyword."""
    url = f"https://www.reddit.com/r/{subreddit}/search.json?q={keyword}&restrict_sr=1&limit={limit}&sort=new"
    headers = {"User-Agent": "RedditAnalyzer/1.0"}
    response = requests.get(url, headers=headers)
    return response.json()["data"]["children"]

# Track "Claude AI" mentions in r/artificial
mentions = track_keyword("artificial", "Claude AI", limit=50)
print(f"Found {len(mentions)} mentions")
```

## Scale with Apify

For production use (thousands of posts, scheduled runs, data storage):

🔗 **[Reddit Scraper on Apify](https://apify.com/knotless_cadence/reddit-scraper-pro)** — Cloud-hosted, handles rate limits, exports to JSON/CSV/Excel.

## More Tools

- [Awesome Web Scraping 2026](https://github.com/spinov001-art/awesome-web-scraping-2026) — 77+ free data collection tools
- [AI Market Research Reports](https://github.com/spinov001-art/ai-market-research-reports) — Market research using web scraping + AI
- [Free API Directory](https://github.com/spinov001-art/free-api-directory) — 100+ free APIs for developers

## Need Custom Data Analysis?

I build data extraction and analysis pipelines for any platform.

**[Hire me →](https://spinov001-art.github.io)** | Email: Spinov001@gmail.com

## License

MIT
