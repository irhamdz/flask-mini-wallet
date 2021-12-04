# Flask Mini Wallet
Simple mini wallet service with flask and postgresql

## Local Development

1. install dependencies
  
```pip install -r requirements.txt```

2. install postgresql
3. create database

```
> psql
CREATE DATABASE miniwallet
```
4. init migrations

```flask db init```

5. migrate table

```
flask db migrate
flask db upgrade
```

6. run app

```
export FLASK_APP=wsgi.py
export FLASK_ENV=development
flask run
```

## Test
```python -m pytest -v    ```
