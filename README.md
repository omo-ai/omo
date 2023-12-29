## Starting the API

`APP_ENV=development CUSTOMER_ENV=some_customer_key docker compose up`

will include the customer-specific environment variabes under `./omo_api/conf/envs/some_customer_key/.env`


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

Open Issue: https://github.com/slackapi/bolt-python/issues/1006

## Pinecone Limitations

Does not support `score_threshold`: https://github.com/langchain-ai/langchain/discussions/4669