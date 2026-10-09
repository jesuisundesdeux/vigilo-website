# Guide du code de vigilo-website

Ce guide s'adresse à un développeur qui reprend le site [vigilo.city](https://vigilo.city) sans le connaître. Il
décrit le code tel qu'il est sur la branche `source` : construction, données, gabarits, JavaScript, contenu, recettes
courantes et pièges connus. Pour les règles générales du dépôt, voir aussi `AGENTS.md` et `README.md`.

Ce fichier est en dehors de `content/` et du montage Hugo (voir `module.mounts` dans `config.yaml`) : il n'est pas
publié sur le site.

## Sommaire

1. [Vue d'ensemble](#1-vue-densemble)
2. [Le script de données `scripts/fetch_instances.py`](#2-le-script-de-données-scriptsfetch_instancespy)
3. [Les gabarits Hugo (`layouts/`)](#3-les-gabarits-hugo-layouts)
4. [JavaScript et CSS (`assets/`)](#4-javascript-et-css-assets)
5. [Conventions du contenu (`content/`, `data/`)](#5-conventions-du-contenu-content-data)
6. [Recettes](#6-recettes)
7. [Pièges connus et dette technique](#7-pièges-connus-et-dette-technique)

---

## 1. Vue d'ensemble

### 1.1 Arborescence

| Chemin | Rôle | Versionné |
|---|---|---|
| `config.yaml` | Configuration Hugo (langue, menu, paramètres, Markdown, montages) | oui |
| `content/` | Pages en Markdown (`_index.fr.md`, quelques `*.md`) et leurs images | oui |
| `layouts/` | Thème propre au site : gabarits, partiels, *render hook* d'image | oui |
| `assets/js/` | `site.js` (cartes), `panoramax.js`, `layers.js` — assemblés par Hugo (esbuild) | oui |
| `assets/css/main.css` | Feuille de style unique | oui |
| `data/openapi.yaml` | Spécification OpenAPI de l'API du backend (page `/fr/api/`) | oui |
| `static/` | Fichiers copiés tels quels : `CNAME` (`vigilo.city`), `images/` (logos, favicon, badges ; `panoramax.svg` : logo officiel de Panoramax, repris du paquet `@panoramax/web-viewer`, licence MIT) | oui |
| `scripts/fetch_instances.py` | Génère `_generated/` à partir de vigilo-conf et de l'API des instances | oui |
| `_generated/` | Données et pages des instances, produites au moment de la construction | **non** (`.gitignore`) |
| `node_modules/` | Dépendances front (Leaflet, Swagger UI, police Inter), montées dans Hugo | non |
| `public/`, `resources/` | Sortie de Hugo et cache des ressources | non |
| `.github/workflows/deploy.yml` | Construction et publication | oui |
| `.github/dependabot.yml` | Mises à jour mensuelles npm et GitHub Actions | oui |
| `Makefile`, `package.json` | Commandes locales | oui |

### 1.2 Configuration Hugo (`config.yaml`)

- `baseURL: https://vigilo.city/`, une seule langue `fr` avec `defaultContentLanguageInSubdir: true` : toutes les
  pages sont sous `/fr/…` ; Hugo génère à la racine un `index.html` qui redirige vers `/fr/`.
- `params` (lus par les gabarits via `site.Params`) :

  | Clé | Valeur | Utilisée par |
  |---|---|---|
  | `description` | description par défaut | `partials/head.html` (si la page n'a pas de `description`) |
  | `editURL` | `https://github.com/jesuisundesdeux/vigilo-website/edit/source/content/` | lien « Modifier cette page » (`partials/footer.html`) |
  | `webapp` | `https://app.vigilo.city` | boutons vers l'application, iframe des statistiques |
  | `github` | `https://github.com/jesuisundesdeux` | liens « Code source » |

- `menus.main` : le menu du haut (Application, Villes, Documentation, API, FAQ, Contact), par `pageRef` et `weight`.
- `markup.goldmark.renderer.unsafe: true` : le Markdown peut contenir du HTML brut (utilisé dans plusieurs pages).
- `markup.goldmark.parser.autoHeadingIDType: blackfriday` : identifiants de titres compatibles avec l'ancien site
  (Hugo 0.55), pour ne pas casser les ancres existantes (ex. `#installer-l-application`).
- `tableOfContents` : niveaux 2 et 3.
- `disableKinds: [taxonomy, term]` : pas de tags ni de catégories Hugo.
- `outputs` : la page d'accueil produit HTML + RSS, les sections seulement HTML.
- `enableRobotsTXT: true` : `robots.txt` par défaut de Hugo.

### 1.3 Montages (`module.mounts`)

Dès qu'un montage est déclaré, Hugo ne lit plus les dossiers par défaut : **seuls les chemins listés existent pour
lui**. C'est pourquoi `doc/` (ce guide) n'est jamais publié.

| Source | Cible Hugo | Pourquoi |
|---|---|---|
| `content` | `content` | pages écrites à la main |
| `_generated/content` | `content` | une page par instance (`villes/<slug>/_index.fr.md`) |
| `data` | `data` | `openapi.yaml` |
| `_generated/data` | `data` | `instances.json`, `categories.json` |
| `assets`, `layouts`, `static` | idem | thème du site |
| `node_modules/leaflet/dist` | `assets/vendor/leaflet` | `leaflet.js`, `leaflet.css`, `images/` |
| `node_modules/swagger-ui-dist` | `assets/vendor/swagger-ui` | `swagger-ui-bundle.js`, `swagger-ui.css` |
| `node_modules/@fontsource-variable/inter/files/inter-latin-wght-normal.woff2` et `…latin-ext…` | `static/fonts/…` | police Inter, référencée en dur par `main.css` (`/fonts/…`) |

Conséquences :

- sans `npm install` / `npm ci`, les ressources `vendor/…` manquent et la construction échoue ;
- sans `_generated/` (script non lancé), `hugo.Data.instances` vaut `nil` et la construction échoue sur
  `layouts/index.html` (`where $instances "online" true` : *can't iterate over <nil>*). Il faut donc toujours lancer
  `scripts/fetch_instances.py` avant Hugo.

### 1.4 Construire en local

Prérequis : Hugo **extended** (la CI utilise 0.166.0), Node.js ≥ 22, Python 3 (bibliothèque standard seulement).

| Commande | Effet |
|---|---|
| `make serve` | `npm install` (si `package.json` a changé) + `fetch_instances.py` + `hugo server` (http://localhost:1313, rechargement à chaud) |
| `make generate` | idem puis `hugo --gc --minify --cleanDestinationDir` dans `public/` |
| `make data` | seulement `python3 scripts/fetch_instances.py` |
| `make doc-backend` | régénère la page de mise à jour depuis vigilo-backend (§ 5.5) |
| `npm run data` / `npm run build` / `npm run serve` | équivalents npm (`build` = data + `hugo --gc --minify`) |

`make serve` ne relance pas le script de données quand on modifie un fichier : relancer `make data` pour rafraîchir
les instances.

`make generate` **ne lance pas** `make doc-backend` : en local, la page de mise à jour est celle versionnée dans
`content/documentation/upgrade/_index.fr.md` ; en CI elle est toujours régénérée.

### 1.5 Intégration continue et publication (`.github/workflows/deploy.yml`)

Déclencheurs : push sur `source`, toutes les pull requests, tous les jours à 4 h 23 UTC (`cron: '23 4 * * *'`, pour
rafraîchir les territoires) et à la demande (`workflow_dispatch`). `concurrency` annule une construction en cours sur
la même référence.

Job `build` (Ubuntu) :

1. `actions/checkout`, Node 22 (cache npm), Python 3.12 ;
2. téléchargement de Hugo extended `HUGO_VERSION` (0.166.0) depuis les releases GitHub ;
3. `npm ci` ;
4. `python3 scripts/fetch_instances.py` (réseau : vigilo-conf + chaque instance) ;
5. régénération de `content/documentation/upgrade/_index.fr.md` (`_index.fr.tpl` + `doc/UPGRADE.md` de la branche
   `master` de vigilo-backend) ;
6. `hugo --gc --minify` ;
7. dépôt de `public/` comme artefact `site` (conservé 7 jours).

Job `deploy` (seulement si l'événement n'est pas une pull request et si la référence est `refs/heads/source`) :
récupère l'artefact et le publie avec `peaceiris/actions-gh-pages@v4` sur la branche `master` (GitHub Pages, domaine
donné par `static/CNAME`). La branche `master` ne contient que le site construit : ne jamais y committer à la main.

Il n'y a pas de tests automatisés : une PR est « verte » si la construction réussit.

---

## 2. Le script de données `scripts/fetch_instances.py`

Script Python 3 sans dépendance externe, lancé avant chaque construction. Il produit tout `_generated/`.

### 2.1 Entrées

| Source | URL | Usage |
|---|---|---|
| `citylist.json` | `CONF_URL + "citylist.json"` | instances ; seules les entrées `prod: true` sont gardées |
| `categorielist.json` | `CONF_URL + "categorielist.json"` | recopié tel quel dans `categories.json` |
| `get_scope.php` | `<api_path>/get_scope.php?scope=<scope>` | nom affiché, emprise, centre, communes, version, contact |
| `get_issues.php` | `<api_path>/get_issues.php?scope=<scope>&count=1` | date de la dernière observation |

`CONF_URL` vaut la variable d'environnement `VIGILO_CONF_URL`, sinon
`https://raw.githubusercontent.com/jesuisundesdeux/vigilo-conf/main/main/`. **Elle doit se terminer par `/`** (les
noms de fichiers y sont concaténés directement).

Toutes les requêtes passent par `get_json()` : en-tête `User-Agent: vigilo-website build`, délai `TIMEOUT = 15`
secondes, décodage UTF-8 puis JSON. Les instances sont interrogées en parallèle (`ThreadPoolExecutor`, 16 tâches).

### 2.2 Traitement d'une instance (`instance_data`)

1. `api_path` : `%3A%2F%2F` remplacé par `://` (certaines entrées de vigilo-conf sont encodées), `/` final retiré ;
   `country` vaut `"France"` par défaut.
2. Appel de `get_scope.php`. La réponse doit être un objet contenant `display_name`, sinon l'instance est considérée
   **injoignable** (message `<nom>: unreachable (...)` sur la sortie d'erreur), et seuls les champs de base sont
   écrits.
3. Si elle répond : `online: true`, `display_name` (ou le nom vigilo-conf s'il est vide), `backend_version`,
   `contact_email`, `cities` (noms triés), `bbox` si les quatre coordonnées sont des nombres, `center` depuis
   `map_center_string` (`"lat,lon"`) ou, à défaut, centre de la `bbox`.
4. Appel de `get_issues.php?count=1` : la date (`time`, timestamp Unix) de la première observation renvoyée donne
   `last_observation` (date UTC `AAAA-MM-JJ`). Toute erreur sur cet appel est ignorée silencieusement.
5. `slug` = `slugify("<display_name>-<code pays>")`, code pays pris dans `COUNTRIES = {"France": "fr", "Belgique": "be"}`
   (`fr` pour tout autre pays).

`slugify` (« mêmes URL que l'ancien générateur ») : minuscules, accents retirés (NFKD), `'`, `"`, `/`, `.` remplacés
par `-`, espaces remplacés par `-`, tirets multiples réduits à un seul, tirets en tête et en fin retirés. Exemple :
`"Toulon - Var"` → `toulon-var-fr`. Les autres caractères (parenthèses, virgules…) sont conservés.

### 2.3 Après la collecte (`main`)

- tri par `display_name` (insensible à la casse) ;
- **unicité des slugs** : si un slug est déjà pris, on lui ajoute `-<slugify(scope)>` ;
- `url = "/fr/villes/<slug>/"` pour les instances en ligne seulement ;
- `shutil.rmtree(_generated)` **après** la collecte (si vigilo-conf est inaccessible, le script s'arrête sur une
  exception avant d'effacer l'ancien `_generated/`) ;
- écriture de `instances.json` et `categories.json` (UTF-8, `indent=1`) ;
- une page par instance **en ligne** ; une instance injoignable reste dans `instances.json` (carte « Injoignable » sur
  `/fr/villes/`) mais n'a pas de page ce jour-là ;
- affichage du bilan `N production instances, M online`.

Si `citylist.json` ou `categorielist.json` ne peut pas être lu, le script échoue : en CI la construction échoue et le
site publié précédemment reste en ligne.

### 2.4 `_generated/data/instances.json`

Tableau d'objets, un par instance `prod: true` :

| Champ | Présent | Contenu |
|---|---|---|
| `name` | toujours | clé de `citylist.json` (identifiant utilisé par l'application : `?instance=<name>`) |
| `country` | toujours | pays vigilo-conf, `"France"` par défaut |
| `api_path` | toujours | URL de l'API, sans `/` final |
| `scope` | toujours | scope vigilo-conf (`XX_nom`) |
| `online` | toujours | `true` si `get_scope.php` a répondu correctement |
| `display_name` | toujours | `display_name` de l'instance, sinon `name` |
| `slug` | toujours | dossier de la page (`/fr/villes/<slug>/`) |
| `backend_version` | en ligne | version renvoyée par `get_scope.php` (`""` si absente) |
| `contact_email` | en ligne | adresse de l'association (`""` si absente) |
| `cities` | en ligne | liste triée des noms de communes |
| `bbox` | en ligne, si coordonnées valides | `[lat_min, lon_min, lat_max, lon_max]` |
| `center` | en ligne, si centre ou `bbox` | `[lat, lon]` |
| `last_observation` | en ligne, si `get_issues.php` répond | `AAAA-MM-JJ` |
| `url` | en ligne | `/fr/villes/<slug>/` |

`_generated/data/categories.json` est la copie exacte de `categorielist.json` (`catid`, `catname`, `catname_en_US`,
`catcolor`, `catresolvable`, `catdisable`…).

### 2.5 Pages générées

`_generated/content/villes/<slug>/_index.fr.md`, avec un front matter écrit en JSON (valide en YAML) :

```yaml
---
title: "Ma Ville"
layout: "instance"
instance: "Ma Ville"
---
```

- `layout: instance` + section `villes` → gabarit `layouts/villes/instance.html` ;
- `instance` est le `name` vigilo-conf : le gabarit retrouve l'instance dans `hugo.Data.instances` par ce champ ;
- le corps est vide : tout l'affichage vient du gabarit.

---

## 3. Les gabarits Hugo (`layouts/`)

### 3.1 Quel gabarit pour quelle page

| Page | Fichier de contenu | Gabarit |
|---|---|---|
| Accueil `/fr/` | `content/_index.fr.md` | `layouts/index.html` |
| Liste des villes `/fr/villes/` | `content/villes/_index.fr.md` | `layouts/villes/list.html` |
| Page d'une instance `/fr/villes/<slug>/` | `_generated/content/villes/<slug>/_index.fr.md` | `layouts/villes/instance.html` (`layout: instance`) |
| « Votre ville ici » `/fr/villes/maville/` | `content/villes/maville/_index.fr.md` | `layouts/villes/list.html` (section de type `villes`, voir § 7) |
| API `/fr/api/` | `content/api/_index.fr.md` | `layouts/api/list.html` |
| Autres sections (`_index.fr.md`) | … | `layouts/_default/list.html` |
| Autres pages (`*.md`) | … | `layouts/_default/single.html` |

Le dossier `layouts/_default/` suit l'ancienne organisation des gabarits Hugo, `layouts/_markup/` la nouvelle
(Hugo ≥ 0.146) ; Hugo 0.166 accepte les deux.

Les données des instances sont lues avec `hugo.Data.instances` et `hugo.Data.categories` (fichiers de
`_generated/data/`), la spécification avec `hugo.Data.openapi`.

### 3.2 `_default/baseof.html`

Squelette commun. Blocs que les gabarits peuvent définir :

| Bloc | Défaut | Rôle |
|---|---|---|
| `head` | vide | ajouts dans `<head>` (ex. CSS de Swagger UI) |
| `bodyclass` | `page` | classe de `<body>` (`home` sur l'accueil) |
| `main` | vide | contenu de `<main id="main">` |
| `scripts` | vide | scripts en fin de page (ex. `map-assets.html`) |

Autour : lien d'évitement « Aller au contenu », `partials/header.html`, `partials/footer.html`.

### 3.3 `_default/list.html` et `_default/single.html`

Une seule ligne chacun : `{{ partial "page-body.html" . }}`.

### 3.4 `partials/page-body.html` (pages de documentation)

- `$top := .FirstSection` : section de premier niveau de la page ;
- **navigation latérale** (`aside.docs-nav`) si la page n'est pas l'accueil et que sa section de premier niveau a des
  sous-pages ; arbre construit par `partials/docs-tree.html` ;
- **table des matières** (`aside.docs-toc`, `.TableOfContents`) si `disableToc` n'est pas à vrai dans le front matter
  et que le contenu compte **plus de deux** titres `h2`/`h3` (`findRE `<h[23]` .Content`) ;
- fil d'Ariane (ancêtres, sauf l'accueil) quand la page n'est pas `$top` ;
- `<h1>` = `title`, puis `description` du front matter en chapeau (`p.lead`) si présente ;
- contenu dans `div.prose` ;
- pour une section : une carte par sous-page (`.Pages.ByWeight`), avec `description` ou, à défaut, le résumé tronqué à
  120 caractères ;
- pour une page simple : liens précédent / suivant (`.PrevInSection` / `.NextInSection`, voir § 7).

Les classes `has-nav` / `has-toc` sur `div.docs` pilotent la grille CSS (1, 2 ou 3 colonnes).

### 3.5 `partials/docs-tree.html`

Partiel récursif, contexte `dict "section" … "current" …`. Liste `section.Pages.ByWeight` ; une entrée est
`open` si c'est la page courante ou un de ses ancêtres, `active` (avec `aria-current="page"`) si c'est la page
courante ; les sous-sections ne sont dépliées que si elles sont ouvertes. L'ordre et l'intitulé viennent de `weight`
et `linkTitle` (ou `title`).

### 3.6 `partials/head.html`

`<title>` (« Vigilo · À pied ou à vélo… » sur l'accueil, « Titre · Vigilo » ailleurs), `description` et balises Open
Graph (`description` de la page ou `site.Params.description` ; image `images/vigilo.png`), `theme-color`, favicon,
préchargement de la police Inter latin, `css/main.css` minifiée + empreinte + attribut `integrity`, lien RSS si la page
a une sortie RSS (accueil).

### 3.7 `partials/header.html`

Logo + menu `site.Menus.main`. Une entrée est active si Hugo la considère courante (`IsMenuCurrent` /
`HasMenuCurrent`) ou si la page courante est la page du menu ou une de ses descendantes. Sur mobile (≤ 900 px), le
menu s'ouvre avec une case à cocher cachée (`#nav-toggle`) et du CSS, sans JavaScript. Bouton « Ouvrir l'appli » vers
`site.Params.webapp`.

### 3.8 `partials/footer.html`

Liens fixes (application, guide, villes, FAQ, documentation, API, Open311, GitHub, contact), licences CC0 et
OpenStreetMap, crédit « Vues immersives Panoramax » avec le logo (`.footer-panoramax`), mentions légales. Le lien **« Modifier cette page »** (`site.Params.editURL` + chemin du fichier) est
affiché pour toute page issue d'un fichier, sauf les pages d'instance (`.Params.instance`), qui sont générées.

### 3.9 `layouts/index.html` (accueil)

Texte d'accroche et sections fixes écrits dans le gabarit (« Comment ça marche ? », « Pourquoi Vigilo ? »,
« Avec Panoramax » : logo et usages de Panoramax dans Vigilo, `.partner-panoramax`). Données :

- `territoires couverts` = nombre d'instances `online` ;
- `communes` = somme des longueurs de `cities` des instances en ligne ;
- carte de toutes les instances : `<div class="map map-large" data-map="instances">` ;
- en bas, le contenu de `content/_index.fr.md` (`section.home-content`, logos des associations partenaires) ;
- bloc `scripts` : `partials/map-assets.html`.

### 3.10 `layouts/villes/list.html` (`/fr/villes/`)

- chapeau avec le nombre d'instances en ligne ;
- carte `data-map="instances"` ;
- grille de toutes les instances de `instances.json`, chacune rendue par `partials/instance-card.html` : lien vers
  `.url` si en ligne, simple bloc grisé (`.offline`) sinon ;
- contenu de `content/villes/_index.fr.md` ;
- cartes vers les sous-pages qui ne sont pas des instances (`where .Pages "Params.instance" "==" nil`, en pratique
  `maville/`).

### 3.11 `partials/instance-card.html`

Contexte : un objet de `instances.json`. Affiche `display_name`, nombre de communes, pays, badge « En ligne » /
« Injoignable », `backend_version`, `last_observation` (formatée avec `time.Format "2 January 2006"`, en français
grâce à `locale: fr-FR`).

### 3.12 `layouts/villes/instance.html` (page d'une instance)

`$i` = l'instance de `hugo.Data.instances` dont `name` vaut `.Params.instance` (`index (where …) 0`).

| Élément | Source |
|---|---|
| Titre, badges (en ligne, `Backend v…`, dernière observation) | `$i` |
| « Signaler dans l'application » | `site.Params.webapp` + `/?instance=<name>` |
| « Contacter l'association » | `contact_email` découpé en `data-mail-user` / `data-mail-domain` (adresse assemblée au clic par `site.js`) |
| Carte des observations | `div[data-map="observations"]` avec `data-api`, `data-scope`, `data-instance`, `data-bbox` (JSON) |
| `#observations-status` | texte d'état rempli par `site.js` |
| `#latest-observations` | liste remplie par `site.js` |
| Données ouvertes | liens `get_issues.php?scope=…&format=json|geojson|csv` |
| Communes | `$i.cities` |
| Statistiques | `<iframe class="stats-frame" data-stats-frame src="<webapp>/stats-iframe.html?instance=<name>">` (hauteur ajustée par `site.js`) |

Le badge « Injoignable lors de la dernière mise à jour du site » n'est jamais affiché en pratique, puisque seules les
instances en ligne ont une page.

### 3.13 `layouts/api/list.html` (`/fr/api/`)

1. Construit `$servers` : un serveur par instance en ligne, `{url: api_path, description: "<display_name> — scope <scope>"}`.
2. `$spec := merge hugo.Data.openapi (dict "servers" $servers)` : la liste `servers: []` de `data/openapi.yaml` est
   remplacée.
3. `$spec | jsonify | resources.FromString "api/openapi.json"` : fichier publié à **`/api/openapi.json`** (bouton
   « Télécharger la spécification OpenAPI »).
4. Tableau repliable « Instances et scopes » (lien vers chaque page d'instance, API, scope).
5. La spécification est aussi incluse dans la page (`<script type="application/json" id="openapi-spec">`) et passée à
   `SwaggerUIBundle` avec : `deepLinking: true`, `docExpansion: 'list'`, `defaultModelsExpandDepth: 0`,
   `tryItOutEnabled: false` (le bouton *Try it out* reste disponible), `supportedSubmitMethods: ['get']` (seuls les
   appels GET peuvent être exécutés depuis la page).
6. CSS et JS de Swagger UI viennent de `assets/vendor/swagger-ui/` (montage npm), avec empreinte.

### 3.14 `partials/map-assets.html`

Inclus dans le bloc `scripts` de l'accueil, de `/fr/villes/` et des pages d'instance :

- `vendor/leaflet/leaflet.css` (sans empreinte) ; les images de `vendor/leaflet/images/*` sont publiées à côté en
  appelant `.RelPermalink` sur chacune (sinon Hugo ne les publierait pas) ;
- `vendor/leaflet/leaflet.js` avec empreinte, `integrity`, `defer` ;
- `js/site.js` assemblé par `js.Build` (esbuild) : `minify` si `hugo.IsProduction` (construction `hugo`, pas
  `hugo server`), cible `es2018`, empreinte, `integrity`, `defer` (exécuté après Leaflet) ;
- `<script type="application/json" id="instances-data">` et `id="categories-data"` : `instances.json` et
  `categories.json` entiers, lus par `site.js`.

### 3.15 `_markup/render-image.html` (images Markdown)

*Render hook* de toutes les images `![alt](src "titre")` :

- reprend les options de l'ancien thème dans l'URL : `?width=300` → attribut `width`, `?classes=shadow,foo` → classes
  (virgules remplacées par des espaces) ; la requête est retirée de `src` ;
- une source relative (ni absolue, ni commençant par `/`) est cherchée dans les ressources de la page (bundle) ;
- sortie : `<img … class="md-img …" loading="lazy">`. CSS : `.prose img.md-img[width]` en bloc, `.prose img.shadow`
  avec ombre.

Les `<img>` écrites en HTML brut dans le Markdown ne passent pas par ce hook.

---

## 4. JavaScript et CSS (`assets/`)

Pas de framework ni d'étape de construction séparée : `site.js` importe `layers.js` et `panoramax.js` (modules ES) et
Hugo les assemble avec esbuild. Leaflet est une variable globale `L` (script chargé avant).

### 4.1 `assets/js/site.js`

Au chargement, le script :

```js
document.querySelectorAll('[data-map="instances"]').forEach(instancesMap);
document.querySelectorAll('[data-map="observations"]').forEach(observationsMap);
enableMailLinks();
enableStatsFrames();
```

#### Utilitaires

| Fonction | Rôle |
|---|---|
| `escapeHtml(value)` | échappe `& < > " '` ; **à utiliser pour toute donnée d'instance insérée en HTML** |
| `readJson(id)` | lit un `<script type="application/json">` (`instances-data`, `categories-data`) |
| `createMap(el, options)` | carte Leaflet (`scrollWheelZoom: false`, `zoomSnap: 0.5`), fonds de `addBaseLayers` ; zoom à la molette activé seulement après le premier `focus` de la carte ; la carte est aussi rangée dans `el.leafletMap` |
| `STATUS` | libellés des états (`status` 0 à 4) : Nouvelle, Résolue, Prise en compte, En cours de résolution, Indiquée comme résolue — même correspondance que `issueStatus()` de vigilo-webapp |

#### Carte des instances (`instancesMap`)

- données : `instances-data` ; seules les instances avec `center` sont placées (donc pas les injoignables) ;
- centre initial `[46.6, 2.4]`, zoom 5.5, puis `fitBounds` sur tous les centres (`maxZoom: 9`), sauf si l'élément porte
  `data-fit="false"` (option prévue par le code, utilisée par aucun gabarit) ;
- un `circleMarker` jaune par instance (gris si hors ligne), info-bulle avec `display_name` ;
- au survol, rectangle de la `bbox` ;
- popup : nom, nombre de communes, liens « Voir les observations » (`url`) et « Ouvrir l'appli »
  (`https://app.vigilo.city/?instance=<name>`, URL écrite en dur).

#### Carte des observations d'une instance (`observationsMap`, `async`)

1. Lit `data-api`, `data-scope`, `data-instance`, `data-bbox`. Catégories initiales : `categories-data` (liste
   nationale de vigilo-conf), indexées par `catid`.
2. Carte en mode canvas (`preferCanvas: true`, fluide avec des milliers de points), cadrée sur la `bbox` si connue ;
   `enablePanoramax(map)`.
3. **Catégories de l'instance** : `fetch(api + '/get_categories.php')` ; si la réponse est un tableau, ses entrées
   remplacent ou complètent la liste nationale (catégories propres ≥ 1000 du backend ≥ 0.0.23). Toute erreur (route
   absente, réseau) est ignorée : on garde la liste nationale.
4. **Observations** : `get_issues.php?scope=<scope>&count=3000`. En cas d'erreur ou de réponse qui n'est pas un
   tableau : message « Les observations de cette instance ne peuvent pas être chargées pour le moment. » dans
   `#observations-status`, et arrêt. `uniqueIssues()` garde une entrée par observation (avant le backend 0.0.26, une
   observation liée à plusieurs résolutions revenait une fois par résolution) avec le statut le plus avancé
   (résolue > indiquée résolue > en cours > prise en compte).
5. Pour chaque observation (de la plus ancienne à la plus récente, pour dessiner les récentes au-dessus) ayant des
   coordonnées valides : `circleMarker` de rayon `radiusFor(zoom)` (4,5 à 10 px, recalculé à chaque `zoomend`).
   Couleur : `categoryColor(cat)` = `CATEGORY_COLORS[catid]` (palette fixe du site pour les catégories nationales),
   sinon `catcolor` de la catégorie, sinon gris. Observation résolue (`status == 1`, `isResolved`) : disque blanc cerclé
   de la couleur ; sinon disque plein cerclé de blanc.
6. Popup construite à l'ouverture (`observationPopup`) : photo (`get_photo.php` si `approved == 1`, sinon
   `generate_panel.php?s=300`, qui sert aussi de repli `onerror`), catégorie, commentaire, adresse, date, état, lien
   « Voir dans l'appli » (`https://app.vigilo.city/?token=…&instance=…`), bouton « Voir avec Panoramax ».
7. Recadrage sur l'ensemble des observations (`maxZoom: 15`), car l'emprise du territoire est souvent bien plus large.
8. **Légende / filtres** (`addLegend`, contrôle Leaflet en haut à droite) : section « État » (À résoudre / Résolues)
   et une ligne par catégorie présente, triée par nombre décroissant, avec compteur. Décocher masque les marqueurs
   (`hidden.cat` / `hidden.state`) ; `#observations-status` indique « N observations affichées sur M ». La légende est
   repliable (bouton « Filtres ») et repliée au départ si la carte fait moins de 600 px de large. Les compteurs sont
   ceux du total, ils ne changent pas avec les filtres.
9. **Dernières observations** : les 10 premières de la réponse dans `#latest-observations` (vignette
   `generate_panel.php?s=150`, titre, catégorie, adresse, date, lien vers l'application).

Toutes les valeurs venant de l'instance (commentaire, adresse, noms de catégories, couleurs, jeton…) passent par
`escapeHtml` ou `encodeURIComponent`.

#### Panoramax sur les cartes

- `enablePanoramax(map)` (cartes d'observations seulement) : un clic n'importe où sur la carte cherche une photo dans
  un rayon d'environ 15 px (au moins 0,0003°) via `showPanoramaxAround`, qui affiche une popup d'attente puis ouvre la
  visionneuse ou « Aucune vue Panoramax à proximité » (fermée après 2,5 s). Ajoute l'indication « Cliquez sur la carte
  pour voir la rue avec Panoramax » en bas à gauche.
- Bouton « Voir avec Panoramax » d'une popup d'observation : branché sur l'événement `popupopen`, rayon 0,0005°.

#### Liens e-mail (`enableMailLinks`)

Pour chaque `a[data-mail-user]`, au clic, `href` devient `mailto:<user>@<domain>` (l'adresse n'apparaît pas dans
l'attribut `href` du HTML ; voir toutefois § 7).

#### Hauteur de l'iframe des statistiques (`enableStatsFrames`)

L'iframe `iframe[data-stats-frame]` a une hauteur CSS initiale de 1500 px. `stats-iframe.html` (vigilo-webapp)
envoie `postMessage({type: 'vigilo-stats-height', height})` ; le site applique la hauteur seulement si :

- `e.data.type === 'vigilo-stats-height'` ;
- `e.source` est la fenêtre de cette iframe **et** `e.origin` est l'origine de son `src` (`new URL(frame.src).origin`) ;
- `0 < height < 20000`.

### 4.2 `assets/js/panoramax.js`

- `PANORAMAX_URL = 'https://explore.panoramax.fr'` (catalogue fédéré de toutes les instances Panoramax).
- `getSearchEndpoint()` : lit une seule fois la page d'accueil STAC (`/api`) et prend le lien `rel: "search"` ; repli
  sur `/api/search`. Le résultat (promesse) est mis en cache dans le module.
- `findPicture(lat, lon, radius)` (exportée) : recherche `?bbox=lon-r,lat-r,lon+r,lat+r&limit=50`, garde la photo la
  plus proche (distance euclidienne en degrés) et renvoie `{id, lat, lon, url, embedUrl}` ou `null` (aussi en cas
  d'erreur). `url` : `…/?pic=<id>` ; `embedUrl` : `…/#focus=pic&pic=<id>&map=18/<lat>/<lon>`.
- `openViewer(picture)` (exportée) : ouvre un `<dialog class="panoramax-dialog">` (créé une seule fois) contenant une
  iframe sur `embedUrl`, un lien « Ouvrir dans Panoramax ↗ » et « Fermer ». Un clic sur le fond ferme ; à la
  fermeture l'iframe repasse sur `about:blank`.

### 4.3 `assets/js/layers.js`

`addBaseLayers(map)` (exportée) ajoute un sélecteur de fonds (en haut à droite) :

| Nom | Source | Classe |
|---|---|---|
| OSM France (défaut) | `{s}.tile.openstreetmap.fr/osmfr` | `tiles-muted` |
| OpenStreetMap | `tile.openstreetmap.org` | `tiles-muted` |
| Plan IGN | Géoplateforme WMTS `GEOGRAPHICALGRIDSYSTEMS.PLANIGNV2` | `tiles-muted` |
| Photos aériennes | Géoplateforme WMTS `ORTHOIMAGERY.ORTHOPHOTOS` | — |

Aucune clé d'API n'est nécessaire. Si OSM France renvoie une erreur avant d'avoir chargé une seule tuile, il est
remplacé par openstreetmap.org. `.tiles-muted` (CSS) désature les fonds pour faire ressortir les observations.

### 4.4 `assets/css/main.css`

Une seule feuille, sans préprocesseur, minifiée et signée par Hugo. Organisation (commentaires `/* ---- … */`) :

| Partie | Contenu |
|---|---|
| en-tête | `@font-face` Inter (latin et latin-ext, police variable 100–900, chemins `/fonts/…`) |
| `:root` | variables : `--yellow` `#fdd835`, `--yellow-dark`, `--yellow-soft`, `--ink`, `--ink-soft`, `--bg`, `--surface`, `--border`, `--link`, rayons, ombres, `--max` (1180 px) |
| base | typographie, `.container` (marges de 16 px), `.muted`, `.small`, `.skip-link`, code |
| Buttons | `.btn`, `.btn-small`, `.btn-large`, `.btn-primary`, `.btn-dark`, `.btn-ghost`, `.cta`, `.link-btn` |
| Header | `.site-header`, `.main-nav`, menu mobile ≤ 900 px |
| Footer | `.site-footer`, `.footer-grid` (1 colonne ≤ 700 px) |
| Home | `.hero`, `.hero-stats`, `.steps`, `.features`, `.section`, `.section.alt` (≤ 800 px : 1 colonne), `.partner-panoramax` (bloc Panoramax, logo au-dessus ≤ 600 px), `.footer-panoramax` |
| Pages | grille `.docs` / `.has-nav` / `.has-toc`, `.docs-nav`, `.docs-toc` (cachée ≤ 1100 px), `.prose`, tableaux, citations, `.prev-next` |
| Cards | `.cards`, `.card`, `.card-link`, `.badge*`, `.instances-grid`, `.instance-card` |
| Maps | `.map`, `.map-large`, `.map-hint`, popups Leaflet, `.obs-popup`, `.obs-cat` (couleur via `--cat`), `.dot`, `.spinner`, `.tiles-muted`, `.obs-tooltip`, `.map-legend` |
| Instance page | `.instance-meta`, `.stats-frame`, `.instance-grid`, `.obs-list`, `.downloads`, `.cities` |
| Panoramax viewer popup | `.panoramax-dialog` |
| API page | `.scopes`, ajustements de `#swagger-ui` |
| fin | `.prose img.shadow`, `.prose img.md-img[width]` (render hook d'image) |

Pas de thème sombre. Les couleurs des catégories sur les cartes sont dans `site.js` (`CATEGORY_COLORS`), pas dans le
CSS.

---

## 5. Conventions du contenu (`content/`, `data/`)

### 5.1 Sections et fichiers

Chaque section est un dossier avec un `_index.fr.md` ; les pages simples d'une section sont des `*.md` (sans suffixe
de langue : la langue par défaut `fr` s'applique). Arborescence actuelle :

```
content/
  _index.fr.md                 accueil (bas de page : logos des partenaires)
  app/  (quesaco/, web/)       présentation et guide de l'application web
  villes/  (maville/)          liste des territoires ; « Votre ville ici »
  documentation/
    utilisation/  installation/ (installation_dedie.md, installation_mutualise.md, initialisation.md)
    configuration/ (global.md, scopes.md, villes.md)  administration/ (moderation.md)
    exploitation_donnees/ (umap/)  upgrade/  maintenance/ (sauvegarde.md)  contribution/
  api/  faq/  open311/  mentions-legales/  contact/
```

### 5.2 Front matter

| Clé | Effet |
|---|---|
| `title` | titre de la page, `<title>`, entrée de navigation |
| `weight` | ordre dans l'arbre de navigation (`docs-tree.html`) et dans les cartes des sections |
| `description` | chapeau sous le titre, cartes de section, balises `description` / Open Graph |
| `linkTitle` | (facultatif) intitulé plus court dans la navigation et le fil d'Ariane |
| `disableToc` | (facultatif) `true` pour ne pas afficher la table des matières |
| `aliases` | anciennes URL redirigées (ex. `content/app/web/_index.fr.md` : `/app/android/…`) ; Hugo les publie sous `/fr/…` |
| `layout`, `instance` | réservés aux pages générées des instances |

Le menu principal n'est pas dans le front matter : il est dans `config.yaml` (`menus.main`).

### 5.3 Images

- Images partagées : `static/images/` (URL `/images/…`), utilisées en HTML brut dans `content/_index.fr.md`.
- Images d'une page : à côté de son `_index.fr.md` (page *bundle*), référencées en relatif :
  `![Export](images/umap_download.png?width=300&classes=shadow)` ; le render hook résout le chemin (§ 3.15).
- Vérifier qu'une image référencée existe : une image manquante n'empêche pas la construction (le render hook garde
  alors le chemin tel quel).

### 5.4 Liens

Écrire les liens internes avec le préfixe de langue (`/fr/villes/`, `/fr/mentions-legales/#…`). Les ancres suivent la
règle *blackfriday* (`autoHeadingIDType`).

### 5.5 La page « Mise à jour » (générée depuis vigilo-backend)

`content/documentation/upgrade/_index.fr.md` = `_index.fr.tpl` (front matter + avertissement « Page générée
automatiquement ») suivi de `doc/UPGRADE.md` de la branche `master` de vigilo-backend.

- en CI, elle est régénérée à chaque construction (étape « Fetch the upgrade documentation ») ;
- en local, `make doc-backend` fait la même chose ; le fichier généré est versionné ;
- **ne pas la modifier dans ce dépôt** : modifier `doc/UPGRADE.md` du backend (la prochaine construction reprend le
  texte). Seul `_index.fr.tpl` (titre, poids, avertissement) se modifie ici.

### 5.6 `data/openapi.yaml`

OpenAPI 3.0.3, affiché par Swagger UI sur `/fr/api/`. Structure :

- `info` (`title`, `version`, `description` en Markdown, `license`) ;
- `servers: []` — **laisser vide** : la liste est injectée à la construction (§ 3.13) ;
- `tags` : Observations, Contribution, Modération, Configuration ;
- `paths` : une entrée par route PHP (`/get_scope.php`, `/get_version.php`, `/get_issues.php`, `/generate_panel.php`,
  `/get_photo.php`, `/mosaic.php`, `/create_issue.php`, `/add_image.php`, `/create_resolution.php`, `/delete.php`,
  `/approve.php`, `/acl.php`, et `/get_categories_list.php` marquée *deprecated*) ;
- `components` : `parameters`, `responses`, `schemas` réutilisables.

La référence est `doc/REST_API.md` de vigilo-backend : toute évolution de l'API y est décrite d'abord, puis reportée
ici. La compatibilité par version est indiquée dans les descriptions (« backend ≥ 0.0.x »).

---

## 6. Recettes

### 6.1 Ajouter une page de documentation

1. Créer `content/documentation/<section>/<page>.md` (page simple) ou `<page>/_index.fr.md` (si elle a des images ou
   des sous-pages) :

   ```markdown
   ---
   title: Sauvegarde de la base
   weight: 2
   description: Sauvegarder et restaurer la base MariaDB d'une instance
   ---

   ## Première partie
   ```

2. Choisir `weight` par rapport aux pages sœurs (navigation latérale, cartes, liens précédent / suivant).
3. Commencer les titres au niveau 2 (`##`) : le `<h1>` vient de `title` ; la table des matières apparaît à partir de
   trois titres `##`/`###`.
4. `make serve`, vérifier la page à 1280 px et 390 px.

Une nouvelle section de premier niveau qui doit apparaître dans le menu du haut s'ajoute aussi dans `menus.main` de
`config.yaml`.

### 6.2 Afficher un nouveau champ sur les pages d'instance

Exemple : un champ `foo` renvoyé par `get_scope.php`.

1. `scripts/fetch_instances.py`, dans `instance_data()`, bloc `if scope:` : ajouter
   `"foo": scope.get("foo") or ""` dans le `data.update({...})`. Les anciennes instances ne renvoient pas le champ :
   prévoir une valeur vide.
2. `layouts/villes/instance.html` (et/ou `partials/instance-card.html`) : `{{ with $i.foo }}…{{ end }}` pour ne rien
   afficher quand il manque. Hugo échappe automatiquement le texte dans les gabarits.
3. Si le champ doit être utilisé en JavaScript, il est déjà disponible dans `instances-data` ; l'insérer dans le HTML
   avec `escapeHtml`.
4. Mettre à jour le tableau du § 2.4.

Une donnée qui change souvent (observations, statistiques) doit plutôt être chargée en direct dans le navigateur
(`site.js`), comme les observations : les données de `_generated/` ne sont rafraîchies qu'une fois par jour.

### 6.3 Modifier les cartes

- Fonds de carte : `assets/js/layers.js` (`layers`, fond par défaut `osmFr`).
- Couleurs des catégories : `CATEGORY_COLORS` dans `site.js`. Une catégorie absente de la table prend `catcolor` de
  vigilo-conf ou de l'instance.
- Taille des points : `radiusFor(zoom)` ; style résolu / non résolu : `style` dans `observationsMap`.
- Nombre d'observations chargées : `count=3000` dans `observationsMap` ; nombre de « dernières observations » :
  `issues.slice(0, 10)`.
- Hauteur des cartes : `.map`, `.map-large` dans `main.css`.
- Une nouvelle carte dans une page : un élément `<div class="map" data-map="instances">` (ou `observations` avec ses
  attributs `data-*`) et `{{ define "scripts" }}{{ partial "map-assets.html" . }}{{ end }}` dans le gabarit.

### 6.4 Mettre à jour la spécification de l'API

1. Lire la modification dans `vigilo-backend/doc/REST_API.md` (route, paramètres, réponse, colonne
   « Compatibilité »).
2. Modifier `data/openapi.yaml` : chemin dans `paths`, paramètres communs dans `components.parameters`, schémas dans
   `components.schemas` ; préciser la version minimale du backend dans `description` ; mettre à jour `info.version`.
3. Ne pas remplir `servers`.
4. Vérifier : la construction Hugo échoue si le YAML est invalide ; ouvrir `/fr/api/` et contrôler la nouvelle route
   (aucune erreur affichée par Swagger UI, appel GET testable avec *Try it out* sur une instance). Aucun validateur
   OpenAPI n'est installé dans le dépôt ; un linter externe (par exemple `npx @redocly/cli lint data/openapi.yaml`)
   peut être utilisé ponctuellement.

### 6.5 Mettre à jour les dépendances

- Dependabot (`.github/dependabot.yml`) ouvre chaque mois des PR pour npm (`package.json` / `package-lock.json`) et
  pour les actions GitHub. Une PR Dependabot est construite par la CI ; avant de fusionner une mise à jour de Leaflet
  ou de Swagger UI, construire en local et vérifier une carte d'instance et la page API.
- Les chemins montés dans `config.yaml` (`node_modules/leaflet/dist`, `swagger-ui-dist`,
  `@fontsource-variable/inter/files/…woff2`) doivent exister dans la nouvelle version ; si un fichier change de nom,
  la construction échoue.
- Hugo : changer `HUGO_VERSION` dans `deploy.yml` (et la version indiquée dans `README.md` / `AGENTS.md`).
- À la main : `npm update` ou `npm install <paquet>@<version>`, puis committer `package.json` et `package-lock.json`.

### 6.6 Tester en local avec une instance locale

Le script accepte une autre source que vigilo-conf. Exemple avec une instance de vigilo-backend lancée en local
(`docker compose up`, écoute sur `BIND`, par exemple `http://127.0.0.1`) :

```sh
mkdir -p /tmp/conf
cat > /tmp/conf/citylist.json <<'EOF'
{"Test local": {"api_path": "http://127.0.0.1", "scope": "34_test", "prod": true, "country": "France"}}
EOF
curl -sSf https://raw.githubusercontent.com/jesuisundesdeux/vigilo-conf/main/main/categorielist.json -o /tmp/conf/categorielist.json
(cd /tmp/conf && python3 -m http.server 8097) &
VIGILO_CONF_URL=http://127.0.0.1:8097/ python3 scripts/fetch_instances.py   # / final obligatoire
hugo server
```

- le `scope` doit exister sur l'instance (`get_scope.php` doit renvoyer `display_name`), sinon elle est
  « injoignable » et n'a pas de page ;
- les routes de lecture du backend envoient `Access-Control-Allow-Origin: *` : le navigateur peut charger les
  observations depuis `localhost:1313` ;
- `make serve` relancerait le script **sans** `VIGILO_CONF_URL` : lancer `hugo server` directement après le script ;
- sans instance du tout, un petit serveur qui répond à `get_scope.php` et `get_issues.php` avec du JSON fixe suffit
  pour construire le site.

### 6.7 Prévisualiser une pull request

Les PR sont construites mais pas publiées. Deux possibilités :

- récupérer l'artefact `site` de l'exécution du workflow (onglet *Actions* de la PR, conservé 7 jours), le décompresser
  et le servir : `python3 -m http.server -d site 8000`, puis ouvrir http://localhost:8000/fr/ (les chemins sont
  absolus depuis la racine, il faut donc servir le dossier à la racine) ;
- ou récupérer la branche et lancer `make serve`.

Vérifier les pages concernées à 1280 et 390 px, sans erreur dans la console JavaScript.

---

## 7. Pièges connus et dette technique

Constats faits sur le code actuel (non corrigés à la date de ce guide).

### Construction

- **`_generated/` est obligatoire** : sans lui, Hugo échoue (§ 1.3). Toujours lancer le script avant Hugo.
- **Une instance injoignable au moment de la construction quotidienne perd sa page** jusqu'à la construction suivante
  (URL en 404 ce jour-là), et elle disparaît de la carte (pas de `center`).
- **Le slug dépend du `display_name` renvoyé par l'instance** : si une association change le nom de son scope, l'URL
  de sa page change sans redirection.
- Les slugs gardent les caractères autres que lettres, chiffres et `' " / .` (parenthèses, virgules…).
- `COUNTRIES` ne connaît que la France et la Belgique ; tout autre pays donne un suffixe `-fr`.
- `content/documentation/upgrade/_index.fr.tpl` est publié tel quel (`/fr/documentation/upgrade/_index.fr.tpl`), car
  Hugo le traite comme une ressource de la page.
- Le lien « Modifier cette page » de la page « Mise à jour » mène au fichier généré, écrasé à chaque construction : la
  modification doit se faire dans vigilo-backend.
- `make generate` ne régénère pas la page de mise à jour, alors que la CI le fait : les deux sorties peuvent
  différer.

### Gabarits

- **Liens précédent / suivant inversés** (`page-body.html`) : dans Hugo, `.PrevInSection` renvoie la page *suivante*
  dans l'ordre des poids. Résultat constaté : sur « Installation sur serveur dédié » (`weight: 1`), le lien
  « ← » mène à la page de poids 2, et sur « Initialisation » (`weight: 3`) le lien « → » mène à la page de poids 2.
- **`/fr/villes/maville/` utilise `villes/list.html`** (section de type `villes`, sans `layout`) : la page « Votre
  ville ici » affiche de nouveau la carte, le compteur et la grille de tous les territoires avant son texte, au lieu du
  gabarit de documentation.
- Le badge « Injoignable lors de la dernière mise à jour du site » de `villes/instance.html` et la couleur grise des
  instances hors ligne dans `instancesMap` ne servent jamais (pas de page ni de `center` pour une instance hors ligne).
- `villes/instance.html` échoue si `.Params.instance` ne correspond à aucune instance (`index` sur une liste vide) ;
  cela n'arrive pas tant que les pages sont générées par le script dans la même exécution.
- Le lien « Signaler dans l'application » écrit `?instance={{ $name }}` sans `urlquery` (l'échappement automatique de
  Go encode les espaces), alors que l'iframe utilise `urlquery`.
- `leaflet.css` est publié sans empreinte (contrairement aux autres ressources).

### JavaScript

- **Adresses e-mail en clair** : `instances-data` (intégré à l'accueil, à `/fr/villes/`, aux pages d'instance et à
  `maville/`) contient `contact_email` de chaque instance. L'assemblage au clic de `enableMailLinks` ne cache donc pas
  les adresses aux robots, contrairement à la règle de `AGENTS.md`.
- `https://app.vigilo.city` est écrit en dur dans `site.js` (popups, liste des dernières observations) au lieu de
  venir de `params.webapp`.
- Chaque page d'instance inclut `instances.json` et `categories.json` entiers, même si elle n'utilise que les
  catégories.
- La carte des observations charge au plus 3000 observations (`count=3000`) ; au-delà, les plus anciennes manquent
  sur la carte et dans les compteurs.
- Les compteurs de la légende ne tiennent pas compte des filtres.

### Contenu et API

- `data/openapi.yaml` est en retard sur le backend : `info.version` vaut `0.0.21`, la route `get_categories.php`
  (backend ≥ 0.0.23, utilisée par `site.js`) n'y figure pas, et `get_categories_list.php` (*deprecated*) n'existe
  plus dans `vigilo-backend/app/`.
- `content/contact/_index.fr.md` indique qu'une adresse de contact est « en bas de la page de chaque ville » ; c'est un
  bouton « Contacter l'association » en haut de la page.
- Aucune validation automatique : ni lien cassé, ni image manquante, ni validité OpenAPI ne sont contrôlés par la CI.
