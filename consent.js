/* Seuil Normand — consentement cookies (CNIL) + balises publicitaires.
   Rien n'est chargé tant que le visiteur n'a pas cliqué « Accepter ».
   Refuser est aussi simple qu'accepter ; le choix est gardé 6 mois. */
(function () {
  "use strict";
  var CFG = {
    GADS_ID: "",            // ex. "AW-123456789" (balise Google Ads)
    GADS_LABEL: "",         // libellé de l'action de conversion « Demande de devis »
    META_PIXEL: "1113394131504095"
  };
  var KEY = "sn-consent", MAX = 182 * 864e5;
  function read() {
    try { var v = JSON.parse(localStorage.getItem(KEY) || "null"); if (v && Date.now() - v.at < MAX) return v.choice; } catch (e) {}
    return null;
  }
  function save(choice) { try { localStorage.setItem(KEY, JSON.stringify({ choice: choice, at: Date.now() })); } catch (e) {} }

  var loaded = false;
  function loadTags() {
    if (loaded) return; loaded = true;
    if (CFG.GADS_ID) {
      var s = document.createElement("script"); s.async = true; s.src = "https://www.googletagmanager.com/gtag/js?id=" + CFG.GADS_ID; document.head.appendChild(s);
      window.dataLayer = window.dataLayer || []; window.gtag = function () { dataLayer.push(arguments); };
      gtag("js", new Date()); gtag("config", CFG.GADS_ID);
    }
    if (CFG.META_PIXEL) {
      !function (f, b, e, v, n, t, s) { if (f.fbq) return; n = f.fbq = function () { n.callMethod ? n.callMethod.apply(n, arguments) : n.queue.push(arguments); }; if (!f._fbq) f._fbq = n; n.push = n; n.loaded = !0; n.version = "2.0"; n.queue = []; t = b.createElement(e); t.async = !0; t.src = v; s = b.getElementsByTagName(e)[0]; s.parentNode.insertBefore(t, s); }(window, document, "script", "https://connect.facebook.net/en_US/fbevents.js");
      fbq("init", CFG.META_PIXEL); fbq("track", "PageView");
    }
  }

  /* Appelé par site.js quand une demande de devis est bien envoyée */
  window.snConversion = function (produits) {
    if (read() !== "ok") return;
    loadTags();
    if (CFG.GADS_ID && CFG.GADS_LABEL && window.gtag) gtag("event", "conversion", { send_to: CFG.GADS_ID + "/" + CFG.GADS_LABEL });
    if (window.fbq) fbq("track", "Lead", { content_name: produits || "" });
  };

  var css = ".cc{position:fixed;left:0;right:0;bottom:0;z-index:50;background:var(--paper);color:var(--slate);border-top:1px solid var(--line);box-shadow:0 -8px 24px rgba(0,0,0,.08);padding:16px max(16px,env(safe-area-inset-right,0px)) calc(16px + env(safe-area-inset-bottom,0px)) max(16px,env(safe-area-inset-left,0px))}" +
    ".cc .in{max-width:72rem;margin:0 auto;display:flex;flex-wrap:wrap;gap:12px 24px;align-items:center;justify-content:space-between}" +
    ".cc p{margin:0;font-size:.92rem;line-height:1.5;max-width:46rem;min-width:0}.cc p a{color:inherit}" +
    ".cc .b{display:flex;gap:10px;flex-wrap:wrap}.cc button{font:600 .95rem var(--f-body);padding:10px 18px;border-radius:6px;cursor:pointer;border:1px solid var(--green);min-width:8.5rem}" +
    ".cc .y{background:var(--green);color:var(--green-ink)}.cc .n{background:transparent;color:var(--green)}";
  function banner() {
    if (document.getElementById("cc")) return;
    var st = document.createElement("style"); st.textContent = css; document.head.appendChild(st);
    var d = document.createElement("div"); d.className = "cc"; d.id = "cc"; d.setAttribute("role", "dialog"); d.setAttribute("aria-label", "Cookies");
    d.innerHTML = '<div class="in"><p>Avec votre accord, nous utilisons des cookies de Google et Meta pour mesurer l\'efficacité de nos publicités. Aucun cookie n\'est déposé si vous refusez, et le site fonctionne de la même façon. <a href="confidentialite.html#cookies">En savoir plus</a></p>' +
      '<div class="b"><button type="button" class="n" data-cc="no">Refuser</button><button type="button" class="y" data-cc="ok">Accepter</button></div></div>';
    document.body.appendChild(d);
    d.addEventListener("click", function (e) {
      var c = e.target.getAttribute("data-cc"); if (!c) return;
      save(c); d.remove(); if (c === "ok") loadTags();
    });
  }
  window.snCookies = function () { var d = document.getElementById("cc"); if (d) d.remove(); banner(); };

  function init() {
    var c = read();
    if (c === "ok") loadTags(); else if (c !== "no") banner();
    document.addEventListener("click", function (e) { var a = e.target.closest && e.target.closest("[data-cookies]"); if (a) { e.preventDefault(); window.snCookies(); } });
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init); else init();
})();
