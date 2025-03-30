# Data Modelling Case

[![linting: pylint](https://img.shields.io/badge/linting-pylint-yellowgreen)](https://github.com/PyCQA/pylint)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Pre-commit: enabled](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![Rye](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/rye/main/artwork/badge.json)](https://rye-up.com)

## Overview
This is an ELT project for extracting TMDB movie details through API calls, loading it to database and transforming data.
The main goal is to build analytical dataset, schedule and monitior workflows.

## Technology stack
* <b>Python</b> is used as the primary programming language for set of scripts.
* <b>PostgreSQL</b> is used as the primary storage.
* <b>DBT</b> is used as the data transformation tool.
* <b>Airflow</b> is used as task orchestration tool.

### Python libraries

* <b>Pandas</b> for basic ETL functions.
* <b>SQLAlchemy</b> for database connections.
* <b>Requests</b> for interacting with API.
