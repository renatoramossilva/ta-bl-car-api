# Car Booking API

## Introduction

The Car Booking API is a FastAPI-based application designed to streamline the process of reserving vehicles from a fleet. The API provides endpoints for managing car availability and booking reservations efficiently. Users can perform the following key actions:

View the fleet of cars: Retrieve a list of all available vehicles in the system.
Check car availability: Verify if specific cars or car models are available for a given date range.
Create bookings: Reserve a car by providing booking details, including dates and times.
This application ensures a seamless reservation experience with proper validation, error handling, and easy-to-use endpoints, making it ideal for car rental businesses or fleet management.


## Table of Contents

- [Project Structure](#project-structure)
- [Requirements](#requirements)
- [Dependency Management with Poetry](#dependency-management-with-poetry)
- [Project setup](#project-setup)
- [API Documentation](api-documentation)
- [Testing the app](#testing)
- [Code Quality](#code-quality)
- [Unit tests](#unity-test)
- [Continuous Integration](#continuous-integration)


## Project Structure

- `/app`: Contains the main application files.
- `/tests`: Unit tests for the API.
- `/docker`: Docker configuration file.


## Requirements

Before you begin, ensure you have the following prerequisites installed on your machine:

- [Python 3.9](https://www.python.org/downloads/) or higher
- [Poetry](https://python-poetry.org/docs/#installation)
- [Docker](https://www.docker.com/get-started)


## Dependency Management with Poetry

This project uses [Poetry](https://python-poetry.org/) for dependency management. Poetry simplifies the process of managing dependencies and packaging Python projects.

Once installed, you can easily manage dependencies by running `poetry add <dependency>` to add the new dependency and `poetry install`, which installs all required packages listed in the [`pyproject.toml`](pyproject.toml)
 file.


## Project setup

Clone this repository to your local machine:

`git clone https://github.com/renatoramossilva/ta-bl-car-api.git`

Navigate to the project directory and install the dependencies using Poetry:

```bash
cd ta-bl-car-api
poetry install
```

To activate the virtual environment created by Poetry, run:

`poetry shell`

You can now run the application using Docker or directly using uvicorn.

To run with Docker, use:

```bash
docker build -f docker/Dockerfile -t my-fastapi-app .
docker run --rm -d -p 8000:8000 -p 5001:5001 my-fastapi-app
```

`docker run`: Runs a Docker container.
`--rm`: Automatically removes the container when it stops.
`-d`: Runs the container in detached mode (in the background).
`-p 8000:8000`: Maps port 8000 of the host to port 8000 of the container (for the app).
`-p 5001:5001`: Maps port 5001 of the host to port 5001 of the container (for the coverage report).
`my-fastapi-app`: The name of the Docker image to run.

Alternatively, to run the application directly, use:

`poetry run uvicorn app.main:app`

Check if the container is running and the application is on:

```bash
docker ps
CONTAINER ID   IMAGE            COMMAND                  CREATED         STATUS         PORTS                                            NAMES
78036af2a241   my-fastapi-app   "sh -c 'uvicorn app.…"   9 seconds ago   Up 9 seconds   0.0.0.0:5001->5001/tcp, 0.0.0.0:8000->8000/tcp   exciting_kilby
```


## API Documentation

The Car Booking API is documented using FastAPI's interactive Swagger UI, which provides a user-friendly interface for exploring and testing the API's endpoints.

The documentation is accessible at: http://localhost:8000/docs
This interface includes detailed information about each endpoint, the required input parameters, response formats, and example requests, allowing developers to understand and integrate with the API effectively.


## Testing

You can use `curl` command to test the endpoints:

# `/car/`

```bash
curl -X 'GET' 'http://127.0.0.1:8000/cars/' -H 'accept: application/json'

{"cars":[{"id":1,"name":"SEAT Ibiza"},{"id":2,"name":"Volkswagen Polo"},{"id":3,"name":"Renault Clio"},{"id":4,"name":"Peugeot 208"},{"id":5,"name":"Ford Fiesta"},{"id":6,"name":"Opel Corsa"},{"id":7,"name":"Citroën C3"},{"id":8,"name":"Toyota Yaris"},{"id":9,"name":"Dacia Sandero"},{"id":10,"name":"Kia Rio"}]}%
```

# `booking`

```bash
curl -X POST "http://127.0.0.1:8000/booking/" \
-H "Content-Type: application/json" \
-d '{
    "car_id": 3,
    "start_date": "2024-11-25",
    "end_date": "2024-11-30",
    "pickup_time": "09:00",
    "dropoff_time": "18:00"
}'
{"message":"Booking successfully created!"}%
```

# `check_car_availability` (Specific car - OK)

```bash
curl -X 'GET' 'http://127.0.0.1:8000/check_car_availability?start_date=2024-11-28&end_date=2024-11-29&car_model=Dacia%20Sandero' -H 'accept: application/json'

{"available_cars":[{"id":9,"name":"Dacia Sandero"}]}%
```

# `check_car_availability` (All cars - OK)

```bash
curl -X 'GET' 'http://127.0.0.1:8000/check_car_availability?start_date=2024-11-28&end_date=2024-11-29' -H 'accept: application/json'
{"available_cars":[{"id":1,"name":"SEAT Ibiza"},{"id":4,"name":"Peugeot 208"},{"id":5,"name":"Ford Fiesta"},{"id":7,"name":"Citroën C3"},{"id":9,"name":"Dacia Sandero"},{"id":10,"name":"Kia Rio"}]}%
```

# `check_car_availability` (NOK)

```bash
curl -X 'GET' 'http://127.0.0.1:8000/check_car_availability?start_date=2024-11-28&end_date=2024-11-29&car_model=Volkswagen%20Polo' -H 'accept: application/json'

{"detail":"No available cars found for the given dates and model."}%
```


## Code Quality

This project uses several tools to maintain code quality and enforce coding standards:

- **[black](https://black.readthedocs.io/)**: A code formatter that ensures consistent code style.
- **[pylint](https://pylint.pycqa.org/)**: A static code analysis tool to enforce coding standards and detect errors.
- **[isort](https://pycqa.github.io/isort/)**: A tool to sort and format imports automatically.
- **[mypy](http://mypy-lang.org/)**: A static type checker to ensure type safety in Python code.


## Unit tests

This project uses `pytest` for unit testing to ensure the functionality of key features like car bookings and availability checks.

# Running Tests

To run the unit tests locally:

`pytest` or `poetry run pytest`

#### Testing Across Python Versions
To verify compatibility with different versions of Python, the project is tested with Python 3.9, 3.10, 3.11, and 3.12. We use `tox` to automate testing across these Python versions.

`tox` or `poetry run tox`


## Continuous Integration

This project uses GitHub Actions to automate code quality checks and testing before merging into the master branch. The tools included in the workflow are described in [Code Quality](#code-quality) session.


## Workflow Overview
Whenever a pull request is opened, the GitHub Actions workflow will trigger and perform the following checks:

- Code Formatting: Run `black` and `isort` to format the code.
- Static Analysis: Execute `pylint` and `mypy` to ensure code quality.
- Unit Testing: Run `pytest` to execute the unit tests and check for coverage. (specifically 3.9, 3.10, 3.11, and 3.12)

This setup ensures that only code that passes all checks is merged into the master branch, maintaining a high standard of code quality throughout the development process.
