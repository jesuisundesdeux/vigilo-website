---
title: Ajout scope
weight: 4
---

## Configuration Scope

Les scopes sont des zones géographiques indépendantes au sein d'une même instance.
Ils correspondent en règle générale à une métropole, une agglomération voire une ville ; un seul scope suffit le plus souvent.

Dans le panneau d'administration, menu **Scopes**, ajouter un scope et remplir ses informations :

* **Identifiant** : `XX_yyyyyyy` où `XX` est le numéro de département (ou le code pays si non français : be, uk…) et
  `yyyyyyy` un nom court (sans espace, accent ni caractère spécial)
* **Nom affiché** : nom de la zone affiché dans les applications
* **Département** : numéro du département, 0 si non applicable
* **Email contact** : adresse de contact de l'association en charge du scope
* **Texte de partage par défaut** : texte proposé quand un utilisateur partage une observation
* **Latitude / longitude minimale / maximale** : limites géographiques de la zone (degrés décimaux)
* **Coordonnées du centre du scope** et **Zoom cartes** : centre et zoom des cartes affichées dans les applications
* **URL carte externe** : si besoin, URL d'une carte qui affiche les observations (voir [Configuration UMAP](/fr/documentation/exploitation_donnees/umap/))
* **URL de base Nominatim** : service de géocodage inverse (adresse à partir de la position), laisser la valeur par défaut sauf besoin
