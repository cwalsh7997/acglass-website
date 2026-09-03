(function () {
  var article = document.querySelector(".acg-flagship-article");
  var host = document.querySelector(".acg-toc-host");
  if (!article || !host) return;
  if (host.querySelector("a[href^='#']")) return;
  var h2s = Array.prototype.slice.call(article.querySelectorAll("h2"));
  var heads = h2s.length ? h2s : Array.prototype.slice.call(article.querySelectorAll("h3"));
  function slug(el, i) {
    if (el.id) return el.id;
    var t = (el.textContent || "").toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");
    el.id = t || ("section-" + (i + 1));
    return el.id;
  }
  var links = heads.map(function (h, i) {
    return { id: slug(h, i), label: (h.textContent || "").replace(/\s+/g, " ").trim() };
  }).filter(function (l) { return l.label; });
  if (!links.length) return;
  var nav = host;
  if (host.tagName !== "NAV") {
    nav = document.createElement("nav");
    nav.className = "acg-toc";
    nav.setAttribute("aria-label", "On this page");
    host.appendChild(nav);
  }
  if (!nav.querySelector(".acg-toc-kicker, .acg-toc-label")) {
    var lab = document.createElement("p");
    lab.className = "acg-toc-kicker";
    lab.textContent = "On this page";
    nav.appendChild(lab);
  }
  var ol = document.createElement("ol");
  links.forEach(function (l) {
    var li = document.createElement("li");
    var a = document.createElement("a");
    a.href = "#" + l.id;
    a.textContent = l.label;
    li.appendChild(a);
    ol.appendChild(li);
  });
  nav.appendChild(ol);
})();
