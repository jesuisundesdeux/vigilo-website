---
title: Sauvegarde
weight: 1
---

## Données à sauvegarder

Il est important de sauvegarder quotidiennement les données Vigilo à un endroit différent que celui où est hebergé le site.

Les données Vigilo sont présentes sous forme de fichiers et d'une base de données.

### Fichiers

Les repertoires suivants doivent être sauvegardés :

* images/ : IMPORTANT ! contient les photos Vigilo
* maps/ : générations des cartes via Mapquest
* caches/ : moins important, contient les caches mais permet d'éviter des problèmes de performances en cas de réinstallation

### Base de données

#### Avec Docker

Ajouter en crontab :

```
# crontab -e -u root
```

La ligne :

```
0 1 * * * /usr/bin/docker exec [CONTAINER_DB_1] sh -c 'exec mysqldump --all-databases -uroot -p"$MYSQL_ROOT_PASSWORD"'  | gzip -c -9 > [REPERTOIRE_BACKUP]/dump.$(date +\%Y\%m\%d\%H\%M).sql.gz
```

Remplacer :

* [CONTAINER_DB_1] par le nom du container de la base de données (visible via docker ps)
* [REPERTOIRE_BACKUP] par le repertoire de savuvegarde

Ne pas oublier de copier régulierement le contenu de REPERTOIRE_BACKUP sur un autre serveur/machines !!!

#### Hebergement mutualisé

Cette procédure dépend de l'hebergeur.

En général la procédure se base sur PhpMyAdmin, vous trouverez un tuto pour effectuer la sauvegarde dessus via le lien https://help.one.com/hc/fr/articles/115005593645-Comment-faire-une-sauvegarde-de-ma-base-de-donn%C3%A9es-

