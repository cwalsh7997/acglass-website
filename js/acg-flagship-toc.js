(function () {
  var article = document.querySelector(".acg-flagship-article");
  var host = document.querySelector(".acg-toc-host");
  if (!article || !host) return;
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
  function list() {
    var ol = document.createElement("ol");
    links.forEach(function (l) {
      var li = document.createElement("li");
      var a = document.createElement("a");
      a.href = "#" + l.id;
      a.textContent = l.label;
      li.appendChild(a);
      ol.appendChild(li);
    });
    return ol;
  }
  var mobile = document.createElement("details");
  mobile.className = "acg-toc-mobile";
  var sum = document.createElement("summary");
  sum.textContent = "On this page";
  mobile.appendChild(sum);
  mobile.appendChild(list());
  var desktop = document.createElement("nav");
  desktop.className = "acg-toc-desktop";
  desktop.setAttribute("aria-label", "On this page");
  var lab = document.createElement("div");
  lab.className = "acg-toc-label";
  lab.textContent = "On this page";
  desktop.appendChild(lab);
  desktop.appendChild(list());
  host.appendChild(mobile);
  host.appendChild(desktop);
})();
