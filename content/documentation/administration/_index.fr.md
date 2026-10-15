---
title: Guide d'administration
weight: 4
---

## Panneau d'administration

Le panneau d'administration (`https://adresse_du_serveur/admin/`) est réservé aux comptes **admin** et **citystaff**
(ces derniers ne voient que l'accueil, les observations et les résolutions de leurs villes, les rapports et, en
consultation, les problèmes) :

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
* **Problèmes** (backend ≥ 0.0.32, administrateurs ; consultation pour les comptes citystaff) : regroupement des observations sous des problèmes, voir
  [Problèmes](#problèmes)
* **Rapports** (backend ≥ 0.0.29, administrateurs et comptes citystaff pour leurs villes) : rapport des observations
  publiées pour une collectivité, en document A4 ou en diaporama, à enregistrer en PDF (« Imprimer / PDF »). On choisit
  la période, les villes et les types d'observation ; le rapport contient les chiffres clés (nombre, évolution, pour
  10 000 habitants, taux de résolution, délai de résolution…), des graphiques, une carte et les lieux récurrents
  (observations similaires regroupées : même catégorie, proches ou dans la même rue) et, pour les administrateurs, les
  problèmes suivis
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

## Problèmes

Menu **Problèmes** (backend ≥ 0.0.32, géré par les administrateurs) : un problème regroupe les observations publiées
d'un même endroit et d'un même type, par exemple « Stationnement sur la piste cyclable de l'avenue X ». Il n'est
visible que dans le panneau d'administration (ni dans l'application, ni sur la carte publique).

**Nouveau problème** :

* **Titre** et **Description** ;
* **Catégories** : une ou plusieurs (catégories nationales et celles de l'instance) ; une observation de l'une
  d'elles peut être rattachée ;
* **Début** et **Fin** (facultative) : période sur la date des observations ;
* **Priorité** (basse, normale, haute, critique) et **Statut** (ouvert, en cours, en attente, résolu, clos) ;
* **Zone** (la recherche au-dessus de la carte la déplace vers une ville ou un lieu) :
  * un **cercle** : cliquer sur la carte pour placer le centre (déplaçable), puis régler le rayon ;
  * un **polygone** : cliquer sur la carte pour ajouter ses points (au moins 3). Un point se **déplace** en le faisant
    glisser ; le petit point au milieu d'un côté **insère** un point (clic ou glisser) ; un clic droit (appui long sur
    mobile) **retire** un point ; « Retirer le dernier point », « Effacer » ;
  * des **rues** (backend ≥ 0.0.33) : une ou plusieurs rues sous la forme « Rue, Ville » (sans ville : la rue dans
    toutes les villes). Le champ propose les rues des observations publiées, et cliquer sur une observation de la carte
    ajoute sa rue. Une observation correspond si son adresse est dans l'une de ces rues, sans tenir compte des
    majuscules, des accents ni du numéro.

  La carte du formulaire affiche les observations de la suggestion (problème créé depuis une suggestion) ou celles
  déjà rattachées au problème modifié ; en zone Rues, celles des rues choisies sont en vert.

La liste se trie par priorité ; on y cherche dans les titres et descriptions, et on filtre par statut (dont « Actifs » :
ouvert, en cours, en attente), priorité et catégorie. **Modifier** (ou « Modifier la zone » sous la carte de la fiche) reprend le formulaire, pour changer par exemple le
polygone ; supprimer un problème ne
supprime pas ses observations. Créations, modifications (avec les valeurs changées) et suppressions sont inscrites au
**Journal**.

Le titre d'un problème ouvre sa **fiche** : informations, carte de la zone et des observations, et observations
rattachées (photo, date, mode et auteur du rattachement).

* **Rattachement des observations existantes** : **Compter** affiche, sans rien modifier, le nombre d'observations
  publiées qui correspondent au problème, celles déjà rattachées, celles à rattacher et celles qui appartiennent à un
  autre problème. **Rattacher** (après confirmation) refait le calcul et rattache celles qui n'appartiennent à aucun
  problème ; on peut recommencer sans risque, rien n'est rattaché deux fois.
* Une observation appartient à **un seul problème** : celles d'un autre problème ne sont jamais déplacées, elles sont
  listées avec un lien vers cet autre problème. Pour les déplacer, les détacher de l'autre problème puis les
  rattacher.
* **Rattacher** une observation à la main : saisir son token (observation publiée, même hors de la zone, des
  catégories ou de la période) ; **Détacher** la retire du problème.

**Rattachement automatique** : quand une observation est publiée (approuvée dans le panneau ou depuis
l'application), elle est rattachée au problème actif (ouvert, en cours, en attente) qui lui correspond, s'il n'y en a
qu'un ; un message l'indique lors de l'approbation dans le panneau. Si plusieurs problèmes correspondent, elle apparaît
dans le cadre **À arbitrer** en haut de la page Problèmes : choisir son problème. Un problème résolu ou clos ne reçoit
plus d'observations automatiquement.

**Problème résolu** (backend ≥ 0.0.34) : quand un problème passe à **Résolu**, sa fiche propose de passer ses
observations en résolues (bouton, après confirmation). Celles qui ne sont dans aucune résolution sont regroupées dans
une nouvelle résolution « Résolue » datée du jour ; les résolutions qui contiennent les autres passent à « Résolue ».
Si ces résolutions contiennent aussi des observations d'un autre endroit, la fiche le signale avant de confirmer : elles
seront résolues également. Les observations apparaissent alors résolues dans l'application.

Sur la fiche, **Statut** et **Priorité** se changent directement ; les **notes internes** (échanges avec la
collectivité, relances, décisions) ne sont visibles que dans le panneau d'administration, jamais publiées ni reprises
dans les rapports.

**Suggestions** : le bouton **Rechercher** du cadre Suggestions propose les groupes d'observations publiées qui
n'appartiennent à aucun problème, de même catégorie et proches (même méthode que les lieux récurrents des rapports).
Les seuils se règlent dans **Configuration**, cadre « Suggestions de problèmes » : nombre minimal d'observations
(3 par défaut), distance de regroupement (50 m) et période analysée (12 mois). **Créer le problème** ouvre le
formulaire prérempli (titre, catégorie, cercle couvrant le groupe, date de la première observation) à vérifier avant
d'enregistrer, puis **Compter** et **Rattacher** depuis sa fiche ; **Ignorer** ne la propose plus. Aucun problème n'est
créé automatiquement.

**Rapport** : un administrateur peut cocher « Inclure les problèmes suivis » dans le formulaire des **Rapports** ; le
rapport contient alors une section « Problèmes suivis » (problèmes ayant des observations dans le rapport : état,
priorité, nombre d'observations, période), sans les notes internes. Les rapports des comptes citystaff n'ont pas cette
section.

## Rôles

* **admin** : accès complet
* **moderator** : modération depuis l'application web, avec la clé API de son compte ; pas d'accès au
  panneau d'administration
* **citystaff** : services d'une ville, n'accèdent qu'aux observations de leurs villes et peuvent en changer le statut
  (prise en compte, en cours de résolution, résolue) ; ils consultent aussi, sans pouvoir les modifier, les problèmes
  qui ont des observations dans leurs villes (sans les notes internes)
* **guest** : compte sans droit, en attente d'un rôle

## Comptes

Menu **Comptes**, **Ajouter un compte** :

* **Rôle**, **Nom utilisateur** ;
* **Login** et **Mot de passe** pour se connecter au panneau d'administration ; sans login, le compte ne sert qu'avec
  sa clé API (cas des modérateurs) ;
* **Clé fournie par la personne** (facultatif, backend 0.0.30) : clé générée par la personne dans l'application web
  (« Devenir modérateur ») et qu'elle vous a transmise ; elle devient la clé API du compte ;
* **Villes du compte citystaff** : villes dont le compte voit les observations.

Sans clé fournie, une clé API est générée à la création du compte. Elle s'affiche dans la liste sur un écran large (bouton en forme
d'œil) et peut être régénérée : l'ancienne clé ne fonctionne alors plus. **Modifier** change le compte ; un mot de
passe laissé vide reste inchangé.

## Webhooks

Menu **Webhooks** : appel d'un ou plusieurs services externes (API, outil de l'association, messagerie, outil de
signalement de la collectivité…) à l'**événement** choisi dans le formulaire (un seul par webhook : les variables
et le corps en dépendent ; créer un webhook par événement à suivre) :

* **Nouvelle observation** (avant modération) : par exemple pour prévenir les modérateurs dans leur canal ;
* **Observation publiée** (approuvée) et **Observation refusée** (désapprouvée) ;
* **Nouvelle résolution** (déclarée dans l'application ou créée dans l'admin) et **Changement d'état d'une
  résolution** : variables `{{resolution_token}}`, `{{resolution_status_name}}`, `{{resolution_comment}}`,
  `{{resolution_observations}}`…

Un webhook créé avant la version 0.0.32 avec plusieurs événements continue d'être envoyé ; il est signalé dans la
liste et doit être modifié pour n'en garder qu'un. Réglages :

* **Modèle** : préremplit le formulaire pour Mastodon, Slack / Mattermost, Discord, Bluesky (via un relais), un outil
  de ticketing de collectivité ([Open311](/fr/open311/)), Redmine ou un JSON générique ; il reste à remplacer les
  valeurs en `MAJUSCULES` ;
* **Méthode**, **URL**, **En-têtes**, **Format du corps** et **Corps**, avec des variables (`{{token}}`,
  `{{comment}}`, `{{photo_url}}`, `{{photo_full_url}}` (photo d'origine même avant modération, lien signé valable
  7 jours, à réserver au canal des modérateurs), `{{observation_url}}`, `{{lat}}`, `{{event_description}}` (l'action
  en une phrase, par exemple « Observation ABCD1234 publiée : Véhicule ou objet gênant, Rue de la Gare
  (Montpellier). »), `{{event_label}}` (nom de l'événement)…) ;
* **Catégories** et **Villes** : limitent le webhook aux observations de ces catégories et de ces villes (aucune
  case cochée : toutes ; **Sans ville référencée** pour les observations hors des villes de l'instance), par exemple
  un webhook par service ou par commune ; une résolution est envoyée si l'une de ses observations correspond
  (version 0.0.30) ;
* **Correspondance des catégories** : le code de chaque catégorie dans l'outil appelé (variable
  `{{categorie_code}}`, par exemple le `service_code` Open311) ; l'option **N'envoyer que les observations des
  catégories qui ont un code** limite le webhook à ces catégories ;
* **Enregistrer et tester** envoie la requête de l'événement choisi avec la dernière observation publiée (ou la
  dernière résolution) ; le journal des derniers envois affiche l'événement et la réponse de chaque appel.

Un service en échec n'empêche jamais la publication. Détails techniques et exemples :
[fonctionnement](https://github.com/jesuisundesdeux/vigilo-backend/blob/master/doc/FONCTIONNEMENT.md#webhooks),
[exemples Mastodon, Slack, Bluesky, ticketing de collectivité, Redmine](https://github.com/jesuisundesdeux/vigilo-backend/blob/master/doc/WEBHOOKS.md).

## Modération

Afin d'ajouter des modérateurs sur l'application, suivre [cette procédure](/fr/documentation/administration/moderation/)
