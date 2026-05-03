# Minimal Django RecipeVault Design

## Goal

Build a very small Django-only RecipeVault application that supports the Docker workshop's future demonstrations without adding Docker files yet.

## Scope

The application includes recipe list, detail, create, edit, and delete flows. Recipes have a title, description, ingredients, notes, and an optional photo upload. The default database is SQLite. Uploaded media uses Django's standard media settings.

This pass intentionally excludes Dockerfile, Compose, Nginx, PostgreSQL service configuration, Codespaces setup, and checkpoint branches.

## Architecture

The repository contains an `app/` Django project. The `recipevault` project owns settings and URL routing. The `recipes` app owns the recipe model, forms, views, templates, and tests.

The app exposes a container/host identifier in template context using `socket.gethostname()`. This is small enough to keep in the app now and useful later for the workshop's scaling demo.

## Testing

Django tests cover list, create, detail, edit, delete, and hostname template context behavior. The tests use SQLite and Django's temporary test database.
