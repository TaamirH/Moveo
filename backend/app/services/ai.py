import os
import httpx


FALLBACK_INSIGHT = (
    "Diversify your watchlist and size positions based on conviction and risk. "
    "Use limit orders and avoid chasing sudden pumps."
)


def _build_prompt(profile):
    investor = profile.get("investor_type") if profile else None
    assets = profile.get("interested_assets") if profile else None
    content = profile.get("content_preferences") if profile else None

    details = []
    if investor:
        details.append(f"Investor type: {investor}.")
    if assets:
        details.append(f"Interested assets: {', '.join(assets)}.")
    if content:
        details.append(f"Content preferences: {', '.join(content)}.")

    context = " ".join(details) if details else "General crypto investor."
    return (
        "You are a crypto advisor. Provide one short, practical insight for today. "
        f"{context} Keep it under 40 words."
    )


async def _openrouter(prompt: str) -> str:
    api_key = os.getenv("OPENROUTER_API_KEY")
    model = os.getenv("OPENROUTER_MODEL", "meta-llama/llama-3.1-8b-instruct")
    if not api_key:
        return ""
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {"Authorization": f"Bearer {api_key}"}
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 80,
    }
    async with httpx.AsyncClient(timeout=15) as client:
        resp = await client.post(url, json=payload, headers=headers)
        if resp.status_code != 200:
            return ""
        data = resp.json()
    try:
        return data["choices"][0]["message"]["content"].strip()
    except (KeyError, IndexError, TypeError):
        return ""


async def _huggingface(prompt: str) -> str:
    api_key = os.getenv("HUGGINGFACE_API_KEY")
    model = os.getenv("HUGGINGFACE_MODEL", "google/flan-t5-large")
    if not api_key:
        return ""
    url = f"https://api-inference.huggingface.co/models/{model}"
    headers = {"Authorization": f"Bearer {api_key}"}
    payload = {"inputs": prompt}
    async with httpx.AsyncClient(timeout=20) as client:
        resp = await client.post(url, json=payload, headers=headers)
        if resp.status_code != 200:
            return ""
        data = resp.json()
    if isinstance(data, list) and data:
        return data[0].get("generated_text", "").strip()
    return ""


async def get_ai_insight(profile: dict):
    prompt = _build_prompt(profile)
    insight = await _openrouter(prompt)
    if not insight:
        insight = await _huggingface(prompt)
        if insight:
            return insight, "huggingface"
    if insight:
        return insight, "openrouter"
    return FALLBACK_INSIGHT, "fallback"
