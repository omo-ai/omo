# Omo - open-source, AI-native enterprise search

Omo is an open-source, AI-native enterprise search platform that allows you connect and chat with data sources such as Google Drive, Notion, Confluece, and more.
Each data source is known as a Connector.

## Running locally

### Configure the environment variables

After cloning the repo, cpoy the environment variables templates:

```
# cp envs/env.template envs/.env.development
# cp envs/example/env.template envs/example/.env
```

Open `envs/.env.development` and add values for the environment variables.

You can use "namespaced" environment variables by placing them in the `envs` directory.
For example, `envs/example/.env` will be loaded
alongside `.env.development`. You can create arbitrary folders under `envs/`
and pass these into the `docker compose` via `ENV_NS` variable.
See more  in the `Starting the API` section.

### Generate an encryption key

Some columns in the database are encrypted since they may store secrets / API keys for data sources. Generate an encryption key
and set the `ENCRYPTION_KEY` environment variable with this value. Don't lose this key or commit to a repo. Doing so will mean you can no longer decrypt values, and if anyone else gains access to it they can decrypt values.

To generate a key, on *nix machines:
```
$ dd if=/dev/urandom bs=32 count=1 2>/dev/null | openssl base64
RMRl4APj5uD4wmlrHAhFUoEp4D1GSiHjQiBDTrPY3CI=
```
Once the key is generated, set this value in `.env.development`:

```
ENCRYPTION_KEY=RMRl4APj5uD4wmlrHAhFUoEp4D1GSiHjQiBDTrPY3CI=
```
Don't use the encryption key above. It's an example.

### Starting the API

Use docker compose to start the environment locally:

`ENV=dev ENV_NS=example docker compose up`

The `ENV_NS` is an optional variable. If specified, it shoudld reference a folder name under `envs/`. For example, `ENV_NS=example` will include additional environment variabes under `envs/example/.env` in addition to `.env.development` in the project root. It's helpful if you want to test different values of environment variables without constantly
changing the value. For example, if you want to test different values for 2 teams, you can create `envs/team_1/.env` and `envs/team_2/.env`, then set `ENV_NS=team_1` or `ENV_NS=team_2`, when running `docker compose`.

You can check the `env_file` attribute in `docker-compose.yaml` to see how `ENV_NS` is used. 


# Building the Docker images


```
aws ecr get-login-password --region us-west-2 | docker login --username AWS --password-stdin 187613313731.dkr.ecr.us-west-2.amazonaws.com

cd omo/omo_api

docker build -t omo_api:v0.2.0 -f Dockerfile.local --platform linux/amd64 . && \
docker tag omo_api:v0.2.0 187613313731.dkr.ecr.us-west-2.amazonaws.com/omo_api:v0.2.0-amd64 && \
docker push 187613313731.dkr.ecr.us-west-2.amazonaws.com/omo_api:v0.2.0-amd64
```

# Deploying the Docker image
```
kubectl rollout restart deployment omo-api
kubectl rollout restart deployment omo-celery
kubectl rollout restart deployment omo-celerybeat
```

# Troubleshooting

Open Issue: https://github.com/slackapi/bolt-python/issues/1006

## How to add a new Connector