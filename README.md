

Omo is an open-source, AI-native enterprise search platform that allows you connect and chat with data sources such as Google Drive, Notion, Confluece, and more.
Our goal is to build an LLM and vector store agnostic generative AI search platform that can power search and Q&A use cases such as

* Internal workplace search
* In-app search or Q&A
* External, customer-facing Q&A

Omo is licensed under Apache 2.0.

A fully-managed, hosted version is available [here](https://helloomo.ai).

Docs: [https://docs.helloomo.ai](https://docs.helloomo.ai)

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
please read our [contribution guidelines](CONTRIBUTING.md), or if you need a custom connector
please contact us.