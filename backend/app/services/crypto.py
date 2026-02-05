import httpx


COINGECKO_MAP = {
    "bitcoin": "bitcoin",
    "btc": "bitcoin",
    "ethereum": "ethereum",
    "eth": "ethereum",
    "solana": "solana",
    "sol": "solana",
    "dogecoin": "dogecoin",
    "doge": "dogecoin",
    "cardano": "cardano",
    "ada": "cardano",
    "xrp": "ripple",
    "ripple": "ripple",
}


def normalize_assets(assets):
    ids = []
    for asset in assets or []:
        key = asset.strip().lower()
        if key in COINGECKO_MAP:
            ids.append(COINGECKO_MAP[key])
    if not ids:
        ids = ["bitcoin", "ethereum"]
    return sorted(list(set(ids)))


async def get_prices(assets):
    ids = normalize_assets(assets)
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {"ids": ",".join(ids), "vs_currencies": "usd"}
    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.get(url, params=params)
        resp.raise_for_status()
        data = resp.json()
    return {coin: data.get(coin, {}) for coin in ids}
