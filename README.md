# Flask Boilerplate (flaskbp)

A boilerplate [Flask](http://flask.pocoo.org/) application designed for use with [Docker Swarm](https://docs.docker.com/engine/swarm/).

## Features

* Development environment docker-compose.yml file allowing for quick setup
* Basic user authentication system
* Common object models for database interactions
* Example views and templates to demonstrate common use cases

## Prerequisites

[Docker Engine 18.02.0](https://github.com/docker/docker-ce/releases/tag/v18.02.0-ce-rc1) or later and [docker-compose 1.20.0](https://github.com/docker/compose/releases/tag/1.20.0-rc1) or later are required to successfully build and manage containers. Additionally, the deployment host must belong to a docker swarm.

Docker installation documentation can be found at the following links:
* [Install Docker](https://docs.docker.com/install/)
* [Install Docker Compose](https://docs.docker.com/compose/install/)

Depending on your operating system and installation method, Docker Engine may be capable of handling compose file format version 3.6, while docker-compose is not. You can verify installed versions of each dependency with the following commands:

```
$ docker --version
Docker version 18.09.3, build 774a1f4

$ docker-compose --version
docker-compose version 1.23.2, build 1110ad01
```

Once docker is installed and versions are verified, ensure the current host belongs to a swarm:

```
$ docker info|grep Swarm
Swarm: active
```

If output of this command is `Swarm: inactive`, you can either join the current host to an existing swarm, or initialize it as swarm master. You can initialize the current host as swarm master with:
```
$ docker swarm init
```

For more information on Docker Swarm, see [Swarm mode overview](https://docs.docker.com/engine/swarm/).

## Dev stack setup

First, clone this repository and ensure your current working directory is the project root path (the dir this README.md file exists in):

```
$ pwd
/flaskbp

$ ls README.md
README.md
```

Example app config and docker-compose files are available as `config.py.example` and `docker-compose.yml.dev.example`. Copy these files to establish a valid configuration:

```
$ cp docker-compose.yml.dev.example docker-compose.yml
$ cp config.py.example config.py
```

Ensure `data` and `logs` directories exist, as default configuration relies on them:

```
$ mkdir data
$ mkdir logs
```

At this point, you can build the container images:

```
$ docker-compose build
```

Once build completes, start the stack:

```
$ docker stack deploy -c docker-compose.yml flaskbp
```

Once started, stack containers will start and abort repeatedly until health checks pass. It generally takes around 2 minutes for the dev stack to reach a healthy state. More on checking status in the next section.

Run the following command when you're ready to stop the stack and purge containers:

```
$ docker stack rm flaskbp
```

## Checking stack status/health

Keep an eye out for deployment problems with `docker stack ps flaskbp`. A stable running deployment should look something like this:

```
$ docker stack ps flaskbp
ID                  NAME                IMAGE                NODE                    DESIRED STATE       CURRENT STATE         ERROR                       PORTS
yfagbelhguw3        flaskbp_app.1       flaskbp_app:latest   linuxkit-025000000001   Running             Running 3 hours ago
69hi1a8f74id         \_ flaskbp_app.1   flaskbp_app:latest   linuxkit-025000000001   Shutdown            Failed 3 hours ago    "task: non-zero exit (1)"
z2a8l4gpkyfw         \_ flaskbp_app.1   flaskbp_app:latest   linuxkit-025000000001   Shutdown            Failed 3 hours ago    "task: non-zero exit (1)"
lboum1j4l9ew         \_ flaskbp_app.1   flaskbp_app:latest   linuxkit-025000000001   Shutdown            Failed 3 hours ago    "task: non-zero exit (1)"
rz66ybqzw526        flaskbp_db.1        flaskbp_db:latest    linuxkit-025000000001   Running             Running 3 hours ago
zb4yesvswvvd        flaskbp_app.1       flaskbp_app:latest   linuxkit-025000000001   Shutdown            Failed 3 hours ago    "task: non-zero exit (1)"
```

NOTE: It's normal for `flaskbp_app` to fail multiple times before `flaskbp_db` enters a healthy running state, and stabilize after.

You can use `docker ps -a`, `docker inspect` and `docker logs` commands to learn more about container health status and the cause of any crashes:

```
$ docker ps -a
CONTAINER ID        IMAGE                COMMAND                  CREATED             STATUS                   PORTS               NAMES
a09871542362        flaskbp_app:latest   "python3 /opt/app/ru…"   3 hours ago         Up 3 hours (healthy)                         flaskbp_app.1.yfagbelhguw3hnefm9xq9eljo
796ead35ffc7        flaskbp_app:latest   "python3 /opt/app/ru…"   3 hours ago         Exited (1) 3 hours ago                       flaskbp_app.1.69hi1a8f74ido5oic9u8hzy87
a28f7f42b483        flaskbp_app:latest   "python3 /opt/app/ru…"   3 hours ago         Exited (1) 3 hours ago                       flaskbp_app.1.z2a8l4gpkyfw1zd7qsl88mj1j
341ff1b69113        flaskbp_app:latest   "python3 /opt/app/ru…"   3 hours ago         Exited (1) 3 hours ago                       flaskbp_app.1.lboum1j4l9ewi9akeo1pwbrvl
ebab9d128d6a        flaskbp_db:latest    "docker-entrypoint.s…"   3 hours ago         Up 3 hours (healthy)     3306/tcp            flaskbp_db.1.rz66ybqzw526yewbqm222fsby
5c7d7b2372cd        flaskbp_app:latest   "python3 /opt/app/ru…"   3 hours ago         Exited (1) 3 hours ago                       flaskbp_app.1.zb4yesvswvvdzlh6mjbbydcta

$ docker inspect --format='{{json .State.Health}}' a09871542362
{"Status":"healthy","FailingStreak":0,"Log":[{"Start":"2019-03-10T21:24:58.3038584Z","End":"2019-03-10T21:24:58.4610159Z","ExitCode":0,"Output":""},{"Start":"2019-03-10T21:25:28.4361019Z","End":"2019-03-10T21:25:28.5875475Z","ExitCode":0,"Output":""},{"Start":"2019-03-10T21:25:58.5592512Z","End":"2019-03-10T21:25:58.7135822Z","ExitCode":0,"Output":""},{"Start":"2019-03-10T21:26:28.6859535Z","End":"2019-03-10T21:26:28.8443406Z","ExitCode":0,"Output":""},{"Start":"2019-03-10T21:26:58.8209221Z","End":"2019-03-10T21:26:58.9737798Z","ExitCode":0,"Output":""}]}

$ docker logs 796ead35ffc7
[2019-03-10 18:13:04,893] INFO in __init__: flaskbp starting
[2019-03-10 18:13:04,956] INFO in __init__: DEBUG and RESET_DB values are True, refreshing DB
[2019-03-10 18:13:04,957] INFO in init_test_db: running refresh routine
[2019-03-10 18:13:04,958] INFO in init_test_db: destroying database
[2019-03-10 18:13:04,958] DEBUG in init_test_db: closing db_session connections
[2019-03-10 18:13:04,959] DEBUG in init_test_db: dropping all tables
[2019-03-10 18:13:05,007] ERROR in init_test_db: OperationalError: (pymysql.err.OperationalError) (2003, "Can't connect to MySQL server on 'db' ([Errno -2] Name or service not known)") (Background on this error at: http://sqlalche.me/e/e3q8)
```

## About

I've used Flask in dozens of personal web projects. I've found that each time I start a Flask project, I inevitably spend hours searching for and improving upon existing solutions across my project base before I can even think about developing anything new.

The goal of this project is to provide a functional, database connected, flask web application that's simple to deploy and ready for new development. This project is very much a work in progress, and subject to change without notice.
