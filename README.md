# Requisitos
## Debug

* Cambiar en .env `DEBUG=True`

```bash
docker run --rm -p 6379:6379 redis:7
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py runserver
```

## Docker

* Cambiar en .env `DEBUG=False`
* URL: `https://127.0.0.1/`

```bash
docker compose up --build -d
```


