(() => {
  document.getElementById("year").textContent = new Date().getFullYear();
  const buttons = [...document.querySelectorAll("[data-theme]")];
  const colors = { blend: "#f6f5ed", mahiru: "#faf3e7", huohuo: "#122c27" };
  function setMood(mood) {
    document.documentElement.dataset.mood = mood;
    buttons.forEach((button) =>
      button.setAttribute(
        "aria-pressed",
        String(button.dataset.theme === mood),
      ),
    );
    document.querySelector('meta[name="theme-color"]').content = colors[mood];
  }
  setMood(document.documentElement.dataset.mood || "blend");
  document.getElementById("mood-picker").hidden = false;
  buttons.forEach((button) =>
    button.addEventListener("click", () => {
      setMood(button.dataset.theme);
      try {
        localStorage.setItem("samuray-mood", button.dataset.theme);
      } catch (_) {}
    }),
  );
  const list = document.getElementById("lines");
  const lines = [...list.children].map((line) => line.textContent);
  const quote = document.createElement("p");
  quote.className = "quote-text";
  quote.setAttribute("aria-live", "polite");
  quote.setAttribute("aria-atomic", "true");
  quote.textContent = lines[0];
  list.replaceWith(quote);
  document.getElementById("thought-controls").hidden = false;
  let index = 0;
  document.getElementById("next").addEventListener("click", () => {
    index = (index + 1) % lines.length;
    quote.textContent = lines[index];
    quote.classList.remove("quote-enter");
    void quote.offsetWidth;
    quote.classList.add("quote-enter");
    document.getElementById("counter").textContent =
      `${String(index + 1).padStart(2, "0")} / ${String(lines.length).padStart(2, "0")}`;
  });
})();
