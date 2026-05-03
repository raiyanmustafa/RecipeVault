# RecipeVault

A deliberately small Django recipe app for the Docker in Practice workshop.

This first version is Django-only. It gives the workshop a tiny real application with code, dependencies, a database, uploaded files, and browser traffic. Docker files are intentionally not included yet.

This app uses permissive demo settings: all hosts are allowed, CSRF middleware is disabled, and framing is allowed. Keep those settings for local workshop demonstrations only.

## Run Locally

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r app/requirements.txt
./scripts/setup_demo.sh
.venv/bin/python app/manage.py runserver 0.0.0.0:8000
```

Open `http://127.0.0.1:8000`.

## Run Tests

```bash
.venv/bin/python app/manage.py test recipes
```

## Load Sample Recipes

```bash
.venv/bin/python app/manage.py loaddata sample_recipes
```

## Quick Demo Setup

```bash
./scripts/setup_demo.sh
```

This runs migrations, creates or resets the `admin` superuser with password `admin`, and loads the sample recipes.

## Workshop-Relevant Behavior

- SQLite database by default
- Optional recipe photo upload under `app/media/`
- Simple CRUD pages
- Host/container name shown in the footer for a later scaling demo
