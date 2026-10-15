"""Builds assets/hq-header.svg: the ShinyQ HQ boot sequence header.

Fonts are embedded as subset WOFF2 data URIs because GitHub serves README
images through a proxy that cannot load web fonts. Animations are CSS so
prefers-reduced-motion shows the final frame. Run: python3 scripts/header.py
"""
import base64
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CYAN, INDIGO, VIOLET = "#22D3EE", "#6366F1", "#8B5CF6"
BG, TEXT, MUTED, OK = "#0B1020", "#C9D1D9", "#7D8590", "#34D399"
W, H = 1200, 300


def font(name: str) -> str:
    return base64.b64encode((ROOT / "assets" / "fonts" / name).read_bytes()).decode()


BOOT = [
    ("power on", "tower online"),
    ("L1 Lobby", "stats ring, skills wall"),
    ("L2 Career Road", "2019 to 2026"),
    ("L3 Labs", "AI and product case studies"),
    ("L4 Writing", "papers, posts, talks"),
    ("RF Roof", "contact uplink"),
]
FLOORS = ["L1", "L2", "L3", "L4", "RF"]
STEP = 0.32
FIRST = 0.55  # the ssh prompt types first
NAME_AT = FIRST + STEP * len(BOOT) + 0.35


def boot_lines() -> str:
    out = [f'<text class="t a" x="44" y="64" fill="{TEXT}" style="animation-delay:.15s"><tspan fill="{CYAN}">$</tspan> ssh visitor@shinyq-hq</text>']
    for i, (key, value) in enumerate(BOOT):
        dots = "." * (18 - len(key))
        y = 64 + (i + 1) * 20
        out.append(
            f'<text class="t a" x="44" y="{y}" style="animation-delay:{FIRST + STEP * i:.2f}s">'
            f'<tspan fill="{MUTED}">[ </tspan><tspan fill="{OK}">OK</tspan><tspan fill="{MUTED}"> ] </tspan>'
            f'<tspan fill="{TEXT}">{key} </tspan><tspan fill="{MUTED}">{dots} </tspan><tspan fill="{TEXT}">{value}</tspan></text>'
        )
    return "".join(out)


def tower() -> str:
    x0, w, fh, gap, base = 960, 150, 30, 8, 236
    parts = [
        f'<rect x="{x0 - 26}" y="{base + 4}" width="{w + 52}" height="6" rx="3" fill="{INDIGO}" opacity=".45"/>',
        f'<line x1="{x0 + w + 16}" y1="{base}" x2="{x0 + w + 16}" y2="{base - 5 * (fh + gap) + gap}" stroke="{CYAN}" stroke-opacity=".3" stroke-dasharray="3 4"/>',
    ]
    for i, label in enumerate(FLOORS):
        y = base - (i + 1) * (fh + gap) + gap
        delay = FIRST + STEP * (i + 1)
        parts.append(f'<rect x="{x0}" y="{y}" width="{w}" height="{fh}" rx="4" fill="#0F172A" stroke="{CYAN}" stroke-opacity=".35"/>')
        parts.append(f'<rect class="a lit" x="{x0 + 4}" y="{y + 4}" width="{w - 8}" height="{fh - 8}" rx="2" fill="url(#neon)" style="animation-delay:{delay:.2f}s"/>')
        for k in range(6):
            parts.append(f'<rect class="a" x="{x0 + 14 + k * 22}" y="{y + 11}" width="10" height="8" rx="1" fill="#E0F2FE" opacity="0" style="animation-delay:{delay + 0.05:.2f}s;--o:.55"/>')
        parts.append(f'<text class="t" x="{x0 - 12}" y="{y + 20}" fill="{MUTED}" font-size="12" text-anchor="end">{label}</text>')
    top = base - 5 * (fh + gap) + gap
    parts.append(f'<line x1="{x0 + w / 2}" y1="{top}" x2="{x0 + w / 2}" y2="{top - 22}" stroke="{CYAN}" stroke-width="2"/>')
    parts.append(f'<circle class="beacon" cx="{x0 + w / 2}" cy="{top - 26}" r="4" fill="{CYAN}" style="animation-delay:{NAME_AT:.2f}s"/>')
    # elevator car rides from L1 to RF in step with the boot log
    parts.append(f'<rect class="car" x="{x0 + w + 10}" y="{base - fh}" width="12" height="{fh - 6}" rx="2" fill="{CYAN}"/>')
    return "".join(parts)


def svg() -> str:
    rise = 5 * 38 - 38  # four floor steps of fh+gap
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-labelledby="title">
<title id="title">Kurniadi Ahmad Wijaya, AI and Software Engineer, Jakarta</title>
<defs>
<style>
@font-face{{font-family:"HQ Mono";src:url(data:font/woff2;base64,{font("jetbrains-mono-subset.woff2")}) format("woff2");font-weight:400 700}}
@font-face{{font-family:"HQ Display";src:url(data:font/woff2;base64,{font("archivo-name.woff2")}) format("woff2");font-weight:600 800;font-stretch:72% 92%}}
.t{{font-family:"HQ Mono",ui-monospace,Menlo,Consolas,monospace;font-size:15px}}
.name{{font-family:"HQ Display","Arial Narrow",sans-serif;font-weight:800;font-stretch:76%;font-variation-settings:"wght" 800,"wdth" 76;font-size:66px;letter-spacing:.5px}}
.a{{opacity:0;animation:show .18s ease-out forwards}}
.lit{{animation:show .25s ease-out forwards}}
.late{{opacity:0;animation:rise .5s cubic-bezier(.2,.8,.2,1) {NAME_AT:.2f}s forwards}}
.late2{{opacity:0;animation:rise .5s cubic-bezier(.2,.8,.2,1) {NAME_AT + 0.25:.2f}s forwards}}
.cursor{{animation:blink 1s steps(1) infinite}}
.beacon{{opacity:.2;animation:pulse 1.6s ease-in-out infinite}}
.car{{animation:ride {STEP * 5:.2f}s ease-in-out {FIRST:.2f}s forwards}}
.scan{{animation:scan 6s linear infinite}}
@keyframes show{{to{{opacity:var(--o,1)}}}}
@keyframes rise{{from{{opacity:0;transform:translateY(8px)}}to{{opacity:1;transform:none}}}}
@keyframes blink{{50%{{opacity:0}}}}
@keyframes pulse{{50%{{opacity:1}}}}
@keyframes ride{{0%{{transform:translateY(0)}}20%{{transform:translateY(-38px)}}40%{{transform:translateY(-76px)}}60%{{transform:translateY(-114px)}}80%,100%{{transform:translateY(-{rise}px)}}}}
@keyframes scan{{from{{transform:translateY(-40px)}}to{{transform:translateY({H + 40}px)}}}}
@media (prefers-reduced-motion:reduce){{
.a,.lit,.late,.late2{{animation:none;opacity:var(--o,1);transform:none}}
.car{{animation:none;transform:translateY(-{rise}px)}}
.cursor,.beacon,.scan{{animation:none}}.beacon{{opacity:1}}.scan{{display:none}}
}}
</style>
<linearGradient id="neon" x1="0" x2="1"><stop offset="0" stop-color="{CYAN}"/><stop offset=".55" stop-color="{INDIGO}"/><stop offset="1" stop-color="{VIOLET}"/></linearGradient>
<linearGradient id="beam" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="{CYAN}" stop-opacity="0"/><stop offset="1" stop-color="{CYAN}" stop-opacity=".07"/></linearGradient>
<pattern id="grid" width="32" height="32" patternUnits="userSpaceOnUse"><path d="M32 0H0V32" fill="none" stroke="{INDIGO}" stroke-opacity=".10"/></pattern>
<filter id="glow" x="-10%" y="-40%" width="120%" height="180%"><feGaussianBlur stdDeviation="5"/></filter>
<clipPath id="card"><rect width="{W}" height="{H}" rx="16"/></clipPath>
</defs>
<g clip-path="url(#card)">
<rect width="{W}" height="{H}" fill="{BG}"/>
<rect width="{W}" height="{H}" fill="url(#grid)"/>
<rect class="scan" width="{W}" height="40" fill="url(#beam)"/>
<rect width="{W}" height="34" fill="#0E1528"/>
<circle cx="24" cy="17" r="5.5" fill="#F87171"/><circle cx="42" cy="17" r="5.5" fill="#FBBF24"/><circle cx="60" cy="17" r="5.5" fill="#34D399"/>
<text class="t" x="{W / 2}" y="22" fill="{MUTED}" font-size="12" text-anchor="middle">visitor@shinyq-hq: ~</text>
{boot_lines()}
<g class="late"><text class="name" x="44" y="250" fill="url(#neon)" filter="url(#glow)" opacity=".45">KURNIADI AHMAD WIJAYA</text><text class="name" x="44" y="250" fill="url(#neon)">KURNIADI AHMAD WIJAYA</text></g>
<text class="t late2" x="46" y="282" fill="{CYAN}" font-size="16">&gt; AI and Software Engineer <tspan fill="{MUTED}">·</tspan> Jakarta<tspan class="cursor"> _</tspan></text>
{tower()}
</g>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="16" fill="none" stroke="{INDIGO}" stroke-opacity=".35"/>
</svg>
'''


if __name__ == "__main__":
    out = ROOT / "assets" / "hq-header.svg"
    out.write_text(svg())
    print(f"wrote {out.relative_to(ROOT)} ({out.stat().st_size} bytes)")
