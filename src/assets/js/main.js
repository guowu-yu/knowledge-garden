const yearEl = document.getElementById("year");
if (yearEl) yearEl.textContent = String(new Date().getFullYear());

const isTopicPage = document.body.classList.contains("page-topic");
const indexBase = isTopicPage ? "../" : "";

async function loadSearchIndex() {
  const res = await fetch(`${indexBase}search-index.json`);
  if (!res.ok) throw new Error("search index missing");
  return res.json();
}

function scoreItem(item, tokens) {
  const hay = `${item.title} ${item.tags.join(" ")} ${item.summary} ${item.text}`.toLowerCase();
  let score = 0;
  for (const token of tokens) {
    if (!token) continue;
    if (item.title.toLowerCase().includes(token)) score += 8;
    if (item.tags.some((t) => t.toLowerCase().includes(token))) score += 5;
    if (item.summary.toLowerCase().includes(token)) score += 3;
    if (hay.includes(token)) score += 1;
    else return 0;
  }
  return score;
}

function renderResults(container, results, query) {
  if (!query) {
    container.hidden = true;
    container.innerHTML = "";
    return;
  }
  container.hidden = false;
  if (!results.length) {
    container.innerHTML = `<div class="empty-result">未找到与「${query}」相关的专题</div>`;
    return;
  }
  container.innerHTML = results
    .slice(0, 8)
    .map(
      (item, i) => `
      <a href="${indexBase}${item.url}" ${i === 0 ? 'aria-selected="true"' : ""}>
        <span class="result-title">${item.title}</span>
        <span class="result-meta">${item.date || ""} · ${(item.tags || []).join(" / ")}</span>
      </a>`
    )
    .join("");
}

function setupSearch(index) {
  const form = document.getElementById("search-form");
  const input = document.getElementById("search-input");
  const resultsEl = document.getElementById("search-results");
  if (!form || !input || !resultsEl) return;

  const run = () => {
    const q = input.value.trim();
    const tokens = q.toLowerCase().split(/\s+/).filter(Boolean);
    const ranked = index
      .map((item) => ({ item, score: scoreItem(item, tokens) }))
      .filter((x) => x.score > 0)
      .sort((a, b) => b.score - a.score)
      .map((x) => x.item);
    renderResults(resultsEl, ranked, q);
  };

  input.addEventListener("input", run);
  form.addEventListener("submit", (e) => {
    e.preventDefault();
    const first = resultsEl.querySelector("a");
    if (first) first.click();
    else run();
  });

  document.addEventListener("click", (e) => {
    if (!resultsEl.contains(e.target) && e.target !== input) {
      resultsEl.hidden = true;
    }
  });
}

function setupTagFilters() {
  const grid = document.getElementById("topic-grid");
  const bar = document.getElementById("tag-filters");
  const toggle = document.getElementById("tag-filters-toggle");
  if (!grid || !bar) return;

  const cards = [...grid.querySelectorAll(".topic-card")];
  const tagSet = new Set();
  cards.forEach((card) => {
    (card.dataset.tags || "")
      .split(/\s+/)
      .filter(Boolean)
      .forEach((t) => tagSet.add(t));
  });

  const tags = ["全部", ...[...tagSet].sort((a, b) => a.localeCompare(b, "zh"))];
  bar.innerHTML = tags
    .map(
      (tag, i) =>
        `<button type="button" class="filter-chip${i === 0 ? " is-active" : ""}" data-tag="${tag}">${tag}</button>`
    )
    .join("");

  let expanded = false;
  let locking = false;

  const syncCollapse = () => {
    if (locking || !toggle) return;
    locking = true;
    try {
      const chips = [...bar.querySelectorAll(".filter-chip")];
      if (!chips.length) return;

      // Measure with every chip visible
      chips.forEach((chip) => {
        chip.hidden = false;
      });

      if (expanded) {
        toggle.hidden = false;
        toggle.textContent = "收起";
        toggle.setAttribute("aria-expanded", "true");
        return;
      }

      const firstTop = chips[0].offsetTop;
      let overflowCount = 0;
      chips.forEach((chip) => {
        if (chip.offsetTop > firstTop + 1) {
          chip.hidden = true;
          overflowCount += 1;
        }
      });

      toggle.hidden = overflowCount === 0;
      toggle.textContent = "展开全部";
      toggle.setAttribute("aria-expanded", "false");
    } finally {
      locking = false;
    }
  };

  bar.addEventListener("click", (e) => {
    const btn = e.target.closest(".filter-chip");
    if (!btn || btn.hidden) return;
    bar.querySelectorAll(".filter-chip").forEach((el) => el.classList.remove("is-active"));
    btn.classList.add("is-active");
    const tag = btn.dataset.tag;
    cards.forEach((card) => {
      const show = tag === "全部" || (card.dataset.tags || "").split(/\s+/).includes(tag);
      card.classList.toggle("is-hidden", !show);
    });
  });

  if (toggle) {
    toggle.addEventListener("click", () => {
      expanded = !expanded;
      syncCollapse();
    });
  }

  const schedule = () => {
    requestAnimationFrame(() => requestAnimationFrame(syncCollapse));
  };
  schedule();
  window.addEventListener("load", schedule);
  if (document.fonts && document.fonts.ready) {
    document.fonts.ready.then(schedule).catch(() => {});
  }
  window.addEventListener("resize", schedule);
  if (typeof ResizeObserver !== "undefined") {
    let lastWidth = -1;
    const ro = new ResizeObserver((entries) => {
      const width = entries[0]?.contentRect?.width ?? 0;
      if (Math.abs(width - lastWidth) < 1) return;
      lastWidth = width;
      schedule();
    });
    ro.observe(bar);
  }
}

setupTagFilters();

loadSearchIndex()
  .then(setupSearch)
  .catch(() => {
    /* search optional if index absent during local preview of raw templates */
  });
