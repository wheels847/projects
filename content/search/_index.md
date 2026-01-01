---
title: "Search"
---

Type a surname, place, or keyword.

<script>
document.addEventListener("DOMContentLoaded", () => {
  const selectors = [
    'button[aria-label="Search"]',
    'a[aria-label="Search"]',
    '[data-search]',
    '#search-button',
    '#search'
  ];
  for (const s of selectors) {
    const el = document.querySelector(s);
    if (el) { el.click(); break; }
  }
});
</script>

If the search box doesn't pop open automatically, click the 🔍 icon in the top right.
