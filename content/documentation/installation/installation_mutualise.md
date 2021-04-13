---
title: Installation sur hebergement PHP/MySQL
weight: 2
---

## Installation sur serveur mutualisé

### Pré-requis

#### Logiciel

* PHP >= 7.1 avec php-gd
* Une base de données MySQL/MariaDB

#### Connaissances

* PHP/MySQL

### Mise en place

#### Téléchargement release

Télécharger la dernière release sur la page https://github.com/jesuisundesdeux/vigilo-backend/tags

Importer le contenu de ```app/``` dans l'arborescence web.

Sur un hebergement type OVH : il est necessaire de supprimer le fichier ```.htaccess``` (sinon : erreur 500 lors de l'accès aux pages php).

#### Mise en place base de données

Executer l'ensemble des scripts MySQL présents dans ```mysql/init/``` dans l'ordre sur MySQL.

Chez OVH : dans phpMyAdmin, enlever les lignes commentées des requêtes SQL (sinon : erreur lors de l'exécution).

#### Configuration

* config/config.php

Copier le fichier config/config.php.tpl vers config/config.php

Renseigner les différents valeurs à configurer concernant la base de données.

### Initialisation 

Dés que l'application est deployée, il est impératif de passer à l'étape d'initialisation : [Procédure Ici](/fr/documentation/installation/initialisation/)

