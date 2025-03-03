# TaskAPI

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Pytest](https://img.shields.io/badge/pytest-%23ffffff.svg?style=for-the-badge&logo=pytest&logoColor=2f9fe3)
![AWS](https://img.shields.io/badge/AWS-%23FF9900.svg?style=for-the-badge&logo=amazon-aws&logoColor=white)
![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)

a simple Task Management CRUD RESTful API.

[Docs](http://3.68.113.178/docs) are currently running on a flat ip address and http on an ECS instance until my DNS propagates properly and I can set it up again.

## v2

There is a [v2 branch](https://github.com/janobyte/taskapi/tree/v2) with a different, modernized *(uv)* setup aiming to accomplish a bit more. Head over there to see the comparison and changes.

## How to Install

Follow these instructions to set up the project on your local machine.

### Prerequisites

Ensure you have the following installed:
- [Git](https://git-scm.com/)
- [Python](https://www.python.org/)

## Clone the Repository

```sh
git clone https://github.com/janobyte/taskapi.git
```

### Navigate to the Project Directory

```sh
cd taskapi
```

### Install Dependencies

```sh
python3 -m venv .venv
```
```sh
source .venv/bin/activate
```
```sh
pip install -r requirements.txt && pip install --upgrade pip
```

### Run the Project

```sh
fastapi dev
```
or
```sh
uvicorn main:app --reload
```

## CI/CD with GitHub Actions

This project uses GitHub Actions for continuous integration and continuous deployment (CI/CD). GitHub Actions automates the process of building, testing, and deploying your application whenever changes are pushed to the repository.

The workflow configuration is defined in the `.github/workflows/ci-cd.yml` file.

```yaml
jobs:
  build-test-deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.13'
        
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
        pip install black pylint mypy pytest pytest-cov
        # awscli
        
    - name: Format with black
      run: |
        black . --check
        
    - name: Lint with pylint
      run: |
        pylint --disable=C0111,C0103,W0611,W0621,W0613,W0105,C0411 $(git ls-files '*.py')
        
    - name: Check types with mypy
      run: |
        mypy .
        
    - name: Test with pytest
      run: |
        pytest --cov=./ --cov-report=xml
```
### Project Pipeline Overview

This project utilizes the following tools to maintain code quality:

1. **Black**: Automatically formats code to ensure consistent style across the codebase.
2. **Pylint**: Enforces coding standards and identifies potential issues, promoting clean and maintainable code.
3. **Mypy**: Performs static type checking to catch type violations.
4. **Pytest**: Runs unit tests to ensure functionality.

These tools together ensure a clean, consistent, and well-tested codebase.


> **Note**
> 
> the approach to this changes a bit in v2, continuous deployment will also only be available in v2 through `awscli`, once I get PostgreSQL+ECS running


## Resources
Everything written here was pretty much based on these 2 docs:
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [SQLModel Docs](https://sqlmodel.tiangolo.com/)
