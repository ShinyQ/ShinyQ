"""Builds the README's small UI pieces under assets/ui/, each in a dark and a light variant.

- key-*.svg: call-to-action keys (Enter the 3D HQ, CV, LinkedIn, Email)
- floor-*.svg: the one-row floor directory, an elevator button per floor of the tower; the lit
  rings chase up from L1 to the roof like a car passing floors

Needs fonttools for text measurement: pip install fonttools brotli && python3 scripts/ui.py
"""
from hq import ASSETS, DISPLAY, THEMES, asset_name, font_faces, measure, text, write

UI = ASSETS / "ui"
ICONS = {
    "cube": '<path d="M8 1.5l6 3.3v6.4L8 14.5 2 11.2V4.8zM2 4.8l6 3.3 6-3.3M8 8.1v6.4"/>',
    "doc": '<path d="M4 1.5h5.5L12.5 4.5v10H4zM9.5 1.5v3h3M6.3 8h4M6.3 10.6h4"/>',
    "person": '<circle cx="8" cy="5.3" r="2.6"/><path d="M3 14.2c.8-2.9 2.7-4.4 5-4.4s4.2 1.5 5 4.4"/>',
    "mail": '<rect x="1.6" y="3.4" width="12.8" height="9.2" rx="1.6"/><path d="M2.2 4.4L8 8.8l5.8-4.4"/>',
    "lock": '<rect x="3" y="7" width="10" height="7" rx="1.5"/><path d="M5.2 7V5.2a2.8 2.8 0 0 1 5.6 0V7"/>',
}
KEYS = [
    ("enter-3d", "Enter the 3D HQ", "cube", True),
    ("cv", "CV", "doc", False),
    ("linkedin", "LinkedIn", "person", False),
    ("email", "Email", "mail", False),
]
FLOORS = [("L1", "Lobby"), ("L2", "Journey"), ("L3", "Work"), ("L4", "Writing"), ("RF", "About"), ("B1", "Engine Room")]
PRIMARY_FILL, PRIMARY_INK = "#6EE7FF", "#071229"
H, LABEL = 44, 16
LABEL_CSS = f'.l{{font-family:{DISPLAY};font-weight:600;font-stretch:92%;font-variation-settings:"wght" 600,"wdth" 92;font-size:{LABEL}px}}'


def icon(name: str, x: float, y: float, color: str, width: float = 1.6) -> str:
    return (f'<g transform="translate({x:.1f} {y:.1f})" fill="none" stroke="{color}" stroke-width="{width}" '
            f'stroke-linecap="round" stroke-linejoin="round">{ICONS[name]}</g>')


def key(theme: str, label: str, glyph: str, primary: bool) -> str:
    t = THEMES[theme]
    pad = 18
    w = round(pad + 16 + 9 + measure(label, LABEL) + pad)
    if primary:
        fill, ink, ico, stroke = PRIMARY_FILL, PRIMARY_INK, PRIMARY_INK, "#0E7490" if theme == "light" else PRIMARY_FILL
        sheen = f'<g clip-path="url(#k)"><rect class="sheen" x="-60" y="0" width="34" height="{H}" fill="#fff" opacity=".5"/></g>'
    else:
        fill, ink, ico, stroke, sheen = t["panel"], t["text"], t["cyan"], t["line"], ""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {H}" width="{w}" height="{H}" role="img" aria-label="{text(label)}">
<defs><style>{font_faces(mono=False, display=True)}
{LABEL_CSS}
.sheen{{transform:skewX(-20deg);animation:sheen 5s ease-in-out 1.2s infinite}}
@keyframes sheen{{0%{{transform:skewX(-20deg) translateX(0)}}35%,100%{{transform:skewX(-20deg) translateX({w + 120}px)}}}}
@media (prefers-reduced-motion:reduce){{.sheen{{animation:none;display:none}}}}
</style><clipPath id="k"><rect x="1" y="1" width="{w - 2}" height="{H - 2}" rx="11"/></clipPath></defs>
<rect x="1" y="1" width="{w - 2}" height="{H - 2}" rx="11" fill="{fill}" stroke="{stroke}"/>
{sheen}
{icon(glyph, pad, (H - 16) / 2, ico)}
<text class="l" x="{pad + 25}" y="{H / 2 + 5.6:.1f}" fill="{ink}">{text(label)}</text>
</svg>
'''


def floor(theme: str, code: str, label: str, slot: int) -> str:
    t = THEMES[theme]
    d = 32
    locked = code == "B1"
    accent = t["warn"] if locked else t["cyan"]
    tw = measure(label, LABEL)
    w = round(6 + d + 10 + tw + (34 if locked else 18))
    cx, cy = 6 + d / 2, H / 2
    lock = icon("lock", 6 + d + 10 + tw + 7, cy - 8, t["dim"], 1.4) if locked else ""
    chase = "" if locked else f".lit{{animation:chase 4.2s ease-in-out {slot * 0.42:.2f}s infinite}}"
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {H}" width="{w}" height="{H}" role="img" aria-label="{code} {text(label)}{" (locked in 3D)" if locked else ""}">
<defs><style>{font_faces(mono=False, display=True)}
{LABEL_CSS}
.c{{font-family:{DISPLAY};font-weight:800;font-stretch:80%;font-variation-settings:"wght" 800,"wdth" 80;font-size:14px}}
{chase}
@keyframes chase{{0%,30%,100%{{opacity:.45}}8%{{opacity:1}}}}
@media (prefers-reduced-motion:reduce){{.lit{{animation:none}}}}
</style>
<filter id="g" x="-40%" y="-40%" width="180%" height="180%"><feGaussianBlur stdDeviation="2"/></filter></defs>
<rect x="1" y="1" width="{w - 2}" height="{H - 2}" rx="{H / 2 - 1}" fill="{t["panel"]}" stroke="{t["line"]}"/>
<circle cx="{cx}" cy="{cy}" r="{d / 2}" fill="{t["bar"]}"/>
<g class="lit" opacity="{.45 if locked else 1}"><circle cx="{cx}" cy="{cy}" r="{d / 2 - 2}" fill="none" stroke="{accent}" stroke-width="2.6" filter="url(#g)" opacity="{t["glow"] + .2:.2f}"/>
<circle cx="{cx}" cy="{cy}" r="{d / 2 - 2}" fill="none" stroke="{accent}" stroke-width="1.6"/></g>
<text class="c" x="{cx}" y="{cy + 5}" text-anchor="middle" fill="{t["dim"] if locked else t["cyan"]}">{code}</text>
<text class="l" x="{6 + d + 10}" y="{cy + 5.6:.1f}" fill="{t["dim"] if locked else t["text"]}">{text(label)}</text>
{lock}
</svg>
'''


if __name__ == "__main__":
    for theme in THEMES:
        for slug, label, glyph, primary in KEYS:
            write(UI / asset_name(f"key-{slug}", theme), key(theme, label, glyph, primary))
        for slot, (code, label) in enumerate(FLOORS):
            write(UI / asset_name(f"floor-{code.lower()}", theme), floor(theme, code, label, slot))
