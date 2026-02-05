import random


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


def get_meme():
    return random.choice(MEMES)
