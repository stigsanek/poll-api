# Poll API

![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/stigsanek/poll-api/pyci.yml?branch=main)
![Code Climate maintainability](https://img.shields.io/codeclimate/maintainability/stigsanek/poll-api)
![Code Climate coverage](https://img.shields.io/codeclimate/coverage/stigsanek/poll-api)

## Description

"Poll API" is voting API service.

## Usage

You can deploy the project locally or via Docker.

### 1. Locally

#### Python

Before installing the package, you need to make sure that you have Python version 3.8 or higher installed.

```bash
>> python --version
Python 3.8.0+
```

If you don't have Python installed, you can download and install it
from [the official Python website](https://www.python.org/downloads/).

#### Poetry

The project uses the Poetry manager. Poetry is a tool for dependency management and packaging in Python. It allows you
to declare the libraries your project depends on and it will manage (install/update) them for you. You can read more
about this tool on [the official Poetry website](https://python-poetry.org/)

#### Dependencies

To work with the package, you need to clone the repository to your computer. This is done using the `git clone` command.
Clone the project on the command line:

```bash
# clone via HTTPS:
>> git clone https://github.com/stigsanek/poll-api.git
# clone via SSH:
>> git@github.com:stigsanek/poll-api.git
```

It remains to move to the directory and install the dependencies:

```bash
>> cd poll-api
>> poetry install --no-root
```

#### Environment

For the application to work, you need to create a file `.env` in the root of the project:

```
PROJECT_NAME="Poll API"
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
BACKEND_CORS_ORIGINS=http://localhost:8000,http://127.0.0.1:8000
```

#### Run

```bash
>> uvicorn poll_api.main:app --reload

INFO: Started server process [1]
INFO: Waiting for application startup.
INFO: Application startup complete.
INFO: Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

Open [http://localhost:8000](http://localhost:8000) in your browser.

### 2. Docker

Docker is a platform designed to help developers build, share, and run modern applications.
You can read more about this tool on [the official Docker website](https://www.docker.com/).
You need to [install Docker Desktop](https://www.docker.com/products/docker-desktop/).
Docker Desktop is an application for the building and sharing of containerized applications and microservices.

#### Environment

Depending on the application mode, different environment files are used.
For development mode, the `.env.dev` file with basic settings has already been created.
For production mode, you need to create an `.env.prod` file:

```
# Database environment
POSTGRES_DB=poll_api
POSTGRES_USER=user
POSTGRES_PASSWORD=password
POSTGRES_HOST=db
POSTGRES_PORT=5432

# App environment
PROJECT_NAME="Poll API"
DEBUG=False
SECRET_KEY=prod
DATABASE_URL=postgresql+psycopg2://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}
BACKEND_CORS_ORIGINS=http://localhost:8000,http://127.0.0.1:8000
```

#### Run development mode

```bash
>> docker-compose -f compose.dev.yml up -d --build

...
...
...
Creating poll-api_db_1  ... done
Creating poll-api_web_1 ... done
```

Open [http://localhost:8000](http://localhost:8000) in your browser.

#### Run production mode

```bash
>> docker-compose -f compose.prod.yml up -d --build

...
...
...
Creating poll-api_db_1  ... done
Creating poll-api_web_1 ... done
```

Open [http://localhost:8000](http://localhost:8000) in your browser.
