# Seuil Normand — sources du site

Branche `source` : le générateur. La branche `main` contient le site publié (GitHub Pages, seuilnormand.fr).

## Construire et publier
```
git clone -b source https://github.com/vtricheur/seuil-normand sn && cd sn
git clone -b main https://github.com/vtricheur/seuil-normand site     # build.py écrit dans ./site
python3 build.py                                                         # régénère tout le site (garde site/.git)
cd site && git add -A && git commit -m "…" && git push                  # publication
```
- Pages produits, villes : `build.py`. Guides : `articles.py` (anciens) et `articles2.py` (ajouts) — mêmes champs : slug, short, product, img, title, h1, desc, lead, body (HTML), sources, date (AAAA-MM-JJ).
- `img` = clé du dictionnaire `IMG` de build.py (hero, hero2, fenetres, fenetres2, volets, volets2, porte-entree, porte-garage, portail, pergola, portes-interieures).
- Visuel réseaux sociaux d'un guide : mettre à jour `tools/guides.json` puis `node tools/guide_cards.js` (Playwright) → `src/kit/guides/<slug>.jpg`, publié sur https://seuilnormand.fr/kit/guides/<slug>.jpg.
- Pages à ne pas indexer : `NOINDEX` dans build.py. Le sitemap et robots.txt sont générés.
- `app/` : source du panneau de pilotage (artifact claude.ai), non publié sur le site.
