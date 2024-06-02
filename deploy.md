```sh
docker-compose up -d --build --no-deps
```

```sh
docker-compose stop
```


1 день

```sh
docker-compose -f ./welcome-task/task/docker-compose.yml up -d --build --no-deps
docker-compose -f ./pickle-rce/task/docker-compose.yml up -d --build --no-deps
docker-compose -f ./off-by-slash/task/docker-compose.yml up -d --build --no-deps
```

2 день 

```sh
docker-compose -f ./welcome-task/task/docker-compose.yml up -d --build --no-deps
docker-compose -f ./pickle-rce/task/docker-compose.yml up -d --build --no-deps
docker-compose -f ./off-by-slash/task/docker-compose.yml up -d --build --no-deps
```

3 день 

```sh
docker-compose -f ./ssti/task/docker-compose.yml up -d --build --no-deps
docker-compose -f ./proxy/task/docker-compose.yml up -d --build --no-deps
```

4 день

```sh
docker-compose -f ./xxe/task/docker-compose.yml up -d --build --no-deps
docker-compose -f ./jwt-none/task/docker-compose.yml up -d --build --no-deps
```
