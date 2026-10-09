---
title: Guide d'administration
weight: 4
---

## Panneau d'administration

Le panneau d'administration (`https://adresse_du_serveur/admin/`) est réservé aux comptes **admin** et **citystaff**
(ces derniers ne voient que l'accueil, les observations et les résolutions de leurs villes) :

* **Accueil** : observations à modérer, résolutions à valider, chiffres clés
* **Observations** : modération (approuver, refuser), modification, suppression, recherche (token ou observations
  similaires, rue, ville, catégorie), rattachement à une résolution, notes privées des modérateurs ; les photos y sont
  affichées sans pixelisation. **Actions groupées** : cocher des observations (ou « Tout sélectionner ») puis choisir
  l'action (approuver, désapprouver, remettre à qualifier, changer la catégorie ou la ville, créer une résolution
  regroupant la sélection, ajouter à une résolution, supprimer)
* **Résolutions** : validation des résolutions déclarées par les citoyens ; actions groupées (changer l'état,
  supprimer) sur les résolutions cochées
* **Villes**, **Scopes**, **Catégories** : voir la [configuration](/fr/documentation/configuration/)
* **Comptes** : création des comptes, rôle, villes des comptes citystaff, clé API (voir [Comptes](#comptes))
* **Configuration** : voir la [configuration de l'instance](/fr/documentation/configuration/global/)
* **Webhooks** : voir [Webhooks](#webhooks)
* **Journal** : actions privilégiées (connexions, modérations, réglages, mises à jour)
* **Mises à jour** : versions installées, mise à jour en un clic, vérifications de sécurité (voir [Mise à jour](/fr/documentation/upgrade/))

Les listes (villes, comptes, catégories de l'instance) se lisent dans un tableau ; **Ajouter** et **Modifier** ouvrent
une fenêtre de saisie, qui se rouvre avec la saisie si une valeur est refusée. Les photos s'ouvrent dans une fenêtre
en cliquant dessus ; une image par défaut s'affiche quand une observation n'a pas de photo. Le panneau s'utilise aussi
sur tablette et smartphone, et propose un thème sombre.

## Rôles

* **admin** : accès complet
* **moderator** : modération depuis l'application web (mode admin), avec la clé API de son compte ; pas d'accès au
  panneau d'administration
* **citystaff** : services d'une ville, n'accèdent qu'aux observations de leurs villes et peuvent en changer le statut
  (prise en compte, en cours de résolution, résolue)
* **guest** : compte sans droit, en attente d'un rôle

## Comptes

Menu **Comptes**, **Ajouter un compte** :

* **Rôle**, **Nom utilisateur** ;
* **Login** et **Mot de passe** pour se connecter au panneau d'administration ; sans login, le compte ne sert qu'avec
  sa clé API (cas des modérateurs) ;
* **Villes du compte citystaff** : villes dont le compte voit les observations.

Une clé API est générée à la création du compte. Elle s'affiche dans la liste sur un écran large (bouton en forme
d'œil) et peut être régénérée : l'ancienne clé ne fonctionne alors plus. **Modifier** change le compte ; un mot de
passe laissé vide reste inchangé.

## Webhooks

Menu **Webhooks** : appel d'un ou plusieurs services externes (API, outil de l'association, messagerie, outil de
signalement de la collectivité…) à chaque publication d'une observation.

* **Modèle** : préremplit le formulaire pour Mastodon, Slack / Mattermost, Discord, Bluesky (via un relais), un outil
  de ticketing de collectivité ([Open311](/fr/open311/)), Redmine ou un JSON générique ; il reste à remplacer les
  valeurs en `MAJUSCULES` ;
* **Méthode**, **URL**, **En-têtes**, **Format du corps** et **Corps**, avec des variables (`{{token}}`,
  `{{comment}}`, `{{photo_url}}`, `{{observation_url}}`, `{{lat}}`…) ;
* **Correspondance des catégories** : le code de chaque catégorie dans l'outil appelé (variable
  `{{categorie_code}}`, par exemple le `service_code` Open311) ; l'option **N'envoyer que les observations des
  catégories qui ont un code** limite le webhook à ces catégories ;
* **Enregistrer et tester** envoie la requête avec la dernière observation publiée ; le journal des derniers envois
  affiche la réponse de chaque appel.

Un service en échec n'empêche jamais la publication. Détails techniques et exemples :
[fonctionnement](https://github.com/jesuisundesdeux/vigilo-backend/blob/master/doc/FONCTIONNEMENT.md#webhooks),
[exemples Mastodon, Slack, Bluesky, ticketing de collectivité, Redmine](https://github.com/jesuisundesdeux/vigilo-backend/blob/master/doc/WEBHOOKS.md).

## Modération

Afin d'ajouter des modérateurs sur l'application, suivre [cette procédure](/fr/documentation/administration/moderation/)
