(function () {
  var CP = window.SN_CP || {};
  var DEST = "https://formsubmit.co/ajax/vtricheur@gmail.com";
  var LIVE_HOSTS = ["seuilnormand.fr", "www.seuilnormand.fr"];

  function zoneInfo(cp) {
    if (!/^\d{5}$/.test(cp)) return null;
    var km = CP[cp];
    if (km === undefined) return { km: null, cls: "far", label: "hors zone" };
    if (km <= 50) return { km: km, cls: "in", label: "dans la zone" };
    return { km: km, cls: "near", label: "hors zone proche" };
  }

  function stamp() { return new Date().toLocaleString("fr-FR", { day: "2-digit", month: "2-digit", hour: "2-digit", minute: "2-digit" }); }
  function send(data) {
    return fetch(DEST, { method: "POST", headers: { "Content-Type": "application/json", "Accept": "application/json" }, body: JSON.stringify(data) })
      .then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); });
  }

  document.querySelectorAll("form.devis").forEach(function (form) {
    var cpInput = form.querySelector("[name=code_postal]");
    var msg = form.querySelector(".form-msg[role=status]");
    var s1 = form.querySelector(".step1"), s2 = form.querySelector(".step2");
    var first = null; /* données de l'étape 1, réutilisées à l'étape 2 */

    function done(t) {
      s2.hidden = true; s1.hidden = true; first = null;
      msg.hidden = false; msg.className = "form-msg ok"; msg.textContent = t || "Merci, nous vous rappelons sous 48 h ouvrées pour préparer votre devis.";
    }
    form.querySelector(".skip").addEventListener("click", function () { done(); });

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      msg.hidden = true;
      var live = LIVE_HOSTS.indexOf(location.hostname) !== -1;
      if (!first) {
        /* ---- étape 1 : 4 champs, la demande part tout de suite ---- */
        var products = Array.prototype.map.call(form.querySelectorAll("[name=produits]:checked"), function (i) { return i.value; });
        if (!products.length) return fail("Cochez au moins un produit pour que nous sachions quoi chiffrer.");
        var bad = [cpInput, form.nom, form.telephone].filter(function (i) { return !i.checkValidity(); })[0];
        if (bad) { bad.reportValidity(); return; }
        if (form._honey && form._honey.value) return;
        var cp = cpInput.value.trim();
        var z = zoneInfo(cp) || { km: null, label: "code postal non reconnu" };
        var nom = form.nom.value.trim();
        var data = {
          _subject: "Nouvelle demande Seuil Normand – " + products.join(", ") + " – " + cp + " – " + nom.slice(0, 40) + " – " + stamp(),
          _template: "table", _captcha: "false",
          "Produits": products.join(", "),
          "Code postal": cp,
          "Distance magasins (interne)": z.km === null ? z.label : z.km + " km (" + z.label + ")",
          "Nom": nom,
          "Téléphone": form.telephone.value.trim(),
          "Page d'origine": document.title
        };
        var btn = s1.querySelector("button[type=submit]");
        var next = function () {
          first = data; s1.hidden = true; s2.hidden = false;
          try { if (window.snConversion) window.snConversion(data["Produits"]); } catch (err) {}
          s2.scrollIntoView({ behavior: "smooth", block: "start" });
        };
        if (!live) { first = data; s1.hidden = true; s2.hidden = false; return; }
        btn.disabled = true; btn.textContent = "Envoi…";
        send(data).then(next).catch(function () { fail("L'envoi n'a pas abouti. Réessayez ou appelez le 06 37 99 00 92."); })
          .finally(function () { btn.disabled = false; btn.textContent = "Être rappelé gratuitement"; });
        return;
      }
      /* ---- étape 2 (facultative) : précisions rattachées à la même demande ---- */
      var d2 = {
        _subject: "Nouvelle demande Seuil Normand – Précisions – " + first["Nom"].slice(0, 40) + " – " + first["Téléphone"] + " – " + stamp(),
        _template: "table", _captcha: "false",
        "Complément": "oui",
        "Nom": first["Nom"], "Téléphone": first["Téléphone"], "Code postal": first["Code postal"], "Produits": first["Produits"],
        "Projet": form.projet.value, "Pose": form.pose.value, "Commune": form.commune.value,
        "Délai": form.delai.value, "Détails": form.details.value, "Email": form.email.value
      };
      if (!live) return done("Aperçu : sur seuilnormand.fr, ces précisions sont envoyées par email. Ici, rien n'a été envoyé.");
      var b2 = s2.querySelector("button[type=submit]");
      b2.disabled = true; b2.textContent = "Envoi…";
      send(d2).then(function () { form.reset(); done("Merci ! Vos précisions sont bien reçues. Nous vous rappelons sous 48 h ouvrées."); })
        .catch(function () { done(); })
        .finally(function () { b2.disabled = false; b2.textContent = "Envoyer ces précisions"; });
    });

    function fail(t) { msg.hidden = false; msg.className = "form-msg err"; msg.textContent = t; }
  });

  document.querySelectorAll("[data-goto]").forEach(function (el) {
    function go() { location.href = el.getAttribute("data-goto"); }
    el.addEventListener("click", go);
    el.addEventListener("keydown", function (e) { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); go(); } });
  });
})();
