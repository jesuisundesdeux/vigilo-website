---
title: Configuration Instance
weight: 2
---

## Configuration de l'instance

Aller sur `https://adresse_du_serveur/admin/`, menu **Configuration**.

### Instance

* **Nom de l'instance** : par exemple « Vigilo Montpellier »
* **URL de base** : adresse de Vigilo sans `https://` (exemple : `vigilo.jesuisundesdeux.org`)
* **Protocole** : `https`
* **Langue** : `fr-FR`
* **Fuseau horaire** : par exemple `Europe/Paris`
* **Jeu de caractères MySQL** : `utf8mb4` (à ne modifier qu'en connaissance de cause)

### Publication

* **Observations non modérées affichées au public** : ce que le public voit d'une observation en attente de
  validation — *Pas d'affichage du tout* (elle n'apparaît qu'une fois validée), *Affichées, photo pixelisée* (la vraie
  photo, pixelisée jusqu'à la validation) ou *Affichées, photo de substitution* (une image générique à la place de la
  photo)
* **Masquer le texte des observations non modérées** : quand les observations non modérées sont affichées, masque leur
  commentaire et leur explication jusqu'à la validation
* **Masquer les observations résolues depuis plus de N jours** : 0 pour ne jamais les masquer

### Photos

* **Serveur de floutage** : si renseigné, chaque photo envoyée est transmise à ce serveur qui masque visages et plaques
  d'immatriculation. Avec Docker, le service fourni s'active avec le profil `blur` (voir
  [l'installation](/fr/documentation/installation/installation_dedie/#options)) ; laisser vide pour utiliser la variable
  `VIGILO_BLUR_URL`, ou pour publier les photos telles qu'envoyées. Si le serveur ne répond pas, la photo est conservée
  telle quelle : la modération reste le garde-fou.

### Anti-spam

* **Observations créées max. par IP et par 10 minutes** : au-delà, les créations depuis la même adresse sont refusées
  temporairement (60 par défaut, 0 = pas de limite)
