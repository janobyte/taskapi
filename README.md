# TaskAPI v2 🚧 WIP

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Pytest](https://img.shields.io/badge/pytest-%23ffffff.svg?style=for-the-badge&logo=pytest&logoColor=2f9fe3)
![AWS](https://img.shields.io/badge/AWS-%23FF9900.svg?style=for-the-badge&logo=amazon-aws&logoColor=white)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)

**this branch will be merged into `main` and deleted once all the changes are ready.**

~~[Docs](http://3.68.113.178/docs) are currently running on a direct IP address (and http only) on an ECS instance until my DNS propagates properly and I can set it up again.~~

Docs down ECS is too expensive.

## v2 Changes

### Modern Project Structure
v2 introduces a modular project structure set up with `uv`, improving organization and scalability.

### Dockerfile for Containerization
A `Dockerfile` has been added for containerization, ensuring consistent environments for deployment and testing. This is essential for deployments and an image is already published to DockerHub.

### Pre-Commit System
A pre-commit system emulates the pipeline locally, allowing to run linting, formatting, and tests before committing.

> **Note**
> 
> for simplicity, more information is left in CI/CD section.

### Improved Pipeline

In v2 the pipeline and the development process is improved reassuring code quality, consistency, and development efficiency.

| **Pipeline Step**         | **v1**                            | **v2**                              |
|---------------------------|-----------------------------------|-------------------------------------|
| **Code Formatting**        | Black                            | Ruff (via `uvx ruff format --check`)|
| **Linting**                | Pylint                           | Ruff (via `uvx ruff check .`)       |
| **Type Checking**          | Mypy                             | Pyright (via `uv run pyright .`)    |
| **Testing**                | Pytest                           | Pytest (via `uv run pytest`)        |
| **Lock File Management**   | Not specified                    | `uv lock --locked` in `lock_file` job|
| **Build Step**             | Not specified                    | `uv build` in the `build` job       |

*+ pre-commit :)*

## How to Install

Installing v2 is entirely different, due to `uv` changes and the new `Dockerfile`.

### Prerequisites

Ensure you have the following installed:
- [Git](https://git-scm.com/)
- [Python](https://www.python.org/)
- [uv](https://docs.astral.sh/uv/)
- [Docker](https://www.docker.com/) (if planning to build and run dockerized)

### Clone the Repository

```sh
git clone https://github.com/janobyte/taskapi.git
```

### Navigate to the Project Directory

```sh
cd taskapi
```

### Checkout the v2 branch

```sh
git checkout v2
```

### Install Dependencies

```sh
uv sync
```

### Run the Project

```sh
fastapi dev src/taskapi/main.py 
```

## Building and using the Docker image

```sh
docker build -t fastapi-docker . 
```

*you can name it whatever*

```sh
docker run -d --name fastapi-docker-container -p 80:80 fastapi-docker
```
*...this one as well*

## CI/CD with GitHub Actions

```yaml
jobs:
  lock_file:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: ./.github/actions/setup
      - run: uv lock --locked
  linting:
    runs-on: ubuntu-latest
    needs: [lock_file]
    steps:
      - uses: actions/checkout@v4
      - uses: ./.github/actions/setup
      - run: uvx ruff check .
  formatting:
    runs-on: ubuntu-latest
    needs: [lock_file]
    steps:
      - uses: actions/checkout@v4
      - uses: ./.github/actions/setup
      - run: uvx ruff format --check .
  type_consistency:
    runs-on: ubuntu-latest
    needs: [lock_file]
    steps:
      - uses: actions/checkout@v4
      - uses: ./.github/actions/setup
      - run: uv run pyright .
  tests:
    runs-on: ubuntu-latest
    needs: [lock_file]
    steps:
      - uses: actions/checkout@v4
      - uses: ./.github/actions/setup
      - run: uv run pytest --cov=./ --cov-report=xml
  build:
    runs-on: [ubuntu-latest]
    needs: [linting, formatting, type_consistency, tests]
    steps:
      - uses: actions/checkout@v4
      - uses: ./.github/actions/setup
      - run: uv build
```
### Quick Overview
Pylint & black were annoying to develop with, especially with VSCode extensions. I changed these based on community merit and personal preference.

*This CI/CD is missing the Deployment section for now as well.*

## TODO:
- Add a docker compose file.
- Finish setting up AWS & Postgres.
- Figure out dev/stage/prod DBs.
- Automate deployments.
- Full test coverage (+ upload/display cov)

**And obviously,**
- Build an actual API :D


