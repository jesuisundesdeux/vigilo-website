---
title: API
weight: 15
description: Documentation de l'API REST des instances Vigilo
---

Chaque territoire Vigilo est servi par sa propre instance de [vigilo-backend](https://github.com/jesuisundesdeux/vigilo-backend), qui expose la même API REST.
Choisissez une instance dans la liste **Servers**, puis testez les appels en lecture avec **Try it out**.

Pour ajouter une observation, l'application crée l'observation (`create_issue.php`), puis envoie sa photo (`add_image.php`) ; l'image publique (`generate_panel.php`) reste pixelisée tant que les modérateurs n'ont pas approuvé l'observation.

Les catégories de chaque instance sont sur `get_categories.php` (backend ≥ 0.0.23) ; pour une instance plus ancienne, utiliser la [liste nationale](https://raw.githubusercontent.com/jesuisundesdeux/vigilo-conf/main/main/categorielist.json). Les observations sont des données ouvertes (CC0), disponibles en JSON, GeoJSON et CSV.

Référence détaillée de chaque route (arguments, erreurs, compatibilité) : [doc/REST_API.md](https://github.com/jesuisundesdeux/vigilo-backend/blob/master/doc/REST_API.md).
