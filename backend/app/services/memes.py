import random
import time
import httpx


MEMES = [
    {
        "title": "When your alt finally pumps",
        "url": "https://i.imgflip.com/4/4t0m5.jpg",
    },
    {
        "title": "HODL through the dip",
        "url": "https://i.imgflip.com/4/3si4.jpg",
    },
    {
        "title": "Crypto market mood",
        "url": "https://i.imgflip.com/4/1bij.jpg",
    },
    {
        "title": "This is fine, just a small correction",
        "url": "https://i.imgflip.com/4/1e7ql7.jpg",
    },
    {
        "title": "Green candles all day",
        "url": "https://i.imgflip.com/4/30b1gx.jpg",
    },
]

CACHE_SECONDS = 300
_LAST_MEMES = []
_LAST_FETCH_AT = 0.0
REDDIT_URL = "https://www.reddit.com/r/cryptocurrencymemes/top.json?limit=25&t=day"


def _is_image(url: str) -> bool:
    return url.endswith((".jpg", ".jpeg", ".png", ".gif"))


async def _fetch_reddit_memes():
    headers = {"User-Agent": "crypto-advisor-demo/1.0"}
    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.get(REDDIT_URL, headers=headers)
        if resp.status_code != 200:
            return []
        data = resp.json()
    items = []
    for child in data.get("data", {}).get("children", []):
        post = child.get("data", {})
        url = post.get("url_overridden_by_dest") or post.get("url")
        if not url or not _is_image(url):
            continue
        title = post.get("title", "Crypto meme")
        items.append({"title": title, "url": url})
    return items


async def get_meme():
    global _LAST_FETCH_AT, _LAST_MEMES
    now = time.time()
    if _LAST_MEMES and (now - _LAST_FETCH_AT) < CACHE_SECONDS:
        meme = random.choice(_LAST_MEMES)
        return {**meme, "source": "reddit"}

    try:
        memes = await _fetch_reddit_memes()
        if memes:
            _LAST_MEMES = memes
            _LAST_FETCH_AT = now
            meme = random.choice(memes)
            return {**meme, "source": "reddit"}
    except httpx.HTTPError:
        pass

    meme = random.choice(MEMES)
    return {**meme, "source": "static"}
