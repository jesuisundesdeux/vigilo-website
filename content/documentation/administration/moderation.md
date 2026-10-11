---
title: Modération
weight: 1
---

## Ajout d'un modérateur 

### Actions modérateur

#### Via l'application web

Pour modérer, il faut une clé modérateur reconnue par l'instance de votre territoire. Dans l'application web
https://app.vigilo.city, menu **Devenir modérateur** :

* soit coller la clé fournie par l'administrateur de votre territoire, puis **Enregistrer** ;
* soit **Générer une clé**, la copier et la transmettre à l'association : un administrateur l'ajoute dans le panneau
  d'administration (voir [Actions administrateur](#actions-administrateur)). Enregistrer la clé dans l'application :
  le menu affiche « Clé modérateur en attente » jusqu'à ce qu'elle soit ajoutée.

La clé est propre à chaque territoire (une clé par territoire si vous modérez plusieurs territoires) et reste
enregistrée sur l'appareil.

Une fois la clé reconnue :

* un bandeau « Vous êtes modérateur » s'affiche sous la barre du haut ;
* le menu propose le raccourci **À modérer** (avec le nombre d'observations en attente), qui n'affiche que les
  observations à modérer ; il devient alors **Toutes les observations**, pour revenir aux filtres précédents avec
  tous les statuts ;
* en ouvrant une observation, les boutons de modération apparaissent en bas de la fiche : valider, refuser, modifier,
  ou remettre en modération. La liste se met à jour sans rechargement, ce qui permet d'enchaîner les observations ;
* le menu **Modération** (ou le lien **Réglages** du bandeau) permet de changer la clé, de la supprimer de l'appareil
  ou de désactiver le mode modérateur (puis de le réactiver) sans supprimer la clé.

### Actions administrateur

Sur le panneau d'administration :

* Aller dans le menu **Comptes**
* **Ajouter un compte** : rôle `moderator`, nom de la personne ; le login et le mot de passe peuvent rester vides
  (le modérateur n'utilise que sa clé), puis **Enregistrer**
* Si la personne a généré une clé dans l'application web, la coller dans **Clé fournie par la personne**
  (backend 0.0.30 ; 20 à 64 lettres ou chiffres) ; sinon une clé API est générée à la création : l'afficher dans la
  liste (bouton en forme d'œil, sur un écran large) et la transmettre au modérateur par un moyen sûr
* Pour retirer l'accès, régénérer la clé (l'ancienne ne fonctionne plus) ou passer le compte en `guest`
