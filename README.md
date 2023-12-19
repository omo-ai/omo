## Starting the API

`APP_ENV=development docker-compose --env-file omo_api/conf/envs/.env.{CUSTOMER_KEY} up`



## Building the Docker images


```
cd omo/omo_api
docker build -t omo_api -f Dockerfile --platform linux/amd64 .
docker tag omo_api:latest 187613313731.dkr.ecr.us-west-2.amazonaws.com/omo_api:latest-amd64
docker push 187613313731.dkr.ecr.us-west-2.amazonaws.com/omo_api:latest-amd64
```

## Troubleshooting
