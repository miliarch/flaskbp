# FlaskBP - Flask Boilerplate

## Build container images

```
cd /project-dir
docker-compose build
```

## Run containers

```
docker stack deploy -c docker-compose.test.yml flaskbp
```

## Check health state

```
docker stack ps flaskbp
<identify guid>
docker inspect --format='{{json .State.Health}}' <guid>
```
