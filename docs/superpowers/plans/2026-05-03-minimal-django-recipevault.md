# Minimal Django RecipeVault Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a minimal Django-only RecipeVault application for the Docker workshop demo.

**Architecture:** Create a Django project in `app/` with one `recipes` app. Keep behavior intentionally small: CRUD, photo upload field, SQLite defaults, and hostname display for the future scaling demo.

**Tech Stack:** Python 3.12, Django 5.0.x, SQLite, Django test runner.

---

### Task 1: Project Skeleton and Tests

**Files:**
- Create: `app/manage.py`
- Create: `app/recipevault/settings.py`
- Create: `app/recipevault/urls.py`
- Create: `app/recipevault/wsgi.py`
- Create: `app/recipes/models.py`
- Create: `app/recipes/forms.py`
- Create: `app/recipes/views.py`
- Create: `app/recipes/urls.py`
- Create: `app/recipes/tests.py`
- Create: `app/templates/base.html`
- Create: `app/recipes/templates/recipes/*.html`
- Create: `app/requirements.txt`

- [x] Write tests for recipe CRUD and hostname context.
- [x] Run tests before implementation to verify Django is missing in the current environment and app behavior is not yet implemented.
- [ ] Install requirements in a local virtual environment.
- [ ] Implement the minimal Django app.
- [ ] Run migrations and tests.
- [ ] Verify the development server can start.
