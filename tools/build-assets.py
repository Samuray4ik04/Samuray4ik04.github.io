#!/usr/bin/env python3
"""Собирает og-cover.jpg (1200×630) и apple-touch-icon.png (180×180) из ava-600.jpg.

    pip install Pillow
    python3 tools/build-assets.py

Карточка печатается теми же шрифтами, что и страница. Скачай их с Google Fonts
(Oswald, PT Mono, Caveat) и укажи файлы:

    STENCIL_TTF=/path/Oswald.ttf MONO_TTF=/path/PTM55FT.ttf MARKER_TTF=/path/Caveat.ttf \
        python3 tools/build-assets.py

Без явных путей скрипт поищет шрифты в системе. Кириллица обязательна —
на карточке русский текст.
"""

import os
import random
import sys
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "ava-600.jpg"

# краски зина
NEWS = (220, 216, 203)
SOOT = (20, 17, 14)
SOOT_2 = (74, 68, 60)
RIOT = (232, 68, 58)
RIOT_INK = (168, 18, 25)

STENCIL_CANDIDATES = [
    "/usr/share/fonts/truetype/oswald/Oswald-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/System/Library/Fonts/Supplemental/Impact.ttf",
    "C:/Windows/Fonts/impact.ttf",
]
MONO_CANDIDATES = [
    "/usr/share/fonts/truetype/pt-mono/PTMono-Regular.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf",
    "/System/Library/Fonts/Menlo.ttc",
    "C:/Windows/Fonts/consola.ttf",
]
MARKER_CANDIDATES = [
    "/usr/share/fonts/truetype/caveat/Caveat-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
    "/System/Library/Fonts/Supplemental/Bradley Hand Bold.ttf",
]


def pick_font(env_var, candidates, label):
    explicit = os.environ.get(env_var)
    if explicit:
        if not Path(explicit).exists():
            sys.exit(f"{env_var}={explicit} — файл не найден")
        return explicit
    for path in candidates:
        if Path(path).exists():
            return path
    sys.exit(f"Не нашёл {label}-шрифт. Укажи его явно: {env_var}=/path/to/font.ttf")


def load(path, size, weight=None):
    font = ImageFont.truetype(path, size)
    if weight is not None:
        try:
            font.set_variation_by_axes([weight])
        except Exception:
            pass
    return font


def text_ls(draw, xy, text, font, fill, spacing=0):
    """Текст с разрядкой — Pillow сам так не умеет. Возвращает ширину."""
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=font, fill=fill)
        x += draw.textlength(ch, font=font) + spacing
    return x - xy[0]


def halftone(img, size):
    """Фотография как из ксерокса: серая, контрастная, в точку."""
    photo = ImageOps.autocontrast(img.convert("L"), cutoff=2).resize(
        (size, size), Image.LANCZOS
    )
    photo = Image.eval(photo, lambda v: min(255, int(20 + v * 1.06)))

    screen = Image.new("L", (size, size), 255)
    dots = ImageDraw.Draw(screen)
    for y in range(0, size, 3):
        for x in range(0, size, 3):
            dots.point((x, y), fill=170)

    return ImageChops.multiply(photo, screen).convert("RGB")


def grain(img, amount=14):
    """Грязь тонера."""
    noise = Image.effect_noise(img.size, 22).convert("L")
    return Image.blend(img, ImageChops.multiply(img, noise.convert("RGB")), amount / 100)


def main():
    if not SRC.exists():
        sys.exit(f"Нет исходника {SRC}")

    stencil_path = pick_font("STENCIL_TTF", STENCIL_CANDIDATES, "узкий гротеск")
    mono_path = pick_font("MONO_TTF", MONO_CANDIDATES, "моноширинный")
    marker_path = pick_font("MARKER_TTF", MARKER_CANDIDATES, "рукописный")

    random.seed(43)
    src = Image.open(SRC).convert("RGB")

    # 1) иконка для iOS
    icon = ROOT / "apple-touch-icon.png"
    src.resize((180, 180), Image.LANCZOS).save(icon, optimize=True)
    print(f"✓ {icon.name} — 180×180")

    # 2) карточка превью
    W, H = 1200, 630
    og = Image.new("RGB", (W, H), NEWS)
    d = ImageDraw.Draw(og)

    mono_s = load(mono_path, 21)
    stencil_xl = load(stencil_path, 132, weight=700)
    stencil_m = load(stencil_path, 34, weight=500)
    marker = load(marker_path, 34, weight=700)

    # колонтитул
    text_ls(d, (72, 60), "САМИЗДАТ № 43 · ТИРАЖ 1 ЭКЗ.", mono_s, SOOT_2, spacing=3)
    d.line([72, 104, W - 72, 104], fill=SOOT, width=3)

    # фотография: чёрный прогон и красный, который не попал
    ph, px, py = 300, 72, 190
    d.rectangle([px + 14, py + 14, px + ph + 13, py + ph + 13], outline=RIOT, width=4)
    og.paste(halftone(src, ph), (px, py))
    tape = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(tape).rectangle([px - 26, py - 12, px + 74, py + 14], fill=(255, 255, 255, 105))
    og.paste(Image.alpha_composite(og.convert("RGBA"), tape).convert("RGB"))

    # имя
    tx = px + ph + 74
    d.text((tx, 158), "SAMURAY", font=stencil_xl, fill=SOOT)
    x2 = tx
    d.text((x2, 262), "43", font=stencil_xl, fill=RIOT_INK)
    x2 += d.textlength("43", font=stencil_xl)
    d.text((x2, 262), "K", font=stencil_xl, fill=SOOT)

    # красная плашка с ролью, положена косо
    band = Image.new("RGBA", (520, 96), (0, 0, 0, 0))
    bd = ImageDraw.Draw(band)
    role = "ЛЮТЫЙ ВАЙБКОДЕР"
    wide = sum(bd.textlength(c, font=stencil_m) + 5 for c in role)
    bd.rectangle([0, 0, wide + 40, 62], fill=RIOT)
    text_ls(bd, (20, 6), role, stencil_m, SOOT, spacing=5)
    band = band.rotate(1.4, resample=Image.BICUBIC, expand=True)
    og.paste(band, (tx - 6, 430), band)

    # низ
    text_ls(d, (tx, 528), "TELEGRAM · GITHUB · TIKTOK", mono_s, SOOT_2, spacing=4)
    d.text((tx, 560), "копируй свободно", font=marker, fill=RIOT_INK)

    og = grain(og)

    cover = ROOT / "og-cover.jpg"
    og.save(cover, quality=88, optimize=True, progressive=True)
    print(f"✓ {cover.name} — {W}×{H}")


if __name__ == "__main__":
    main()
