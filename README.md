# Quick start

## Configure the environment variables

`cp envs/env.template envs/.env.development`

Open `envs/.env.development` and add values for the environment variables.

### Adding namespaced environment variables

More environment variables can be added in a subfolder under `envs`:

```
mkdir envs/some_env_vars
touch envs/some_env_vars/.env
```

These can be passed in when starting the API. See the next section for more info.

## Starting the API

Use docker compose to start the environment locally:

`APP_ENV=development ENV_NS=some_env_vars docker compose up`

The `ENV_NS` is optional and will include additional environment variabes under `envs/some_env_var/.env` in addition to `.env.development`.

The `ENV_NS` variable is helpful if you want to test different values of environment variables. For example, say you have two teams or customers you want to deploy to, each with their own specific env vars. You can create a

`envs/customer_1/.env` and `envs/customer_2/.env` with customer-specific environment variables to test with. It's more convenient than having a single
`.env` file that you repeatedly have to change the values for if you want to test different things.

You can check the `env_file` attribute in `docker-compose.yaml` to see how `ENV_NS` is used. 


## Building the Docker images


```
aws ecr get-login-password --region us-west-2 | docker login --username AWS --password-stdin 187613313731.dkr.ecr.us-west-2.amazonaws.com

cd omo/omo_api

docker build -t omo_api:v0.2.0 -f Dockerfile.local --platform linux/amd64 . && \
docker tag omo_api:v0.2.0 187613313731.dkr.ecr.us-west-2.amazonaws.com/omo_api:v0.2.0-amd64 && \
docker push 187613313731.dkr.ecr.us-west-2.amazonaws.com/omo_api:v0.2.0-amd64
```

## Deploying the Docker image
```
kubectl rollout restart deployment omo-api
kubectl rollout restart deployment omo-celery
kubectl rollout restart deployment omo-celerybeat
```

## Troubleshooting

Open Issue: https://github.com/slackapi/bolt-python/issues/1006

## How to add a new Connector