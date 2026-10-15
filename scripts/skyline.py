"""Builds assets/hq-skyline.svg: the last 52 weeks of contributions as a neon skyline.

One building per week, height from that week's contribution count, with the
ShinyQ HQ rover driving along the street. Window lights are deterministic per
week so a rerun with the same data writes the same file.

Needs GITHUB_TOKEN (any token that can read the public GraphQL API).
Run: GITHUB_TOKEN=$(gh auth token) python3 scripts/skyline.py
"""
import base64
import json
import math
import os
import random
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
USER = os.environ.get("SKYLINE_USER", "ShinyQ")
CYAN, INDIGO, VIOLET = "#22D3EE", "#6366F1", "#8B5CF6"
BG, MUTED = "#0B1020", "#7D8590"
W, H, STREET = 1200, 230, 176

QUERY = """query($login:String!){user(login:$login){contributionsCollection{contributionCalendar{
totalContributions weeks{contributionDays{contributionCount date}}}}}}"""


def fetch() -> tuple[int, list[tuple[str, int]]]:
    body = json.dumps({"query": QUERY, "variables": {"login": USER}}).encode()
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=body,
        headers={"Authorization": f"bearer {os.environ['GITHUB_TOKEN']}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=30) as res:
        data = json.load(res)
    if "errors" in data:
        raise SystemExit(f"GraphQL error: {data['errors']}")
    cal = data["data"]["user"]["contributionsCollection"]["contributionCalendar"]
    weeks = [(w["contributionDays"][0]["date"], sum(d["contributionCount"] for d in w["contributionDays"])) for w in cal["weeks"]]
    return cal["totalContributions"], weeks[-52:]


def font() -> str:
    return base64.b64encode((ROOT / "assets" / "fonts" / "jetbrains-mono-subset.woff2").read_bytes()).decode()


def svg(total: int, weeks: list[tuple[str, int]]) -> str:
    peak = max((c for _, c in weeks), default=1) or 1
    slot = (W - 80) / len(weeks)
    bw = slot * 0.78
    parts = []
    for i, (start, count) in enumerate(weeks):
        h = 6 + 128 * math.sqrt(count / peak)
        x = 40 + i * slot
        y = STREET - h
        glow = 0.35 + 0.65 * (count / peak)
        parts.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{bw:.1f}" height="{h:.1f}" rx="1.5" fill="url(#neon)" opacity="{glow:.2f}"><title>{start}: {count} contributions</title></rect>')
        rng = random.Random(start)
        for wy in range(int(y) + 6, STREET - 6, 8):
            for wx in (x + bw * 0.25, x + bw * 0.6):
                if rng.random() < 0.4:
                    parts.append(f'<rect x="{wx:.1f}" y="{wy}" width="2.6" height="2.6" fill="#E0F2FE" opacity=".75"/>')
    rover = (
        f'<g class="rover"><rect x="0" y="{STREET - 21}" width="34" height="19" rx="5" fill="#0F172A" stroke="{CYAN}" stroke-width="2"/>'
        f'<rect x="6" y="{STREET - 16}" width="22" height="9" rx="2" fill="{CYAN}"/>'
        f'<circle cx="12" cy="{STREET - 11.5}" r="1.6" fill="{BG}"/><circle cx="22" cy="{STREET - 11.5}" r="1.6" fill="{BG}"/>'
        f'<line x1="17" y1="{STREET - 21}" x2="17" y2="{STREET - 28}" stroke="{CYAN}" stroke-width="1.5"/><circle cx="17" cy="{STREET - 29}" r="2" fill="#F472B6"/>'
        f'<circle cx="8" cy="{STREET}" r="4" fill="{INDIGO}"/><circle cx="26" cy="{STREET}" r="4" fill="{INDIGO}"/></g>'
    )
    caption = f"{total:,} contributions in the last year · one building per week · the HQ grows with every merge"
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-labelledby="title">
<title id="title">{total} GitHub contributions in the last year, drawn as a skyline with one building per week</title>
<defs>
<style>
@font-face{{font-family:"HQ Mono";src:url(data:font/woff2;base64,{font()}) format("woff2");font-weight:400 700}}
.t{{font-family:"HQ Mono",ui-monospace,Menlo,Consolas,monospace;font-size:14px}}
.rover{{animation:drive 14s linear infinite}}
@keyframes drive{{from{{transform:translateX(-60px)}}to{{transform:translateX({W + 20}px)}}}}
@media (prefers-reduced-motion:reduce){{.rover{{animation:none;transform:translateX({W / 2 - 17}px)}}}}
</style>
<linearGradient id="neon" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="{CYAN}"/><stop offset=".6" stop-color="{INDIGO}"/><stop offset="1" stop-color="{VIOLET}"/></linearGradient>
<pattern id="grid" width="32" height="32" patternUnits="userSpaceOnUse"><path d="M32 0H0V32" fill="none" stroke="{INDIGO}" stroke-opacity=".08"/></pattern>
<filter id="glow" x="-5%" y="-200%" width="110%" height="500%"><feGaussianBlur stdDeviation="3"/></filter>
<clipPath id="card"><rect width="{W}" height="{H}" rx="16"/></clipPath>
</defs>
<g clip-path="url(#card)">
<rect width="{W}" height="{H}" fill="{BG}"/><rect width="{W}" height="{H}" fill="url(#grid)"/>
{"".join(parts)}
<line x1="20" x2="{W - 20}" y1="{STREET + 1}" y2="{STREET + 1}" stroke="{CYAN}" stroke-width="3" filter="url(#glow)" opacity=".8"/>
<line x1="20" x2="{W - 20}" y1="{STREET + 1}" y2="{STREET + 1}" stroke="{CYAN}" stroke-width="1.5"/>
{rover}
<text class="t" x="{W / 2}" y="{H - 22}" fill="{MUTED}" text-anchor="middle">{caption}</text>
</g>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="16" fill="none" stroke="{INDIGO}" stroke-opacity=".35"/>
</svg>
'''


if __name__ == "__main__":
    total, weeks = fetch()
    out = ROOT / "assets" / "hq-skyline.svg"
    out.write_text(svg(total, weeks))
    print(f"wrote {out.relative_to(ROOT)}: {total} contributions over {len(weeks)} weeks")
