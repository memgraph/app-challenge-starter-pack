# Memgraph App Challenge - Starter Pack

<p align="center">
  <a href="https://www.linkedin.com/company/memgraph">
    <img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn"/>
  </a>
  <a href="https://memgr.ph/join-discord">
    <img src="https://img.shields.io/badge/Discord-7289DA?style=for-the-badge&logo=discord&logoColor=white" alt="Discord"/>
  </a>
  <a href="https://twitter.com/memgraphdb">
    <img src="https://img.shields.io/badge/Twitter-1DA1F2?style=for-the-badge&logo=twitter&logoColor=white" alt="Twitter"/>
  </a>
</p>

<p align="center">
  <img src="https://public-assets.memgraph.com/app-challenge-starter-pack/demo.png" width="600"/>
</p>

<p align="center">
  <a href="https://github.com/memgraph/memgraph-platform/LICENSE">
    <img src="https://img.shields.io/github/license/g-despot/app-challenge-starter-pack.svg" alt="license"/>
  </a>
</p>

## The application

A Python starter pack for building streaming applications with Memgraph.
The app consists of three components:
* **server**: A Flask Python server that loads the initial data into Memgraph and fetches the graph to visualize it.
* **stream**: A service that sends data to the Kafka cluster.
* **Memgraph**: The graph platform that receives data from Kafka.

If you want to build a graph application with streaming data and Kafka, check out the **[Example Streaming App](https://github.com/memgraph/example-streaming-app)**.

## Starting the app

You can start the app by running:
```
docker-compose build
docker compose up server
```

The `stream` service that sends data to Kafka can be started with:
```
docker compose up stream
```

## Documentation

If you need help with using Memgraph, here are few resources that could be of help:
* **[Getting started](https://docs.memgraph.com/memgraph/getting-started)**: Where to start with exploring Memgraph, from installation to querying.
* **[MAGE](https://docs.memgraph.com/mage)**: Running and implementing complex graph theory algorithms with ease.
* **[Cypher manual](https://docs.memgraph.com/cypher-manual/)**: Learn the Cypher query language for analyzing graph data.

## License

This is an open-source project and you are free to use it under the [MIT license](./LICENSE).
