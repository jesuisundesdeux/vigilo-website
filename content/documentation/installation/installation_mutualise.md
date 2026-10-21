---
title: Installation sur hebergement PHP/MySQL
weight: 2
---

## Installation sur serveur mutualisé

### Pré-requis

#### Logiciel

* PHP 7.3 à 8.5 avec les extensions `mysqli`, `gd`, `curl` et `fileinfo` (`zip` et `sodium` pour les mises à jour depuis l'administration)
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
`migrations/` (voir la [documentation de mise à jour](/fr/documentation/upgrade/)).

#### Base de données

Créer une base (vide) et un utilisateur chez l'hébergeur, et noter le serveur, le nom de la base, l'utilisateur et le
mot de passe. Les tables sont créées par l'assistant d'installation (backend 0.0.31 et plus récent).

#### Assistant d'installation

Ouvrir `https://adresse_du_serveur/admin/` : tant que l'instance n'est pas installée, l'assistant d'installation
s'affiche (voir [Initialisation](/fr/documentation/installation/initialisation/)). Il demande le **code d'installation**
écrit dans le fichier `caches/setup-code.php` du serveur (à ouvrir par FTP ou avec le gestionnaire de fichiers de
l'hébergeur), puis :

1. teste l'accès à la base (connexion et droits de création des tables) et enregistre `config/config.php`. Si le
   dossier `config/` n'est pas accessible en écriture, l'assistant affiche le contenu du fichier à déposer par FTP ;
2. crée les tables avec les scripts de `migrations/` ;
3. crée le compte administrateur et renseigne le nom et l'adresse de l'instance.

Installation manuelle (versions antérieures, ou sans l'assistant) : copier `config/config.php.tpl` vers
`config/config.php` en renseignant l'accès à la base, puis créer les tables avec un accès SSH
(`php scripts/vigilo-migrate.php --app=<racine du site>`) ou dans phpMyAdmin (`SET SESSION innodb_strict_mode=OFF;` puis
les fichiers `app/migrations/init-X.Y.Z.sql` dans l'ordre des versions) ; l'assistant ne demande alors plus que le
compte administrateur.

### Initialisation

Dès que l'application est déployée, passer à l'étape d'initialisation : [procédure ici](/fr/documentation/installation/initialisation/)
