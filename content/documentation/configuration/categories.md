---
title: Catégories
weight: 6
---

## Configuration Catégories

Les catégories classent les observations (stationnement sur piste cyclable, trottoir encombré…). La liste nationale
([vigilo-conf](https://github.com/jesuisundesdeux/vigilo-conf)) est commune à toutes les instances ; chaque instance
peut l'adapter depuis le panneau d'administration, menu **Catégories** (back-end 0.0.23 ou plus récent).

L'application web lit la liste de l'instance. Les applications qui ne la lisent pas encore continuent d'utiliser la
liste nationale.

### Catégories nationales

Le tableau affiche chaque catégorie nationale, son nombre d'observations et son état :

* **Désactiver** : la catégorie n'est plus proposée dans l'application ; les observations existantes la gardent ;
* **Réactiver** : la catégorie est de nouveau proposée.

Une catégorie « Désactivée nationalement » est retirée de la liste nationale et ne peut pas être réactivée sur
l'instance.

### Catégories de l'instance

**Ajouter une catégorie** ouvre une fenêtre :

* **Nom** (obligatoire) et **Nom en anglais** (facultatif) ;
* **Couleur** de la catégorie sur les cartes ;
* **Résolvable** : les citoyens peuvent déclarer l'observation résolue ;
* **Active** : la catégorie est proposée dans les applications.

Les catégories de l'instance sont numérotées à partir de 1000 (numéros jamais utilisés par la liste nationale). Le
bouton **Modifier** rouvre la même fenêtre. À la suppression d'une catégorie
utilisée par des observations, la fenêtre propose de **déplacer** ces observations vers une autre catégorie active ou
de les **supprimer** (avec leurs photos, définitivement). Pour seulement ne plus la proposer, la désactiver (décocher
**Active**).

**Une catégorie qui pourrait servir à d'autres instances ?** Proposez-la aussi dans la liste nationale : ouvrez une
pull request sur [vigilo-conf](https://github.com/jesuisundesdeux/vigilo-conf) en ajoutant une entrée à
`main/categorielist.json` (numéro libre en dessous de 1000, nom, nom en anglais, couleur, résolvable). Une fois
fusionnée, elle est proposée par toutes les instances et comptée dans les statistiques communes ; vous pourrez alors
déplacer les observations de votre catégorie vers la catégorie nationale (supprimer votre catégorie en choisissant
« déplacer ») puis désactiver les doublons.

Pour transmettre les catégories à un outil externe (Open311, Redmine…), voir la correspondance des catégories des
[webhooks](/fr/documentation/administration/#webhooks).
