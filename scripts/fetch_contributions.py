import json
import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime

USERNAME = "JyotinderYadav"

URL = f"https://github.com/users/{USERNAME}/contributions"

response = requests.get(
    URL,
    headers={
        "User-Agent": "Mozilla/5.0"
    },
    timeout=30
)

response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

days = []

for rect in soup.select("td.ContributionCalendar-day"):
    date = rect.get("data-date")
    level = rect.get("data-level")

    if date and level is not None:
        days.append({
            "date": date,
            "level": int(level)
        })

if not days:
    raise RuntimeError(
        "No contribution data found. GitHub may have changed its HTML structure."
    )

data = {
    "username": USERNAME,
    "generated_at": datetime.utcnow().isoformat() + "Z",
    "days": days
}

with open("data/contributions.json", "w") as f:
    json.dump(data, f, indent=2)

print(f"Fetched {len(days)} contribution days for {USERNAME}")
print("Saved to data/contributions.json")