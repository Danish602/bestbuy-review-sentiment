"""Generates SYNTHETIC demo reviews (NOT real BestBuy data) so the analysis half of the notebook
can be tested offline. Every row is marked Source = SYNTHETIC-DEMO. Never submit this as real data."""
import random
import pandas as pd

random.seed(42)
POS = [
    ("Great design", "The design is sleek and it looks great on my counter."),
    ("Easy setup", "Setup was easy and the app walked me through it in minutes."),
    ("Sounds great", "The sound is clear and the speaker gets loud enough for the kitchen."),
    ("Worth the price", "Honestly a great value for the price, would buy again."),
    ("Works perfectly", "Works perfectly and the screen is bright and responsive."),
    ("Love it", "I love it. Build quality feels solid and it is fast."),
    ("Good deal", "Bought it on sale, very happy with the quality and the features."),
    ("Recommended", "Highly recommend, the voice assistant understands me every time."),
]
NEG = [
    ("Wifi problems", "The wifi keeps disconnecting and I have to re-pair it every few days. Very frustrating."),
    ("Stopped working", "It stopped working after two months and the support was useless."),
    ("Too expensive", "Overpriced for what it does, the price is not worth it."),
    ("Laggy", "The screen is laggy and slow, the app freezes all the time."),
    ("Poor sound", "The sound is tinny and the speaker is weak, disappointed."),
    ("Hard to set up", "Setup was confusing and the instructions were terrible."),
    ("Delivery issue", "Delivery was late and the box arrived damaged, returning it."),
    ("Flimsy", "Feels cheap and flimsy, I would not buy it again."),
]
MIX = [
    ("Okay", "The sound is good but the wifi connection drops sometimes."),
    ("Mixed", "Nice design and easy to use, but a bit expensive."),
    ("Decent", "It works fine, battery and charging are okay, nothing special."),
]

rows = []
for i in range(1, 61):
    r = random.random()
    if r < 0.55:   t, body = random.choice(POS); rating = random.choice([5, 5, 5, 4, 4])
    elif r < 0.85: t, body = random.choice(NEG); rating = random.choice([1, 1, 2, 2, 3])
    else:          t, body = random.choice(MIX); rating = random.choice([3, 3, 4])
    extra = random.choice(["", " " + random.choice(POS)[1], " " + random.choice(NEG)[1]]) if random.random() < 0.3 else ""
    date = f"202{random.choice([3, 4])}-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}"
    rows.append({"key": f"DEMO-{i:04d}", "dom_id": None, "title": t, "review_text": body + extra,
                 "date_raw": date, "rating": float(rating), "source": "SYNTHETIC-DEMO",
                 "reviewer_name": f"Demo User {i}", "filters_seen_in": "demo"})
pd.DataFrame(rows).to_csv("demo_reviews_raw.csv", index=False)
print("wrote", len(rows), "synthetic rows")
