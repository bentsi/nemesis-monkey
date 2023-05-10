# nemesis-monkey
A framework for applying faults on targets

## Installation
Prepare pyenv environment
```commandline
    pyenv install 3.11.3  # Install Python 3.11.3
    pyenv virtualenv 3.11.3 nemesis-monkey
    pyenv activate nemesis-monkey
    curl -sSL https://install.python-poetry.org | python
```

### Dev Environment
```commandline
    poetry install
    pre-commit install
```

### Prod Environment
```commandline
    poetry install --without=dev
```
