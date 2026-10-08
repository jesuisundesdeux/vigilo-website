---
title: Ajout scope
weight: 4
---

## Configuration Scope

Les scopes sont des zones géographiques indépendantes au sein d'une même instance.
Ils correspondent en règle générale à une métropole, une agglomération voire une ville ; un seul scope suffit le plus souvent.

Dans le panneau d'administration, menu **Scopes**, le bouton **Ajouter un scope** ouvre une fenêtre qui demande
l'identifiant, le nom affiché, le département et l'email de contact, puis **Créer le scope**. Chaque scope s'affiche
ensuite dans un cadre où compléter ses informations, tracer son territoire sur la carte et **Enregistrer** :

* **Identifiant** : `XX_nom` où `XX` est le numéro de département (01 à 95, 2A, 2B, 971 à 976) ou le code pays si non
  français (be, ch…), et `nom` un nom court du territoire, sans espace, accent ni caractère spécial (exemple :
  `34_montpellier`). Le format est vérifié à l'enregistrement et le département se remplit automatiquement. Une fois
  l'instance référencée, ne plus changer l'identifiant : il est utilisé par les applications
* **Nom affiché** : nom de la zone affiché dans les applications
* **Département** : numéro du département, 0 si non applicable
* **Email contact** : adresse de contact de l'association en charge du scope
* **Zoom cartes** : niveau de zoom des cartes à l'ouverture des applications (réglable aussi avec la carte, ci-dessous)
* **URL carte externe** : si besoin, URL d'une carte qui affiche les observations (voir [Configuration UMAP](/fr/documentation/exploitation_donnees/umap/))
* **URL de base Nominatim** : service de géocodage inverse (adresse à partir de la position), laisser la valeur par défaut sauf besoin

### Territoire, centre et zoom : avec la carte

La carte du scope remplit les coordonnées sans avoir à les saisir :

* **Rechercher** une ville ou un lieu pour y déplacer la carte ;
* **Tracer le territoire** : cliquer-glisser sur la carte pour dessiner le rectangle qui limite la zone (les observations
  hors du rectangle sont refusées). Ou cadrer la carte puis **Territoire = vue de la carte** ;
* **Centre et zoom = vue de la carte** : cadrer la carte comme elle doit s'afficher à l'ouverture des applications, puis
  cliquer ; le marqueur du centre peut aussi être déplacé ;
* **Enregistrer**.

Les champs latitude / longitude minimale et maximale, centre et zoom restent modifiables à la main.

Le bouton **Importer les villes du territoire** mène à l'[import des communes](/fr/documentation/configuration/villes/)
du rectangle tracé. Le bouton **Supprimer** du cadre supprime le scope.
