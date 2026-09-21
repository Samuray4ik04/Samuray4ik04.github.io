(() => {
  const artwork = document.querySelector(".artwork");
  if (!artwork) return;

  const LINES = {
    mahiru: [
      "Опять не поел? Я принесла бенто.",
      "Не сиди до утра за кодом, ладно?",
      "Это не для тебя. Просто… лишнее осталось.",
      "Хмф. Только не простудись.",
      "Ты опять забыл зонтик?",
      "Если устал — просто скажи.",
    ],
    huohuo: [
      "А-а! Не пугай так!",
      "Х-Хвостик, не вылезай!",
      "Я не боюсь. Совсем чуть-чуть.",
      "Можно я просто постою рядом?",
      "Только не призраки, только не призраки…",
      "Я… я справлюсь. Наверное.",
    ],
  };
  const BUBBLE_MS = 2600;
  const MAX_TILT = 7;
  const MAX_SHIFT = 10;

  const characters = [...artwork.querySelectorAll(".character")];
  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)");

  // Реплики по клику: без повторов подряд.
  characters.forEach((figure) => {
    const button = figure.querySelector(".character-poke");
    const bubble = figure.querySelector(".bubble");
    const lines = LINES[button.dataset.character];
    let last = -1;
    let timer = 0;

    button.hidden = false;
    button.addEventListener("click", () => {
      requestOrientation();
      let next = Math.floor(Math.random() * lines.length);
      if (next === last) next = (next + 1) % lines.length;
      last = next;

      bubble.textContent = lines[next];
      bubble.classList.add("is-visible");
      figure.classList.remove("is-poked");
      void figure.offsetWidth;
      figure.classList.add("is-poked");

      clearTimeout(timer);
      timer = setTimeout(() => bubble.classList.remove("is-visible"), BUBBLE_MS);
    });
  });

  // Наклон: x и y в диапазоне -1…1.
  let frame = 0;
  function tilt(x, y) {
    cancelAnimationFrame(frame);
    frame = requestAnimationFrame(() => {
      characters.forEach((figure) => {
        figure.style.setProperty("--rx", `${(-y * MAX_TILT).toFixed(2)}deg`);
        figure.style.setProperty("--ry", `${(x * MAX_TILT).toFixed(2)}deg`);
        const img = figure.querySelector("img");
        img.style.setProperty("--px", `${(-x * MAX_SHIFT).toFixed(1)}px`);
        img.style.setProperty("--py", `${(-y * MAX_SHIFT).toFixed(1)}px`);
      });
    });
  }
  function reset() {
    artwork.classList.remove("is-tilting");
    tilt(0, 0);
  }
  const clamp = (value) => Math.max(-1, Math.min(1, value));

  // Мышь: считаем от центра иллюстраций, влияние затухает на расстоянии.
  window.addEventListener("pointermove", (event) => {
    if (event.pointerType !== "mouse" || reduceMotion.matches) return;
    const box = artwork.getBoundingClientRect();
    const x = (event.clientX - (box.left + box.width / 2)) / box.width;
    const y = (event.clientY - (box.top + box.height / 2)) / box.height;
    artwork.classList.add("is-tilting");
    tilt(clamp(x), clamp(y));
  });
  document.documentElement.addEventListener("pointerleave", reset);

  // Телефон: наклон устройства. На iOS разрешение просим по первому тапу.
  let orientationAsked = false;
  function onOrientation(event) {
    if (event.gamma === null || reduceMotion.matches) return;
    artwork.classList.add("is-tilting");
    tilt(clamp(event.gamma / 30), clamp((event.beta - 45) / 30));
  }
  function requestOrientation() {
    if (orientationAsked) return;
    orientationAsked = true;
    const Orientation = window.DeviceOrientationEvent;
    if (typeof Orientation?.requestPermission !== "function") return;
    Orientation.requestPermission()
      .then((state) => {
        if (state === "granted")
          window.addEventListener("deviceorientation", onOrientation);
      })
      .catch(() => {});
  }
  if (typeof window.DeviceOrientationEvent?.requestPermission !== "function")
    window.addEventListener("deviceorientation", onOrientation);

  reduceMotion.addEventListener("change", reset);
})();
