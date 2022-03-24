# P13_FOSTER_Harris

## Résumé

Site web d'Orange County Lettings.

Orange County Lettings est un service de location immobilière.

## Développement local

### Prérequis de base

- Une application de type 'terminal' - GitBash, Mintty, Cygwin (si vous êtes sur Windows) 
   ou les terminaux par défaut si vous utilisez Macintosh ou Linux. 
- Compte GitHub
- Git CLI
- Interpréteur Python, version 3.9 ou supérieure

Dans le reste de la documentation sur le développement local, il est supposé que la commande `python` de votre OS shell exécute l'interpréteur Python ci-dessus (à moins qu'un environnement virtuel ne soit activé).

### Installation
#### Pour les développeurs et utilisateurs (windows 10/11, mac, linux) :
##### Clonez la source de orange_county_lettings localement (en utilisant votre terminal) :
```sh
$ git clone https://github.com/harrisafoster/P13_FOSTER_Harris.git
$ cd P13_FOSTER_Harris
```
##### Dans votre terminal dans le dossier P13_FOSTER_Harris/ : Créer et activer un environnement virtuel avec (windows 10) :
```sh
$ python -m venv env
$ source ./env/Scripts/activate
```
##### Créer et activer un environnement virtuel avec (mac & linux) :
```sh
$ virtualenv venv
$ source venv/bin/activate
```
##### Installez les packages requis avec :
```sh
$ pip install -r requirements.txt
```
#### Installez le db de base avec :
Toujours dans P13_FOSTER_Harris, allez télécharger la base de données initiale 
[ici](https://github.com/OpenClassrooms-Student-Center/Python-OC-Lettings-FR/raw/master/oc-lettings-site.sqlite3)
et placez-la à la racine du projet.

#### Faites les migrations nécessaires avec :

```sh
$ python manage.py migrate
```

#### Générez votre propre secret_key et renseignez vos propres variables d'environnement :
Vous allez remarquer que vous n'avez pas de fichier .env et c'est normal. Cette étape permet de
protéger des données sensibles de l'application. Pour créer, renseigner et utiliser votre nouvelle clé secrète veuillez suivre les 
étapes ci-dessous. Vous allez suivre un processus similaire pour renseigner tous les variables d'environnement locaux :
```sh
$ touch .env
$ python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

### _**Variables d'environnement pour le développement local**_
Veuillez renseigner votre nouvelle clé secrète et les variables ci-dessous aussi dans votre fichier .env
```sh
secret_key=votre_nouvelle_cle
DEBUG=False
PORT=8000
LOCAL_DEV=True

DATABASE_URL=url_de_votre_db_postgre_heroku ('vous pouvez laisser cette valeur vide pour le développement local')

HEROKU_APP_NAME=nom_de_votre_application_heroku ('vous pouvez laisser cette valeur vide pour le développement local')

SENTRY_URL_KEY=url_secret_de_votre_SENTRY ('vous pouvez laisser cette valeur vide pour le développement local')
```

Après avoir fait cela, l'import de vos variables d'environnement fonctionneront au niveau local

#### Linting

Depuis la racine du projet, exécutez la commande ci-dessous
```sh
$ flake8
```

#### Tests

Depuis la racine du projet, exécutez la commande ci-dessous
```sh
$ pytest
```

#### Faire tourner votre application en local avec :

```sh
$ python manage.py runserver
```

#### Panel d'administration

- Aller sur `http://127.0.0.1:8000/admin`
- Connectez-vous avec l'utilisateur `admin`, mot de passe `Abc1234!`


## Tests et déploiement via CircleCI et Heroku

- Lors d'un 'push' sur la branche master, CircleCI récupère le code pour lancer les tests et le linting (peluchage) du code.
- Si cette action est satisfaite, il exécute une dockerisation de l'application et envoie l'image sur DockerHub.
- Si l'action précédente a réussi, il déploie l'application sur Heroku.

Le Pipeline du projet est disponible sur CircleCI en public en [cliquant ici](https://app.circleci.com/pipelines/github/harrisafoster/P13_FOSTER_Harris?filter=all).

### Prérequis

- Compte CircleCI que vous pouvez créer [ici](https://circleci.com/signup/)
- Compte DockerHub que vous pouvez créer [ici](https://hub.docker.com/)
- Compte Heroku que vous pouvez créer [ici](https://signup.heroku.com/)
- Installer HerokuCLI [ici](https://devcenter.heroku.com/articles/getting-started-with-python#set-up)

### Installation

1. Créer un projet CircleCI et le lier à votre repository GitHub (à faire en ligne avec votre compte CircleCI)
2. Créer un projet DockerHub (à faire en ligne avec votre compte DockerHub)
3. Créer un projet Heroku (à faire en ligne avec votre compte Heroku)
#### Etapes ci-dessous expliquées en détail plus bas
4. Obtenir un token d'authentification Heroku 
5. Créer et migrer votre base de données Postgres Heroku 
6. Renseigner les variables d'environnement du déploiement

#### Etape 4: Obtenir un token d'authentification Heroku

```sh
$ heroku.cmd login
$ heroku.cmd authorizations:create
```
Notez ce token, vous allez en avoir besoin pour le déploiement

#### Etape 5: Créer et migrer votre base de données Postgres Heroku
Le déploiement de Heroku nécessite une base de données PostgreSQL (qui sera utilisé pour la version déployée, mais pas la version locale)

- Tout d'abord, créez un backup de vos données locales avec `python manage.py dumpdata > backup.json`
- Changez votre valeur LOCAL_DEV dans votre fichier .env à `LOCAL_DEV=False`
- Connectez-vous à votre compte heroku avec `$ heroku.cmd login`
- Créez votre base de données postgreSQL heroku avec : `$ heroku.cmd addons:create heroku-postgresql:hobby-dev`
- Ou en suivant les instructions en ligne sur votre projet heroku (Resources => Heroku Postgres => Add => Hobby Dev - Free => submit order form)
- Une fois que votre base de données est créée cherchez son URL unique sure heroku.com (votre_projet => installed addons => votre_db => settings => database credentials => view credentials => URI)
- Changez la valeur de DATABASE_URL dans votre fichier .env à `DATABASE_URL=votre_URI_unique_de_base_de_données`
- Ensuite, il suffit de faire (dans l'ordre, dans votre terminal) 
  - `$ python manage.py migrate` 
  - `$ python manage.py shell` 
  - `>>> from django.contrib.contenttypes.models import ContentType`
  - `>>> ContentType.objects.all().delete()`
  - `$ python manage.py loaddata backup.json`
- Après ces étapes, votre base de données sur heroku postgres sera opérationnelle

#### Etape 6: Variables d'environnement du déploiement : 

##### Au niveau local, mettez ces valeurs dans votre fichier .env
```sh
secret_key=votre_cle_secrète
DEBUG=True
PORT=8000
LOCAL_DEV=True

DATABASE_URL=url_de_votre_db_postgre_heroku (url_unique_de_votre_db_heroku_postgres)

HEROKU_APP_NAME=nom_de_votre_application_heroku (nom_unique_de_votre_application ex. oc-lettings-15)

SENTRY_URL_KEY=url_secret_de_votre_SENTRY (toujours vide pour le moment, ajouter plus tard)
```
---------------
##### Au niveau du CircleCi, mettez ces valeurs dans les variables d'environnement du projet CircleCi

(Project Settings => Environment variables => Add Environment Variable)
```sh
secret_key=votre_cle_secrète
DEBUG=False
PORT=8000
LOCAL_DEV=False

HEROKU_APP_NAME=nom_de_votre_application_heroku (nom_unique_de_votre_application ex. oc-lettings-15)
HEROKU_TOKEN=votre_token_authorization
DOCKER_USER=votre_nom_utilisateur_de_docker
DOCKER_PASSWORD=votre_mot_de_passe_docker
```


### Utilisation

- Si l'installation est respectée, l'exécution du pipeline se lancera à chaque nouveau push sur GitHub.
- Les tests et le linting du code se feront à chaque push dans n'importe quelle branche contenant la configuration CircleCI.
- La dockerization sur DockerHub et le déploiement sur Heroku s'exécuteront à chaque push dans la branche master.
- Après le déploiement le site est accéssible à l'adresse: [oc-lettings-15.herokuapp.com](https://oc-lettings-15.herokuapp.com/)

## Exécution du docker en local

### Prérequis

- Compte [DockerHub](https://hub.docker.com/)
- Installer [Docker Desktop](https://www.docker.com/products/docker-desktop)
- Pipeline du dernier commit réussi.

### Utilisation

1. Depuis une image créée localement : 
```sh
$ docker login
$ docker compose up
```
Accédez au site avec sur votre port 8000, ex. http://127.0.0.1:8000/

La commande `$ docker compose up` fonctionne parce que le fichier docker-compose.yml contient des instructions pour faire tourner l'application en local via docker.

2. Depuis une image récupérée du répositoire en ligne : 
```sh
$ docker login
$ docker run -p 8000:8000 --env-file .env docker_user/docker_repository:latest_tag
```
Accédez au site avec sur votre port 8000, ex. http://127.0.0.1:8000/

A savoir qu'il faut utiliser votre nom d'utilisateur de docker, votre nom du répo docker, ainsi que le tag de votre dernière image qui a été mis sur docker
## Sentry

Sentry est une application de suivi d'erreurs non gérées.

### Prérequis

- Compte [Sentry](https://sentry.io/signup/)

### Utilisation

- Créer un projet Sentry
- Sur le site sentry.io trouvez votre SENTRY_URL unique via :
- settings => projects => votre_projet => Client Keys (DSN) => copier le DSN
- Maintenant vous pouvez changer votre variable d'environnement (local .env et sur CircleCI) à `SENTRY_URL_KEY=votre_DSN`
