FROM python:3.12-slim

WORKDIR /app

# Layer 1: copy only the dependency list first so Docker can cache installs.
COPY app/requirements.txt ./requirements.txt

# Layer 2: install the Python packages the Django app needs.
RUN pip install --no-cache-dir -r requirements.txt

# Layer 3: copy the Django project code, fixtures, and demo media images.
COPY app/ .

# Layer 4: create the SQLite database schema inside the demo image.
RUN python manage.py migrate --noinput

# Layer 5: create the demo admin account inside the demo image.
# RUN python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); user = User.objects.create_superuser('admin', 'admin@example.com', 'admin'); print('Superuser ready: admin / admin')"

# Layer 6: load sample recipes and image references into the demo database.
# RUN python manage.py loaddata sample_recipes

EXPOSE 8000

# Runtime command: start the Django development server.
CMD ["sh", "-c", "python manage.py runserver 0.0.0.0:${APP_PORT:-8000}"]
