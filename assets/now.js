(() => {
  const repoLink = document.getElementById("now-repo");
  const pushedNote = document.getElementById("now-pushed");
  if (!repoLink || !pushedNote) return;

  const API_URL =
    "https://api.github.com/users/Samuray4ik04/repos?sort=pushed&per_page=5";
  const CACHE_KEY = "samuray-last-push";
  const CACHE_MS = 10 * 60 * 1000;
  const UNITS = [
    ["year", 365 * 24 * 3600],
    ["month", 30 * 24 * 3600],
    ["week", 7 * 24 * 3600],
    ["day", 24 * 3600],
    ["hour", 3600],
    ["minute", 60],
  ];

  function timeAgo(date) {
    const seconds = (date - Date.now()) / 1000;
    const format = new Intl.RelativeTimeFormat("ru", { numeric: "auto" });
    for (const [unit, size] of UNITS) {
      if (Math.abs(seconds) >= size)
        return format.format(Math.round(seconds / size), unit);
    }
    return "только что";
  }

  function render({ name, url, pushedAt }) {
    repoLink.href = url;
    repoLink.firstChild.textContent = `${name} `;
    pushedNote.textContent = `последний пуш — ${timeAgo(new Date(pushedAt))}`;
  }

  function readCache() {
    try {
      const cached = JSON.parse(sessionStorage.getItem(CACHE_KEY));
      if (cached && Date.now() - cached.savedAt < CACHE_MS) return cached.repo;
    } catch (_) {}
    return null;
  }

  function writeCache(repo) {
    try {
      sessionStorage.setItem(
        CACHE_KEY,
        JSON.stringify({ savedAt: Date.now(), repo }),
      );
    } catch (_) {}
  }

  const cached = readCache();
  if (cached) return render(cached);

  // Без сети или при лимите API остаётся статичный текст из HTML.
  fetch(API_URL, { headers: { Accept: "application/vnd.github+json" } })
    .then((response) => (response.ok ? response.json() : Promise.reject()))
    .then((repos) => {
      const latest = repos.find((repo) => !repo.fork && repo.pushed_at);
      if (!latest) return;
      const repo = {
        name: latest.name,
        url: latest.html_url,
        pushedAt: latest.pushed_at,
      };
      writeCache(repo);
      render(repo);
    })
    .catch(() => {});
})();
