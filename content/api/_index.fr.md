---
title: API
weight: 15
description: Documentation de l'API REST des instances Vigilo
---

Chaque territoire Vigilo est servi par sa propre instance de [vigilo-backend](https://github.com/jesuisundesdeux/vigilo-backend), qui expose la même API REST.
Choisissez une instance dans la liste **Servers**, puis testez les appels en lecture avec **Try it out**.

Pour ajouter une observation, l'application crée l'observation (`create_issue.php`), envoie sa photo (`add_image.php`), puis affiche le panneau généré (`generate_panel.php`).
