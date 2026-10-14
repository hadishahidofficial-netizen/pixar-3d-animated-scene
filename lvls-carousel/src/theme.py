"""LVLS Agency — carousel design system: palettes, fonts, layout metrics."""
from pathlib import Path

from PIL import ImageFont

ROOT = Path(__file__).resolve().parent.parent
FONT_DIR = ROOT / "assets" / "fonts"
OUT_DIR = ROOT / "exports"

# ---------------------------------------------------------------- palettes ---
def mix(a, b, t):
    """Opaque blend of two RGB triples (ImageDraw cannot alpha-composite)."""
    return tuple(int(round(a[i] + (b[i] - a[i]) * t)) for i in range(3))


def _build(bg_top, bg_bottom, white, ink, accent, accent_soft, accent_ink,
           ghost_rgb, ghost_a, vignette, noise, glow_alpha):
    bg_mid = mix(bg_top, bg_bottom, 0.55)
    return {
        "bg_top": bg_top,
        "bg_bottom": bg_bottom,
        # pre-blended (opaque) UI tones — ImageDraw writes pixels, no blending
        "surface": mix(bg_mid, white, 0.055),
        "surface_strong": mix(bg_mid, white, 0.10),
        "stroke": mix(bg_mid, white, 0.17),
        "stroke_soft": mix(bg_mid, white, 0.085),
        "ink": ink,
        "ink_dim": mix(ink, bg_mid, 0.38),
        "ink_faint": mix(ink, bg_mid, 0.62),
        "accent": accent,
        "accent_soft": accent_soft,
        "accent_ink": accent_ink,
        "ghost": (*ghost_rgb, ghost_a),   # composited via alpha layer, RGBA ok
        "vignette": vignette,
        "noise": noise,
        "glow": accent,
        "glow_alpha": glow_alpha,
    }


PALETTES = {
    "dark": _build(
        bg_top=(15, 15, 17), bg_bottom=(30, 29, 33),
        white=(255, 255, 255), ink=(245, 243, 238),
        accent=(255, 106, 0), accent_soft=(255, 168, 92),
        accent_ink=(255, 248, 240),
        ghost_rgb=(255, 255, 255), ghost_a=15,
        vignette=62, noise=4, glow_alpha=30,
    ),
    "light": _build(
        bg_top=(246, 243, 237), bg_bottom=(229, 224, 214),
        white=(18, 18, 20), ink=(20, 19, 21),
        accent=(224, 72, 0), accent_soft=(198, 62, 0),
        accent_ink=(255, 250, 245),
        ghost_rgb=(20, 19, 21), ghost_a=16,
        vignette=24, noise=3, glow_alpha=18,
    ),
}

BRAND = "LVLS AGENCY"
BRAND_LINE = "EMAIL FLOWS FOR FASHION BRANDS"
HANDLE_PLACEHOLDER = "@yourhandle"

# ------------------------------------------------------------------- fonts ---
_FONT_FILES = {
    "disp": "ArchivoExpanded-Black.ttf",
    "disp_xb": "ArchivoExpanded-ExtraBold.ttf",
    "disp_b": "ArchivoExpanded-Bold.ttf",
    "disp_m": "ArchivoExpanded-Medium.ttf",
    "head": "Archivo-Black.ttf",
    "body_b": "ArchivoCondensed-Bold.ttf",
    "body_m": "ArchivoCondensed-Medium.ttf",
    "label": "Archivo-Medium.ttf",
    "num": "ArchivoCondensed-Bold.ttf",
    "serif": "InstrumentSerif-Italic.ttf",
    "blk_it": "Archivo-BlackItalic.ttf",
    "bold": "Archivo-Bold.ttf",
    "cond_bi": "ArchivoCondensed-BoldItalic.ttf",
}
_cache: dict[tuple[str, int], ImageFont.FreeTypeFont] = {}


def font(key: str, size: int) -> ImageFont.FreeTypeFont:
    size = max(4, int(round(size)))
    ck = (key, size)
    if ck not in _cache:
        _cache[ck] = ImageFont.truetype(str(FONT_DIR / _FONT_FILES[key]), size)
    return _cache[ck]


# ------------------------------------------------------------------ layout ---
class Layout:
    """Proportional layout metrics, derived from the slide box."""

    def __init__(self, w: int, h: int):
        self.w, self.h = w, h
        self.s = w / 1080.0                     # horizontal scale
        self.v = h / 1350.0                     # vertical scale
        self.m = round(76 * self.s)             # side margin
        self.top_y = round(74 * self.v)
        self.r = round(18 * self.s)             # generic corner radius
        self.sw = round(4.2 * self.s)           # generic stroke width


def px(v: float, s: float) -> int:
    return int(round(v * s))
