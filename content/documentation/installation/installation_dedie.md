---
title: Installation sur serveur dédié avec Docker
weight: 1
---

## Installation Vigilo sur serveur dédié avec Docker

### Pré-requis

#### Logiciel

* OS Linux
* Docker avec Docker Compose (`docker compose`)
* Un reverse proxy (Nginx, Caddy, Traefik…) qui gère le certificat HTTPS (Let's Encrypt) et l'accès public à Vigilo :
  les applications refusent les instances en HTTP

#### Connaissances

* Linux / Docker

### Mise en place

Récupérer le dépôt (seuls `docker-compose.yml` et `.env_sample` sont utilisés : le code est dans l'image Docker) :

```
$ git clone https://github.com/jesuisundesdeux/vigilo-backend.git
$ cd vigilo-backend
$ cp .env_sample .env
```

Adapter les valeurs dans `.env` :

* `VOLUME_PATH` : répertoire persistant du serveur où sont stockées les données (base, photos, caches, logs)
* `MYSQL_ROOT_PASSWORD`, `MYSQL_PASSWORD` : mots de passe de la base de données
* `BIND` : adresse d'écoute `HOTE:PORT` vers laquelle le reverse proxy redirige (par exemple `127.0.0.1:8080`)
* `VIGILO_IMAGE` : image du back-end, `vigilobs/vigilo-backend:0.0` par défaut (suit les correctifs de la série 0.0)
* `AUTOUPDATE` : `true` (défaut) pour migrer la base automatiquement au démarrage après une mise à jour

Lancer le service :

```
$ docker compose up -d
```

La base est créée au premier démarrage.

### Options

* **Serveur de floutage** : masque automatiquement visages et plaques d'immatriculation sur les photos reçues.
  Ajouter `VIGILO_BLUR_URL=http://blur:8000/blur` dans `.env` et démarrer avec `docker compose --profile blur up -d`
  ([documentation](https://github.com/jesuisundesdeux/vigilo-backend/blob/master/blur-server/README.md)).
* **Mise à jour depuis l'administration** : renseigner `WATCHTOWER_TOKEN` (chaîne aléatoire) et
  `VIGILO_WATCHTOWER_URL=http://watchtower:8080` dans `.env`, puis démarrer avec `docker compose --profile watchtower up -d`.
  Le bouton **Mettre à jour l'image avec Watchtower** apparaît alors dans le menu **Mises à jour**. Le service utilise
  l'image `nickfedor/watchtower:1` (l'ancienne image `containrrr/watchtower` ne démarre plus avec Docker Engine 29) ;
  Watchtower a accès au socket Docker et n'agit que sur le conteneur `web`, à la demande
  ([détails](/fr/documentation/upgrade/#docker)).

Les deux options se combinent : `docker compose --profile blur --profile watchtower up -d`.

### Initialisation

Dès que le service est démarré, passer à l'étape d'initialisation : [procédure ici](/fr/documentation/installation/initialisation/)
