const links = [...document.querySelectorAll(".nav-link")];
const views = [...document.querySelectorAll(".view")];
const sidebar = document.querySelector("#sidebar");
const menu = document.querySelector("#menu");

function showSection(section) {
  const selected = document.getElementById(section) || document.getElementById("dashboard");
  links.forEach((link) => link.classList.toggle("active", link.dataset.section === selected.id));
  views.forEach((view) => view.classList.toggle("active", view === selected));
  document.querySelector("#page-title").textContent = selected.querySelector("h2").textContent;
  sidebar.classList.remove("open");
  menu.setAttribute("aria-expanded", "false");
}

links.forEach((link) => link.addEventListener("click", () => showSection(link.dataset.section)));
menu.addEventListener("click", () => {
  const open = sidebar.classList.toggle("open");
  menu.setAttribute("aria-expanded", String(open));
});
window.addEventListener("hashchange", () => showSection(location.hash.slice(1)));

fetch("/api/v1/status", { headers: { Accept: "application/json" } })
  .then((response) => {
    if (!response.ok) throw new Error("Status endpoint unavailable");
    return response.json();
  })
  .then((status) => {
    document.querySelector("#version").textContent = status.version;
    document.querySelector("#api-state").innerHTML = '<i class="dot"></i> Online';
  })
  .catch(() => {
    document.querySelector("#api-state").innerHTML = '<i class="dot error"></i> Offline';
  });

showSection(location.hash.slice(1) || "dashboard");
