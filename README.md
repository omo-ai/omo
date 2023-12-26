## Starting the API

```
APP_ENV=development docker compose --env-file omo_api/conf/envs/{CUSTOMER_KEY}.env.local up
```


## Building the Docker images


```
aws ecr get-login-password --region us-west-2 | docker login --username AWS --password-stdin 187613313731.dkr.ecr.us-west-2.amazonaws.com

cd omo/omo_api

docker build -t omo_api -f Dockerfile.local --platform linux/amd64 . && \
docker tag omo_api:latest 187613313731.dkr.ecr.us-west-2.amazonaws.com/omo_api:latest-amd64 && \
docker push 187613313731.dkr.ecr.us-west-2.amazonaws.com/omo_api:latest-amd64
```

## Deploying the Docker image
```
kubectl rollout restart deployment omo-api
```

## Troubleshooting
