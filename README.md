# Flask Mini Wallet
Simple mini wallet service with flask and postgresql

## Local Development

1; Install dependencies
  
```python
pip install -r requirements.txt
```

2; Install [postgresql](https://www.postgresql.org/download/)

3; Create database

```bash
> psql
CREATE DATABASE miniwallet
```

4; Init migrations

```python
flask db init
```

5; Migrate table

```python
flask db migrate
flask db upgrade
```

6; Run app

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

import this collection [file](Mini-Wallet.postman_collection.json)
