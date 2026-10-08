---
title: Modération
weight: 1
---

## Ajout d'un modérateur 

### Actions modérateur

#### Via l'application web

Pour modérer, il faut la clé API d'un compte **moderator**, fournie par un administrateur de votre territoire (voir
[Actions administrateur](#actions-administrateur)). Une fois la clé reçue :

* Ouvrir l'application web https://app.vigilo.city et son menu
* Appuyer 10 fois sur le logo Vigilo en haut du menu : la fenêtre « Devenir modérateur » s'ouvre
* Coller la clé fournie par l'administrateur, puis **Enregistrer**

Depuis la version 0.0.22 du back-end, les clés sont créées par l'instance : une clé produite par le bouton **Générer**
de l'application ne peut pas être enregistrée par l'administrateur. Tant que la clé n'est pas reconnue par
l'instance, le menu affiche « Presque modérateur ».

Une fois la clé enregistrée :

* Dans le menu, cliquer sur **Activer mode admin** et confirmer : le fond de la page passe en rouge
* La liste affiche alors par défaut les observations à modérer (modifiable dans les filtres)
* En ouvrant une observation, les boutons de modération apparaissent en bas de la fiche : approuver, refuser, modifier, ou remettre en modération. La liste se met à jour sans rechargement, ce qui permet d'enchaîner les observations

### Actions administrateur

Sur le panneau d'administration :

* Aller dans le menu **Comptes**
* **Ajouter un compte** : rôle `moderator`, nom de la personne ; le login et le mot de passe peuvent rester vides
  (le modérateur n'utilise que sa clé), puis **Enregistrer**
* Une clé API est générée à la création : l'afficher dans la liste (bouton en forme d'œil, sur un écran large) et la
  transmettre au modérateur par un moyen sûr
* Pour retirer l'accès, régénérer la clé (l'ancienne ne fonctionne plus) ou passer le compte en `guest`
