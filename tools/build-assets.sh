#!/usr/bin/env sh
# Пересобирает og-cover.jpg (1200×630) из tools/og-card.html.
# Карточка рисуется тем же браузером и теми же шрифтами, что и сама страница,
# поэтому превью не разъезжается с дизайном.
#
#   sh tools/build-assets.sh [путь-к-chromium]
#
# Нужны chromium (или chrome) и ImageMagick.
set -e
cd "$(dirname "$0")/.."
BROWSER="${1:-chromium-browser}"

"$BROWSER" --headless --no-sandbox --disable-gpu --hide-scrollbars \
  --virtual-time-budget=6000 --window-size=1200,630 \
  --screenshot="$PWD/og-cover.png" "file://$PWD/tools/og-card.html"

magick og-cover.png -quality 90 og-cover.jpg
rm -f og-cover.png
echo "og-cover.jpg готов"
