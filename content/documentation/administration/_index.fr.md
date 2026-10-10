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
  regroupant la sélection, ajouter à une résolution, archiver ou désarchiver, supprimer).
  **Archivage** (administrateurs, backend ≥ 0.0.29) : une observation archivée n'est plus listée dans l'application
  ni sur la carte, mais reste comptée dans les statistiques. Archiver une observation (bouton de sa ligne), une
  sélection (actions groupées), ou toutes les observations d'une période et d'une catégorie (ou de toutes) avec le
  cadre « Archiver par période » : le nombre d'observations concernées s'affiche avant de confirmer. Le filtre
  « Archives » de la recherche retrouve les observations archivées, qui peuvent être désarchivées
* **Résolutions** : validation des résolutions déclarées par les citoyens ; actions groupées (changer l'état,
  supprimer) sur les résolutions cochées
* **Rapports** (backend ≥ 0.0.29, administrateurs et comptes citystaff pour leurs villes) : rapport des observations
  publiées pour une collectivité, en document A4 ou en diaporama, à enregistrer en PDF (« Imprimer / PDF »). On choisit
  la période, les villes et les types d'observation ; le rapport contient les chiffres clés (nombre, évolution, pour
  10 000 habitants, taux de résolution, délai de résolution…), des graphiques, une carte et les lieux récurrents
  (observations similaires regroupées : même catégorie, proches ou dans la même rue)
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
signalement de la collectivité…) aux **événements** cochés dans le formulaire (un ou plusieurs) :

* **Nouvelle observation** (avant modération) : par exemple pour prévenir les modérateurs dans leur canal ;
* **Observation publiée** (approuvée) et **Observation refusée** (désapprouvée) ;
* **Nouvelle résolution** (déclarée dans l'application ou créée dans l'admin) et **Changement d'état d'une
  résolution** : variables `{{resolution_token}}`, `{{resolution_status_name}}`, `{{resolution_comment}}`,
  `{{resolution_observations}}`…

Les webhooks existants restent abonnés à la publication. Réglages :

* **Modèle** : préremplit le formulaire pour Mastodon, Slack / Mattermost, Discord, Bluesky (via un relais), un outil
  de ticketing de collectivité ([Open311](/fr/open311/)), Redmine ou un JSON générique ; il reste à remplacer les
  valeurs en `MAJUSCULES` ;
* **Méthode**, **URL**, **En-têtes**, **Format du corps** et **Corps**, avec des variables (`{{token}}`,
  `{{comment}}`, `{{photo_url}}`, `{{photo_full_url}}` (photo d'origine même avant modération, lien signé valable
  7 jours, à réserver au canal des modérateurs), `{{observation_url}}`, `{{lat}}`, `{{event_description}}` (l'action
  en une phrase, par exemple « Observation ABCD1234 publiée : Véhicule ou objet gênant, Rue de la Gare
  (Montpellier). »), `{{event_label}}` (nom de l'événement)…) ;
* **Correspondance des catégories** : le code de chaque catégorie dans l'outil appelé (variable
  `{{categorie_code}}`, par exemple le `service_code` Open311) ; l'option **N'envoyer que les observations des
  catégories qui ont un code** limite le webhook à ces catégories ;
* **Enregistrer et tester** envoie la requête du premier événement coché avec la dernière observation publiée (ou la
  dernière résolution) ; le journal des derniers envois affiche l'événement et la réponse de chaque appel.

Un service en échec n'empêche jamais la publication. Détails techniques et exemples :
[fonctionnement](https://github.com/jesuisundesdeux/vigilo-backend/blob/master/doc/FONCTIONNEMENT.md#webhooks),
[exemples Mastodon, Slack, Bluesky, ticketing de collectivité, Redmine](https://github.com/jesuisundesdeux/vigilo-backend/blob/master/doc/WEBHOOKS.md).

## Modération

Afin d'ajouter des modérateurs sur l'application, suivre [cette procédure](/fr/documentation/administration/moderation/)
