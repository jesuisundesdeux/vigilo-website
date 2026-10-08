---
title: Installation de Vigilo
weight: 2
---

## Installation du back-end

Chaque instance dispose de son propre back-end ([vigilo-backend](https://github.com/jesuisundesdeux/vigilo-backend)), installable de deux manières.

### Serveur dédié avec Docker (recommandé)

Le code est livré dans une image Docker versionnée : installation et mises à jour se font en quelques commandes,
et les options (serveur de floutage, mise à jour depuis l'administration) s'activent simplement.
Nécessite des compétences d'administration système (Linux, Docker, reverse proxy HTTPS).

[La procédure est disponible ici](/fr/documentation/installation/installation_dedie/)

### Hébergement mutualisé PHP/MySQL

Solution plus accessible, sans administration de serveur. Les mises à jour se font ensuite depuis le panneau
d'administration.

[La procédure est disponible ici](/fr/documentation/installation/installation_mutualise/)
