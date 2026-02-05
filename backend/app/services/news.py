import os
import time
import httpx
import feedparser


CACHE_SECONDS = 120
_LAST_NEWS = []
_LAST_FETCH_AT = 0.0

RSS_FEEDS = [
    "https://feeds.feedburner.com/CoinDesk",
    "https://cointelegraph.com/rss",
]

FALLBACK_NEWS = [
    {
        "title": "Bitcoin volatility eases as markets await next rate decision",
        "url": "https://example.com/bitcoin-volatility",
        "source": "Fallback",
    },
    {
        "title": "Ethereum roadmap update focuses on scaling rollups",
        "url": "https://example.com/ethereum-roadmap",
        "source": "Fallback",
    },
    {
        "title": "Solana ecosystem sees growth in daily active users",
        "url": "https://example.com/solana-growth",
        "source": "Fallback",
    },
]


def _format_items(items):
    formatted = []
    for item in items:
        formatted.append(
            {
                "title": item.get("title"),
                "url": item.get("url"),
                "source": item.get("source", {}).get("title")
                if isinstance(item.get("source"), dict)
                else item.get("source", ""),
            }
        )
    return formatted


def _rss_fallback():
    for url in RSS_FEEDS:
        try:
            feed = feedparser.parse(url)
            if not feed.entries:
                continue
            source = getattr(feed.feed, "title", "RSS")
            items = []
            for entry in feed.entries[:6]:
                items.append(
                    {
                        "title": entry.get("title"),
                        "url": entry.get("link"),
                        "source": source,
                    }
                )
            if items:
                return items
        except Exception:
            continue
    return []


async def get_news(assets):
    global _LAST_FETCH_AT, _LAST_NEWS
    now = time.time()
    if _LAST_NEWS and (now - _LAST_FETCH_AT) < CACHE_SECONDS:
        return _LAST_NEWS

    token = os.getenv("CRYPTOPANIC_TOKEN")
    if not token:
        rss_items = _rss_fallback()
        return rss_items or FALLBACK_NEWS

    url = "https://cryptopanic.com/api/v1/posts/"
    params = {
        "auth_token": token,
        "filter": "rising",
        "public": "true",
    }
    if assets:
        params["currencies"] = ",".join([a.upper()[:5] for a in assets])

    try:
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.get(url, params=params)
            if resp.status_code != 200:
                rss_items = _rss_fallback()
                return rss_items or FALLBACK_NEWS
            data = resp.json()
        news = _format_items(data.get("results", []))[:6]
        if not news:
            rss_items = _rss_fallback()
            news = rss_items or FALLBACK_NEWS
        _LAST_NEWS = news
        _LAST_FETCH_AT = now
        return news
    except httpx.HTTPError:
        return _LAST_NEWS or _rss_fallback() or FALLBACK_NEWS
