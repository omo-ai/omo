

Omo is an open-source, AI-native enterprise search platform that allows you connect and chat with data sources such as Google Drive, Notion, Confluece, and more.
Our goal is to build an LLM and vector store agnostic generative AI search platform that can power search and Q&A use cases such as

* Internal workplace search
* In-app search or Q&A
* External, customer-facing Q&A

Omo is licensed under Apache 2.0.

A fully-managed, hosted version is available [here](https://helloomo.ai).

## Design goals

1. API-first: support many different clients
2. Declarative pipelines: flexibility to define and configure indexing and retrieval pipelines steps.
3. LLM agnostic: plug-in an LLM of your choice
4. Vector store agnostic: plug-in a vector store of your choice
5. Cloud-agnostic: Run a self-hosted instance in your cloud
6. Ensure data is secure and provie ability to host on-prem.


## Features / Roadmap

| Feature | Description | Supported | Roadmap | Notes |
| --- | --- | --- | --- | --- |
| Chat UI | Turn-based chat UI | ✅ ||| 
| Chat history | Track recent chat history | ✅ || History length is configurable |
| Slack client | Search via Slack app | ✅ |||
| Dark mode | Toggle between dark and light themes | ✅ |||
| Source citations | Answer returns a list of documents searched | ✅ |||
| LLM agnostic | Support GPT, LLama 3, Claude, or Gemini. | ✅ |  | Configured via env variable |
| Embedding model agnostic | Use an embedding model of your choice |✅| | Configured via env variable |
| Kubernetes / containers | Run on container infrastructure |✅|| AWS EKS supported |
| Multi-tenancy | Single deployment supports many users | ✅ |||
| Vector store agnostic | Use a vector store of your choice || ✅ | Only Pinecone is supported at the moment |
| Declarative pipelines | Define your pipeline steps in YAML ||✅||
| Agents, tools, function calling | Low-code UI to create agents || ✅ ||
| Hybrid search | Return ranked list of links in addition to gen AI answer ||✅||
| Search contexts | Search personal and org wide Connectors ||✅||
| Multi-modal support | Voice and image support ||✅||

For items on the roadmap, please visit our Issues tab

## Connectors

The data sources that you can connect are known as Connectors. Supported Connectors include

| Connector | Supported | Roadmap | Notes |
| --- | --- | --- | --- |
| Google Drive |✅ |
| Notion |✅ |
| Confluence | |✅|
| Airtable ||✅ 
| OneDrive ||✅
| Slack ||✅

All connectors are self-service configured via a UI. We'd like to support the 
widest catalog of Connectors. If you'd like to contribute a connector,
please read our Contribution Guide, or if you need a custom connector
please contact us.


# Running locally

## Configure the environment variables

All environment variables are stored in the `envs/` directory. 
After cloning the repo, copy the environment variables templates:

```
# cp envs/env.template envs/.env.development
# cp envs/example/env.template envs/example/.env
```

Open `envs/.env.development` and add values for the environment variables.
Please note that Omo was originally developed with OpenAI's chat and embedding
models and Pinecone as the vector store.

You can use "namespaced" environment variables by placing them in the `envs` directory.
For example, `envs/example/.env` will be loaded
alongside `.env.development`. You can create arbitrary folders under `envs/`
and pass these into the `docker compose` via `ENV_NS` variable.
See more  in the `Starting the API` section.

## Generate an encryption key

Some columns in the database are encrypted. Generate an encryption key
and set the `ENCRYPTION_KEY` environment variable with this value. Don't lose 
this key or commit to a repo. Doing so will mean you can no longer
decrypt values, and if anyone else gains access to it they can decrypt values.

Note: There are utilities to use a secrets manager as well if you choose.

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

## Starting the UI and API

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

## Deploying the Docker image
```
kubectl rollout restart deployment omo-api
kubectl rollout restart deployment omo-celery
kubectl rollout restart deployment omo-celerybeat
```