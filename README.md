# topiq

A beginner-friendly Django starter project named `topiq` with a `website` app and a modern homepage.

## Project structure

```text
topiq/
├── manage.py
├── README.md
├── requirements.txt
├── run.sh
├── templates/
├── topiq/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── website/
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── models.py
    ├── static/
    │   └── website/
    │       └── css/
    │           └── style.css
    ├── templates/
    │   └── website/
    │       └── index.html
    ├── tests.py
    ├── urls.py
    └── views.py
```

## Run locally

1. Create and activate a virtual environment.
2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Apply migrations:

   ```bash
   python manage.py migrate
   ```

4. Start the development server:

   ```bash
   python manage.py runserver
   ```

5. Open `http://127.0.0.1:8000/` in your browser.
