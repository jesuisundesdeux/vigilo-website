# vigilo-website

Site [vigilo.city](https://vigilo.city) : présentation de Vigilo, carte des territoires et de leurs observations, documentation et API.

## Fonctionnement

- Site statique [Hugo](https://gohugo.io/) (thème propre au site, dans `layouts/` et `assets/`).
- Les territoires viennent de [vigilo-conf](https://github.com/jesuisundesdeux/vigilo-conf) (`citylist.json`, instances en production) ; `scripts/fetch_instances.py` interroge l'API de chaque instance (`get_scope.php`) au moment de la construction et génère une page par territoire (dossier `_generated/`, non versionné).
- Les cartes utilisent [Leaflet](https://leafletjs.com/) ; les observations sont chargées en direct depuis l'API de chaque instance. Un clic sur une carte ouvre la vue immersive [Panoramax](https://panoramax.fr) la plus proche.
- La page API affiche la spécification OpenAPI du backend (`data/openapi.yaml`) avec Swagger UI ; la liste des serveurs est générée depuis vigilo-conf.
- Les dépendances front (Leaflet, Swagger UI, police Inter) sont gérées avec npm (`package.json`) et mises à jour par Dependabot.

## Développement

Prérequis : Hugo **extended** ≥ 0.146, Node.js ≥ 22, Python 3.

```sh
make serve      # npm install + données des instances + serveur local sur http://localhost:1313
make generate   # construction dans public/
```

Les pages sont dans `content/` (Markdown).

## Publication

GitHub Actions (`.github/workflows/deploy.yml`) construit le site à chaque push sur la branche `source`, chaque jour (mise à jour des territoires) et à la demande, puis le publie sur la branche `master` servie par GitHub Pages. Les pull requests sont construites sans être publiées.
