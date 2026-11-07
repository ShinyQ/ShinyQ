"""Rebuilds assets/fonts/archivo-display.woff2, the Archivo subset the SVG assets embed.

Source font: Archivo[wdth,wght].ttf from https://github.com/google/fonts/tree/main/ofl/archivo
(SIL Open Font License 1.1, see assets/fonts/LICENSE-Archivo.txt). The axes are trimmed to the
weights and widths the assets use and the glyphs to Latin letters, digits and basic punctuation.

Run: pip install fonttools brotli && python3 scripts/fonts.py path/to/Archivo[wdth,wght].ttf
"""
import string
import sys
from pathlib import Path

from fontTools import subset
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer

OUT = Path(__file__).resolve().parent.parent / "assets" / "fonts" / "archivo-display.woff2"
GLYPHS = string.ascii_letters + string.digits + " !%&'()+,-./:;?·~"


def main(src: str) -> None:
    font = instancer.instantiateVariableFont(TTFont(src), {"wght": (600, 800), "wdth": (72, 92)})
    options = subset.Options()
    options.flavor = "woff2"
    options.layout_features = ["kern", "liga", "lnum", "tnum"]
    subsetter = subset.Subsetter(options)
    subsetter.populate(text=GLYPHS)
    subsetter.subset(font)
    font.flavor = "woff2"
    font.save(OUT)
    print(f"wrote {OUT.name} ({OUT.stat().st_size:,} bytes)")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    main(sys.argv[1])
