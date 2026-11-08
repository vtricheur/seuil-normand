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

  document.querySelectorAll("form.devis").forEach(function (form) {
    var cpInput = form.querySelector("[name=code_postal]");
    var msg = form.querySelector(".form-msg");
    var btn = form.querySelector("button[type=submit]");


    form.addEventListener("submit", function (e) {
      e.preventDefault();
      msg.hidden = true;
      var products = Array.prototype.map.call(form.querySelectorAll("[name=produits]:checked"), function (i) { return i.value; });
      if (!products.length) { return fail("Cochez au moins un produit pour que nous sachions quoi chiffrer."); }
      if (!form.checkValidity()) { form.reportValidity(); return; }
      var cp = cpInput.value.trim();
      var z = zoneInfo(cp) || { km: null, label: "code postal non reconnu" };
      var data = {
        _subject: "Nouvelle demande Seuil Normand – " + products.join(", ") + " – " + cp,
        _template: "table",
        _captcha: "false",
        "Produits": products.join(", "),
        "Projet": form.projet.value,
        "Pose": form.pose.value,
        "Code postal": cp,
        "Commune": form.commune.value,
        "Distance magasins (interne)": z.km === null ? z.label : z.km + " km (" + z.label + ")",
        "Détails": form.details.value,
        "Délai": form.delai.value,
        "Nom": form.nom.value,
        "Téléphone": form.telephone.value,
        "Email": form.email.value,
        "Page d'origine": document.title
      };
      if (form._honey && form._honey.value) return;
      if (LIVE_HOSTS.indexOf(location.hostname) === -1) {
        return ok("Aperçu : sur seuilnormand.fr, ce bouton envoie la demande par email. Ici, rien n'a été envoyé.");
      }
      btn.disabled = true; btn.textContent = "Envoi…";
      fetch(DEST, { method: "POST", headers: { "Content-Type": "application/json", "Accept": "application/json" }, body: JSON.stringify(data) })
        .then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); })
        .then(function () { form.reset(); ok("Demande reçue. Nous vous rappelons sous 48 h ouvrées pour préciser votre projet et préparer le devis."); })
        .catch(function () { fail("L'envoi n'a pas abouti. Vérifiez votre connexion et réessayez, ou appelez le 06 37 99 00 92."); })
        .finally(function () { btn.disabled = false; btn.textContent = "Recevoir mon devis gratuit"; });
    });

    function ok(t) { msg.hidden = false; msg.className = "form-msg ok"; msg.textContent = t; }
    function fail(t) { msg.hidden = false; msg.className = "form-msg err"; msg.textContent = t; }
  });

  document.querySelectorAll("[data-goto]").forEach(function (el) {
    function go() { location.href = el.getAttribute("data-goto"); }
    el.addEventListener("click", go);
    el.addEventListener("keydown", function (e) { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); go(); } });
  });
})();
