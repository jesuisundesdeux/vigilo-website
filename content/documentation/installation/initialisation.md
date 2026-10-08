---
title: Initialisation
weight: 3
---

## Création du compte administrateur

* Docker : `install.php` est mis en place automatiquement au premier démarrage.
  Hébergement mutualisé : copier `install_app/install.php` (de l'archive) à la racine du site.
* Ouvrir `https://adresse_du_serveur/install.php` et remplir les champs pour créer le compte administrateur.
* Le fichier `install.php` se supprime ensuite (il refuse de fonctionner dès qu'un compte existe).

## Vérifications

Le panneau d'administration (`https://adresse_du_serveur/admin/`, menu **Mises à jour**) affiche des vérifications de
sécurité : répertoires `images/` et `caches/` non accessibles depuis le web, absence de `install.php`, HTTPS,
version de PHP.

## Configuration

Il est à présent possible de configurer l'application : [procédure ici](/fr/documentation/configuration/)
