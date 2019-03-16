# Flask Boilerplate (flaskbp)

A boilerplate [Flask](http://flask.pocoo.org/) application designed for use with [Docker Swarm](https://docs.docker.com/engine/swarm/).

## Features

* Development environment docker-compose.yml file allowing for quick setup
* Basic user authentication system
* Common object models for database interactions
* Example views and templates to demonstrate common use cases

## Prerequisites

### Python

Setup scripts are written in Python and require Python version 3.4 at minimum - the pathlib module was released in version 3.4 and is used extensively. All modules used in setup scripts are provided by the Python standard library. 

### Docker

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

## Dev stack setup and usage

### Clone this repository:

```
$ git clone https://github.com/miliarch/flaskbp.git myproject
Cloning into 'myproject'...
```

Note: Cloning to a project path with a different name than `flaskbp` isn't required, but is supported in the rename portion of the `app_setup_dev.py` script.

### Change directory to the project root:

```
$ cd myproject/
```

### Run the `app_setup_dev.py` script:

```
$ ./app_setup_dev.py
Renaming /tmp/myproject/flaskbp to /tmp/myproject/myproject

Replacing references to flaskbp in files:
  - /tmp/myproject/run_app.py
  - /tmp/myproject/myproject/__init__.py
  - /tmp/myproject/myproject/init_test_db.py
  - /tmp/myproject/myproject/views.py
  - /tmp/myproject/myproject/models.py
  - /tmp/myproject/containers/app/healthcheck.py
  - /tmp/myproject/containers/app/Dockerfile
  - /tmp/myproject/containers/app/requirements.txt
  - /tmp/myproject/containers/db/Dockerfile
  - /tmp/myproject/docker-compose.yml.dev.example

Copying config example files:
  + /tmp/myproject/docker-compose.yml.dev.example -> /tmp/myproject/docker-compose.yml
  + /tmp/myproject/config.py.example -> /tmp/myproject/config.py

Creating default directories:
  + /tmp/myproject/data created
  + /tmp/myproject/logs created

DONE
```

As shown in the output above, this script renames the nested `flaskbp` directory to match the parent project directory name, replaces references to `flaskbp` in project files, copies example configuration files to the correct location, and creates required directories for the development environment

### Build the container images:

```
$ docker-compose build
```

### Start the stack:

```
$ docker stack deploy -c docker-compose.yml <stackname>
```

Note: Replace `<stackname>` with whatever name you'd like the stack to have. You'll need to use this name to control the stack later on, so it should mean something to you. 

### Wait for the stack to stabilize

Once started, stack containers will start and abort repeatedly until health checks pass. It generally takes around 2 minutes for the dev stack to reach a healthy state. Skip to the *Checking stack status/health* section for more info on viewing stack status and diagnosing issues.

### Connect to the application and start programming

Default development configuration shares the project directory with the app container, and runs the built-in Flask web server in debug mode. This allows for on-the-fly changes to project files, which will automatically prompt restart of the web server. This reduces time to test changes during development, as the app container doesn't need to be rebuilt and redeployed after each change.

You can connect to the application by visiting [http://localhost:5000](http://localhost:5000) in your web browser.

### Stop the stack

Run the following command when you're ready to stop the stack and purge containers:

```
$ docker stack rm <stackname>
```

## Checking stack status/health

Keep an eye out for deployment problems with `docker stack ps <stackname>`. A stable running deployment should look something like this:

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

NOTE: It's normal for the `<projectname>_app` container to fail multiple times before `<projectname>_db` enters a healthy running state, and stabilize after.

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

The goal of this project is to provide a functional, database connected, Flask web application that is simple to deploy and ready for new development. This project is very much a work in progress, and subject to change without notice.
