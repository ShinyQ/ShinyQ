"""Builds the animated header: assets/hq-header.svg (dark) and assets/hq-header-light.svg.

The elevator doors of ShinyQ HQ slide open, the boot log checks every floor while the car rides
from L1 to the roof, and the name lights up. Every element's resting style is its final frame and
the animations only play into it, so a renderer without CSS animation (or a visitor who prefers
reduced motion) still gets the finished header. Run: python3 scripts/header.py
"""
import random

from hq import ASSETS, DISPLAY, MONO, THEMES, asset_name, font_faces, neon_gradient, write

W, H = 1200, 340
BOOT = [
    ("power on", "tower online"),
    ("L1 Lobby", "Highlights Hall, Rover, Ask"),
    ("L2 Career Archive", "2016 to today"),
    ("L3 Labs", "three wings of case studies"),
    ("L4 Library", "posts, papers, talks"),
    ("RF Roof", "comms uplink"),
]
LOCKED = ("B1 Engine Room", "locked: visit every floor")
FLOORS = ["L1", "L2", "L3", "L4", "RF"]
DOOR_AT, DOOR_FOR = 0.25, 0.85
FIRST, STEP = 0.85, 0.28
NAME_AT = FIRST + STEP * (len(BOOT) + 1) + 0.1
X0, TW, FH, GAP, BASE = 950, 160, 30, 8, 292
RIDE = 4 * (FH + GAP)


def at(k: int) -> float:
    return FIRST + STEP * k


def boot_lines(t: dict) -> str:
    out = [f'<text class="t in" x="44" y="68" style="animation-delay:.55s"><tspan fill="{t["cyan"]}">$</tspan>'
           f'<tspan fill="{t["text"]}"> ssh visitor@shinyq.my.id</tspan></text>']
    rows = [(k, v, "OK", t["ok"], t["text"]) for k, v in BOOT] + [(*LOCKED, "--", t["warn"], t["dim"])]
    for i, (key, value, mark, mark_fill, fill) in enumerate(rows):
        dots = "." * (20 - len(key))
        out.append(
            f'<text class="t in" x="44" y="{68 + (i + 1) * 20}" style="animation-delay:{at(i):.2f}s">'
            f'<tspan fill="{t["muted"]}">[ </tspan><tspan fill="{mark_fill}">{mark}</tspan><tspan fill="{t["muted"]}"> ] </tspan>'
            f'<tspan fill="{fill}">{key} </tspan><tspan fill="{t["dim"]}">{dots} </tspan><tspan fill="{fill}">{value}</tspan></text>'
        )
    return "".join(out)


def readout(t: dict) -> str:
    x, y, w, h = 800, 112, 104, 70
    parts = [
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{t["panel"]}" stroke="{t["line"]}"/>',
        f'<text class="t" x="{x + 14}" y="{y + 20}" font-size="10" letter-spacing="3" fill="{t["muted"]}">FLOOR</text>',
        f'<path class="arrow" d="M{x + w - 22} {y + 50}l8-12 8 12z" fill="{t["cyan"]}" style="animation-delay:{at(1):.2f}s"/>',
    ]
    for i, code in enumerate(FLOORS):
        if i == 0:
            style = f"animation:blip {at(2):.2f}s steps(1) 0s"
        elif i < 4:
            style = f"animation:blip {STEP:.2f}s steps(1) {at(i + 1):.2f}s"
        else:
            style = f"animation:wait {at(5):.2f}s steps(1) 0s"
        hidden = ' opacity="0"' if i < 4 else ""
        parts.append(f'<text class="d" x="{x + 14}" y="{y + 58}" font-size="40" fill="{t["cyan"]}"{hidden} style="{style}">{code}</text>')
    return "".join(parts)


def tower(t: dict) -> str:
    cx = X0 + TW / 2
    top = BASE - 5 * (FH + GAP) + GAP
    shaft = X0 + TW + 16
    parts = [
        f'<ellipse cx="{cx}" cy="{BASE + 16}" rx="170" ry="30" fill="url(#pool)"/>',
        f'<ellipse cx="{cx}" cy="{BASE + 16}" rx="134" ry="18" fill="none" stroke="{t["indigo"]}" stroke-opacity=".45" stroke-width="2"/>',
        f'<ellipse class="ring" cx="{cx}" cy="{BASE + 16}" rx="134" ry="18" fill="none" stroke="{t["cyan"]}" stroke-width="3" stroke-linecap="round" stroke-dasharray="1 21"/>',
        rover(t, cx),
        f'<line x1="{shaft}" y1="{BASE}" x2="{shaft}" y2="{top}" stroke="{t["cyan"]}" stroke-opacity=".35" stroke-dasharray="3 4"/>',
    ]
    for i, label in enumerate(FLOORS):
        y = BASE - (i + 1) * (FH + GAP) + GAP
        lit = at(i + 1)
        parts.append(f'<rect x="{X0}" y="{y}" width="{TW}" height="{FH}" rx="4" fill="{t["panel"]}" stroke="{t["cyan"]}" stroke-opacity=".4"/>')
        parts.append(f'<rect class="in" x="{X0 + 4}" y="{y + 4}" width="{TW - 8}" height="{FH - 8}" rx="2" fill="url(#neon)" style="animation-delay:{lit:.2f}s"/>')
        for k in range(6):
            parts.append(f'<rect class="in" x="{X0 + 16 + k * 23}" y="{y + 11}" width="11" height="8" rx="1" fill="{t["window"]}" opacity=".6" style="animation-delay:{lit + 0.06:.2f}s"/>')
        parts.append(f'<text class="t" x="{X0 - 12}" y="{y + 20}" fill="{t["muted"]}" font-size="12" text-anchor="end">{label}</text>')
    parts.append(f'<line x1="{cx}" y1="{top}" x2="{cx}" y2="{top - 22}" stroke="{t["cyan"]}" stroke-width="2"/>')
    parts.append(f'<circle cx="{cx}" cy="{top - 26}" r="9" fill="{t["cyan"]}" opacity=".25" filter="url(#soft)"/>')
    parts.append(f'<circle class="beacon" cx="{cx}" cy="{top - 26}" r="4" fill="{t["cyan"]}" style="animation-delay:{NAME_AT:.2f}s"/>')
    parts.append(f'<rect class="car" x="{shaft - 6}" y="{BASE - FH + 3}" width="12" height="{FH - 6}" rx="2" fill="{t["cyan"]}" style="animation-delay:{at(1):.2f}s"/>')
    return "".join(parts)


def rover(t: dict, cx: float) -> str:
    """The HQ rover patrols the ring at the tower's base (drawn before the tower, which hides it at the back)."""
    body = (f'<rect x="-11" y="-16" width="22" height="13" rx="4" fill="{t["panel"]}" stroke="{t["cyan"]}" stroke-width="1.5"/>'
            f'<rect x="-7" y="-13" width="14" height="5" rx="1.5" fill="{t["cyan"]}"/>'
            f'<line x1="0" y1="-16" x2="0" y2="-21" stroke="{t["cyan"]}" stroke-width="1.2"/><circle cx="0" cy="-22" r="1.6" fill="{t["warn"]}"/>'
            f'<circle cx="-6" cy="-2" r="2.6" fill="{t["indigo"]}"/><circle cx="6" cy="-2" r="2.6" fill="{t["indigo"]}"/>')
    rx, ry, cy = 134, 18, BASE + 16
    path = f"M{cx - rx},{cy} a{rx},{ry} 0 1,0 {2 * rx},0 a{rx},{ry} 0 1,0 {-2 * rx},0"
    return (f'<g class="rover-move">{body}<animateMotion dur="16s" repeatCount="indefinite" path="{path}"/></g>'
            f'<g class="rover-park" transform="translate({cx - 96} {cy + 18})">{body}</g>')


def motes(t: dict) -> str:
    rng = random.Random(7)
    out = []
    for i in range(18):
        x = rng.uniform(560, 1180) if i % 3 else rng.uniform(20, 1180)
        dur = rng.uniform(7, 12)
        out.append(f'<circle cx="{x:.0f}" cy="{rng.uniform(250, 330):.0f}" r="{rng.choice((1, 1.4, 1.8))}" '
                   f'fill="{t["cyan"] if i % 2 else t["violet"]}" opacity=".5" '
                   f'style="animation-duration:{dur:.1f}s;animation-delay:-{rng.uniform(0, dur):.1f}s"/>')
    return f'<g class="motes">{"".join(out)}</g>'


def doors(t: dict) -> str:
    half = W / 2
    left = (f'<g class="door dl"><rect x="0" y="34" width="{half}" height="{H - 34}" fill="{t["door"]}"/>'
            f'<rect x="0" y="34" width="{half}" height="{H - 34}" fill="url(#brush)"/>'
            f'<line x1="{half - 1}" y1="34" x2="{half - 1}" y2="{H}" stroke="{t["cyan"]}" stroke-width="2"/>'
            f'<text class="t" x="{half - 24}" y="{H / 2 + 22}" text-anchor="end" font-size="13" letter-spacing="6" fill="{t["muted"]}">SHINYQ</text></g>')
    right = (f'<g class="door dr"><rect x="{half}" y="34" width="{half}" height="{H - 34}" fill="{t["door"]}"/>'
             f'<rect x="{half}" y="34" width="{half}" height="{H - 34}" fill="url(#brush)"/>'
             f'<line x1="{half + 1}" y1="34" x2="{half + 1}" y2="{H}" stroke="{t["cyan"]}" stroke-width="2"/>'
             f'<text class="t" x="{half + 24}" y="{H / 2 + 22}" font-size="13" letter-spacing="6" fill="{t["muted"]}">HQ</text></g>')
    return left + right


def svg(theme: str) -> str:
    t = THEMES[theme]
    title = "Kurniadi Ahmad Wijaya, Forward Deployed AI Engineer, Jakarta. Elevator doors open on ShinyQ HQ at shinyq.my.id."
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-labelledby="title">
<title id="title">{title}</title>
<defs>
<style>
{font_faces(mono=True, display=True)}
.t{{font-family:{MONO};font-size:15px}}
.d{{font-family:{DISPLAY};font-weight:800;font-stretch:80%;font-variation-settings:"wght" 800,"wdth" 80}}
.name{{font-family:{DISPLAY};font-weight:800;font-stretch:76%;font-variation-settings:"wght" 800,"wdth" 76;font-size:68px;letter-spacing:.5px}}
.in{{animation:fade .22s ease-out backwards}}
.rise{{animation:rise .6s cubic-bezier(.2,.8,.2,1) backwards}}
.dl{{transform:translateX(-{W / 2 + 10}px);animation:open-l {DOOR_FOR}s cubic-bezier(.7,0,.25,1) {DOOR_AT}s backwards}}
.dr{{transform:translateX({W / 2 + 10}px);animation:open-r {DOOR_FOR}s cubic-bezier(.7,0,.25,1) {DOOR_AT}s backwards}}
.car{{transform:translateY(-{RIDE}px);animation:ride {STEP * 4:.2f}s ease-in-out backwards}}
.arrow{{opacity:.3;animation:arrow {STEP * 2:.2f}s ease-in-out 2}}
.beacon{{animation:pulse 1.8s ease-in-out infinite backwards}}
.cursor{{animation:blink 1s steps(1) infinite}}
.ring{{animation:chase 5s linear infinite}}
.scan{{animation:scan 7s linear infinite}}
.motes circle{{animation:drift 9s linear infinite}}
.rover-park{{display:none}}
@keyframes fade{{from{{opacity:0}}}}
@keyframes rise{{from{{opacity:0;transform:translateY(10px)}}}}
@keyframes open-l{{from{{transform:none}}}}
@keyframes open-r{{from{{transform:none}}}}
@keyframes ride{{0%{{transform:none}}25%{{transform:translateY(-{RIDE / 4:.0f}px)}}50%{{transform:translateY(-{RIDE / 2:.0f}px)}}75%{{transform:translateY(-{RIDE * 3 / 4:.0f}px)}}}}
@keyframes blip{{0%,100%{{opacity:1}}}}
@keyframes wait{{0%,100%{{opacity:0}}}}
@keyframes arrow{{50%{{opacity:1}}}}
@keyframes pulse{{0%,100%{{opacity:.3}}50%{{opacity:1}}}}
@keyframes blink{{50%{{opacity:0}}}}
@keyframes chase{{to{{stroke-dashoffset:-240}}}}
@keyframes scan{{from{{transform:translateY(-60px)}}to{{transform:translateY({H + 60}px)}}}}
@keyframes drift{{0%{{transform:translateY(0);opacity:0}}15%{{opacity:.8}}85%{{opacity:.5}}100%{{transform:translateY(-230px);opacity:0}}}}
@media (prefers-reduced-motion:reduce){{
*{{animation:none!important}}
.doors,.motes,.scan,.rover-move{{display:none}}
.rover-park{{display:inline}}
}}
</style>
{neon_gradient(t)}
<linearGradient id="beam" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="{t["cyan"]}" stop-opacity="0"/><stop offset="1" stop-color="{t["cyan"]}" stop-opacity=".08"/></linearGradient>
<linearGradient id="fadeg" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".25"/><stop offset="1" stop-color="#fff"/></linearGradient>
<radialGradient id="glowv" cx="880" cy="110" r="420" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="{t["violet"]}" stop-opacity=".26"/><stop offset="1" stop-color="{t["violet"]}" stop-opacity="0"/></radialGradient>
<radialGradient id="glowc" cx="140" cy="340" r="340" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="{t["cyan"]}" stop-opacity=".13"/><stop offset="1" stop-color="{t["cyan"]}" stop-opacity="0"/></radialGradient>
<radialGradient id="pool"><stop offset="0" stop-color="{t["cyan"]}" stop-opacity=".22"/><stop offset="1" stop-color="{t["cyan"]}" stop-opacity="0"/></radialGradient>
<pattern id="grid" width="32" height="32" patternUnits="userSpaceOnUse"><path d="M32 0H0V32" fill="none" stroke="{t["indigo"]}" stroke-opacity="{t["grid"]}"/></pattern>
<pattern id="brush" width="7" height="7" patternUnits="userSpaceOnUse"><path d="M0 0V7" stroke="{t["indigo"]}" stroke-opacity=".12"/></pattern>
<mask id="fade"><rect width="{W}" height="{H}" fill="url(#fadeg)"/></mask>
<filter id="glow" x="-10%" y="-40%" width="120%" height="180%"><feGaussianBlur stdDeviation="7"/></filter>
<filter id="soft" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="3"/></filter>
<clipPath id="card"><rect width="{W}" height="{H}" rx="18"/></clipPath>
</defs>
<g clip-path="url(#card)">
<rect width="{W}" height="{H}" fill="{t["bg"]}"/>
<rect width="{W}" height="{H}" fill="url(#glowv)"/>
<rect width="{W}" height="{H}" fill="url(#glowc)"/>
<rect width="{W}" height="{H}" fill="url(#grid)" mask="url(#fade)"/>
<rect class="scan" width="{W}" height="60" fill="url(#beam)"/>
{motes(t)}
{boot_lines(t)}
{readout(t)}
{tower(t)}
<g class="rise" style="animation-delay:{NAME_AT:.2f}s"><text class="name" x="42" y="282" fill="url(#neon)" filter="url(#glow)" opacity="{t["glow"]}">KURNIADI AHMAD WIJAYA</text><text class="name" x="42" y="282" fill="url(#neon)">KURNIADI AHMAD WIJAYA</text></g>
<text class="t rise" x="45" y="318" font-size="16" style="animation-delay:{NAME_AT + 0.3:.2f}s"><tspan fill="{t["cyan"]}">&gt; Forward Deployed AI Engineer</tspan><tspan fill="{t["dim"]}"> · </tspan><tspan fill="{t["text"]}">Jakarta</tspan><tspan fill="{t["dim"]}"> · </tspan><tspan fill="{t["violet"]}">shinyq.my.id</tspan><tspan class="cursor" fill="{t["cyan"]}"> _</tspan></text>
<g class="doors">{doors(t)}</g>
<rect width="{W}" height="34" fill="{t["bar"]}"/>
<line x1="0" y1="34" x2="{W}" y2="34" stroke="{t["line"]}"/>
<circle cx="24" cy="17" r="5.5" fill="#F87171"/><circle cx="42" cy="17" r="5.5" fill="#FBBF24"/><circle cx="60" cy="17" r="5.5" fill="#34D399"/>
<text class="t" x="{W / 2}" y="22" fill="{t["muted"]}" font-size="12" text-anchor="middle">visitor@shinyq.my.id: ~</text>
<text class="t" x="{W - 24}" y="22" fill="{t["dim"]}" font-size="11" letter-spacing="2" text-anchor="end">EN · ID</text>
</g>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="18" fill="none" stroke="{t["indigo"]}" stroke-opacity=".35"/>
</svg>
'''


if __name__ == "__main__":
    for theme in THEMES:
        write(ASSETS / asset_name("hq-header", theme), svg(theme))
