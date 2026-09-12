import json
from pathlib import Path
from datetime import datetime

DATA_FILE = Path("data/contributions.json")
OUTPUT_FILE = Path("contrib-heatmap.svg")

PALETTE = [
    "#161b22",  # 0 - none
    "#0e4429",  # 1
    "#006d32",  # 2
    "#26a641",  # 3
    "#39d353",  # 4
    "#69f0a0",  # 5
]

CELL = 12
GAP = 3
STEP = CELL + GAP

LEFT = 40
TOP = 45

with open(DATA_FILE, "r") as f:
    data = json.load(f)

days = data["days"]

# Convert contribution data into a lookup table
contributions = {
    item["date"]: item["level"]
    for item in days
}

# Convert dates to datetime objects
parsed_days = []

for item in days:
    date = datetime.strptime(item["date"], "%Y-%m-%d")
    parsed_days.append((date, item["level"]))

parsed_days.sort()

# GitHub contribution calendar normally has 7 rows
weeks = {}

for date, level in parsed_days:
    # Sunday = 0, Monday = 1, ..., Saturday = 6
    weekday = (date.weekday() + 1) % 7

    # Determine week number relative to first date
    first_date = parsed_days[0][0]
    days_from_start = (date - first_date).days
    week = days_from_start // 7

    weeks.setdefault(week, {})
    weeks[week][weekday] = level

num_weeks = max(weeks.keys()) + 1

WIDTH = LEFT + num_weeks * STEP + 20
HEIGHT = TOP + 7 * STEP + 80

svg = []

svg.append(
    f'''<svg xmlns="http://www.w3.org/2000/svg"
    width="{WIDTH}"
    height="{HEIGHT}"
    viewBox="0 0 {WIDTH} {HEIGHT}">
'''
)

# Background
svg.append(
    f'<rect width="100%" height="100%" fill="#0d1117" rx="12"/>\n'
)

# Title
svg.append(
    '''
<text x="40" y="25"
      fill="#f0f6fc"
      font-family="monospace"
      font-size="13"
      font-weight="bold">
  github.com/JyotinderYadav — contributions
</text>
'''
)

# Animation definitions
svg.append(
    '''
<style>
.cell {
    opacity: 0;
    transform-box: fill-box;
    transform-origin: center;
    animation: appear 0.45s ease-out forwards;
}

@keyframes appear {
    from {
        opacity: 0;
        transform: translateY(-8px);
    }

    to {
        opacity: 1;
        transform: translateY(0);
    }
}
</style>
'''
)

# Draw contribution cells
for week, week_days in weeks.items():

    for weekday, level in week_days.items():

        x = LEFT + week * STEP
        y = TOP + weekday * STEP

        color = PALETTE[min(level, len(PALETTE) - 1)]

        delay = (week * 7 + weekday) * 0.015

        svg.append(
            f'''
<rect
    class="cell"
    x="{x}"
    y="{y}"
    width="{CELL}"
    height="{CELL}"
    rx="3"
    fill="{color}"
    style="animation-delay:{delay:.3f}s"
/>
'''
        )

# Legend
legend_y = TOP + 7 * STEP + 25

svg.append(
    f'''
<text x="{LEFT}" y="{legend_y}"
      fill="#8b949e"
      font-family="monospace"
      font-size="10">
  Less
</text>
'''
)

for i, color in enumerate(PALETTE):

    x = LEFT + 32 + i * STEP

    svg.append(
        f'''
<rect
    x="{x}"
    y="{legend_y - 10}"
    width="{CELL}"
    height="{CELL}"
    rx="3"
    fill="{color}"
/>
'''
    )

svg.append(
    f'''
<text x="{LEFT + 32 + len(PALETTE) * STEP + 5}"
      y="{legend_y}"
      fill="#8b949e"
      font-family="monospace"
      font-size="10">
  More
</text>
'''
)

# Footer
svg.append(
    f'''
<text x="{LEFT}"
      y="{HEIGHT - 12}"
      fill="#8b949e"
      font-family="monospace"
      font-size="10">
  {len(days)} days · generated {data["generated_at"][:10]}
</text>
'''
)

svg.append("</svg>")

OUTPUT_FILE.write_text("".join(svg), encoding="utf-8")

print(f"Created {OUTPUT_FILE}")
print(f"Size: {WIDTH} x {HEIGHT}")
print(f"Weeks: {num_weeks}")