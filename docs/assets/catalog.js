"use strict";

(() => {
  const tools = document.querySelector(".catalog-tools");
  const search = document.querySelector("#talk-search");
  const buttons = [...document.querySelectorAll("[data-topic]")];
  const groups = [...document.querySelectorAll(".talk-group")];
  const rows = [...document.querySelectorAll(".talk-row")];
  const count = document.querySelector(".result-count");
  const empty = document.querySelector(".empty-state");
  let topic = "all";
  const normalize = text => text.normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase();

  function update() {
    const terms = normalize(search.value.trim()).split(/\s+/).filter(Boolean);
    let visible = 0;
    for (const group of groups) {
      let groupVisible = 0;
      for (const row of group.querySelectorAll(".talk-row")) {
        const haystack = normalize(row.textContent + " " + group.dataset.topic + " " + group.querySelector("h3").textContent);
        const matches = (topic === "all" || group.dataset.topic === topic) && terms.every(term => haystack.includes(term));
        row.hidden = !matches;
        groupVisible += Number(matches);
      }
      group.hidden = groupVisible === 0;
      visible += groupVisible;
    }
    count.textContent = `${visible} of ${rows.length} talks shown below`;
    empty.hidden = visible !== 0;
  }

  for (const button of buttons) {
    button.addEventListener("click", () => {
      topic = button.dataset.topic;
      for (const item of buttons) item.setAttribute("aria-pressed", String(item === button));
      update();
    });
  }
  search.addEventListener("input", update);
  document.querySelector("#clear-filters").addEventListener("click", () => {
    search.value = "";
    topic = "all";
    for (const button of buttons) button.setAttribute("aria-pressed", String(button.dataset.topic === "all"));
    update();
    search.focus();
  });
  tools.hidden = false;
  count.hidden = false;
  update();
})();
