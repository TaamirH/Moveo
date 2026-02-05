import os
import httpx


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


async def get_news(assets):
    token = os.getenv("CRYPTOPANIC_TOKEN")
    if not token:
        return FALLBACK_NEWS

    url = "https://cryptopanic.com/api/v1/posts/"
    params = {
        "auth_token": token,
        "filter": "rising",
        "public": "true",
    }
    if assets:
        params["currencies"] = ",".join([a.upper()[:5] for a in assets])

    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.get(url, params=params)
        if resp.status_code != 200:
            return FALLBACK_NEWS
        data = resp.json()
    return _format_items(data.get("results", []))[:6] or FALLBACK_NEWS
