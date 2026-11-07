"""Shared look for the README assets: the two themes, the embedded fonts and small SVG helpers.

GitHub serves README images through a proxy that cannot load web fonts, so every SVG embeds its
fonts as WOFF2 data URIs. The palette follows the 3D Highlights Hall at https://shinyq.my.id:
deep indigo, cyan #6ee7ff and violet #a78bfa, with a light twin for GitHub's light theme.
"""
import base64
from functools import cache
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
SITE = "https://shinyq.my.id"

THEMES = {
    "dark": {
        "bg": "#0B0A20", "panel": "#121131", "bar": "#100F2A", "line": "#2A2A5C",
        "text": "#E7E9FF", "muted": "#8D90BC", "dim": "#5B5E8C",
        "cyan": "#6EE7FF", "indigo": "#818CF8", "violet": "#A78BFA", "ok": "#34D399", "warn": "#F472B6",
        "glow": 0.55, "grid": 0.10, "window": "#E0F7FF", "door": "#15143A",
    },
    "light": {
        "bg": "#F6F7FF", "panel": "#FFFFFF", "bar": "#ECEEFF", "line": "#CDD0F5",
        "text": "#151738", "muted": "#555A85", "dim": "#9095BE",
        "cyan": "#0E7490", "indigo": "#4F46E5", "violet": "#7C3AED", "ok": "#047857", "warn": "#BE185D",
        "glow": 0.18, "grid": 0.09, "window": "#FFFFFF", "door": "#E3E5FF",
    },
}


def asset_name(stem: str, theme: str) -> str:
    """Dark keeps the bare name, so links to the original file keep working."""
    return f"{stem}.svg" if theme == "dark" else f"{stem}-light.svg"


@cache
def _font(name: str) -> str:
    return base64.b64encode((ASSETS / "fonts" / name).read_bytes()).decode()


def font_faces(mono: bool = True, display: bool = False) -> str:
    out = []
    if mono:
        out.append(f'@font-face{{font-family:"HQ Mono";src:url(data:font/woff2;base64,{_font("jetbrains-mono-subset.woff2")}) format("woff2");font-weight:400 700}}')
    if display:
        out.append(f'@font-face{{font-family:"HQ Display";src:url(data:font/woff2;base64,{_font("archivo-display.woff2")}) format("woff2");font-weight:600 800;font-stretch:72% 92%}}')
    return "".join(out)


MONO = '"HQ Mono",ui-monospace,SFMono-Regular,Menlo,Consolas,monospace'
DISPLAY = '"HQ Display","Arial Narrow",Arial,sans-serif'


def neon_gradient(t: dict, gid: str = "neon", vertical: bool = False) -> str:
    axis = 'x1="0" x2="0" y1="0" y2="1"' if vertical else 'x1="0" x2="1"'
    return (f'<linearGradient id="{gid}" {axis}><stop offset="0" stop-color="{t["cyan"]}"/>'
            f'<stop offset=".55" stop-color="{t["indigo"]}"/><stop offset="1" stop-color="{t["violet"]}"/></linearGradient>')


def text(s: str) -> str:
    return escape(s, quote=False)


@cache
def _display_at(wght: int, wdth: int):
    from fontTools.ttLib import TTFont  # only the UI kit needs fonttools: pip install fonttools brotli
    from fontTools.varLib import instancer

    font = instancer.instantiateVariableFont(TTFont(ASSETS / "fonts" / "archivo-display.woff2"), {"wght": wght, "wdth": wdth})
    return font.getBestCmap(), font["hmtx"], font["head"].unitsPerEm


def measure(s: str, size: float, wght: int = 600, wdth: int = 92) -> float:
    """Advance width of `s` in the embedded display font, without kerning (close enough for padding)."""
    cmap, hmtx, upm = _display_at(wght, wdth)
    return sum(hmtx[cmap[ord(c)]][0] for c in s) * size / upm


def write(path: Path, svg: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(svg)
    print(f"wrote {path.relative_to(ROOT)} ({path.stat().st_size:,} bytes)")
