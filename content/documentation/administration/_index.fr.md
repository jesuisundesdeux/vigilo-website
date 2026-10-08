---
title: Guide d'administration
weight: 4
---

## Panneau d'administration

Le panneau d'administration (`https://adresse_du_serveur/admin/`) est réservé aux comptes **admin** et **citystaff** :

* **Accueil** : observations à modérer, résolutions à valider, chiffres clés
* **Observations** : modération (approuver, refuser), modification, suppression, filtres (statut, ville, catégorie,
  adresse, doublons proches), notes privées des modérateurs ; les photos y sont affichées sans pixelisation
* **Résolutions** : validation des résolutions déclarées par les citoyens
* **Villes**, **Scopes** : voir la [configuration](/fr/documentation/configuration/)
* **Comptes** : création des comptes, rôle, villes des comptes citystaff, clé de modération
* **Configuration** : voir la [configuration de l'instance](/fr/documentation/configuration/global/)
* **Webhooks** : appel d'un ou plusieurs services externes (API, outil de l'association, messagerie…) à chaque
  publication d'une observation, avec une URL, des en-têtes et un corps personnalisables par des variables
  (`{{token}}`, `{{comment}}`, `{{photo_url}}`, `{{observation_url}}`, `{{lat}}`…), un bouton de test et le journal des
  envois ([détails](https://github.com/jesuisundesdeux/vigilo-backend/blob/master/doc/FONCTIONNEMENT.md#webhooks))
* **Journal** : actions privilégiées (connexions, modérations, réglages, mises à jour)
* **Mises à jour** : versions installées, mise à jour en un clic, vérifications de sécurité (voir [Mise à jour](/fr/documentation/upgrade/))

## Rôles

* **admin** : accès complet
* **moderator** : modération depuis l'application web (mode admin), avec une clé associée à son compte
* **citystaff** : services d'une ville, n'accèdent qu'aux observations de leurs villes et peuvent en changer le statut
  (prise en compte, en cours de résolution, résolue)

## Modération

Afin d'ajouter des modérateurs sur l'application, suivre [cette procédure](/fr/documentation/administration/moderation/)
