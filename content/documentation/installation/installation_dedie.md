---
title: Installation sur serveur dédié avec Docker
weight: 1
---

## Installation Vigilo sur serveur dédié avec Docker

### Pré-requis

#### Logiciel

* OS Linux, processeur `amd64` (x86-64) ou `arm64` (Raspberry Pi 4/5, serveurs ARM)
* Docker Engine récent (Docker Engine 29 compris) avec Docker Compose v2 (`docker compose`, pas l'ancien
  `docker-compose`)
* Fournis par les images : PHP 8.5, MariaDB LTS (`mariadb:lts`) — voir les
  [versions prises en charge](/fr/documentation/installation/#versions-prises-en-charge)
* Un reverse proxy (Nginx, Caddy, Traefik…) qui gère le certificat HTTPS (Let's Encrypt) et l'accès public à Vigilo :
  les applications refusent les instances en HTTP

#### Connaissances

* Linux / Docker

### Mise en place

Le code est dans l'image Docker : il suffit de deux fichiers, `.env` et `docker-compose.yml`, dans un répertoire du
serveur (par exemple `/opt/vigilo`).

#### `.env`

```ini
# Appliquer les migrations de la base au démarrage du conteneur (false : depuis l'administration)
AUTOUPDATE=true

# Répertoire persistant des données (base, photos, caches, journaux)
VOLUME_PATH=/data/vigilo
# Adresse d'écoute HOTE:PORT, vers laquelle le reverse proxy redirige
BIND=127.0.0.1:8080

# Base de données (créée au premier démarrage)
MYSQL_ROOT_PASSWORD=mot-de-passe-root
MYSQL_USER=vigilo
MYSQL_PASSWORD=mot-de-passe-vigilo
MYSQL_HOST=db
MYSQL_DATABASE=vigilo

# Image du back-end : le tag 0.0 suit les correctifs de la série 0.0
VIGILO_IMAGE=vigilobs/vigilo-backend:0.0

# Mise à jour depuis l'administration (Watchtower) : chaîne aléatoire,
# par exemple le résultat de : openssl rand -hex 32
WATCHTOWER_TOKEN=a-remplacer

# Serveur de floutage (facultatif, voir plus bas)
# VIGILO_BLUR_URL=http://blur:8000/blur
```

Remplacer les mots de passe et `WATCHTOWER_TOKEN` par des valeurs aléatoires, et protéger le fichier
(`chmod 600 .env`).

#### `docker-compose.yml`

Identique au [fichier du dépôt](https://github.com/jesuisundesdeux/vigilo-backend/blob/master/docker-compose.yml) :

```yaml
# Vigilo backend with Docker.
#
# The code comes from the versioned image: "docker compose pull && docker compose up -d"
# installs the latest patch of the 0.0 series, the database is migrated at startup
# (AUTOUPDATE). Watchtower updates it from the admin (page "Mises à jour"): set
# WATCHTOWER_TOKEN in .env (e.g. openssl rand -hex 32).
#
# To mask the faces and licence plates of the photos before they are published,
# start the blur server too and set VIGILO_BLUR_URL=http://blur:8000/blur in .env:
#
#   docker compose --profile blur up -d
#
# This file works on its own (no copy of the repository needed): the code is in the images.
# Development with the code of this repository: see docker-compose.dev.yml.
services:
  db:
    image: ${MARIADB_IMAGE:-mariadb:lts}
    restart: always
    volumes:
      - ${VOLUME_PATH}/db/mysql:/var/lib/mysql
    environment:
      - MARIADB_ROOT_PASSWORD=${MYSQL_ROOT_PASSWORD}
      - MARIADB_USER=${MYSQL_USER}
      - MARIADB_PASSWORD=${MYSQL_PASSWORD}
      - MARIADB_DATABASE=${MYSQL_DATABASE}
      # Upgrade the data files when the MariaDB image changes major version
      - MARIADB_AUTO_UPGRADE=1

  web:
    image: ${VIGILO_IMAGE:-vigilobs/vigilo-backend:0.0}
    restart: always
    ports:
      - "${BIND}:80"
    depends_on:
      - db
    volumes:
      - ${VOLUME_PATH}/files/caches:/var/www/html/caches
      - ${VOLUME_PATH}/files/images:/var/www/html/images
      - ${VOLUME_PATH}/logs/apache2/var_log_apache2:/var/log/apache2
    environment:
      - MYSQL_HOST
      - MYSQL_USER
      - MYSQL_PASSWORD
      - MYSQL_DATABASE
      - AUTOUPDATE
      # Update button of the admin (service watchtower)
      - VIGILO_WATCHTOWER_URL=${VIGILO_WATCHTOWER_URL:-http://watchtower:8080}
      - VIGILO_WATCHTOWER_TOKEN=${WATCHTOWER_TOKEN:-}
      # Blur server (profile "blur"); empty: photos published as sent. The admin
      # setting "Serveur de floutage" takes precedence when filled in.
      - VIGILO_BLUR_URL=${VIGILO_BLUR_URL:-}
      # Closed set of instances (demo): shared configuration (citylist.json,
      # categorielist.json) and web app other than vigilo-conf and app.vigilo.city
      - VIGILO_CONF_URL=${VIGILO_CONF_URL:-}
      - VIGILO_WEBAPP_URL=${VIGILO_WEBAPP_URL:-}
      # Install code of the setup assistant chosen by the host (12+ letters or digits)
      # instead of the one written in caches/setup-code.php
      - VIGILO_SETUP_CODE=${VIGILO_SETUP_CODE:-}
      # Reverse proxies in front of the container (networks separated by commas, e.g.
      # 172.16.0.0/12): client IP taken from X-Forwarded-For (anti-spam, login throttling)
      - VIGILO_TRUSTED_PROXIES=${VIGILO_TRUSTED_PROXIES:-}
    labels:
      # Only this container is updated by Watchtower
      - com.centurylinklabs.watchtower.enable=true

  # Updates the "web" image when asked from the admin (HTTP API, not published on the
  # host), never on its own. Only the containers labelled
  # com.centurylinklabs.watchtower.enable=true are touched.
  # nickfedor/watchtower is the maintained fork of containrrr/watchtower (archived): the
  # latter speaks the Docker API 1.25, refused by Docker Engine 29 and later.
  watchtower:
    image: ${WATCHTOWER_IMAGE:-nickfedor/watchtower:1}
    restart: always
    command: --http-api-update --label-enable --cleanup
    environment:
      - WATCHTOWER_HTTP_API_TOKEN=${WATCHTOWER_TOKEN:?WATCHTOWER_TOKEN must be set in .env (e.g. openssl rand -hex 32)}
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock

  # Optional: blur server (blur-server/), masks the faces and licence plates of every
  # photo sent to the backend. Enable with: docker compose --profile blur up -d
  blur:
    image: ${VIGILO_BLUR_IMAGE:-ghcr.io/jesuisundesdeux/vigilo-blur:0.0}
    profiles: ["blur"]
    restart: always
    environment:
      # Photos processed at the same time (CPU and memory)
      - BLUR_WORKERS=${BLUR_WORKERS:-2}
```

#### Démarrage

```
$ docker compose up -d
```

La base est créée au premier démarrage. Le service `watchtower` démarre aussi : il permet de mettre à jour l'image
depuis le menu **Mises à jour** de l'administration (bouton **Mettre à jour l'image avec Watchtower**). Il n'agit que
sur le conteneur `web`, seulement à la demande, et son API n'est pas exposée sur le serveur. Pour vous en passer,
retirez le service `watchtower` du fichier ; les mises à jour se font alors avec
`docker compose pull && docker compose up -d` ([détails](/fr/documentation/upgrade/#docker)).

### Option : serveur de floutage

Masque automatiquement visages et plaques d'immatriculation sur les photos reçues. Décommenter
`VIGILO_BLUR_URL=http://blur:8000/blur` dans `.env` et démarrer avec `docker compose --profile blur up -d`
([documentation](https://github.com/jesuisundesdeux/vigilo-backend/blob/master/blur-server/README.md)).

### Initialisation

Dès que le service est démarré, ouvrir `https://<votre domaine>/admin/` : l'assistant d'installation demande le code
d'installation affiché par `docker compose logs web`, puis crée le compte administrateur. La suite est décrite dans
l'[étape d'initialisation](/fr/documentation/installation/initialisation/).
