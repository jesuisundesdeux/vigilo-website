---
title: Installation sur hebergement PHP/MySQL
weight: 2
---

## Installation sur serveur mutualisé

### Pré-requis

#### Logiciel

* PHP 7.3 à 8.3 avec les extensions `mysqli`, `gd`, `curl` et `fileinfo` (`zip` et `sodium` pour les mises à jour depuis l'administration)
* Une base de données MySQL ou MariaDB
* Un certificat HTTPS (les applications refusent les instances en HTTP)

#### Connaissances

* PHP / MySQL, transfert de fichiers (FTP/SFTP), phpMyAdmin

### Mise en place

#### Téléchargement

Télécharger l'archive **Source code** de la dernière version sur https://github.com/jesuisundesdeux/vigilo-backend/releases
et copier le contenu du répertoire `app/` à la racine du site.

Le serveur web doit pouvoir écrire dans `images/` et `caches/` (et dans tout le répertoire du code pour les mises à jour
depuis l'administration). Avec Nginx (qui ne lit pas les `.htaccess`), interdire l'accès à `images/`, `caches/`,
`migrations/` et `install.php` (voir la [documentation de mise à jour](/fr/documentation/upgrade/)).

#### Base de données

Créer une base et un utilisateur, puis créer les tables :

* avec un accès SSH : `php scripts/vigilo-migrate.php --app=<racine du site>` depuis le répertoire de l'archive ;
* sinon, dans phpMyAdmin, exécuter `SET SESSION innodb_strict_mode=OFF;` puis les fichiers `app/migrations/init-X.Y.Z.sql`
  **dans l'ordre des versions** (0.0.1, 0.0.2, … jusqu'à la dernière).

#### Configuration

Copier `config/config.php.tpl` vers `config/config.php` et renseigner l'accès à la base de données.

### Initialisation

Dès que l'application est déployée, passer à l'étape d'initialisation : [procédure ici](/fr/documentation/installation/initialisation/)
