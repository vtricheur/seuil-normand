/* Seuil Normand — consentement cookies (CNIL) + balises publicitaires.
   Rien n'est chargé tant que le visiteur n'a pas cliqué « Accepter ».
   Refuser est aussi simple qu'accepter ; le choix est gardé 6 mois. */
(function () {
  "use strict";
  var CFG = {
    GADS_ID: "AW-18579177641",   // balise Google Ads (compte 752-054-0837)
    GADS_LABEL: "QDoJCKbn27kdEKmBn5tF",  // conversion « Envoi de formulaire de lead »
    META_PIXEL: "1113394131504095",
    CLARITY: "zgl6tikrxy",        // Microsoft Clarity (projet Seuil Normand)
    GOATCOUNTER: ""               // compteur de visites SANS cookies (exempté de consentement) : code du compte GoatCounter
  };
  /* Compteur sans cookies : chargé pour tout le monde, il ne dépose rien sur l'appareil et ne suit personne d'un site à l'autre */
  window.snTrack = function (name, title) { try { if (window.goatcounter && window.goatcounter.count) window.goatcounter.count({ path: "evt-" + name, title: title || name, event: true }); } catch (e) {} };
  if (CFG.GOATCOUNTER && !/^(localhost|127\.)/.test(location.hostname)) {
    var gc = document.createElement("script"); gc.async = true; gc.src = "https://gc.zgo.at/count.js";
    gc.setAttribute("data-goatcounter", "https://" + CFG.GOATCOUNTER + ".goatcounter.com/count");
    document.head.appendChild(gc);
  }
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
    if (CFG.CLARITY) {
      (function (c, l, a, r, i, t, y) { c[a] = c[a] || function () { (c[a].q = c[a].q || []).push(arguments); }; t = l.createElement(r); t.async = 1; t.src = "https://www.clarity.ms/tag/" + i; y = l.getElementsByTagName(r)[0]; y.parentNode.insertBefore(t, y); })(window, document, "clarity", "script", CFG.CLARITY);
      window.clarity("consentv2", { ad_Storage: "denied", analytics_Storage: "granted" });
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

  /* bandeau compact : carte flottante au-dessus de la barre « Appeler » sur mobile, n'occupe plus le bas de l'écran */
  var css = ".cc{position:fixed;z-index:50;right:max(12px,env(safe-area-inset-right,0px));bottom:calc(12px + env(safe-area-inset-bottom,0px));width:min(420px,calc(100% - 24px));background:var(--paper);color:var(--slate);border:1px solid var(--line);border-radius:10px;box-shadow:0 8px 24px rgba(0,0,0,.14);padding:10px 12px}" +
    ".cc .in{display:flex;gap:8px 10px;align-items:center;flex-wrap:wrap}" +
    ".cc p{margin:0;font-size:.8rem;line-height:1.35;flex:1 1 12rem;min-width:0}.cc p a{color:inherit}" +
    ".cc .b{display:flex;gap:6px}.cc button{font:600 .82rem var(--f-body);padding:7px 12px;border-radius:6px;cursor:pointer;border:1px solid var(--green);min-width:5.5rem}" +
    ".cc .y{background:var(--green);color:var(--green-ink)}.cc .n{background:transparent;color:var(--green)}" +
    "@media (max-width:760px){.cc{left:max(8px,env(safe-area-inset-left,0px));right:auto;width:calc(100% - 16px);bottom:calc(72px + env(safe-area-inset-bottom,0px));padding:7px 9px}.cc .in{flex-wrap:nowrap}.cc p{font-size:.72rem;flex:1 1 auto}.cc button{min-width:0;padding:6px 9px;font-size:.78rem}}";
  function banner() {
    if (document.getElementById("cc")) return;
    var st = document.createElement("style"); st.textContent = css; document.head.appendChild(st);
    var d = document.createElement("div"); d.className = "cc"; d.id = "cc"; d.setAttribute("role", "dialog"); d.setAttribute("aria-label", "Cookies");
    d.innerHTML = '<div class="in"><p>Cookies de mesure (Google, Meta, Clarity) ? Rien n\'est déposé si vous refusez. <a href="confidentialite.html#cookies">Détails</a></p>' +
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
