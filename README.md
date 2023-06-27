# Technical Test - GeoKapti

In this test, a microservices application was developed to solve a delivery route planning problem.


## Problem Description
The objective of the test is to develop two microservices as a REST API for a delivery route planning company. The required microservices are as follows:

1. Register a location: Accept the name, latitude, and longitude of a location and return a unique ID for that location.

2. Receive a list of location IDs and calculate the total distance of the route.

The second microservice is implemented as a wrapper for a process that communicates via publish/subscribe queues. It subscribes to an inbound queue to receive the list of location IDs and publishes the solution to the problem in the outbound queue.

Python and the FastAPI framework were used for the API development, along with Docker for containerization, and RabbitMQ as the message broker.

## Technologies Used

- Python: The main programming language used to develop the application.
- FastAPI: A web framework used to create the REST API.
- Docker: A platform used to containerize the application and its dependencies.
- RabbitMQ: A message broker used for communication between microservices.

## Project Structure

```
+ app/
  + api/
    - celery.py
    - dependecies.py
    - main.py
    + routers/
      - calculate_distance.py
      - calculate_distance_haversine.py
      - create_location.py
      - delete_location.py
      - get_task_status.py
      - read_location.py
      - read_locations.py
      - register_user.py
      - token.py
      - update_location.py
    + schemas/
      - location.py
      - user.py
  + infrastructure/
    - database.py
  + tests/
- Dockerfile
- docker-compose.yml
- requirements.txt
```

## Running the Application
Follow these steps to run the application:

1. Make sure you have Docker and Docker Compose installed on your system.

2. Clone this repository to your local machine.

3. Navigate to the project's root directory.

4. Run the following command to build the Docker images and start the services:
```
docker-compose up --build
```
5. Once the services are up and running, you can access the API at
http://localhost:8000

6. You can see and use openapi autodocumentation tool or any API client to perform the following operations:

![OpenAPi Autodocumentation](endpoints.PNG)