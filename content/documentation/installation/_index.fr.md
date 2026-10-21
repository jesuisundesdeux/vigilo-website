---
title: Installation de Vigilo
weight: 2
---

## Versions prises en charge

| Composant | Versions | Remarques |
|---|---|---|
| Back-end (vigilo-backend) | Dernière version publiée ([releases](https://github.com/jesuisundesdeux/vigilo-backend/releases)) | Mise à jour possible depuis la **0.0.17** ou plus récente ([mises à jour](/fr/documentation/upgrade/)) |
| PHP | **7.3 à 8.5** | Image Docker : PHP 8.5. Extensions : `mysqli`, `gd`, `curl`, `fileinfo` (`zip` et `sodium` pour les mises à jour depuis l'administration) |
| Base de données | **MariaDB 10.3** ou plus récente, **MySQL 5.7** ou plus récente (InnoDB) | Testé en continu avec MariaDB 11.4 ; l'installation Docker utilise MariaDB LTS (`mariadb:lts`) |
| Docker | Docker Engine récent (29 compris) et **Docker Compose v2** (`docker compose`) | Images `linux/amd64` et `linux/arm64` ; mises à jour depuis l'administration avec Watchtower (`nickfedor/watchtower`) |
| HTTPS | Obligatoire | Les applications refusent une instance en HTTP |
| Application web ([app.vigilo.city](https://app.vigilo.city)) | Toute instance en back-end **0.0.17** ou plus récent | Les fonctions récentes (catégories propres à l'instance, etc.) demandent un back-end à jour ; sinon l'application revient au fonctionnement précédent |

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
