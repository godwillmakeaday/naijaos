/* naijaOS — progressive enhancements. No framework. Degrades gracefully. */
(function () {
  "use strict";

  /* ---- OPERATING CONDITIONS FEED ----------------------------------------
     Indicative placeholders. Replace `SIGNALS` with a live data source
     (NBS / CBN releases) when wiring production. Each value is illustrative
     and must be verified against the latest official release before use.   */
  var SIGNALS = {
    asOf: "INDICATIVE PLACEHOLDERS · verify against latest NBS / CBN releases",
    items: [
      { label: "Headline inflation", value: "~mid-30s%", trend: "indicative", dir: "up" },
      { label: "Food inflation",     value: "~high-30s%", trend: "indicative", dir: "up" },
      { label: "Transport cost",     value: "elevated",  trend: "indicative", dir: "up" },
      { label: "Naira / USD",        value: "four-figure", trend: "indicative", dir: "flat" },
      { label: "PMS (petrol)",       value: "deregulated", trend: "watch pump", dir: "up" },
      { label: "Policy rate",        value: "tightened", trend: "indicative", dir: "flat" }
    ]
  };

  function renderSignals() {
    var grid = document.querySelector("[data-signal-grid]");
    if (!grid) return;
    grid.innerHTML = SIGNALS.items.map(function (s) {
      var arrow = s.dir === "up" ? "▲" : s.dir === "down" ? "▼" : "•";
      return (
        '<div class="cell">' +
          '<div class="cell__label">' + s.label + "</div>" +
          '<div class="cell__val">' + s.value + "</div>" +
          '<div class="cell__trend ' + s.dir + '">' + arrow + " " + s.trend + "</div>" +
        "</div>"
      );
    }).join("");
    var stamp = document.querySelector("[data-signal-asof]");
    if (stamp) stamp.textContent = SIGNALS.asOf;
  }

  /* ---- MOBILE NAV -------------------------------------------------------- */
  function nav() {
    var btn = document.querySelector(".menu-btn");
    var drawer = document.querySelector(".drawer");
    if (!btn || !drawer) return;
    btn.addEventListener("click", function () {
      var open = drawer.classList.toggle("open");
      btn.setAttribute("aria-expanded", String(open));
      btn.textContent = open ? "Close" : "Menu";
    });
  }

  /* ---- LAST UPDATED LABELS ---------------------------------------------- */
  function lastUpdated() {
    document.querySelectorAll("[data-updated]").forEach(function (el) {
      var raw = el.getAttribute("data-updated");
      if (!raw) return;
      var d = new Date(raw);
      if (isNaN(d)) return;
      var fmt = d.toLocaleDateString("en-GB", { day: "2-digit", month: "short", year: "numeric" });
      el.textContent = el.getAttribute("data-prefix") ? el.getAttribute("data-prefix") + " " + fmt : fmt;
    });
  }

  /* ---- TOC SCROLL-SPY ---------------------------------------------------- */
  function scrollSpy() {
    var links = Array.prototype.slice.call(document.querySelectorAll(".toc__list a[href^='#']"));
    if (!links.length || !("IntersectionObserver" in window)) return;
    var map = {};
    links.forEach(function (a) {
      var id = a.getAttribute("href").slice(1);
      var sec = document.getElementById(id);
      if (sec) map[id] = a;
    });
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) {
          links.forEach(function (l) { l.classList.remove("active"); });
          var a = map[e.target.id];
          if (a) a.classList.add("active");
        }
      });
    }, { rootMargin: "-30% 0px -60% 0px" });
    Object.keys(map).forEach(function (id) { io.observe(document.getElementById(id)); });
  }

  /* ---- FILTER TABS ------------------------------------------------------- */
  function tabs() {
    document.querySelectorAll("[data-tabs]").forEach(function (group) {
      var btns = group.querySelectorAll(".tab");
      var targetSel = group.getAttribute("data-tabs");
      var items = document.querySelectorAll(targetSel + " [data-cat]");
      btns.forEach(function (btn) {
        btn.addEventListener("click", function () {
          btns.forEach(function (b) { b.setAttribute("aria-selected", "false"); });
          btn.setAttribute("aria-selected", "true");
          var cat = btn.getAttribute("data-filter");
          items.forEach(function (it) {
            var show = cat === "all" || it.getAttribute("data-cat") === cat;
            it.style.display = show ? "" : "none";
          });
        });
      });
    });
  }

  /* ---- "IN PRODUCTION" LINKS -------------------------------------------- */
  function soon() {
    var toast = document.createElement("div");
    toast.className = "toast";
    toast.textContent = "In production — page not yet published.";
    document.body.appendChild(toast);
    var t;
    document.querySelectorAll("[data-soon]").forEach(function (el) {
      el.addEventListener("click", function (e) {
        e.preventDefault();
        toast.classList.add("show");
        clearTimeout(t);
        t = setTimeout(function () { toast.classList.remove("show"); }, 2200);
      });
    });
  }

  document.addEventListener("DOMContentLoaded", function () {
    renderSignals();
    nav();
    lastUpdated();
    scrollSpy();
    tabs();
    soon();
  });
})();
