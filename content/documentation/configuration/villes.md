---
title: Ajout villes
weight: 5
---

## Configuration Villes

Dans le panneau d'administration, menu **Villes**, ajouter l'ensemble des villes du territoire : en les important
(ci-dessous), ou une à une avec le bouton **Ajouter une ville**, qui ouvre une fenêtre (nom, scope, code postal,
surface, population, site).
Cela permet de filtrer les observations par ville et de limiter les comptes des services municipaux (citystaff) aux
observations de leurs villes.

### Importer les communes du territoire

En haut de la page **Villes**, **Importer les communes d'un territoire** (ou le bouton **Importer les villes du
territoire** d'un scope) :

1. choisir le scope et cliquer sur **Rechercher les communes du territoire** : les communes françaises dont le centre est
   dans le rectangle du scope s'affichent sur une carte et dans une liste, avec leur code postal, leur surface et leur
   population ([geo.api.gouv.fr](https://geo.api.gouv.fr)) ;
2. décocher celles à ne pas importer (les communes déjà présentes sont signalées) ;
3. cliquer sur **Importer la sélection**.

Le territoire du scope doit avoir été tracé au préalable sur la page [Scopes](/fr/documentation/configuration/scopes/).

### Modifier ou supprimer une ville

Dans la liste, **Modifier** ouvre la fenêtre de la ville ; dans la fenêtre, le bouton **Wikidata** complète le code
postal, la surface, la population et le site à partir du nom. **Supprimer** retire la ville. Si une valeur est
refusée, la fenêtre se rouvre avec la saisie.

Hors de France, ajouter les villes à la main (avec l'aide de Wikidata).
