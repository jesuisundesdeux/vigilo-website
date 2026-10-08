---
title: Vigilo et Open311
description: Vigilo transmet les observations aux outils de signalement des collectivités compatibles Open311
---

## Vigilo est compatible Open311

À partir de la version 0.0.22 du back-end, une instance Vigilo peut transmettre automatiquement chaque observation
publiée à l'outil de gestion des signalements d'une collectivité, dès lors que cet outil est compatible **Open311**.
L'observation devient une demande d'intervention dans le logiciel du service concerné (voirie, propreté, police
municipale…), sans ressaisie.

## Open311, qu'est-ce que c'est ?

[Open311](https://www.open311.org/) est un **standard ouvert** pour signaler les problèmes de l'espace public :
nid-de-poule, éclairage en panne, dépôt sauvage, stationnement gênant… Son nom vient du « 311 », le numéro des
services municipaux non urgents aux États-Unis.

Sa spécification, [GeoReport v2](https://wiki.open311.org/GeoReport_v2/), définit une **API commune** à tous les outils
de signalement :

* **les services** (`services`) : les types de demandes que la collectivité accepte, chacun avec un code ;
* **les demandes** (`requests`) : un signalement, avec sa position, son adresse, sa description, une photo et un
  numéro de suivi ;
* **le suivi** : l'état de chaque demande (ouverte, fermée) et la réponse du service.

Une application compatible peut donc envoyer ses signalements à n'importe quelle collectivité compatible, sans
développement spécifique. Open311 est utilisé par de nombreuses villes, en Amérique du Nord comme en Europe, et par des
outils de signalement comme [FixMyStreet](https://www.fixmystreet.com/).

## Comment Vigilo l'utilise

1. Un citoyen ajoute une observation dans Vigilo.
2. Les modérateurs de l'association locale la valident ; visages et plaques d'immatriculation sont floutés.
3. À la publication, l'instance envoie une demande Open311 (`POST requests`) à l'outil de la collectivité, avec :
   * la position et l'adresse ;
   * la catégorie, le commentaire et l'explication ;
   * la photo (lien `media_url`) ;
   * l'identifiant de l'observation Vigilo.
4. La collectivité traite la demande dans son propre outil, avec son numéro de suivi.

L'envoi passe par les **webhooks** du panneau d'administration de l'instance. La configuration prête à l'emploi est
dans la [documentation des webhooks](https://github.com/jesuisundesdeux/vigilo-backend/blob/master/doc/WEBHOOKS.md#ticketing-de-collectivité-open311).

## Mettre en place la transmission

**Collectivité** : fournir à l'association qui gère l'instance Vigilo de votre territoire :

* l'adresse de votre API Open311 ;
* une clé d'API (`api_key`) ;
* le code du service destinataire (`service_code`).

**Association** : dans le panneau d'administration de l'instance, menu **Webhooks**, ajouter un webhook Open311 avec
ces informations, puis **Enregistrer et tester**.

Le contact de chaque association est sur la page [Les villes](/fr/villes/). Votre territoire n'a pas encore d'instance
Vigilo ? Voir [Votre ville ici](/fr/villes/maville/).

## Bon à savoir

* La transmission va de Vigilo vers la collectivité. L'état d'avancement de la demande dans l'outil de la collectivité
  ne remonte pas automatiquement dans Vigilo : l'association ou les comptes « services municipaux » de l'instance le
  mettent à jour.
* Toutes les observations publiées sont transmises au même service. Pour répartir par catégorie ou par commune,
  la répartition se fait côté collectivité, ou avec un outil d'automatisation.
* Seules les observations validées par les modérateurs sont transmises.
* Les observations restent par ailleurs disponibles en données ouvertes ([API Vigilo](/fr/api/), JSON, GeoJSON, CSV).
