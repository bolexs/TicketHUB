<p align="center">
  <a href="" rel="noopener">
 <img width=200px height=200px src="https://i.pinimg.com/originals/f9/ca/ad/f9caad5c1cf0d948ea9c747160ca342b.jpg" alt="TicketHUB"></a>
</p>

<h3 align="center">TicketHUB</h3>

<div align="center">

[![Status](https://img.shields.io/badge/status-active-success.svg)]()
[![GitHub Issues](https://img.shields.io/github/issues/bolexs/TicketHUB.svg)](https://github.com/bolexs/TicketHUB/issues)
[![GitHub Pull Requests](https://img.shields.io/github/issues-pr/bolexs/TicketHUB.svg)](https://github.com/bolexs/TicketHUB/pulls)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](/LICENSE)

</div>

---

<p align="center"> TicketHub is an API aimed at simplifying the process of purchasing tickets for various events such as concerts, conferences, sports events, and more.
    <br> 
</p>

## 📝 Table of Contents

- [About](#about)
- [Getting Started](#getting_started)
- [Deployment](#deployment)
- [Built Using](#built_using)
- [Authors](#authors)
- [Acknowledgments](#acknowledgement)

## 🧐 About <a name = "about"></a>

TicketHUB aims to provide developers with a seamless and efficient experience for integrating event ticketing functionality into their applications.

## 🏁 Getting Started <a name = "getting_started"></a>

These instructions will get you a copy of TicketHUB API up and running on your local machine for development and testing purposes. See [deployment](#deployment) for notes on how to deploy the project.

### Prerequisites

 You need to install Python on your local computer, kindly follow the highlighted text to install it if you don't have it installed.

- [Python](https://www.python.org/downloads/)

### Installing

You can install by first cloning the repository, then following the steps and procedures as listed below.

Git clone

  ```bash
  git clone git@github.com:bolexs/TicketHUB.git
  ```

Setup virtual environment

  ```bash
  cd app
  python -m venv venv
  source venv/bin/activate   # for linux
  venv\Scripts\activate      # for windows
  ```

Install dependencies

  ```bash
  pip install -r requirements.txt
  ```

Create .env file

  ```bash
  cd app
  touch .env
  ```

Copy the example in env.example and paste it in .env

  ```bash
  cp env.example .env
  ```

  You can use sqlite by default, but if you want to use postgresql, you need to install it and create a database and set it as the `DB_TYPE` in the .env file. Same goes for mysql.

Before running the server, you need to run the migrations. We are making use of [alembic](https://alembic.sqlalchemy.org/en/latest/), which is a migration tool used in python.

 To run migrations

 ```bash
  alembic upgrade head
 ```

 > [!CAUTION]
 > Ensure to run migrations after every change done to the models and schema so it will immediately be reflected to the database.

 To run server

 ```bash
   uvicorn main:app --host 0.0.0.0 --port 80 --reload
 ```

 > [!NOTE]
> Docker implementation will be done after initial set up has been done


## 🔧 Running the tests <a name = "tests"></a>

Make sure you are in the root directory of the project.

  ```bash
  cd app
  ```

  ```bash
  pytest
  ```

### And coding style tests

Flake8 is a Python linting tool that checks your Python codebase for errors, styling issues and complexity

```bash
flake8 app
```


## 🚀 Deployment <a name = "deployment"></a>

> [!NOTE]
> Will be updated

## ⛏️ Built Using <a name = "built_using"></a>

- [PostgresSQL](https://www.postgresql.org/) - Database
- [FastAPI](https://fastapi.tiangolo.com/) - Server Framework


## ✍️ Authors <a name = "authors"></a>

- [@Bolu Ade-ojo](https://github.com/bolexs)
- [@Babafemi Olatona](https://github.com/babafemiolatona)

See also the list of [contributors](https://github.com/bolexs/TicketHUB/contributors) who participated in this project.

## 🎉 Acknowledgements <a name = "acknowledgement"></a>

- Hat tip to anyone whose code was used
- Inspiration
- References
