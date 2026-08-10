# samuray4ik04.github.io

Личная страница-визитка. Один HTML-файл, без сборки и зависимостей.

**→ https://samuray4ik04.github.io/**

## Что внутри

| Файл | Назначение |
|---|---|
| `index.html` | вся страница: разметка, стили и скрипт в одном файле |
| `404.html` | страница «не найдено» в том же оформлении |
| `ava-600.webp` / `.jpg` | аватар, 600×600 (webp с jpg-фолбэком) |
| `og-cover.jpg` | карточка превью 1200×630 для Telegram, X и прочих |
| `favicon.png`, `apple-touch-icon.png` | иконки, 64×64 и 180×180 |

## Оформление

Палитра и типографика в духе Anthropic:

- **цвета** — ivory `#F0EEE6`, book cloth `#CC785C`, kraft `#D4A27F`, slate `#141413`;
- **шрифты** — [Source Serif 4](https://fonts.google.com/specimen/Source+Serif+4) для текста, [JetBrains Mono](https://fonts.google.com/specimen/JetBrains+Mono) для подписей;
- тёмная тема через `prefers-color-scheme`, все пары цветов проходят WCAG AA (≥ 4.5:1);
- анимации отключаются при `prefers-reduced-motion` и встают на паузу, когда вкладка скрыта.

## Разработка

Сборка не нужна — достаточно открыть файл или поднять любой статический сервер:

```sh
python3 -m http.server 8000
```

Деплой: пуш в `master`, дальше GitHub Pages сам.

## Пересоздать ассеты

`og-cover.jpg` и `apple-touch-icon.png` собираются из `ava-600.jpg` скриптом `tools/build-assets.py`:

```sh
pip install Pillow
python3 tools/build-assets.py
```
