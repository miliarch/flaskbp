# FlaskBP - Flask Boilerplate

## Build container images

```
cd /project-dir
docker-compose build
```

## Run containers

First, make sure your docker host belongs to a swarm (you should know if it does). If it doesn't, run the following to initialize a swarm and set master node:

```
docker swarm init --advertise-addr <MANAGER-IP>
```

Second, deploy the application:

```
docker stack deploy -c docker-compose.yml flaskbp
```

Third, check container status until they are running/available:

```
docker stack ps flaskbp
```

Finally, attempt connection to the application (usually http://localhost:5000 in a development environment)

## Check health state

```
docker stack ps flaskbp
<identify guid>
docker inspect --format='{{json .State.Health}}' <guid>
```
