# ds-deployment

For the tutorial to work, you first need to bring up the environment using Docker Compose.

```shell
docker-compose -f ./deployment/docker-compose.testing.yaml up -d
```

Once the environment is up and running, we recommend following the notebooks in `./src` for the PULL case and the PUSH case against the Fiware Context Broker.