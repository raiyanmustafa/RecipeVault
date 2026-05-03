#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PYTHON_BIN="${PYTHON_BIN:-$ROOT_DIR/.venv/bin/python}"
MANAGE_PY="$ROOT_DIR/app/manage.py"

if [ ! -x "$PYTHON_BIN" ]; then
  echo "Python executable not found at: $PYTHON_BIN"
  echo "Create the virtual environment first:"
  echo "  python3 -m venv .venv"
  echo "  .venv/bin/python -m pip install -r app/requirements.txt"
  exit 1
fi

"$PYTHON_BIN" "$MANAGE_PY" makemigrations
"$PYTHON_BIN" "$MANAGE_PY" migrate --noinput

"$PYTHON_BIN" "$MANAGE_PY" shell <<'PY'
from django.contrib.auth import get_user_model

User = get_user_model()
user, _created = User.objects.get_or_create(
    username="admin",
    defaults={
        "email": "admin@example.com",
        "is_staff": True,
        "is_superuser": True,
    },
)
user.email = "admin@example.com"
user.is_staff = True
user.is_superuser = True
user.set_password("admin")
user.save()
print("Superuser ready: admin / admin")
PY

"$PYTHON_BIN" "$MANAGE_PY" loaddata sample_recipes

echo "RecipeVault demo setup complete."
