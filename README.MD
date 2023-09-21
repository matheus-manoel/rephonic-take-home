# Rephonic Dev Assignment

## Setup and run
On application root directory, run the following commands:

1. Create virtual environment
```bash
# create virtual environment
python3 -m venv venv
source venv/bin/activate
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Initialize database (sqlite)
```bash
python3 init_db.py
```

4. Run redis server on port 5672
```bash
redis-server --port 5672
```

5. Run celery worker
```bash
celery -A app.celery worker
```

6. Create db migration
```bash
flask db init
flask db migrate -m "Initial migration."
flask db upgrade
```

7. Run flask server
```bash
flask run
```

## Run tests

```bash
python -m unittest discover tests/
```
