# tapway-assessment

Main objective: Setup a multi-container service that receives and validate a JSON payload via POST request, and append the transformed data into a CSV file through a RabbitMQ Queue. 

## Requirements
[Docker](https://docs.docker.com/engine/install/) and [Docker Compose V2](https://docs.docker.com/compose/install/) is needed to run this repo. Please install them and run the following two commands to ensure they are installed
```bash
docker --version
docker compose version
```
This repo is successfully run on 
```bash
Docker version 23
Docker Compose version v2
```

## Project Structure
```cmd
|-- README.md
|-- docker-compose.yml
|-- docker_version.txt
|-- consumer_data*
    |-- data.csv
|-- rabbitmq_data*
    ...
|-- src
    |-- producer
        |-- Dockerfile
        |-- requirements.txt
        |-- producer.py
        |-- utils
            |-- __init__.py
            |-- custom_validator.py
            |-- schema.json
    |-- consumer
        |-- Dockerfile
        |-- requirements.txt
        |-- consumer.py    
|-- test
    |-- Dockerfile
    |-- requirements.txt
    |-- run_test.py

(*) Persistent volume from docker containers. Auto-created after first build

```


## How to use
At the project directory, run the following to create and run images as a service of 3 separate containers:
```bash
docker compose up -d
```
Wait for the containers to finish initiated (terminal shows that all 3 containers are *Started* or *Healthy*)
```bash
[+] Running 3/3
 ✔ Container tapway-assessment-rabbitmq-1  Healthy
 ✔ Container tapway-assessment-producer-1  Started 
 ✔ Container tapway-assessment-consumer-1  Started
 ```
`-d` is detached mode. Running in detached mode so that user will not accidentally kill the service. Now, user may send POST request to `http://localhost:5000/` with JSON body

To stop the service, run:
```bash
docker compose stop
```

To start the service again, run:
```bash
docker compose start
```

To stop and destroy the containers, run:
```bash
docker compose down
```

## Logging
In detached mode, logs of each container will not be printed out on the terminal. However, they can be accessed with command:
```bash
docker logs <container_name>
```
To see the names of running containers, run:
```bash
docker ps
```
To list out all containers (even stopped containers), run:
```bash
docker ps -a
```

## Documentation
The 3 separate containers are:
- **producer** (simple python Flask app that accepts data as JSON body with POST endpoint `http://localhost:5000/`)
- **rabbitmq** (official RabbitMQ image)
- **consumer** (plain python script)

The **producer** receives JSON body and will validate the data with the following JSON schema and sends the data to the message broker (**rabbitmq**)
```cmd
{
  "device_id": str,
  "client_id": str,
  "created_at": str, # timestamp, e.g. '2023-02-07 14:56:49.386042'
  "data": {
  "license_id": str,
  "preds": [
      {
        "image_frame": str, # base64 string
        "prob": float,
        "tags": str[]
      },
      ...
    ]
  }
}
```

The **consumer** receives the message from **rabbitmq**, transforms and append to a CSV file (at `consumer_data/data.csv`)

## Test script
To test the service, change directory to `./test`. The test script `run_test.py` will send 1000 requests, with randomly generated JSON payload with 3 predictions. The CSV file (`consumer_data/data.csv`) should have 3000 new entries upon completion of the test script.

There are two alternatives to run the test script:
1. With docker engine installed, just run the following command:
```bash
docker run -it --rm --network tapway-assessment_rabbitmq_network $(docker build -q .) python run_test.py
```
Note: the `--network` value follows the format `{project_directory_name}_rabbitmq_network`. If the project directory's name is change, please edit the command as well. One can check the list of networks with the command:
```bash 
docker network ls
```

2. The host Operating System has a working Python 3 interpreter installed. At the `./test` directory, run:
```bash
pip install -r requirements.txt
```

```bash
python run_test.py
```


