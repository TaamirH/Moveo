import time
import httpx


COINGECKO_MAP = {
    "bitcoin": "bitcoin",
    "btc": "bitcoin",
    "ethereum": "ethereum",
    "eth": "ethereum",
    "xrp": "ripple",
    "ripple": "ripple",
    "tether": "tether",
    "usdt": "tether",
    "binancecoin": "binancecoin",
    "bnb": "binancecoin",
    "solana": "solana",
    "sol": "solana",
    "usd-coin": "usd-coin",
    "usdc": "usd-coin",
    "cardano": "cardano",
    "ada": "cardano",
    "dogecoin": "dogecoin",
    "doge": "dogecoin",
    "toncoin": "toncoin",
    "ton": "toncoin",
    "tron": "tron",
    "trx": "tron",
    "polkadot": "polkadot",
    "dot": "polkadot",
    "polygon": "polygon",
    "matic": "polygon",
    "chainlink": "chainlink",
    "link": "chainlink",
    "avalanche": "avalanche-2",
    "avax": "avalanche-2",
    "shiba-inu": "shiba-inu",
    "shib": "shiba-inu",
    "litecoin": "litecoin",
    "ltc": "litecoin",
    "bitcoin-cash": "bitcoin-cash",
    "bch": "bitcoin-cash",
    "uniswap": "uniswap",
    "uni": "uniswap",
    "cosmos": "cosmos",
    "atom": "cosmos",
    "stellar": "stellar",
    "xlm": "stellar",
    "ethereum-classic": "ethereum-classic",
    "etc": "ethereum-classic",
    "monero": "monero",
    "xmr": "monero",
    "okb": "okb",
    "aptos": "aptos",
    "apt": "aptos",
    "near": "near",
    "filecoin": "filecoin",
    "fil": "filecoin",
    "lido-dao": "lido-dao",
    "ldo": "lido-dao",
    "arbitrum": "arbitrum",
    "arb": "arbitrum",
    "optimism": "optimism",
    "op": "optimism",
    "maker": "maker",
    "mkr": "maker",
    "aave": "aave",
    "the-graph": "the-graph",
    "grt": "the-graph",
    "vechain": "vechain",
    "vet": "vechain",
    "quant": "quant-network",
    "qnt": "quant-network",
    "pepe": "pepe",
    "sui": "sui",
    "kaspa": "kaspa",
    "kas": "kaspa",
    "immutable-x": "immutable-x",
    "imx": "immutable-x",
    "render": "render-token",
    "rndr": "render-token",
    "thorchain": "thorchain",
    "rune": "thorchain",
    "injective": "injective-protocol",
    "inj": "injective-protocol",
    "celestia": "celestia",
    "tia": "celestia",
    "internet-computer": "internet-computer",
    "icp": "internet-computer",
    "leo-token": "leo-token",
    "leo": "leo-token",
    "stacks": "stacks",
    "stx": "stacks",
    "bitget-token": "bitget-token",
    "bgb": "bitget-token",
    "fdusd": "fdusd",
    "bittensor": "bittensor",
    "tao": "bittensor",
    "dogwifhat": "dogwifhat",
    "wif": "dogwifhat",
    "bonk": "bonk",
}

CACHE_SECONDS = 30
_LAST_PRICES = {}
_LAST_FETCH_AT = 0.0


def normalize_assets(assets):
    ids = []
    for asset in assets or []:
        key = asset.strip().lower()
        if not key:
            continue
        if key in COINGECKO_MAP:
            ids.append(COINGECKO_MAP[key])
    if not ids:
        ids = ["bitcoin", "ethereum"]
    return sorted(list(set(ids)))[:5]


async def get_prices(assets):
    global _LAST_FETCH_AT, _LAST_PRICES
    ids = normalize_assets(assets)
    now = time.time()
    if _LAST_PRICES and (now - _LAST_FETCH_AT) < CACHE_SECONDS:
        return _LAST_PRICES

    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {"ids": ",".join(ids), "vs_currencies": "usd"}
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.get(url, params=params)
            resp.raise_for_status()
            data = resp.json()
        _LAST_PRICES = {coin: data.get(coin, {}) for coin in ids}
        _LAST_FETCH_AT = now
        return _LAST_PRICES
    except httpx.HTTPError:
        return _LAST_PRICES or {coin: {} for coin in ids}
