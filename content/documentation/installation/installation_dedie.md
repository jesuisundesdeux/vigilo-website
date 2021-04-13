---
title: Installation sur serveur dédié avec Docker
weight: 1
---

## Installation Vigilo sur serveur dédié avec Docker

### Pré-requis

#### Logiciel

* OS Linux
* Docker
* Docker-compose
* Un reverse-proxy comme Nginx afin de géré la couche SSL et l'accès public à Vigilo

#### Connaissances

* OS Linux / PHP / MySQL / Docker 

### Mise en place

A charge à l'administrateur d'installer le necessaire en amont pour permettre la mise en place d'un certificat SSL (LetsEncrypt).

Cloner le repo git complet en adaptant la version en remplacant X.X.X par le dernier tag existant (voir https://github.com/jesuisundesdeux/vigilo-backend/tags)

```
$ git clone https://github.com/jesuisundesdeux/vigilo-backend.git
$ git checkout vX.X.X
```

Copier le .env_sample vers .env_prod

```
$ cp .env_sample .env_prod
```

Adapter les valeurs dans ```.env_prod``` :

* VOLUME_PATH : Repertoire persistent sur le serveur où seront stockées les données de Vigilo
* MYSQL_ROOT_PASSWORD : Mot de passe root de la base de données
* MYSQL_PASSWORD : Mot de passe du compte vigilo de la base de données
* BIND : Adresse d'écoute HOST:PORT permettant d'accéder au conteneur à partir d'un reverse proxy sur l'hote ou à partir d'un autre container.

Adapter si besoin ce fichier au contexte du serveur sur lequel il est hebergé.

Lancer le service :

```
$ make ENV=prod install
```

### Initialisation 

Dés que la partie serveur est installée, il est impératif de passer à l'étape d'initialisation : [Procédure Ici](/fr/documentation/installation/initialisation/)

