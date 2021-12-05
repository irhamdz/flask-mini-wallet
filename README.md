# Flask Mini Wallet
Simple mini wallet service with flask and postgresql

## Local Development

1; install dependencies
  
```python
pip install -r requirements.txt
```

2; install postgresql
3; create database

```bash
> psql
CREATE DATABASE miniwallet
```

4; init migrations

```python
flask db init
```

5; migrate table

```python
flask db migrate
flask db upgrade
```

6; run app

```python
export FLASK_APP=wsgi.py
export FLASK_ENV=development
flask run
```

## Test

- pytest

```python
python -m pytest -v
```

- Postman

import this collection [file] (Mini-Wallet.postman_collection.json)
