### Building a RESTful API using Flask, PostgreSQL, JWT, Postman, pytest, uWSGI, NGINX & Docker

### Quick guide to get started

1. Choose the folder to host the API and clone the repository
```shell
$ git clone https://github.com/docedos/studentbook.git studentbook
$ cd studentbook
```

2. Start and activate a virtual eviroment:
```shell
$ python3.6 -m venv .venv
$ source .venv/bin/activate
```

3. Install all the API requirements:

* Flask: http://flask.pocoo.org/
* Flask-RESTful: https://flask-restful.readthedocs.io/en/latest/
* Psycopg2: http://initd.org/psycopg/
* Pytest: https://docs.pytest.org/en/latest/
* Requests: https://2.python-requests.org/en/master/

```shell
(.venv) $ pip3 install -r requirements.txt
```

4. Create a database with the name of `studentbook` in PostgreSQL and execute the queries of file `database.sql`. Open the file `/app/models/pg_connection.py` and modify the connection attrbutes. 

5. Run the development server:
```shell
$ python run.py
```

6. Navigate to [http://127.0.0.1:8080](http://127.0.0.1:8080)


### Run tests with Pytest
```
(.venv) $ pytest -v
```
