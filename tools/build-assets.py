#!/usr/bin/env python3
"""Собирает og-cover.jpg (1200×630) и apple-touch-icon.png (180×180) из ava-600.jpg.

    pip install Pillow
    python3 tools/build-assets.py

Шрифты берутся из системы. Если автопоиск не сработал, укажи файлы явно:

    SERIF_TTF=/path/Lora-Regular.ttf MONO_TTF=/path/JetBrainsMono-Regular.ttf \
        python3 tools/build-assets.py

Важно: шрифты должны содержать кириллицу — на карточке есть русский текст.
"""

import os
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "ava-600.jpg"

# палитра Anthropic
BONE = (240, 238, 230)
INK = (20, 20, 19)
MUTED = (99, 96, 90)
CLAY = (204, 120, 92)
LINE = (218, 214, 200)

SERIF_CANDIDATES = [
    "/usr/share/fonts/truetype/lora/Lora-Regular.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf",
    "/System/Library/Fonts/Supplemental/Georgia.ttf",
    "C:/Windows/Fonts/georgia.ttf",
]
MONO_CANDIDATES = [
    "/usr/share/fonts/truetype/jetbrains-mono/JetBrainsMono-Regular.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf",
    "/System/Library/Fonts/Menlo.ttc",
    "C:/Windows/Fonts/consola.ttf",
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
    sys.exit(
        f"Не нашёл {label}-шрифт. Укажи его явно: {env_var}=/path/to/font.ttf "
        f"python3 tools/build-assets.py"
    )


def main():
    if not SRC.exists():
        sys.exit(f"Нет исходника {SRC}")

    serif_path = pick_font("SERIF_TTF", SERIF_CANDIDATES, "серифный")
    mono_path = pick_font("MONO_TTF", MONO_CANDIDATES, "моноширинный")

    src = Image.open(SRC).convert("RGB")

    # 1) иконка для iOS
    icon = ROOT / "apple-touch-icon.png"
    src.resize((180, 180), Image.LANCZOS).save(icon, optimize=True)
    print(f"✓ {icon.name} — 180×180")

    # 2) карточка превью
    W, H = 1200, 630
    og = Image.new("RGB", (W, H), BONE)
    d = ImageDraw.Draw(og)
    d.rectangle([40, 40, W - 41, H - 41], outline=LINE, width=1)

    size, ax, ay, radius = 300, 96, 165, 44
    mask = Image.new("L", (size * 4, size * 4), 0)
    ImageDraw.Draw(mask).rounded_rectangle(
        [0, 0, size * 4 - 1, size * 4 - 1], radius=radius * 4, fill=255
    )
    og.paste(
        src.resize((size, size), Image.LANCZOS),
        (ax, ay),
        mask.resize((size, size), Image.LANCZOS),
    )

    tx = ax + size + 68
    serif = ImageFont.truetype(serif_path, 92)
    mono = ImageFont.truetype(mono_path, 26)
    mono_s = ImageFont.truetype(mono_path, 19)

    d.text((tx, 196), "ЛИЧНАЯ СТРАНИЦА", font=mono_s, fill=CLAY)
    d.text((tx, 236), "Samuray43k", font=serif, fill=INK)
    d.text((tx, 352), "лютый вайбкодер", font=mono, fill=MUTED)
    d.line([tx, 410, tx + 90, 410], fill=CLAY, width=3)
    d.text((tx, 436), "telegram · github · tiktok", font=mono_s, fill=MUTED)

    cover = ROOT / "og-cover.jpg"
    og.save(cover, quality=88, optimize=True, progressive=True)
    print(f"✓ {cover.name} — {W}×{H}")


if __name__ == "__main__":
    main()
