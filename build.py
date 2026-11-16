import json, html, os, shutil
from articles import ARTICLES
from articles2 import ARTICLES2
for _a in ARTICLES: _a.setdefault("date", "2026-11-10")
for _a in ARTICLES2: _a.setdefault("date", "2026-11-16")
ARTICLES = ARTICLES2 + ARTICLES

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "src")
OUT = os.path.join(ROOT, "site")
SITE = "https://seuilnormand.fr"
FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Gloock&family=IBM+Plex+Mono:wght@400;500&family=Public+Sans:wght@400;500;600;700&display=swap">'
e = html.escape

# ---------- Données ----------
PRODUCTS = [
  dict(slug="fenetres", short="Fenêtres", name="Fenêtres et baies vitrées", spec="Uw ≤ 1,3",
    ico='<rect class="ico" x="10" y="8" width="30" height="34"/><line class="ico" x1="25" y1="8" x2="25" y2="42"/><line class="ico" x1="10" y1="25" x2="40" y2="25"/>',
    tagline="Fenêtres PVC, aluminium, bois ou mixtes, posées en neuf ou en rénovation.",
    title="Fenêtres sur mesure PVC, alu, bois – Eure | Seuil Normand",
    desc="Devis gratuit pour vos fenêtres et baies vitrées sur mesure (PVC, alu, bois) autour d'Évreux, Rouen, Bernay et du Neubourg. Fabrication française.",
    intro="Changer ses fenêtres, c'est le poste qui fait le plus de différence sur le confort et la facture de chauffage. Nous chiffrons des menuiseries sur mesure de fabrication française, en PVC, aluminium, bois ou bois-alu, pour la rénovation comme pour le neuf.",
    points=["Fenêtres à la française, oscillo-battantes et coulissantes", "Baies vitrées et portes-fenêtres grandes dimensions", "Double ou triple vitrage, vitrage feuilleté de sécurité", "Coloris au choix, bicolore intérieur / extérieur", "Pose en rénovation sur dormant existant ou en dépose totale"],
    specs=[("Isolation (coefficient Uw)", "de 1,3 à 0,8 W/m².K selon le vitrage"), ("Matériaux", "PVC, aluminium, bois, bois-alu"), ("Mesures utiles", "largeur × hauteur du tableau, en cm"), ("Aides possibles", "selon votre situation (rénovation énergétique)")],
    faq=[("Faut-il prendre les mesures avant de demander un devis ?", "Non. Une estimation suffit pour un premier prix : nombre de fenêtres et dimensions approximatives. Les cotes exactes sont relevées avant la commande."),
         ("PVC ou aluminium ?", "Le PVC isole bien pour un budget contenu. L'aluminium permet des profils plus fins et de grandes baies. Le bois garde le cachet des maisons anciennes, fréquent en Normandie."),
         ("Combien de temps entre le devis et la pose ?", "Comptez en général 6 à 10 semaines de fabrication pour du sur-mesure, selon la saison et les options.")]),
  dict(slug="volets", short="Volets", name="Volets roulants et battants", spec="motorisé",
    ico='<rect class="ico" x="10" y="8" width="30" height="34"/><line class="ico" x1="10" y1="14" x2="40" y2="14"/><line class="ico" x1="10" y1="20" x2="40" y2="20"/><line class="ico" x1="10" y1="26" x2="40" y2="26"/><rect class="ico-acc" x="10" y="8" width="30" height="4"/>',
    tagline="Volets roulants motorisés, battants et coulissants, en rénovation ou en neuf.",
    title="Volets roulants et battants sur mesure – Eure | Seuil Normand",
    desc="Volets roulants motorisés ou solaires, volets battants alu ou PVC : devis gratuit autour d'Évreux, Rouen, Louviers et Brionne.",
    intro="Un volet bien choisi protège du froid, de la chaleur et des intrusions. Nous chiffrons des volets roulants (filaires, radio ou solaires) et des volets battants qui respectent le style des façades normandes.",
    points=["Volets roulants en rénovation, coffre extérieur ou intérieur", "Motorisation filaire, radio ou solaire sans travaux électriques", "Volets battants aluminium ou PVC, aspect bois possible", "Pilotage par télécommande ou smartphone", "Remplacement de manœuvre manuelle par moteur"],
    specs=[("Manœuvre", "manuelle, filaire, radio, solaire"), ("Tablier", "PVC ou aluminium"), ("Mesures utiles", "largeur × hauteur de la fenêtre, en cm"), ("Nombre", "précisez le nombre de volets")],
    faq=[("Peut-on motoriser des volets existants ?", "Souvent oui, selon l'état du tablier et du coffre. Indiquez-le dans votre demande avec une photo si possible."),
         ("Le volet solaire fonctionne-t-il en Normandie ?", "Oui. Les panneaux se rechargent aussi par temps couvert. Il évite de tirer des câbles, ce qui simplifie la pose en rénovation.")]),
  dict(slug="porte-entree", short="Porte d'entrée", name="Portes d'entrée", spec="5 points",
    ico='<rect class="ico" x="14" y="6" width="22" height="38"/><circle class="ico-acc" cx="31" cy="26" r="1.8"/><line class="ico" x1="8" y1="44" x2="42" y2="44"/>',
    tagline="Portes d'entrée acier, aluminium, bois ou mixtes, sécurisées et isolantes.",
    title="Porte d'entrée sur mesure alu, acier, bois | Seuil Normand",
    desc="Portes d'entrée sur mesure en aluminium, acier, bois ou mixte : devis gratuit près d'Évreux, Rouen, Bernay et du Neubourg.",
    intro="La porte d'entrée donne le ton de la maison et en assure la sécurité. Nous chiffrons des portes contemporaines ou classiques, de fabrication française, avec serrure multipoints et bonne isolation thermique.",
    points=["Aluminium, acier, bois ou mixte bois-alu", "Serrure 3 ou 5 points, options anti-effraction", "Vitrages décoratifs, impostes et tierces", "Poignées, barres de tirage et coloris au choix", "Ouverture motorisée ou par empreinte digitale en option"],
    specs=[("Isolation (coefficient Ud)", "selon modèle, à partir d'environ 1,0 W/m².K"), ("Sécurité", "serrure multipoints, cylindre renforcé"), ("Mesures utiles", "largeur × hauteur de l'ouverture, en cm"), ("Sens d'ouverture", "poussant gauche ou droit, vu de l'extérieur")],
    faq=[("Combien coûte une porte d'entrée ?", "Le prix dépend surtout du matériau, des vitrages et de la sécurité. Le devis gratuit vous donne un prix précis pour votre ouverture."),
         ("Peut-on garder le dormant existant ?", "C'est possible en rénovation si le dormant est sain, ce qui évite de reprendre la maçonnerie.")]),
  dict(slug="porte-garage", short="Porte de garage", name="Portes de garage", spec="motorisable",
    ico='<path class="ico" d="M6 44V18l19-10 19 10v26"/><rect class="ico" x="12" y="24" width="26" height="20"/><line class="ico" x1="12" y1="30" x2="38" y2="30"/><line class="ico" x1="12" y1="36" x2="38" y2="36"/>',
    tagline="Portes sectionnelles, enroulables, basculantes ou battantes, motorisées.",
    title="Porte de garage motorisée sur mesure – Eure | Seuil Normand",
    desc="Porte de garage sectionnelle, enroulable, basculante ou battante, motorisée : devis gratuit autour d'Évreux, Rouen, Pont-Audemer et Brionne.",
    intro="Une porte de garage motorisée change le quotidien. Nous chiffrons des portes sur mesure de fabrication française, adaptées à la taille de votre ouverture et à la place disponible sous plafond.",
    points=["Sectionnelle plafond ou latérale", "Enroulable pour les garages sans retombée", "Basculante et battante pour les rénovations simples", "Motorisation, télécommandes et commande smartphone", "Portillon intégré et hublots en option"],
    specs=[("Mesures utiles", "largeur × hauteur de l'ouverture, en cm"), ("Retombée de linteau", "hauteur entre le haut de l'ouverture et le plafond"), ("Écoinçons", "place libre à gauche et à droite de l'ouverture"), ("Isolation", "panneaux isolés de 40 mm courants")],
    faq=[("Quelle porte choisir si j'ai peu de place sous le plafond ?", "La porte enroulable, ou une sectionnelle à faible retombée. Indiquez la retombée de linteau dans votre demande."),
         ("Peut-on motoriser une porte existante ?", "Selon le modèle, oui. Pour une vieille porte basculante, le remplacement est souvent plus fiable.")]),
  dict(slug="portail", short="Portail", name="Portails et clôtures", spec="sur mesure",
    ico='<line class="ico" x1="6" y1="12" x2="6" y2="44"/><line class="ico" x1="44" y1="12" x2="44" y2="44"/><path class="ico" d="M8 20h17v22H8zM25 20h17v22H25z"/><line class="ico" x1="12" y1="20" x2="12" y2="42"/><line class="ico" x1="16" y1="20" x2="16" y2="42"/><line class="ico" x1="34" y1="20" x2="34" y2="42"/><line class="ico" x1="38" y1="20" x2="38" y2="42"/>',
    tagline="Portails battants ou coulissants en aluminium, portillons et clôtures assorties.",
    title="Portail alu battant ou coulissant – Eure | Seuil Normand",
    desc="Portails aluminium battants ou coulissants, motorisés, portillons et clôtures : devis gratuit autour d'Évreux, Rouen, Louviers et du Neubourg.",
    intro="Le portail est la première chose qu'on voit de chez vous. Nous chiffrons des portails aluminium sur mesure, battants ou coulissants, avec portillon et clôture assortis, motorisés si vous le souhaitez.",
    points=["Portails battants ou coulissants", "Aluminium sans entretien, nombreux coloris", "Portillons et clôtures de la même gamme", "Motorisation, interphone et visiophone", "Piliers et poteaux selon votre terrain"],
    specs=[("Largeur de passage", "entre piliers, en cm"), ("Hauteur souhaitée", "en cm"), ("Terrain", "plat ou en pente (précisez)"), ("Coulissant", "place de refoulement disponible le long de la clôture")],
    faq=[("Battant ou coulissant ?", "Le battant convient aux allées plates avec de la place pour l'ouverture. Le coulissant libère l'allée mais demande de la place le long de la clôture."),
         ("Faut-il une déclaration en mairie ?", "Selon le plan local d'urbanisme de votre commune, un portail ou une clôture peut demander une déclaration préalable. Renseignez-vous auprès de votre mairie.")]),
  dict(slug="pergola", short="Pergola", name="Pergolas bioclimatiques", spec="lames orientables",
    ico='<line class="ico" x1="8" y1="16" x2="8" y2="44"/><line class="ico" x1="42" y1="16" x2="42" y2="44"/><rect class="ico" x="5" y="10" width="40" height="6"/><line class="ico" x1="12" y1="10" x2="12" y2="16"/><line class="ico" x1="19" y1="10" x2="19" y2="16"/><line class="ico" x1="26" y1="10" x2="26" y2="16"/><line class="ico" x1="33" y1="10" x2="33" y2="16"/><rect class="ico-acc" x="5" y="10" width="40" height="2"/>',
    tagline="Pergolas aluminium à lames orientables, adossées ou autoportées.",
    title="Pergola bioclimatique sur mesure – Eure | Seuil Normand",
    desc="Pergola bioclimatique aluminium à lames orientables, adossée ou autoportée, sur mesure : devis gratuit près d'Évreux, Rouen et du Neubourg.",
    intro="Une pergola bioclimatique permet de profiter de la terrasse de mars à octobre : les lames s'orientent pour laisser passer le soleil ou fermer en cas d'averse. Nous chiffrons des pergolas sur mesure de fabrication française.",
    points=["Lames orientables motorisées, étanches une fois fermées", "Adossée à la façade ou autoportée", "Stores latéraux, éclairage LED, capteur de pluie", "Structure aluminium, coloris au choix", "Dimensions sur mesure selon la terrasse"],
    specs=[("Dimensions de la terrasse", "largeur × profondeur, en cm"), ("Implantation", "adossée ou autoportée"), ("Exposition", "orientation de la terrasse (sud, ouest…)"), ("Urbanisme", "déclaration préalable souvent requise au-delà de 5 m²")],
    faq=[("Faut-il une autorisation pour une pergola ?", "Au-delà de 5 m² d'emprise, une déclaration préalable est en général demandée, et un permis au-delà de 20 m² dans certains cas. Vérifiez auprès de votre mairie."),
         ("Une pergola résiste-t-elle au vent normand ?", "Les pergolas sérieuses sont dimensionnées pour le vent et la neige. Les lames se mettent en position de sécurité automatiquement avec un capteur.")]),
  dict(slug="portes-interieures", short="Portes intérieures", name="Portes intérieures", spec="bloc-porte",
    ico='<rect class="ico" x="15" y="6" width="20" height="38"/><rect class="ico" x="19" y="10" width="12" height="13"/><rect class="ico" x="19" y="27" width="12" height="13"/><circle class="ico-acc" cx="32" cy="25" r="1.5"/>',
    tagline="Blocs-portes, portes coulissantes et verrières pour la rénovation intérieure.",
    title="Portes intérieures et coulissantes – Eure | Seuil Normand",
    desc="Portes intérieures, blocs-portes, portes coulissantes et portes à galandage : devis gratuit autour d'Évreux, Rouen, Bernay et Brionne.",
    intro="Changer les portes intérieures transforme une maison sans gros travaux. Nous chiffrons des portes intérieures de fabrication française : blocs-portes complets, portes seules, coulissantes ou à galandage.",
    points=["Blocs-portes complets ou portes seules", "Portes coulissantes en applique ou à galandage", "Portes vitrées et verrières d'atelier", "Finitions prépeintes, laquées ou plaquées bois", "Portes techniques : coupe-feu, isophoniques"],
    specs=[("Mesures utiles", "largeur de passage, hauteur et épaisseur de cloison"), ("Nombre de portes", "précisez pièce par pièce si possible"), ("Sens d'ouverture", "poussant gauche ou droit"), ("Finition", "à peindre, laquée, bois")],
    faq=[("Bloc-porte ou porte seule ?", "Si l'huisserie est en bon état et aux bonnes dimensions, la porte seule suffit. Sinon le bloc-porte complet donne un résultat plus propre."),
         ("Peut-on poser une porte à galandage en rénovation ?", "Oui, avec un châssis à intégrer dans la cloison. Cela demande un peu de reprise de plâtrerie.")]),
]

CITIES = [
  ("evreux", "Évreux", "27000", 18), ("rouen", "Rouen", "76000", 39), ("louviers", "Louviers", "27400", 21),
  ("elbeuf", "Elbeuf", "76500", 20), ("bernay", "Bernay", "27300", 13), ("le-neubourg", "Le Neubourg", "27110", 6),
  ("brionne", "Brionne", "27800", 0), ("pont-audemer", "Pont-Audemer", "27500", 23), ("val-de-reuil", "Val-de-Reuil", "27100", 27),
  ("conches-en-ouche", "Conches-en-Ouche", "27190", 17), ("lisieux", "Lisieux", "14100", 34), ("vernon", "Vernon", "27200", 40),
  ("bourg-achard", "Bourg-Achard", "27310", 19), ("gaillon", "Gaillon", "27600", 30),
]
MORE_TOWNS = [("Grand Bourgtheroulde", 17), ("Gravigny", 17), ("Saint-Sébastien-de-Morsent", 14), ("Caudebec-lès-Elbeuf", 21),
  ("Pont-de-l'Arche", 26), ("Beuzeville", 32), ("Breteuil", 31), ("Les Andelys", 39), ("Pacy-sur-Eure", 34), ("Honfleur", 43)]


IMG = {
  "hero": "photo-1748063578185-3d68121b11ff", "hero2": "photo-1783125127341-81112b795c23",
  "fenetres": "photo-1774199679021-db3b421867c3", "fenetres2": "photo-1600210492493-0946911123ea",
  "volets": "photo-1534691601885-2b18af007add", "volets2": "photo-1496045737814-5ef82eb050fd",
  "porte-entree": "photo-1607900840367-a83dcd63296d", "porte-garage": "photo-1770756051811-1612ac8bedfa",
  "portail": "photo-1759043164225-ecacd7e0b9e5", "pergola": "photo-1761158494048-9693304c68b0",
  "portes-interieures": "photo-1628744876657-abd5086695dc",
}
ALT = {"hero": "Maison contemporaine avec grandes baies vitrées au crépuscule", "hero2": "Maison blanche avec porte de garage",
  "fenetres": "Séjour lumineux avec grandes baies vitrées", "fenetres2": "Salon avec fenêtres sur le jardin",
  "volets": "Façade blanche avec volets verts", "volets2": "Volets en bois sur une fenêtre ancienne",
  "porte-entree": "Porte d'entrée grise sur une façade en brique", "porte-garage": "Maison moderne avec porte de garage",
  "portail": "Portail métallique devant une maison", "pergola": "Pergola aluminium contemporaine",
  "portes-interieures": "Entrée lumineuse avec porte intérieure noire"}
def img(key, w=1200, h=None, cls="", eager=False):
    q = f"?auto=format&fit=crop&w={w}&q=70" + (f"&h={h}" if h else "")
    q2 = f"?auto=format&fit=crop&w={w//2}&q=70" + (f"&h={h//2}" if h else "")
    u = "https://images.unsplash.com/" + IMG[key]
    return (f'<img class="{cls}" src="{u}{q}" srcset="{u}{q2} {w//2}w, {u}{q} {w}w" sizes="(max-width: 820px) 100vw, 50vw" '
            f'alt="{e(ALT[key])}" {"" if eager else "loading=lazy"} decoding="async">')
VIDEO = dict(src="https://videos.pexels.com/video-files/10959786/10959786-hd_1280_720_30fps.mp4",
             poster="https://images.pexels.com/videos/10959786/pexels-photo-10959786.jpeg?auto=compress&w=1280")


CITY_TEXT = {
 "evreux": ("Préfecture de l'Eure, Évreux mêle centre ancien, quartiers pavillonnaires des années 1960 à 1980 et constructions récentes. Dans ces maisons, changer des fenêtres simple vitrage ou une porte de garage d'origine fait vite baisser la facture de chauffage.", ["Gravigny", "Saint-Sébastien-de-Morsent", "Guichainville", "Angerville-la-Campagne", "Arnières-sur-Iton"]),
 "rouen": ("À Rouen et dans sa métropole, on rénove aussi bien des maisons à pans de bois que des pavillons de la rive gauche. Les menuiseries sur mesure permettent de respecter le style d'une façade ancienne tout en gagnant en isolation.", ["Bois-Guillaume", "Mont-Saint-Aignan", "Sotteville-lès-Rouen", "Le Grand-Quevilly", "Bonsecours"]),
 "louviers": ("Entre la vallée de l'Eure et le plateau, Louviers compte beaucoup de maisons en brique et de pavillons à rénover. Fenêtres, volets roulants et portails font partie des demandes les plus courantes du secteur.", ["Val-de-Reuil", "Incarville", "Pinterville", "Acquigny", "Le Vaudreuil"]),
 "elbeuf": ("À Elbeuf et dans les communes de la boucle de Seine, les maisons de ville en brique côtoient les lotissements. Une porte d'entrée isolante ou des fenêtres neuves changent vraiment le confort d'un logement ancien.", ["Caudebec-lès-Elbeuf", "Saint-Pierre-lès-Elbeuf", "Saint-Aubin-lès-Elbeuf", "Cléon", "Tourville-la-Rivière"]),
 "bernay": ("Bernay, aux portes du Pays d'Auge, garde de nombreuses maisons à colombages et longères. Nous chiffrons des menuiseries bois ou alu adaptées à ce bâti traditionnel comme aux maisons plus récentes.", ["Menneval", "Plasnes", "Serquigny", "Courbépine", "Saint-Léger-de-Rôtes"]),
 "le-neubourg": ("Au cœur du plateau du Neubourg, entre champs et villages, les maisons individuelles avec terrain sont la règle. Portails, portes de garage et pergolas y sont souvent demandés avec les fenêtres.", ["Saint-Aubin-d'Écrosville", "Vitot", "Crosville-la-Vieille", "Sainte-Colombe-la-Commanderie", "Le Troncq"]),
 "brionne": ("Dans la vallée de la Risle, Brionne et ses environs comptent beaucoup de maisons anciennes en pierre et en brique. Des fenêtres et des volets sur mesure permettent de les isoler sans dénaturer leur façade.", ["Calleville", "Harcourt", "Neuville-sur-Authou", "Aclou", "Saint-Cyr-de-Salerne"]),
 "pont-audemer": ("Surnommée la Venise normande, Pont-Audemer a un patrimoine à colombages important, entouré de quartiers pavillonnaires. Fenêtres bois, portes d'entrée et volets battants sont des demandes fréquentes.", ["Saint-Germain-Village", "Manneville-sur-Risle", "Toutainville", "Corneville-sur-Risle", "Saint-Mards-de-Blacarville"]),
 "val-de-reuil": ("Ville nouvelle des années 1970, Val-de-Reuil compte de nombreux logements de cette époque dont les menuiseries arrivent en fin de vie. Les remplacer améliore nettement l'isolation et le confort.", ["Léry", "Poses", "Le Vaudreuil", "Pîtres", "Louviers"]),
 "conches-en-ouche": ("Dans le Pays d'Ouche, autour de Conches, les maisons de campagne et les corps de ferme rénovés demandent souvent des menuiseries sur mesure, des portails larges et des portes de garage adaptées.", ["Ferrières-Haut-Clocher", "La Bonneville-sur-Iton", "Collandres-Quincarnon", "Sébécourt", "Le Fidelaire"]),
 "lisieux": ("Capitale du Pays d'Auge, Lisieux et ses environs mêlent maisons normandes traditionnelles et pavillons. Nous chiffrons des menuiseries qui respectent ce style comme des modèles contemporains.", ["Saint-Désir", "Hermival-les-Vaux", "Ouilly-le-Vicomte", "Glos", "Beuvillers"]),
 "vernon": ("En bord de Seine, Vernon et ses environs comptent maisons bourgeoises, pavillons et constructions récentes. Pergolas et grandes baies vitrées y sont souvent demandées pour profiter du jardin.", ["Saint-Marcel", "Saint-Just", "Gasny", "Pacy-sur-Eure", "La Chapelle-Longueville"]),
 "bourg-achard": ("Dans le Roumois, autour de Bourg-Achard, beaucoup de maisons récentes et de longères rénovées. Portails motorisés, portes de garage et fenêtres sont au cœur des projets du secteur.", ["Bosroumois", "Grand Bourgtheroulde", "Thénouville", "Le Landin", "Barneville-sur-Seine"]),
 "gaillon": ("Entre Seine et coteaux, Gaillon et Le Val d'Hazey comptent beaucoup de maisons individuelles. Volets roulants, fenêtres et portes de garage motorisées y sont parmi les demandes les plus fréquentes.", ["Le Val d'Hazey", "Saint-Aubin-sur-Gaillon", "Ailly", "Courcelles-sur-Seine", "Fontaine-Heudebourg"]),
}
CITY_IMG = {"evreux": "hero2", "rouen": "fenetres", "louviers": "volets", "elbeuf": "porte-entree", "bernay": "volets2", "le-neubourg": "portail",
 "brionne": "porte-garage", "pont-audemer": "fenetres2", "val-de-reuil": "hero", "conches-en-ouche": "pergola", "lisieux": "porte-entree",
 "vernon": "pergola", "bourg-achard": "portail", "gaillon": "hero2"}

LEGAL = dict(name="Victor Tricheur", siret="994 247 831 00013", phone="06 37 99 00 92", email="contact@seuilnormand.fr")
FACEBOOK = "https://www.facebook.com/profile.php?id=61596127125985"
INSTAGRAM = "https://www.instagram.com/seuilnormand/"
NOINDEX = {"mentions-legales", "confidentialite", "404"}
TODAY = __import__("datetime").date.today().isoformat()

# ---------- Gabarits ----------
def head(title, desc, path, artifact=False):
    canon = SITE + "/" + ("" if path == "index.html" else path)
    robots = '<meta name="robots" content="noindex, follow">\n' if path[:-5] in NOINDEX else '<meta name="robots" content="index, follow, max-image-preview:large">\n'
    meta = (f'<title>{e(title)}</title>\n{robots}<meta name="claude:viewport-fit-sides" content="cover">\n'
            f'<meta name="description" content="{e(desc)}">\n<link rel="canonical" href="{canon}">\n'
            f'<link rel="icon" href="favicon.svg" type="image/svg+xml"><link rel="icon" href="favicon.png" type="image/png" sizes="64x64"><link rel="apple-touch-icon" href="apple-touch-icon.png">\n'
            f'<meta property="og:type" content="website"><meta property="og:site_name" content="Seuil Normand"><meta property="og:image" content="{SITE}/og-image.png"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta name="twitter:card" content="summary_large_image"><meta name="theme-color" content="#2e5a4c">\n'
            f'<meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{canon}"><meta property="og:locale" content="fr_FR">\n'
            f'{FONTS}\n<link rel="stylesheet" href="style.css">\n')
    if artifact:
        return meta
    return ('<!doctype html>\n<html lang="fr">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n' + meta + '</head>\n<body>\n')

def tail(artifact=False):
    s = '<script src="cp.js"></script>\n<script src="site.js"></script>\n'
    return s if artifact else s + '</body>\n</html>\n'

def topbar():
    return ('<header class="top"><div class="wrap">'
            '<a class="brand" href="index.html"><b>Seuil Normand</b><span>Fenêtres, portes, portails · Eure</span></a>'
            '<nav aria-label="Menu principal"><a href="index.html#gamme">Nos produits</a><a href="index.html#zone">Secteur</a><a href="index.html#fonctionnement">Comment ça marche</a><a href="conseils.html">Conseils</a></nav>'
            '<a class="btn" href="#devis">Demander un devis</a></div></header>\n')

def loc(name):
    """'à Évreux' / 'au Neubourg'"""
    if name.startswith("Le "): return "au " + name[3:]
    if name.startswith("Les "): return "aux " + name[4:]
    return "à " + name

def footer():
    prods = "".join(f'<li><a href="{p["slug"]}.html">{e(p["name"])}</a></li>' for p in PRODUCTS)
    cities = "".join(f'<li><a href="{c[0]}.html">Menuiserie {e(loc(c[1]))}</a></li>' for c in CITIES)
    return (f'<footer><div class="wrap">'
            f'<div><h3>Seuil Normand</h3><p class="small">Service gratuit de demande de devis pour vos menuiseries et fermetures, en lien avec un négoce-menuisier installé dans l\'Eure depuis 50 ans.</p>'
            f'<p class="small" style="margin-top:.6rem">Tél. <span class="mono">{LEGAL["phone"]}</span></p>'
            f'<p class="small social"><a href="{FACEBOOK}" rel="me noopener" target="_blank">Facebook</a> · <a href="{INSTAGRAM}" rel="me noopener" target="_blank">Instagram @seuilnormand</a></p></div>'
            f'<div><h3>Produits</h3><ul>{prods}</ul></div>'
            f'<div><h3>Secteur</h3><ul>{cities}</ul></div>'
            f'<div><h3>Informations</h3><ul><li><a href="mentions-legales.html">Mentions légales</a></li><li><a href="confidentialite.html">Données personnelles</a></li><li><a href="fonctionnement.html">Fonctionnement du service</a></li><li><a href="conseils.html">Conseils et prix</a></li></ul></div>'
            f'</div></footer>\n')

def form(prefill=None, heading="Votre devis gratuit", place=""):
    chips = "".join(
        f'<label><input type="checkbox" name="produits" value="{e(p["short"])}" id="p-{p["slug"]}"{" checked" if p["slug"]==prefill else ""}> {e(p["short"])}</label>'
        for p in PRODUCTS)
    aside_place = f" à {e(place)}" if place else " dans l'Eure et autour"
    return f'''<section id="devis" class="band"><div class="wrap quote">
<div class="quote-aside">
  <p class="eyebrow">Devis gratuit, sans engagement</p>
  <h2>{e(heading)}</h2>
  <p>Décrivez votre projet{aside_place}. Nous vous rappelons sous 48 h ouvrées pour le préciser, puis vous recevez un devis chiffré.</p>
  <ul><li>Fabrication française, sur mesure</li><li>Conseils d'un négoce-menuisier normand établi depuis 50 ans</li><li>Vous restez libre de ne pas donner suite</li></ul>
</div>
<form class="devis" novalidate>
  <fieldset><legend>Que souhaitez-vous ?</legend><div class="chips">{chips}</div></fieldset>
  <div class="row2">
    <div class="field"><label for="projet">Type de projet</label><select id="projet" name="projet"><option>Rénovation</option><option>Construction neuve</option><option>Je ne sais pas encore</option></select></div>
    <div class="field"><label for="pose">Pose</label><select id="pose" name="pose"><option>Fourniture et pose</option><option>Fourniture seule</option><option>À voir ensemble</option></select></div>
  </div>
  <div class="row2">
    <div class="field"><label for="code_postal">Code postal du chantier</label><input type="text" id="code_postal" name="code_postal" inputmode="numeric" pattern="[0-9]{{5}}" maxlength="5" required autocomplete="postal-code" placeholder="27800"></div>
    <div class="field"><label for="commune">Commune</label><input type="text" id="commune" name="commune" autocomplete="address-level2" placeholder="Brionne"></div>
  </div>
  <div class="field"><label for="details">Votre projet <span class="hint">nombre, dimensions approximatives, matériau souhaité</span></label><textarea id="details" name="details" placeholder="Ex. : 4 fenêtres PVC blanc, environ 100 × 120 cm, et une porte-fenêtre 140 × 215 cm"></textarea></div>
  <div class="field"><label for="delai">Quand souhaitez-vous réaliser les travaux ?</label><select id="delai" name="delai"><option>Dès que possible</option><option>Dans les 3 mois</option><option>Dans 3 à 6 mois</option><option>Plus tard / je me renseigne</option></select></div>
  <div class="row2">
    <div class="field"><label for="nom">Nom</label><input type="text" id="nom" name="nom" required autocomplete="name"></div>
    <div class="field"><label for="telephone">Téléphone</label><input type="tel" id="telephone" name="telephone" required autocomplete="tel" pattern="[0-9 +.]{{10,}}"></div>
  </div>
  <div class="field"><label for="email">Email</label><input type="email" id="email" name="email" required autocomplete="email"></div>
  <input type="text" name="_honey" id="_honey" tabindex="-1" autocomplete="off" aria-hidden="true" style="position:absolute;left:-9999px">
  <label class="consent" for="consent"><input type="checkbox" id="consent" name="consent" required> J'accepte que mes coordonnées soient transmises au professionnel partenaire pour l'établissement de mon devis. <a href="confidentialite.html">En savoir plus</a></label>
  <button class="btn" type="submit">Recevoir mon devis gratuit</button>
  <p class="form-msg" hidden role="status"></p>
</form>
</div></section>
'''

ELEVATION = '''<figure class="elevation">
<svg viewBox="0 0 560 330" role="img" aria-labelledby="elev-t">
<title id="elev-t">Élévation d'une maison normande avec ses menuiseries : fenêtres, volets, porte d'entrée, porte de garage, portail et pergola</title>
<line class="elev-ground" x1="0" y1="290" x2="560" y2="290"/>
<path class="elev-fill" d="M70 290V130L180 60L290 130V290Z"/>
<path class="elev-fine" d="M70 130H290M100 150V290M130 150L160 200M260 150V290M230 150L200 200M100 210H260"/>
<rect class="elev-fill" x="108" y="160" width="40" height="46"/><line class="elev-fine" x1="128" y1="160" x2="128" y2="206"/>
<rect class="elev-shutter" x="92" y="160" width="14" height="46"/><rect class="elev-shutter" x="150" y="160" width="14" height="46"/>
<rect class="elev-fill" x="212" y="160" width="40" height="46"/><line class="elev-fine" x1="232" y1="160" x2="232" y2="206"/>
<rect class="elev-shutter" x="196" y="160" width="14" height="46"/><rect class="elev-shutter" x="254" y="160" width="14" height="46"/>
<rect class="elev-fill" x="162" y="222" width="36" height="68"/><circle cx="191" cy="258" r="2" fill="var(--oak)"/>
<rect class="elev-fill" x="164" y="96" width="32" height="24"/><line class="elev-fine" x1="180" y1="96" x2="180" y2="120"/>
<path class="elev-fill" d="M290 290V180H380V290Z"/>
<path class="elev-stroke" d="M284 180L335 150L386 180"/>
<rect class="elev-fill" x="302" y="210" width="66" height="80"/>
<path class="elev-fine" d="M302 226H368M302 242H368M302 258H368M302 274H368"/>
<path class="elev-stroke" d="M400 290V196M548 290V196"/>
<rect class="elev-fill" x="396" y="190" width="156" height="8"/>
<path class="elev-fine" d="M410 190v8M424 190v8M438 190v8M452 190v8M466 190v8M480 190v8M494 190v8M508 190v8M522 190v8M536 190v8"/>
<path class="elev-stroke" d="M10 290V246M58 290V246"/>
<path class="elev-fine" d="M12 252H56M12 284H56M18 252V284M26 252V284M34 252V284M42 252V284M50 252V284"/>
<path class="elev-dim" d="M302 300H368M302 296V304M368 296V304"/><text class="elev-dimtext" x="335" y="314" text-anchor="middle">240 cm</text>
<path class="elev-dim" d="M108 150H148M108 146V154M148 146V154"/><text class="elev-dimtext" x="128" y="143" text-anchor="middle">100</text>
<g class="elev-tag" tabindex="0" role="link" data-goto="fenetres.html" aria-label="Fenêtres"><line x1="232" y1="160" x2="232" y2="40"/><rect x="200" y="22" width="72" height="22" rx="2"/><text x="236" y="37" text-anchor="middle">Fenêtres</text></g>
<g class="elev-tag" tabindex="0" role="link" data-goto="volets.html" aria-label="Volets"><line x1="99" y1="160" x2="70" y2="96"/><rect x="24" y="76" width="62" height="22" rx="2"/><text x="55" y="91" text-anchor="middle">Volets</text></g>
<g class="elev-tag" tabindex="0" role="link" data-goto="porte-entree.html" aria-label="Porte d'entrée"><line x1="180" y1="240" x2="180" y2="232"/><rect x="128" y="300" width="104" height="22" rx="2"/><line x1="180" y1="290" x2="180" y2="300"/><text x="180" y="315" text-anchor="middle">Porte d'entrée</text></g>
<g class="elev-tag" tabindex="0" role="link" data-goto="porte-garage.html" aria-label="Porte de garage"><line x1="335" y1="210" x2="335" y2="128"/><rect x="290" y="106" width="110" height="22" rx="2"/><text x="345" y="121" text-anchor="middle">Porte de garage</text></g>
<g class="elev-tag" tabindex="0" role="link" data-goto="pergola.html" aria-label="Pergola"><line x1="474" y1="190" x2="474" y2="160"/><rect x="440" y="138" width="68" height="22" rx="2"/><text x="474" y="153" text-anchor="middle">Pergola</text></g>
<g class="elev-tag" tabindex="0" role="link" data-goto="portail.html" aria-label="Portail"><line x1="34" y1="246" x2="34" y2="228"/><rect x="2" y="206" width="64" height="22" rx="2"/><text x="34" y="221" text-anchor="middle">Portail</text></g>
</svg>
<figcaption>Élévation façade · cotes en cm · cliquez une étiquette</figcaption>
</figure>'''

def range_list():
    items = "".join(f'''<a href="{p["slug"]}.html"><svg viewBox="0 0 50 50" aria-hidden="true">{p["ico"]}</svg><div><h3>{e(p["name"])}</h3><p>{e(p["tagline"])}</p></div><span class="spec">{e(p["spec"])}</span></a>''' for p in PRODUCTS)
    return f'<div class="range">{items}</div>'

def zone_block(h="Nous intervenons dans l'Eure et autour"):
    lis = "".join(f'<li><a href="{c[0]}.html">{e(c[1])}</a></li>' for c in sorted(CITIES, key=lambda c: c[1]))
    lis += "".join(f'<li>{e(n)}</li>' for n, k in sorted(MORE_TOWNS))
    return f'''<section id="zone"><div class="wrap zone">
<div class="section-head" style="margin:0">
  <p class="eyebrow">Secteur d'intervention</p><h2>{e(h)}</h2>
  <p>Nous intervenons autour du Neubourg, de Brionne et d'Évreux, jusqu'à Rouen, Lisieux et Vernon. Votre commune n'est pas dans la liste ? Envoyez votre demande, nous vous répondons.</p>
</div>
<ul class="zone-list" aria-label="Communes desservies">{lis}</ul>
</div></section>
'''

STEPS = '''<section id="fonctionnement" class="band"><div class="wrap">
<div class="section-head"><p class="eyebrow">Comment ça marche</p><h2>Du formulaire au devis en trois temps</h2></div>
<ol class="steps">
<li><h3>Vous décrivez votre projet</h3><p>Deux minutes en ligne : les produits, votre code postal, quelques dimensions si vous les avez.</p></li>
<li><h3>Un conseiller vous rappelle</h3><p>Sous 48 h ouvrées, pour préciser les mesures, les matériaux et vos contraintes, ou caler un passage chez vous.</p></li>
<li><h3>Vous recevez votre devis</h3><p>Un prix détaillé établi par notre négoce-menuisier partenaire. Gratuit, et vous restez libre d'accepter ou non.</p></li>
</ol>
</div></section>
'''

def crumbs(*items):
    """items = (nom, chemin) ; l'accueil est ajouté en tête"""
    lst = [("Accueil", "")] + list(items)
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + "/" + u} for i, (n, u) in enumerate(lst)]}

def jsonld(obj):
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False) + '</script>\n'

AREA = [{"@type": "City", "name": c[1]} for c in CITIES]
SERVICE = {"@context": "https://schema.org", "@type": "Service", "name": "Seuil Normand – devis menuiseries et fermetures",
           "serviceType": "Fourniture et pose de menuiseries", "areaServed": AREA, "url": SITE + "/",
           "provider": {"@type": "Organization", "name": "Seuil Normand", "telephone": "+33637990092", "url": SITE + "/"}}

# ---------- Pages ----------
BRAND = {"@context": "https://schema.org", "@graph": [
    {"@type": "WebSite", "@id": SITE + "/#website", "name": "Seuil Normand", "alternateName": ["SeuilNormand", "seuilnormand.fr"], "url": SITE + "/", "inLanguage": "fr-FR", "publisher": {"@id": SITE + "/#org"}},
    {"@type": "Organization", "@id": SITE + "/#org", "name": "Seuil Normand", "url": SITE + "/", "logo": SITE + "/apple-touch-icon.png", "image": SITE + "/og-image.png",
     "description": "Service gratuit de demande de devis pour fenêtres, volets, portes, portails et pergolas sur mesure dans l'Eure et en Normandie.",
     "email": "contact@seuilnormand.fr", "telephone": "+33637990092", "areaServed": "Eure (27), Normandie", "sameAs": [FACEBOOK, INSTAGRAM], "address": {"@type": "PostalAddress", "postalCode": "27110", "addressLocality": "Le Neubourg", "addressRegion": "Normandie", "addressCountry": "FR"}}]}

def page_index(art=False):
    t = "Seuil Normand – Fenêtres, portes, portails et pergolas dans l'Eure"
    d = "Seuil Normand : devis gratuit pour vos fenêtres, volets, portes, portails et pergolas sur mesure autour d'Évreux, Rouen, Bernay et du Neubourg."
    if art: t = "Seuil Normand"
    return (head(t, d, "index.html", art) + jsonld(SERVICE) + jsonld(BRAND) + topbar() +
f'''<main>
<section class="hero"><div class="wrap">
<div class="hero-text">
  <p class="eyebrow">Seuil Normand · Eure · Seine-Maritime · Pays d'Auge</p>
  <h1>Fenêtres, portes, portails et pergolas sur mesure dans l'Eure</h1>
  <p class="lead"><strong>Seuil Normand</strong> est un service gratuit de demande de devis : décrivez votre projet, nous le confions à un négoce-menuisier normand établi depuis 50 ans. Devis gratuit, fabrication française.</p>
  <div class="hero-cta"><a class="btn" href="#devis">Demander mon devis gratuit</a><a class="btn ghost" href="#gamme">Voir les produits</a></div>
  <div class="facts"><div><strong>7</strong>familles de produits</div><div><strong>100 %</strong>sur mesure</div><div><strong>48 h</strong>pour vous rappeler</div></div>
</div>
{ELEVATION}
</div></section>
<section class="showcase"><div class="showcase-media"><video autoplay muted loop playsinline preload="metadata" poster="{VIDEO["poster"]}"><source src="{VIDEO["src"]}" type="video/mp4"></video></div>
<div class="wrap showcase-text"><p class="eyebrow">Sur mesure</p><p class="showcase-line">Pergola, baies vitrées, porte de garage : chaque élément est fabriqué aux cotes de votre maison.</p></div></section>
<section class="gallery-sec"><div class="wrap">
<div class="section-head"><p class="eyebrow">Inspirations</p><h2>Des idées pour votre maison</h2></div>
<div class="gallery">
<a href="fenetres.html" class="g g-big">{img("hero", 1400, 900)}<span>Baies vitrées</span></a>
<a href="pergola.html" class="g">{img("pergola", 800, 600)}<span>Pergolas</span></a>
<a href="porte-entree.html" class="g">{img("porte-entree", 800, 600)}<span>Portes d'entrée</span></a>
<a href="volets.html" class="g">{img("volets", 800, 600)}<span>Volets</span></a>
<a href="porte-garage.html" class="g">{img("porte-garage", 800, 600)}<span>Portes de garage</span></a>
</div>
<p class="credit">Photos d'illustration : Unsplash et Pexels, licence libre.</p>
</div></section>
<section id="gamme"><div class="wrap">
<div class="section-head"><p class="eyebrow">Nos produits</p><h2>Tout ce qui ouvre et ferme la maison</h2><p>Chaque produit a sa page avec les mesures à préparer et les questions fréquentes.</p></div>
{range_list()}
</div></section>
{STEPS}
{zone_block()}
{home_conseils()}
{form()}
</main>
''' + footer() + tail(art))

def page_product(p):
    others = "".join(f'<a href="{c[0]}.html">{e(p["short"])} {e(loc(c[1]))}</a>' for c in CITIES)
    rows = "".join(f'<tr><th scope="row">{e(a)}</th><td>{e(b)}</td></tr>' for a, b in p["specs"])
    faq = "".join(f'<details><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q, a in p["faq"])
    faq_ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in p["faq"]]}
    svc = dict(SERVICE, name=p["name"] + " – Seuil Normand", serviceType=p["name"], url=f'{SITE}/{p["slug"]}.html')
    pts = "".join(f"<li>{e(x)}</li>" for x in p["points"])
    return (head(p["title"], p["desc"], p["slug"] + ".html") + jsonld(svc) + jsonld(faq_ld) + jsonld(crumbs((p["name"], p["slug"] + ".html"))) + topbar() +
f'''<main>
<div class="wrap"><p class="crumbs"><a href="index.html">Accueil</a> › {e(p["name"])}</p>
<div class="page-head"><p class="eyebrow">{e(p["short"])} · Eure et alentours</p><h1>{e(p["name"])} sur mesure dans l'Eure</h1><p class="lead">{e(p["intro"])}</p><div class="hero-cta"><a class="btn" href="#devis">Demander un devis {e(p["short"].lower())}</a></div></div>
<figure class="page-photo">{img(p["slug"], 1600, 700, eager=True)}<figcaption>Photo d'illustration (Unsplash, licence libre)</figcaption></figure></div>
<section style="padding-top:0"><div class="wrap cols">
<div class="prose"><h2>Ce que nous chiffrons</h2><ul>{pts}</ul>
<h2 style="margin-top:1rem">Questions fréquentes</h2><div>{faq}</div></div>
<div class="prose"><h2>À préparer pour le devis</h2><div class="table-scroll"><table class="spec-table">{rows}</table></div>
<p class="hint">Pas sûr de vos mesures ? Donnez une estimation : elles sont vérifiées avant toute commande.</p>
{related(p["slug"])}<h3 style="margin-top:1rem">Près de chez vous</h3><div class="link-row">{others}</div></div>
</div></section>
{form(prefill=p["slug"], heading="Devis " + p["short"].lower() + " gratuit")}
</main>
''' + footer() + tail())

def page_city(c):
    slug, name, cp, km = c
    links = "".join(f'<a href="{p["slug"]}.html">{e(p["name"])}</a>' for p in PRODUCTS)
    t = f"Menuiserie {loc(name)} : fenêtres, portes, portails | Seuil Normand"
    d = f"Devis gratuit {loc(name)} ({cp}) : fenêtres, volets, portes d'entrée, portes de garage, portails et pergolas sur mesure. Fabrication française."
    svc = dict(SERVICE, areaServed={"@type": "City", "name": name}, url=f"{SITE}/{slug}.html")
    return (head(t, d, slug + ".html") + jsonld(svc) + jsonld(crumbs(("Menuiserie " + loc(name), slug + ".html"))) + topbar() +
f'''<main>
<div class="wrap"><p class="crumbs"><a href="index.html">Accueil</a> › <a href="index.html#zone">Secteur</a> › {e(name)}</p>
<div class="page-head"><p class="eyebrow mono">{e(name)} · {cp}</p><h1>Fenêtres, portes, portails et pergolas {e(loc(name))}</h1>
<p class="lead">Vous habitez {e(name)} ou ses environs ? Nous intervenons chez vous. Décrivez votre projet de menuiserie : nous vous rappelons pour le préciser et vous recevez un devis gratuit.</p>
<div class="hero-cta"><a class="btn" href="#devis">Demander un devis {e(loc(name))}</a></div></div>
<figure class="page-photo">{img(CITY_IMG.get(slug, "hero2"), 1600, 600, eager=True)}<figcaption>Photo d'illustration (Unsplash, licence libre)</figcaption></figure></div>
<section style="padding-top:0"><div class="wrap">
<div class="prose" style="margin-bottom:2rem;max-width:46rem"><h2>Vos menuiseries {e(loc(name))}</h2><p>{e(CITY_TEXT[slug][0])}</p><p>Communes voisines également desservies : {e(", ".join(CITY_TEXT[slug][1]))}.</p></div>
<div class="section-head"><h2>Nos produits {e(loc(name))}</h2></div>
{range_list()}
<h3 style="margin-top:1.5rem">Accès rapide</h3><div class="link-row" style="margin-top:.6rem">{links}</div><h3 style="margin-top:1.5rem">Nos guides</h3><div class="link-row" style="margin-top:.6rem">{"".join(f'<a href="{x["slug"]}.html">{e(x["short"])}</a>' for x in ARTICLES)}</div>
</div></section>
{form(heading="Votre devis à " + name, place=name)}
</main>
''' + footer() + tail())


def home_conseils():
    lis = "".join(f'<li><a href="{a["slug"]}.html"><b>{e(a["h1"])}</b></a><br><span class="hint">{e(a["desc"])}</span></li>' for a in ARTICLES[:6])
    return (f'<section id="conseils"><div class="wrap"><div class="section-head"><p class="eyebrow">Conseils</p><h2>Prix, aides et démarches : nos guides</h2></div>'
            f'<ul class="prose" style="list-style:none;padding:0;display:grid;gap:1.1rem;max-width:46rem">{lis}</ul>'
            f'<p style="margin-top:1rem"><a class="btn ghost" href="conseils.html">Tous les conseils</a></p></div></section>')

def related(slug):
    arts=[a for a in ARTICLES if a["product"]==slug]
    if not arts: return ""
    return '<h3 style="margin-top:1rem">À lire</h3><ul>' + "".join(f'<li><a href="{a["slug"]}.html">{e(a["h1"])}</a></li>' for a in arts) + '</ul>'

def page_article(a):
    others="".join(f'<li><a href="{o["slug"]}.html">{e(o["h1"])}</a></li>' for o in ARTICLES if o is not a)
    src="".join(f'<li><a href="{u}" target="_blank" rel="noopener">{e(t)}</a></li>' for t,u in a["sources"])
    prod=[p for p in PRODUCTS if p["slug"]==a["product"]][0]
    ld={"@context":"https://schema.org","@type":"Article","headline":a["h1"],"description":a["desc"],"datePublished":a["date"],"dateModified":a["date"],
        "author":{"@type":"Organization","name":"Seuil Normand"},"publisher":{"@type":"Organization","name":"Seuil Normand","logo":{"@type":"ImageObject","url":SITE+"/apple-touch-icon.png"}},
        "mainEntityOfPage":f'{SITE}/{a["slug"]}.html',"image":SITE+"/og-image.png"}
    return (head(a["title"], a["desc"], a["slug"]+".html") + jsonld(ld) + jsonld(crumbs(("Conseils", "conseils.html"), (a["h1"] if "h1" in a else a["title"].split(" | ")[0], a["slug"] + ".html"))) + topbar() +
f'''<main><div class="wrap">
<p class="crumbs"><a href="index.html">Accueil</a> › <a href="conseils.html">Conseils</a> › {e(a["short"])}</p>
<div class="page-head"><p class="eyebrow">Conseils · mis à jour en novembre 2026</p><h1>{e(a["h1"])}</h1><p class="lead">{e(a["lead"])}</p></div>
<figure class="page-photo">{img(a["img"], 1600, 600, eager=True)}<figcaption>Photo d'illustration (Unsplash, licence libre)</figcaption></figure>
<div class="cols"><article class="prose">{a["body"]}
<div class="card-cta"><h2>Un projet de {e(prod["short"].lower())} ?</h2><p>Décrivez-le en deux minutes : nous vous rappelons et vous recevez un devis gratuit, sans engagement.</p><p><a class="btn" href="#devis">Demander mon devis</a> <a class="btn ghost" href="{prod["slug"]}.html">Voir la page {e(prod["short"])}</a></p></div>
<h2>Sources</h2><ul class="sources">{src}</ul>
<p class="hint">Les prix indiqués sont des moyennes nationales relevées en 2026, à titre indicatif. Les règles sur les aides changent régulièrement : vérifiez votre situation avant de signer.</p>
</article>
<aside class="prose"><h3>Autres conseils</h3><ul>{others}</ul></aside></div>
</div>
{form(prefill=a["product"], heading="Votre devis gratuit")}
</main>
''' + footer() + tail())

def page_conseils():
    cards="".join(f'<a href="{a["slug"]}.html" class="g conseil">{img(a["img"],800,500)}<span>{e(a["short"])}</span></a>' for a in ARTICLES)
    lis="".join(f'<li><a href="{a["slug"]}.html"><b>{e(a["h1"])}</b></a><br><span class="hint">{e(a["desc"])}</span></li>' for a in ARTICLES)
    return (head("Conseils, prix et aides pour vos menuiseries | Seuil Normand", "Prix 2026, aides, TVA réduite et démarches pour vos fenêtres, portes de garage, portails et pergolas dans l'Eure.", "conseils.html") + topbar() +
f'''<main><div class="wrap"><p class="crumbs"><a href="index.html">Accueil</a> › Conseils</p>
<div class="page-head"><p class="eyebrow">Conseils</p><h1>Prix, aides et démarches pour vos menuiseries</h1><p class="lead">Des guides concrets pour préparer votre projet avant de demander un devis.</p></div>
<ul class="prose conseil-list" style="list-style:none;padding:0;display:grid;gap:1.2rem;max-width:46rem">{lis}</ul></div>
{form()}</main>''' + footer() + tail())

def page_text(slug, title, body):
    return (head(title + " | Seuil Normand", title + " du site Seuil Normand.", slug + ".html") + topbar() +
            f'<main><div class="wrap legal"><p class="crumbs"><a href="index.html">Accueil</a> › {e(title)}</p><h1>{e(title)}</h1>{body}</div></main>' + footer() + tail())

MENTIONS = f'''<p class="hint">Dernière mise à jour : 7 novembre 2026</p>
<h2>Éditeur du site</h2>
<p>Seuil Normand est un nom commercial exploité par {LEGAL["name"]}, entrepreneur individuel (micro-entreprise).<br>
SIRET : <span class="mono">{LEGAL["siret"]}</span><br>
Adresse : 27110 Le Neubourg, France<br>
Téléphone : <span class="mono">{LEGAL["phone"]}</span><br>
Email : {LEGAL["email"]}<br>
Directeur de la publication : {LEGAL["name"]}</p>
<h2>Hébergement</h2>
<p>[Hébergeur à compléter une fois le site mis en ligne : nom, adresse et téléphone.]</p>
<h2>Activité</h2>
<p>Seuil Normand est un service gratuit de mise en relation. Il ne vend pas lui-même de produits et ne réalise pas de travaux. Les devis, la vente et la pose sont assurés par le professionnel partenaire, sous sa propre responsabilité.</p>
<h2>Propriété intellectuelle</h2>
<p>Les textes et illustrations de ce site appartiennent à leur auteur. Toute reproduction sans autorisation est interdite.</p>'''

CONFID = f'''<p class="hint">Dernière mise à jour : 7 novembre 2026</p>
<h2>Ce que nous collectons</h2><p>Lorsque vous remplissez le formulaire : vos nom, téléphone, email, code postal, commune et la description de votre projet.</p>
<h2>Pourquoi</h2><p>Uniquement pour traiter votre demande de devis : vous rappeler, préciser votre projet et le transmettre au professionnel partenaire qui établit le devis. Base légale : votre consentement, que vous donnez en cochant la case du formulaire.</p>
<h2>Qui y a accès</h2><ul style="padding-left:1.2rem;display:grid;gap:.3rem"><li>Seuil Normand ({LEGAL["name"]}).</li><li>Le négoce-menuisier partenaire qui établit votre devis.</li><li>Nos prestataires techniques : FormSubmit (transmission du formulaire par email) et Google (messagerie). Certains sont situés aux États-Unis ; les transferts reposent sur les garanties prévues par le RGPD, comme le Data Privacy Framework ou les clauses contractuelles types.</li></ul>
<h2>Combien de temps</h2><p>12 mois après notre dernier échange sur votre projet, puis vos données sont supprimées.</p>
<h2>Vos droits</h2><p>Vous pouvez accéder à vos données, les faire corriger ou supprimer, vous opposer à leur traitement et retirer votre consentement à tout moment en écrivant à {LEGAL["email"]}. Réponse sous un mois. En cas de désaccord, vous pouvez saisir la CNIL (cnil.fr).</p>
<h2>Cookies</h2><p>Ce site ne dépose aucun cookie publicitaire ni de mesure d'audience.</p>'''

FONCT = '''<h2>Ce que fait Seuil Normand</h2><p>Seuil Normand est un service gratuit qui recueille vos demandes de devis de menuiseries et fermetures (fenêtres, volets, portes, portails, pergolas) et les transmet à un négoce-menuisier partenaire installé dans l'Eure.</p>
<h2>Comment Seuil Normand est rémunéré</h2><p>Le service est gratuit pour vous. Seuil Normand peut être rémunéré par le professionnel partenaire lorsqu'un projet est signé. Cette rémunération n'est jamais ajoutée à votre devis par Seuil Normand.</p>
<h2>Votre engagement</h2><p>Aucun. Vous êtes libre de ne donner suite à aucun devis.</p>
<h2>Secteur</h2><p>Nous intervenons dans l'Eure et les secteurs voisins. Les demandes plus éloignées sont étudiées au cas par cas.</p>'''

def build():
    os.makedirs(OUT, exist_ok=True)
    for f in os.listdir(OUT):
        if f == ".git": continue
        fp = os.path.join(OUT, f)
        shutil.rmtree(fp) if os.path.isdir(fp) else os.remove(fp)
    shutil.copy(os.path.join(SRC, "style.css"), OUT)
    shutil.copy(os.path.join(SRC, "site.js"), OUT)
    for f in ["kit-pub.html", "favicon.svg", "favicon.png", "favicon.ico", "apple-touch-icon.png", "og-image.png", "CNAME", ".nojekyll"]:
        if os.path.exists(os.path.join(SRC, f)): shutil.copy(os.path.join(SRC, f), OUT)
    if os.path.isdir(os.path.join(SRC, "kit")): shutil.copytree(os.path.join(SRC, "kit"), os.path.join(OUT, "kit"))
    with open(os.path.join(SRC, "cp.json")) as f:
        cp = f.read().strip()
    open(os.path.join(OUT, "cp.js"), "w").write("window.SN_CP=" + cp + ";\n")
    pages = {"index.html": page_index()}
    for p in PRODUCTS: pages[p["slug"] + ".html"] = page_product(p)
    for c in CITIES: pages[c[0] + ".html"] = page_city(c)
    pages["conseils.html"] = page_conseils()
    for a in ARTICLES: pages[a["slug"] + ".html"] = page_article(a)
    pages["mentions-legales.html"] = page_text("mentions-legales", "Mentions légales", MENTIONS)
    pages["confidentialite.html"] = page_text("confidentialite", "Données personnelles", CONFID)
    pages["404.html"] = page_text("404", "Page introuvable", '<p>Cette page n\'existe pas ou a été déplacée.</p><p><a class="btn" href="index.html">Retour à l\'accueil</a> <a class="btn ghost" href="index.html#devis">Demander un devis</a></p>')
    pages["fonctionnement.html"] = page_text("fonctionnement", "Fonctionnement du service", FONCT)
    for name, content in pages.items():
        open(os.path.join(OUT, name), "w").write(content)
    open(os.path.join(OUT, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\nDisallow: /kit-pub.html\nDisallow: /kit/\nSitemap: {SITE}/sitemap.xml\n")
    urls = "".join(f"<url><loc>{SITE}/{'' if n=='index.html' else n}</loc><lastmod>{TODAY}</lastmod></url>" for n in pages if n[:-5] not in NOINDEX)
    open(os.path.join(OUT, "sitemap.xml"), "w").write(f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n')
    open(os.path.join(ROOT, "artifact-index.html"), "w").write(page_index(art=True))
    print(len(pages), "pages")

build()
