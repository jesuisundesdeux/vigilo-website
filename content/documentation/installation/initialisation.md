---
title: Initialisation
weight: 3
---

## Assistant d'installation

Au premier accès à `https://adresse_du_serveur/admin/`, l'assistant d'installation (`admin/setup.php`, backend 0.0.31
et plus récent) prend la main tant que l'instance n'est pas installée.

* **Code d'installation** : il prouve que vous administrez le serveur ; sans lui, rien ne peut être modifié.
  * Hébergement mutualisé : fichier `caches/setup-code.php` du serveur (FTP, gestionnaire de fichiers) ;
  * Docker : affiché au démarrage du conteneur (`docker compose logs web | grep -i "code d'installation"`), ou
    `docker compose exec web cat caches/setup-code.php`.
* **Base de données** : hébergement mutualisé, formulaire d'accès à la base avec un bouton **Tester la connexion**
  (connexion et droits de création des tables), puis écriture de `config/config.php` ; Docker, vérification de la
  connexion avec les variables `MYSQL_*` du fichier `.env`.
* **Initialisation de la base** : création des tables (scripts de `migrations/`), ou mise à jour d'une base plus
  ancienne. L'assistant compare la version de la base à celle du code et refuse une base plus récente que le code.
  Avec Docker, la base est déjà initialisée au démarrage du conteneur.
* **Compte administrateur** : login et mot de passe (10 caractères au moins), nom de l'instance, et **URL de base**
  et protocole, détectés d'après l'adresse utilisée dans le navigateur (à corriger si l'instance est publiée à une
  autre adresse).

Le compte créé, l'assistant ouvre l'administration et se ferme définitivement (le code d'installation est supprimé).

## Première configuration

L'accueil de l'administration affiche les étapes de configuration restantes, avec un lien vers chaque page (et un
badge « Étape N » dans le menu) : nom et adresse de l'instance, territoire (scope), villes, référencement de
l'instance dans [vigilo-conf](https://github.com/jesuisundesdeux/vigilo-conf) pour apparaître dans l'application, puis,
facultatif, modérateurs et serveur de floutage des photos.

## Vérifications

Le panneau d'administration (`https://adresse_du_serveur/admin/`, menu **Mises à jour**) affiche des vérifications de
sécurité : répertoires `images/` et `caches/` non accessibles depuis le web, absence de l'ancien `install.php`, HTTPS,
version de PHP.

## Configuration

Il est à présent possible de configurer l'application : [procédure ici](/fr/documentation/configuration/)
