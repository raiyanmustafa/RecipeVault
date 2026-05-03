# Docker in Practice: Workshop Planning Document

**Session subtitle:** Build, Ship, and Scale Applications Anywhere  
**Workshop style:** Docker-first, application-light, hands-on  
**Example project:** RecipeVault — a tiny recipe management web app  
**Recommended duration:** 90–120 minutes  
**Delivery environment:** GitHub Codespaces + Docker Compose

---

## 1. Core Workshop Philosophy

This workshop is **not** a Django, Flask, Python, Nginx, or PostgreSQL workshop.

The application exists only as a teaching vehicle. The main goal is to help participants understand Docker by watching one small application become a containerized system.

The guiding rule for the whole session:

> Every change we make to the project must teach a Docker concept.

The story of the workshop is:

> We start with a tiny Python recipe app. It has code, dependencies, a database, and uploaded images. First, we package the app into a Docker image. Then we run it as a container. Then we use Compose to define it as a service. Then we add configuration, volumes, a database service, service dependencies, health checks, a proxy container, and finally multiple backend containers. The app is simple on purpose — the focus is Docker.

---

## 2. What the Audience Should Learn

By the end, participants should understand these Docker concepts:

1. Docker image
2. Docker container
3. Dockerfile
4. Build context
5. `.dockerignore`
6. Base image
7. Dockerfile instructions such as `FROM`, `WORKDIR`, `COPY`, `RUN`, `EXPOSE`, and `CMD`
8. Port publishing
9. Docker Compose
10. Compose services
11. Compose project lifecycle
12. Docker networks
13. Service discovery by name
14. Environment variables
15. `.env` files
16. Named volumes
17. Bind mounts
18. Read-only mounts
19. Persistent data
20. Multi-container applications
21. Official/prebuilt images
22. `depends_on`
23. Container health checks
24. Restart policies
25. Container logs
26. `exec` into running containers
27. Scaling a service
28. Public vs private containers
29. Disposable application containers vs persistent state
30. Why Docker is useful for development and deployment

---

## 3. The Example Project

### 3.1 Project Name

**RecipeVault**

### 3.2 Project Description

RecipeVault is a small recipe management web application.

Users can:

- View a list of recipes
- Add a recipe title
- Add a description
- Add ingredients
- Add quantities or notes
- Upload a recipe photo
- View recipe details
- Delete or edit recipes if desired

The app has just enough real-world behavior to make Docker meaningful:

| Application feature | Why it matters for Docker |
|---|---|
| Python web app | Lets us build a custom Docker image |
| Dependencies | Shows why image builds are useful |
| SQLite database at first | Shows local file/state problems |
| PostgreSQL later | Shows multi-container systems |
| Uploaded images | Shows persistence and shared volumes |
| Static files/CSS | Shows proxy/static-serving concept without going deep |
| Browser access | Shows port publishing |
| Nginx proxy | Shows public entrypoint vs internal services |
| Multiple app containers | Shows scaling from the same image |

### 3.3 Important Teaching Boundary

Do not spend time explaining framework internals.

You can say:

> This is a small Python web app. It has a page, a database, and file uploads. We will treat it as a black box and focus on how Docker runs it.

Avoid explaining:

- Django views/models/forms
- Flask routing details
- SQL query logic
- Template syntax
- Python package internals
- PostgreSQL administration
- Nginx tuning

---

## 4. Recommended Tech Choice for the App

Use the lightest app that gives you database records and uploads.

Recommended stack:

```text
Python web app
SQLite first
PostgreSQL later
Basic HTML templates
Uploaded images folder
Dockerfile
Docker Compose
Nginx container
```

Good implementation options:

### Option A — Tiny Flask app

This is the simplest for a Docker-focused workshop.

Useful because:

- Small codebase
- Easy to treat as a black box
- Easy to support file uploads
- Easy to switch database configuration through `DATABASE_URL`

### Option B — Tiny Django app

This is fine if you are more comfortable building it.

But if you choose Django, do **not** teach Django concepts during the workshop. Present it only as “the Python app.”

### Recommended choice

Use **Flask or a very minimal Django app**, whichever you can prepare fastest and debug confidently.

The Docker session should not depend on participants understanding the framework.

---

## 5. Final Architecture Journey

### 5.1 Starting point

```text
Browser
   ↓
Python web app running locally
   ↓
SQLite database file
   ↓
Local uploads folder
```

### 5.2 Final target

```text
Browser
   ↓
Published port on host/Codespaces
   ↓
Nginx container
   ↓
Docker network
   ↓
Python app container(s)
   ↓
PostgreSQL container
   ↓
Named database volume

Uploaded recipe images
   ↓
Shared named media volume
```

### 5.3 Final architecture diagram

```text
                    Browser
                       ↓
              Host published port
                       ↓
                Nginx container
             public-facing service
                       ↓
              Docker internal network
                       ↓
        ┌──────────────┴──────────────┐
        ↓                             ↓
 Python app container 1       Python app container 2
        ↓                             ↓
        └──────────────┬──────────────┘
                       ↓
              PostgreSQL container
                       ↓
              postgres_data volume

Recipe photo uploads
        ↓
   media_data volume
        ↓
Mounted read/write by app
Mounted read-only by Nginx
```

---

## 6. Session Positioning

### 6.1 Title

**Docker in Practice**

### 6.2 Subtitle

**Build, Ship, and Scale Applications Anywhere**

### 6.3 Strong opening message

> Running code is not the same as deploying an application.

### 6.4 Short intro script

> Today we are not here to learn a Python framework. We are here to learn Docker. We will use a tiny recipe app as our example system because it has the things real applications usually have: code, dependencies, configuration, a database, uploaded files, and browser traffic. Step by step, we will turn this small app into a containerized application stack.

---

## 7. Recommended Time Plan

### 7.1 120-minute version

| Time | Section | Main Docker concept |
|---:|---|---|
| 0:00–0:10 | Introduction and final architecture preview | Application as a system |
| 0:10–0:25 | Docker mental model | Image, container, Dockerfile |
| 0:25–0:40 | Run app locally and identify problems | Local dependency/state problem |
| 0:40–0:55 | Build first Docker image | Dockerfile, build context, layers |
| 0:55–1:05 | Run first container | Container, port publishing |
| 1:05–1:15 | Move to Compose | Service, declarative app stack |
| 1:15–1:25 | Add environment variables | Runtime configuration |
| 1:25–1:35 | Add media volume | Persistence, named volumes |
| 1:35–1:50 | Add PostgreSQL container | Multi-container app, service DNS |
| 1:50–2:00 | Add depends_on and healthcheck | Dependency, readiness |
| 2:00–2:12 | Add Nginx proxy | Public/private service, ports vs expose |
| 2:12–2:20 | Debugging and lifecycle | logs, ps, exec, restart |
| 2:20–2:30 | Scaling demo and recap | Same image, multiple containers |

This table is longer than 120 minutes because it includes buffer. In practice, you can combine some sections.

### 7.2 Recommended actual 2-hour pacing

| Time | Section |
|---:|---|
| 0:00–0:10 | Intro: why Docker and what we are building |
| 0:10–0:25 | Docker basics: image, container, Dockerfile, Compose |
| 0:25–0:35 | Show RecipeVault locally |
| 0:35–0:50 | Dockerfile + build image |
| 0:50–1:00 | Run container + port mapping |
| 1:00–1:12 | Docker Compose service |
| 1:12–1:25 | Environment variables + `.env` |
| 1:25–1:38 | Volumes for uploaded images |
| 1:38–1:55 | PostgreSQL service + Docker networking |
| 1:55–2:07 | `depends_on` + healthcheck |
| 2:07–2:22 | Nginx proxy + ports vs expose |
| 2:22–2:30 | Logs, exec, restart policy, scaling demo, recap |

### 7.3 90-minute compressed version

| Time | Section |
|---:|---|
| 0:00–0:10 | Intro + Docker mental model |
| 0:10–0:25 | Dockerfile + image + container |
| 0:25–0:35 | Compose basics |
| 0:35–0:50 | Environment variables + volumes |
| 0:50–1:05 | PostgreSQL service + networking |
| 1:05–1:20 | Nginx proxy + ports vs expose |
| 1:20–1:30 | Logs, exec, scale, recap |

---

## 8. Repository Structure

Recommended repo structure:

```text
recipevault-docker-workshop/
├── app/
│   ├── recipevault/              # Python app code
│   ├── requirements.txt
│   ├── static/
│   ├── templates/
│   ├── media/                    # ignored; mounted later
│   └── app.py or manage.py
├── nginx/
│   └── default.conf
├── .devcontainer/
│   └── devcontainer.json
├── .dockerignore
├── .env.example
├── Dockerfile
├── compose.yaml
└── README.md
```

### 8.1 Suggested branches

Prepare branches/checkpoints so nobody gets stuck:

```text
main
  Local RecipeVault app only

01-dockerfile
  Dockerfile and .dockerignore added

02-container-run
  App can be built and run manually with docker run

03-compose-web
  App defined as a Compose service

04-env-and-volumes
  Runtime config and media volume added

05-postgres
  PostgreSQL service added

06-healthcheck
  depends_on and healthcheck added

07-nginx-proxy
  Nginx proxy added

08-debug-lifecycle
  restart policy and debugging commands demonstrated

09-scale
  Multiple app containers behind proxy
```

### 8.2 Why branches matter

Workshops fail when one small error blocks a participant. Branches give every participant a safe checkpoint.

Recommended recovery command:

```bash
git checkout 05-postgres
docker compose up --build
```

---

## 9. Codespaces Setup

The workshop should run in GitHub Codespaces so participants only need a browser.

Codespaces gives participants a development environment in the cloud. GitHub describes dev containers as Docker containers configured to provide development environments.

### 9.1 `.devcontainer/devcontainer.json`

```json
{
  "name": "RecipeVault Docker Workshop",
  "image": "mcr.microsoft.com/devcontainers/base:ubuntu",
  "features": {
    "ghcr.io/devcontainers/features/docker-in-docker:2": {}
  },
  "customizations": {
    "vscode": {
      "extensions": [
        "ms-azuretools.vscode-docker",
        "ms-python.python",
        "redhat.vscode-yaml"
      ]
    }
  },
  "forwardPorts": [8080, 8000],
  "postCreateCommand": "docker --version && docker compose version"
}
```

### 9.2 Instructor note

Test this before the session. Docker-in-Docker behavior in Codespaces should be validated with your exact repo.

### 9.3 Participant setup instructions

Participants should only need:

1. A GitHub account
2. The workshop repository link
3. A browser
4. Codespaces enabled for their account/organization

Participant command check:

```bash
docker --version
docker compose version
```

---

## 10. Stage-by-Stage Workshop Plan

Each stage below includes:

- What you add
- What participants do
- What Docker concept is taught
- Suggested explanation
- Commands
- Validation

---

# Stage 0 — Show the app as a black box

## What you show

Run the app locally in the Codespaces terminal.

Example:

```bash
cd app
python app.py
```

Or, if using Django:

```bash
cd app
python manage.py runserver 0.0.0.0:8000
```

## Docker concepts prepared

This stage prepares the problem Docker solves:

- Local dependency problems
- App configuration problems
- Local database file problem
- Uploaded file persistence problem
- “Works on my machine” problem

## What you say

> The app is intentionally simple. It has pages, a database, and image uploads. We are not going to study the app. We are going to study what it takes to run this app in a repeatable Docker-based setup.

## Validation

Open the app in the browser and create a recipe with an image.

---

# Stage 1 — Create the first Dockerfile

## What you add

`Dockerfile`

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY app/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ .

EXPOSE 8000

CMD ["python", "app.py"]
```

If using Django:

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY app/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

## Docker concepts taught

| Docker concept | Explanation |
|---|---|
| `FROM` | Selects the base image |
| `WORKDIR` | Sets the working directory inside the image/container |
| `COPY` | Copies files from build context into the image |
| `RUN` | Runs commands while building the image |
| `EXPOSE` | Documents the container port |
| `CMD` | Defines the default process when the container starts |
| Image | Built package containing app + dependencies |
| Container | Running process created from an image |

## What you say

> A Dockerfile is the recipe for building an image. The image is the packaged version of the app. A container is a running instance of that image.

## Commands

```bash
docker build -t recipevault .
```

## Validation

```bash
docker images | grep recipevault
```

---

# Stage 2 — Add `.dockerignore`

## What you add

`.dockerignore`

```text
.git
.github
.devcontainer
__pycache__
*.pyc
.venv
.env
.env.*
app/media
app/db.sqlite3
*.log
.DS_Store
README.md
```

## Docker concepts taught

- Build context
- Excluding unnecessary files
- Faster builds
- Avoiding secrets in images
- Avoiding accidental local state in images

## What you say

> Docker builds from a build context. If we send unnecessary files into the build, the image build can become slower, larger, and less safe. `.dockerignore` lets us control what enters the build process.

## Commands

```bash
docker build -t recipevault .
```

## Validation

Check that local database and media files are not copied into the image.

```bash
docker run --rm recipevault ls -la
```

---

# Stage 3 — Run the first container

## What you do

Run the image as a container and publish the port.

```bash
docker run --rm -p 8000:8000 recipevault
```

## Docker concepts taught

- Container runtime
- Port publishing
- Host port vs container port
- Foreground container process
- Stopping a container

## What you say

> The app is listening inside the container on port 8000. The browser is outside the container. The `-p 8000:8000` flag publishes the container port to the host environment.

## Key explanation

```text
-p HOST_PORT:CONTAINER_PORT

-p 8000:8000 means:
  Browser/host uses port 8000
  Container receives traffic on port 8000
```

## Validation

Open the forwarded port in Codespaces.

## Useful commands

```bash
docker ps
docker stop <container_id>
```

---

# Stage 4 — Move to Docker Compose

## What you add

`compose.yaml`

```yaml
services:
  web:
    build: .
    ports:
      - "8000:8000"
```

## Docker concepts taught

- Docker Compose
- Service definition
- Declarative app configuration
- Project lifecycle
- `docker compose up`
- `docker compose down`

## What you say

> Instead of typing long `docker run` commands, Compose lets us describe the application as services in a file.

## Commands

```bash
docker compose up --build
```

In another terminal:

```bash
docker compose ps
docker compose down
```

## Validation

Open port 8000 again and verify the app works.

---

# Stage 5 — Add environment variables

## What you add

`.env.example`

```env
APP_ENV=development
DEBUG=1
APP_PORT=8000
DATABASE_URL=sqlite:///data/db.sqlite3
MEDIA_ROOT=/app/media
```

Update `compose.yaml`:

```yaml
services:
  web:
    build: .
    ports:
      - "${APP_PORT:-8000}:8000"
    environment:
      APP_ENV: ${APP_ENV:-development}
      DEBUG: ${DEBUG:-1}
      DATABASE_URL: ${DATABASE_URL:-sqlite:///data/db.sqlite3}
      MEDIA_ROOT: ${MEDIA_ROOT:-/app/media}
```

## Docker concepts taught

- Runtime configuration
- Environment variables
- `.env` interpolation
- Same image, different runtime configuration
- Avoiding hardcoded settings

## What you say

> The image should not change every time configuration changes. Docker lets us build one image and run it with different environment variables.

## Important concept

```text
Image = app package
Environment variables = runtime configuration
```

## Commands

```bash
cp .env.example .env
docker compose up --build
```

## Validation

Change `APP_PORT` in `.env`, restart Compose, and show that the host port changes without rebuilding the image.

---

# Stage 6 — Add a volume for uploaded images

## What you add

Update `compose.yaml`:

```yaml
services:
  web:
    build: .
    ports:
      - "${APP_PORT:-8000}:8000"
    environment:
      APP_ENV: ${APP_ENV:-development}
      DEBUG: ${DEBUG:-1}
      DATABASE_URL: ${DATABASE_URL:-sqlite:///data/db.sqlite3}
      MEDIA_ROOT: /app/media
    volumes:
      - media_data:/app/media

volumes:
  media_data:
```

## Docker concepts taught

- Container filesystem lifecycle
- Named volumes
- Persistent data
- Application data vs application image

## What you say

> Containers are disposable. Uploaded recipe images are not disposable. A named volume stores important data outside the container lifecycle.

## Demo flow

1. Start the app.
2. Upload a recipe image.
3. Stop and remove containers.
4. Start the app again.
5. Show that the uploaded image still exists.

## Commands

```bash
docker compose up --build
```

Stop:

```bash
docker compose down
```

Start again:

```bash
docker compose up
```

Inspect volume:

```bash
docker volume ls
docker volume inspect recipevault-docker-workshop_media_data
```

## Important warning

`docker compose down` removes containers and networks, but it does not remove named volumes by default. `docker compose down -v` removes named volumes too.

---

# Stage 7 — Add PostgreSQL as a database service

## What you add

Update `.env.example`:

```env
APP_ENV=development
DEBUG=1
APP_PORT=8000
DATABASE_URL=postgresql://recipeuser:recipepass@db:5432/recipevault
MEDIA_ROOT=/app/media
POSTGRES_DB=recipevault
POSTGRES_USER=recipeuser
POSTGRES_PASSWORD=recipepass
```

Update `compose.yaml`:

```yaml
services:
  web:
    build: .
    ports:
      - "${APP_PORT:-8000}:8000"
    environment:
      APP_ENV: ${APP_ENV:-development}
      DEBUG: ${DEBUG:-1}
      DATABASE_URL: ${DATABASE_URL}
      MEDIA_ROOT: /app/media
    volumes:
      - media_data:/app/media
    depends_on:
      - db

  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: ${POSTGRES_DB:-recipevault}
      POSTGRES_USER: ${POSTGRES_USER:-recipeuser}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:-recipepass}
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  media_data:
  postgres_data:
```

## Docker concepts taught

- Multi-container application
- Official images
- App container vs dependency container
- Service names as hostnames
- Docker default network
- Database persistence
- Named volume for database data

## What you say

> The database is not installed on our machine. It is not inside the app container either. It is its own container, running from the official PostgreSQL image.

## Critical explanation

```text
From your laptop:
  localhost means your laptop

From inside the web container:
  localhost means the web container itself

So the database hostname is not localhost.
Inside Compose, the database hostname is the service name:
  db
```

## Commands

```bash
cp .env.example .env
docker compose up --build
```

If your app needs migrations or database initialization:

```bash
docker compose exec web python manage.py migrate
```

Or for a Flask/SQLAlchemy app, use your own init command:

```bash
docker compose exec web python -m recipevault.init_db
```

## Validation

Check containers:

```bash
docker compose ps
```

Check database logs:

```bash
docker compose logs db
```

---

# Stage 8 — Add `depends_on` and health checks

## Why this stage matters

`depends_on` controls startup order, but startup order is not the same as service readiness.

A database container can be running before the database is actually ready to accept connections.

## What you add

Update `compose.yaml`:

```yaml
services:
  web:
    build: .
    ports:
      - "${APP_PORT:-8000}:8000"
    environment:
      APP_ENV: ${APP_ENV:-development}
      DEBUG: ${DEBUG:-1}
      DATABASE_URL: ${DATABASE_URL}
      MEDIA_ROOT: /app/media
    volumes:
      - media_data:/app/media
    depends_on:
      db:
        condition: service_healthy

  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: ${POSTGRES_DB:-recipevault}
      POSTGRES_USER: ${POSTGRES_USER:-recipeuser}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:-recipepass}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER:-recipeuser} -d ${POSTGRES_DB:-recipevault}"]
      interval: 5s
      timeout: 5s
      retries: 5
      start_period: 10s

volumes:
  media_data:
  postgres_data:
```

## Docker concepts taught

- Dependency order
- Service readiness
- Container health
- Health check command
- Reliable startup

## What you say

> Compose can start the database before the app. But a running container is not always a ready service. Health checks let Docker know whether the service inside the container is actually healthy.

## Commands

```bash
docker compose up --build
```

Check health:

```bash
docker compose ps
```

## Validation

The database should show as healthy before the web app starts or becomes stable.

---

# Stage 9 — Add Nginx as a reverse proxy container

## What you add

`nginx/default.conf`

```nginx
server {
    listen 80;

    client_max_body_size 10M;

    location /media/ {
        alias /media/;
    }

    location / {
        proxy_pass http://web:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Update `compose.yaml`:

```yaml
services:
  proxy:
    image: nginx:alpine
    ports:
      - "8080:80"
    volumes:
      - ./nginx/default.conf:/etc/nginx/conf.d/default.conf:ro
      - media_data:/media:ro
    depends_on:
      - web

  web:
    build: .
    expose:
      - "8000"
    environment:
      APP_ENV: ${APP_ENV:-development}
      DEBUG: ${DEBUG:-1}
      DATABASE_URL: ${DATABASE_URL}
      MEDIA_ROOT: /app/media
    volumes:
      - media_data:/app/media
    depends_on:
      db:
        condition: service_healthy

  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: ${POSTGRES_DB:-recipevault}
      POSTGRES_USER: ${POSTGRES_USER:-recipeuser}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:-recipepass}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER:-recipeuser} -d ${POSTGRES_DB:-recipevault}"]
      interval: 5s
      timeout: 5s
      retries: 5
      start_period: 10s

volumes:
  media_data:
  postgres_data:
```

## Docker concepts taught

- Public service vs private service
- `ports` vs `expose`
- Reverse proxy as another container
- Bind-mounted config files
- Read-only volume mounts
- Internal Docker networking

## What you say

> We are not studying Nginx deeply. We are using Nginx to show that infrastructure components can also be containers. The browser talks to the proxy. The proxy talks to the app over the Docker network.

## Key explanation

```text
ports:
  Publishes a container port to the outside world

expose:
  Documents/opens a port only for other containers on the Docker network
```

Now:

```text
Browser can access:
  proxy on port 8080

Browser should not directly access:
  web
  db
```

## Commands

```bash
docker compose up --build
```

## Validation

Open port `8080` instead of `8000`.

Check services:

```bash
docker compose ps
```

---

# Stage 10 — Share media between app and proxy

## What you demonstrate

The same `media_data` volume is mounted by two containers:

```yaml
services:
  web:
    volumes:
      - media_data:/app/media

  proxy:
    volumes:
      - media_data:/media:ro
```

## Docker concepts taught

- Shared named volume
- Read/write mount
- Read-only mount
- Separating responsibilities between containers

## What you say

> The app writes uploaded files. The proxy only reads them. Docker lets us mount the same volume into multiple containers with different permissions.

## Key concept

```text
web container:
  media_data mounted read/write

proxy container:
  media_data mounted read-only
```

## Validation

1. Upload a recipe image through the app.
2. Open the recipe detail page.
3. Image should load through Nginx from `/media/...`.

---

# Stage 11 — Add restart policies

## What you add

```yaml
services:
  proxy:
    image: nginx:alpine
    restart: unless-stopped

  web:
    build: .
    restart: unless-stopped

  db:
    image: postgres:16-alpine
    restart: unless-stopped
```

## Docker concepts taught

- Container lifecycle
- Long-running services
- Failure recovery
- Restart policy

## What you say

> Containers are running processes. Processes can stop or crash. Restart policies tell Docker what to do when that happens.

## Commands

```bash
docker compose ps
docker compose restart web
docker compose logs web
```

## Validation

Restart a container and observe that the stack recovers.

---

# Stage 12 — Logs, exec, and debugging

## Docker concepts taught

- Operational visibility
- Inspecting services
- Reading logs
- Entering running containers
- Debugging containerized systems

## Commands to teach

```bash
# See running services
docker compose ps

# View logs from all services
docker compose logs

# Follow logs from one service
docker compose logs -f web

# Enter the app container
docker compose exec web sh

# Enter the database container
docker compose exec db sh

# Run a database readiness command manually
docker compose exec db pg_isready -U recipeuser -d recipevault

# See created volumes
docker volume ls

# Inspect a volume
docker volume inspect recipevault-docker-workshop_postgres_data
```

## What you say

> Running containers is only half the story. We also need to inspect them, read logs, and debug them when something goes wrong.

## Good mini-demo

Break the database password in `.env`, restart, and show how logs reveal the failure.

---

# Stage 13 — Scaling the app service

## Option A — Use Compose scale

```bash
docker compose up --scale web=2
```

This may conflict with fixed container names or host port mappings. It works best when only the proxy publishes ports and the web service uses `expose`.

## Option B — Define two web services manually

Use this if you want a more controlled demo.

```yaml
services:
  web1:
    build: .
    expose:
      - "8000"
    environment:
      DATABASE_URL: ${DATABASE_URL}
      MEDIA_ROOT: /app/media
    volumes:
      - media_data:/app/media
    depends_on:
      db:
        condition: service_healthy

  web2:
    build: .
    expose:
      - "8000"
    environment:
      DATABASE_URL: ${DATABASE_URL}
      MEDIA_ROOT: /app/media
    volumes:
      - media_data:/app/media
    depends_on:
      db:
        condition: service_healthy

  proxy:
    image: nginx:alpine
    ports:
      - "8080:80"
    volumes:
      - ./nginx/default.conf:/etc/nginx/conf.d/default.conf:ro
      - media_data:/media:ro
    depends_on:
      - web1
      - web2
```

Nginx load balancing config:

```nginx
upstream recipevault_backend {
    server web1:8000;
    server web2:8000;
}

server {
    listen 80;

    client_max_body_size 10M;

    location /media/ {
        alias /media/;
    }

    location / {
        proxy_pass http://recipevault_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## Docker concepts taught

- Same image, multiple containers
- Horizontal scaling
- Load balancing concept
- Stateless application containers
- Shared external state

## What you say

> Because the app is packaged as an image, Docker can run more than one container from the same image. The app containers should be replaceable. Persistent state lives in the database and media volume.

## Validation

Add a small endpoint or header in the app that displays the container hostname. Refresh the page to show requests hitting different containers.

Example Python logic if you choose to add it:

```python
import socket
HOSTNAME = socket.gethostname()
```

Display it in the page footer:

```html
<small>Served by container: {{ hostname }}</small>
```

This is the only app-level change worth making because it visually demonstrates Docker scaling.

---

## 11. Final Compose File Example

Use this only after participants understand the stages. Do not show the full file at the beginning.

```yaml
services:
  proxy:
    image: nginx:alpine
    ports:
      - "8080:80"
    volumes:
      - ./nginx/default.conf:/etc/nginx/conf.d/default.conf:ro
      - media_data:/media:ro
    depends_on:
      - web
    restart: unless-stopped

  web:
    build: .
    expose:
      - "8000"
    environment:
      APP_ENV: ${APP_ENV:-development}
      DEBUG: ${DEBUG:-1}
      DATABASE_URL: ${DATABASE_URL}
      MEDIA_ROOT: /app/media
    volumes:
      - media_data:/app/media
    depends_on:
      db:
        condition: service_healthy
    restart: unless-stopped

  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: ${POSTGRES_DB:-recipevault}
      POSTGRES_USER: ${POSTGRES_USER:-recipeuser}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:-recipepass}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER:-recipeuser} -d ${POSTGRES_DB:-recipevault}"]
      interval: 5s
      timeout: 5s
      retries: 5
      start_period: 10s
    restart: unless-stopped

volumes:
  media_data:
  postgres_data:
```

---

## 12. Slide Deck / Visual Backdrop Plan

You said you want to generate a presentation later. This section is designed for that.

### Slide 1 — Title

**Docker in Practice**  
Build, Ship, and Scale Applications Anywhere

Visual: Docker whale / containers / app stack illustration.

### Slide 2 — Session Promise

> We will not learn a Python framework. We will learn how Docker runs application systems.

Visual: app as a black box.

### Slide 3 — The App

RecipeVault:

- Web page
- Database records
- Uploaded images

Visual: simple UI screenshot or mockup.

### Slide 4 — Why Docker?

Problems:

- Different machines
- Different Python versions
- Missing packages
- Local database files
- Lost uploads
- Manual setup

Visual: “works on my machine” meme-style diagram.

### Slide 5 — Docker Mental Model

```text
Dockerfile → Image → Container
```

Visual: recipe → packaged box → running process.

### Slide 6 — Dockerfile

Show the Dockerfile and highlight:

- `FROM`
- `WORKDIR`
- `COPY`
- `RUN`
- `CMD`

Visual: layered image stack.

### Slide 7 — Build Context

Show `.dockerignore`.

Message:

> Not every file should enter the image build.

Visual: repo folder → filtered build context → image.

### Slide 8 — First Container

Command:

```bash
docker run -p 8000:8000 recipevault
```

Visual:

```text
Browser → Host port → Container port → App
```

### Slide 9 — Why Compose?

Message:

> Long commands do not scale. Compose describes the system.

Visual:

```text
docker run ... docker run ... docker run ...
           ↓
       compose.yaml
```

### Slide 10 — Compose Service

Show first Compose service:

```yaml
services:
  web:
    build: .
    ports:
      - "8000:8000"
```

Visual: one service box.

### Slide 11 — Runtime Configuration

Message:

> Same image, different environment.

Visual:

```text
recipevault image
   ├── DEBUG=1
   ├── DEBUG=0
   └── DATABASE_URL=...
```

### Slide 12 — Container Filesystem Problem

Message:

> Containers are disposable. Data is not.

Visual: container deleted, data volume remains.

### Slide 13 — Named Volume for Uploads

Show:

```yaml
volumes:
  - media_data:/app/media
```

Visual: app container connected to volume.

### Slide 14 — Database as a Service

Message:

> The database is another container, not something installed manually.

Visual:

```text
web → db
```

### Slide 15 — Docker Networking

Message:

> Containers find each other by service name.

Visual:

```text
web container connects to hostname: db
```

### Slide 16 — localhost Confusion

Important slide:

```text
localhost from laptop ≠ localhost from container
```

Visual: laptop box and container box both with their own localhost.

### Slide 17 — depends_on

Message:

> Start the database before the app.

Visual: db starts first, web starts second.

### Slide 18 — Health Checks

Message:

> Running does not always mean ready.

Visual:

```text
Container running ✅
Service ready? maybe
Healthcheck confirms ✅
```

### Slide 19 — Add Nginx Proxy

Message:

> Add infrastructure as another container.

Visual:

```text
Browser → Nginx → Web
```

### Slide 20 — ports vs expose

Message:

```text
ports = public to host/browser
expose = internal to Docker network
```

Visual: proxy has public door, web/db are internal rooms.

### Slide 21 — Shared Media Volume

Message:

> App writes. Proxy reads.

Visual:

```text
web --rw--> media_data <--ro-- nginx
```

### Slide 22 — Logs and Exec

Commands:

```bash
docker compose logs -f web
docker compose exec web sh
```

Visual: magnifying glass over containers.

### Slide 23 — Restart Policies

Message:

> Docker can restart long-running services when they stop.

Visual: crashed container → restarted container.

### Slide 24 — Scaling

Message:

> Same image, multiple containers.

Visual:

```text
Nginx
  ├── web1
  └── web2
```

### Slide 25 — Final Recap

Final architecture diagram.

Key sentence:

> We did not just run an app. We defined a containerized application system.

---

## 13. Instructor Script by Stage

### Opening script

> Most people think Docker is about running a command. But Docker becomes powerful when we use it to describe a whole application system. Today our app is intentionally simple. The app is not the lesson. Docker is the lesson.

### Before Dockerfile

> Right now, this app depends on this environment. Python version, packages, database file, upload folder — all of that exists here. We want to package and run it in a repeatable way.

### Before Compose

> One container is easy to run manually. But real applications have multiple parts. Compose lets us describe those parts as services.

### Before volumes

> A container is replaceable. If we rebuild it, delete it, or start a new one, important user data should not disappear.

### Before PostgreSQL

> We are not adding PostgreSQL to learn database administration. We are adding it to show how Docker runs application dependencies as separate services.

### Before Nginx

> We are not adding Nginx to become Nginx experts. We are adding it to show public and private services in a container network.

### Before scaling

> Once the app is packaged as an image, we can create more than one container from it. That is the foundation of horizontal scaling.

---

## 14. What To Avoid

Avoid these topics in the main session:

- Django internals
- Flask internals
- React
- Redis
- Celery
- Kubernetes
- Docker Swarm
- CI/CD
- Cloud deployment
- SSL certificates
- Advanced Nginx configuration
- Advanced PostgreSQL management
- Image vulnerability scanning
- Multi-stage builds, unless you have extra time

You can mention them as future learning topics at the end.

---

## 15. Recommended Hands-On Commands Cheat Sheet

Participants should leave knowing these commands:

```bash
# Build an image
docker build -t recipevault .

# Run a container manually
docker run --rm -p 8000:8000 recipevault

# Start Compose stack
docker compose up --build

# Start in background
docker compose up -d --build

# Stop stack
docker compose down

# Stop stack and remove volumes
docker compose down -v

# List Compose services
docker compose ps

# View logs
docker compose logs

# Follow logs for one service
docker compose logs -f web

# Execute shell in running container
docker compose exec web sh

# List volumes
docker volume ls

# Inspect volume
docker volume inspect <volume_name>

# Restart service
docker compose restart web

# Scale service
docker compose up --scale web=2
```

---

## 16. Troubleshooting Plan

### Problem: Port already in use

Fix:

```bash
docker compose down
```

Or change `.env`:

```env
APP_PORT=8081
```

### Problem: Database connection error

Check:

```bash
docker compose logs db
docker compose ps
```

Explain:

- Is `db` healthy?
- Is `DATABASE_URL` using `db` as hostname?
- Did the password match the database environment variables?

### Problem: Uploaded images disappear

Check:

```bash
docker volume ls
docker compose down -v
```

Explain:

- If `down -v` was used, volumes were deleted.
- If the media folder was not mounted, files stayed inside the container.

### Problem: Nginx returns 502 Bad Gateway

Check:

```bash
docker compose logs proxy
docker compose logs web
docker compose ps
```

Explain:

- Proxy cannot reach app.
- Service name or port might be wrong.
- Web service may not be running.

### Problem: Compose scale does not work

Likely reason:

- The `web` service has a fixed host port under `ports`.

Fix:

- Only the proxy should publish ports.
- The `web` service should use `expose` instead of `ports`.

---

## 17. Pre-Session Preparation Checklist

### App checklist

- [ ] Recipe list page works
- [ ] Add recipe page works
- [ ] Image upload works
- [ ] Image display works
- [ ] App supports SQLite or simple local DB
- [ ] App supports PostgreSQL through `DATABASE_URL`
- [ ] App supports configurable media path through `MEDIA_ROOT`
- [ ] App can display container hostname for scaling demo

### Docker checklist

- [ ] Dockerfile builds successfully
- [ ] `.dockerignore` excludes local state
- [ ] Compose web-only stage works
- [ ] Environment variables work
- [ ] Media volume persists uploads
- [ ] PostgreSQL container works
- [ ] PostgreSQL volume persists data
- [ ] Healthcheck works
- [ ] Nginx proxy works
- [ ] Nginx serves media read-only
- [ ] Restart policy works
- [ ] Logs and exec commands work
- [ ] Scaling demo works

### Codespaces checklist

- [ ] Codespace opens successfully
- [ ] Docker is available
- [ ] Docker Compose is available
- [ ] Ports forward correctly
- [ ] All branches/checkpoints are available
- [ ] README has recovery instructions

---

## 18. Suggested README Structure for the Workshop Repo

```markdown
# RecipeVault Docker Workshop

## What this is
A tiny Python web app used to learn Docker concepts.

## What this is not
This is not a Python framework tutorial.

## Start in Codespaces
1. Open this repo in Codespaces.
2. Run `docker --version`.
3. Run `docker compose version`.

## Workshop checkpoints
- `main`
- `01-dockerfile`
- `02-container-run`
- `03-compose-web`
- `04-env-and-volumes`
- `05-postgres`
- `06-healthcheck`
- `07-nginx-proxy`
- `08-debug-lifecycle`
- `09-scale`

## Recovery
If something breaks:

```bash
git checkout 05-postgres
docker compose down -v
docker compose up --build
```

## Useful commands
...
```

---

## 19. Docker Concept Mapping Table

| Stage | Change made | Docker concept taught |
|---|---|---|
| 0 | Run app locally | Why Docker is needed |
| 1 | Add Dockerfile | Image build, base image, CMD, EXPOSE |
| 2 | Add `.dockerignore` | Build context control |
| 3 | Run container | Container runtime, port publishing |
| 4 | Add Compose | Service, declarative stack |
| 5 | Add environment variables | Runtime config, `.env` interpolation |
| 6 | Add media volume | Persistence, named volume |
| 7 | Add PostgreSQL | Multi-container app, official image |
| 8 | Add `depends_on` and healthcheck | Startup order, readiness |
| 9 | Add Nginx | Public/private services, proxy container |
| 10 | Share media volume | Shared volumes, read-only mounts |
| 11 | Add restart policy | Container lifecycle and recovery |
| 12 | Logs and exec | Debugging and operations |
| 13 | Scale app | Same image, multiple containers |

---

## 20. Final Takeaway

The final message participants should leave with:

> Docker is not just a way to run one application. Docker lets us package software, isolate services, define networks, persist data, inject configuration, observe running systems, and scale components from the same image.

The application is intentionally small. The Docker concepts are the real product of the session.

---

## 21. Reference Sources

Use these for preparing accurate slides and explanations:

- Docker overview: https://docs.docker.com/get-started/docker-overview/
- Dockerfile reference: https://docs.docker.com/reference/dockerfile/
- Docker build context and `.dockerignore`: https://docs.docker.com/build/concepts/context/
- Docker Compose file reference: https://docs.docker.com/reference/compose-file/
- Docker Compose services reference: https://docs.docker.com/reference/compose-file/services/
- Docker Compose networking: https://docs.docker.com/compose/how-tos/networking/
- Docker Compose startup order: https://docs.docker.com/compose/how-tos/startup-order/
- Docker volumes: https://docs.docker.com/engine/storage/volumes/
- Persisting container data: https://docs.docker.com/get-started/docker-concepts/running-containers/persisting-container-data/
- Docker restart policies: https://docs.docker.com/engine/containers/start-containers-automatically/
- GitHub Codespaces dev containers: https://docs.github.com/en/codespaces/setting-up-your-project-for-codespaces/adding-a-dev-container-configuration/introduction-to-dev-containers
- Nginx reverse proxy docs: https://docs.nginx.com/nginx/admin-guide/web-server/reverse-proxy/
- Nginx load balancing docs: https://nginx.org/en/docs/http/load_balancing.html
