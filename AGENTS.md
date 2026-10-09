# AGENTS.md — vigilo-website

Informations pour les agents IA (et les humains) qui travaillent sur ce dépôt.

## Le projet

Site [vigilo.city](https://vigilo.city) : présentation de Vigilo, carte des territoires (instances) et de leurs
observations, documentation utilisateur (installation, configuration, administration d'une instance), page API,
FAQ, mentions légales, page Open311.

- Site statique **Hugo** (extended ≥ 0.146 ; la CI utilise 0.166), thème propre au site (`layouts/`, `assets/`),
  contenu en Markdown dans `content/`, en **français** uniquement.
- **Branche de travail : `source`.** La branche `master` contient le site construit (GitHub Pages) : ne jamais y
  committer à la main.

## Organisation

Guide détaillé du code (construction, script de données, gabarits, JavaScript, recettes) : `doc/GUIDE_CODE.md`.

| Chemin | Contenu |
|---|---|
| `content/` | Pages (`_index.fr.md`) : `app/`, `villes/`, `documentation/` (installation, configuration, administration, maintenance, upgrade, utilisation, contribution, exploitation des données), `api/`, `faq/`, `open311/`, `mentions-legales/`, `contact/` |
| `layouts/` | Gabarits : `_default/`, `villes/instance.html` (page d'une instance : carte, statistiques intégrées, données ouvertes), `api/list.html` (Swagger UI), `partials/` |
| `assets/js/site.js` | Cartes Leaflet (instances, observations d'une instance avec filtres état / catégories), contacts, iframe des statistiques |
| `assets/js/panoramax.js`, `layers.js` | Vue immersive Panoramax, fonds de carte |
| `assets/css/main.css` | Styles |
| `data/openapi.yaml` | Spécification OpenAPI de l'API du backend, affichée par Swagger UI sur `/fr/api/` |
| `scripts/fetch_instances.py` | Génère `_generated/` (non versionné) : `data/instances.json` (instances de vigilo-conf + `get_scope.php` de chacune), `data/categories.json`, une page par instance |
| `config.yaml` | Configuration Hugo ; `params.webapp` = URL de l'application web (https://app.vigilo.city) |

## Règles à respecter

- **Documentation du code** : toute modification du code (gabarits, JavaScript, scripts, configuration) s'accompagne, dans la
  même PR, de la mise à jour de la documentation concernée dans `doc/` (`GUIDE_CODE.md`) et de ce fichier si
  l'organisation ou les règles changent.
- **Données en direct** : les observations sont chargées depuis l'API de chaque instance dans le navigateur ; une
  instance peut être lente, en panne ou en ancienne version. Toujours un message ou un repli (ex. catégories : 
  `get_categories.php` de l'instance, sinon la liste nationale de vigilo-conf).
- **Sécurité** : échapper toute donnée venant d'une instance (`escapeHtml` dans `site.js`) ; les adresses e-mail des
  associations ne sont pas écrites en clair dans le HTML (assemblées au clic).
- **Documentation** : `content/documentation/upgrade/_index.fr.md` est généré depuis `doc/UPGRADE.md` du backend
  (`make doc-backend`, en-tête dans `_index.fr.tpl`) : modifier d'abord le backend. La documentation technique de
  référence (API détaillée, architecture, webhooks) est dans `vigilo-backend/doc/` ; le site la résume et y renvoie.
- **API** : `data/openapi.yaml` doit suivre `vigilo-backend/doc/REST_API.md` (YAML valide, OpenAPI 3).
- **Langue** : contenu et messages de commit en **français** ; commentaires du code en anglais, courts.

## Construire et vérifier

Prérequis : Hugo extended, Node.js ≥ 22, Python 3.

```sh
make serve       # npm install + données des instances + serveur local http://localhost:1313
make generate    # construction dans public/
make data        # seulement les données des instances (VIGILO_CONF_URL=... pour une autre source)
```

Pas de tests automatisés : la CI construit le site. Pour vérifier un changement, construire (`hugo --quiet`) sans
erreur et contrôler les pages concernées dans un navigateur (desktop et 390 px), sans erreur JavaScript. Pour tester
les cartes sans réseau, servir un `citylist.json` local via `VIGILO_CONF_URL` pointant vers une instance locale.

## Publication

`.github/workflows/deploy.yml` : à chaque push sur `source`, chaque jour (4 h 23 UTC, mise à jour des territoires) et à
la demande, construction (`npm ci`, `fetch_instances.py`, `hugo --gc --minify`) et publication sur `master`
(GitHub Pages, domaine vigilo.city). Les pull requests sont seulement construites.

## Dépôts liés

- [vigilo-backend](https://github.com/jesuisundesdeux/vigilo-backend) : API et documentation technique (`doc/`).
- [vigilo-webapp](https://github.com/jesuisundesdeux/vigilo-webapp) : application (app.vigilo.city), dont
  `stats-iframe.html` intégrée dans les pages des instances.
- [vigilo-conf](https://github.com/jesuisundesdeux/vigilo-conf) : liste des instances et catégories nationales.
