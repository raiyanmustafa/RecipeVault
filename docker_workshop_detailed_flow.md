# Docker in Practice — Detailed Workshop Flow

## Workshop Title

**DOCKER IN PRACTICE**  
**Build, Ship, and Run Applications Anywhere**

## Core Direction

This workshop is a Docker-first practical session. The application is only a teaching vehicle.

The session should not become a Django workshop, Python workshop, Nginx workshop, or PostgreSQL workshop. Those technologies appear only because they create realistic deployment problems that Docker can solve.

The central message is:

> We start with a small working application and gradually turn it into a containerized application system.

The final result should help participants understand how Docker is used to package, run, configure, connect, debug, persist, and scale application components.

---

# 1. Demo Application

## Application Name

**RecipeVault**

## Application Purpose

RecipeVault is a tiny recipe-management web app. It is intentionally simple. It only exists to give us a realistic application to containerize.

The app should include:

- A basic web UI
- A backend application written in Python/Django
- A database-backed recipe list
- Recipe name/title
- Recipe description
- Ingredients
- Quantities
- Recipe image upload
- Admin page
- Local SQLite database at first
- Local media/upload folder at first

## What the App Should Demonstrate

The app must be small, but it should still contain the main things real applications need:

| Application Part | Why It Matters for Docker |
|---|---|
| Python backend | Shows app dependencies and runtime packaging |
| Web UI | Gives a visible browser result |
| SQLite database | Shows the problem of local state |
| Uploaded images | Shows the need for persistent media storage |
| Admin/setup script | Shows setup steps that should be repeatable |
| Logs | Shows container monitoring/debugging |
| Database replacement | Shows multi-container architecture |
| Nginx proxy | Shows public vs private services |
| Multiple app instances | Shows scaling from one image |

## What Not to Focus On

Avoid spending time teaching:

- Django models
- Django views
- Django forms
- Django templates
- Django admin internals
- PostgreSQL administration
- Nginx configuration syntax in depth
- Advanced Python packaging

Treat the app as a black box:

> This is a Python web application that has code, dependencies, a database, uploaded files, configuration, and logs.

---

# 2. High-Level Workshop Story

The flow should match this story:

1. We first run the application normally on the local machine.
2. We inspect what the application needs: code, packages, database, media folder, setup script, and server command.
3. We identify the problem: the setup works locally, but it is not reproducible or deployable.
4. We create a Dockerfile to define the application environment.
5. We build an image from the Dockerfile.
6. We run a container from the image.
7. We move from manual `docker run` commands to Docker Compose.
8. We expose the app through ports and understand Docker networking.
9. We inspect logs and enter containers for debugging.
10. We add bind mounts for a development workflow.
11. We define separate normal/development environments.
12. We replace SQLite with PostgreSQL in a separate container.
13. We add volumes so database data survives container recreation.
14. We handle service startup dependencies.
15. We add restart policies and healthchecks for stability.
16. We stop exposing the database publicly and use internal Docker networking.
17. We add Nginx as the only public-facing container.
18. We share the media volume so the app writes files and Nginx reads files.
19. We scale the app by running multiple app containers.
20. We finish with a production-style architecture.

---

# 3. Final Target Architecture

The final system should look like this:

```text
Browser
  ↓
Nginx container
  ↓
RecipeVault app container 1
RecipeVault app container 2
  ↓
PostgreSQL container
  ↓
postgres_data volume

Media flow:
RecipeVault writes uploaded files → media_data volume → Nginx reads media files
```

Important final properties:

- Only Nginx is exposed to the outside world.
- Django/RecipeVault app containers are private.
- PostgreSQL is private.
- App containers communicate with the database over an internal Docker network.
- Database data persists in a named volume.
- Media uploads persist in a named volume.
- Nginx can read media files through a read-only volume mount.
- App containers can be scaled because state is outside the app containers.

---

# 4. Detailed Stage-by-Stage Plan

## Stage 0 — Run the Application Locally

### What Happens

Start by showing that RecipeVault works without Docker.

Possible flow:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
./scripts/setup.sh
python manage.py runserver
```

The setup script can do things like:

- Run database migrations
- Create initial data
- Create admin user
- Prepare media/static folders

Then open the app in the browser.

Show:

- Main recipe list page
- Recipe detail page
- Add/edit recipe page
- Admin page
- Uploaded image visible in UI

### What to Explain

Explain only enough of the app to establish the system components:

```text
Browser → Python web app → SQLite database file
                         → local media uploads folder
```

### Docker Concept Prepared

This stage prepares the problem Docker solves:

- Local environments are inconsistent.
- Manual setup steps are easy to forget.
- Dependencies may differ across machines.
- Local database and media folders are not deployment-ready.
- The app works, but only because this specific machine is configured correctly.

### Speaker Message

> The app works locally, but that does not mean it is deployable or reproducible.

---

## Stage 1 — State the Problem Clearly

### Problem Statement

The current application setup is messy because it depends on the local machine.

Problems to highlight:

- Different operating systems may behave differently.
- Python versions may differ.
- Packages may not be version-locked properly.
- System dependencies may be missing.
- SQLite is just a local file.
- Uploaded images are stored in a local folder.
- Setup requires manual commands.
- Recreating the environment on another machine is risky.
- This creates the classic problem: “It works on my machine.”

### Analogy

`requirements.txt` is like a parts list for Python dependencies.

But Dockerfile goes further:

- It defines the base environment.
- It defines where the app lives.
- It defines what files are copied.
- It defines what commands are run.
- It defines what process starts when the container runs.

### Docker Concept

- Reproducible environments
- Environment as code
- Application packaging

### Speaker Message

> If requirements.txt tells us what Python packages to install, Dockerfile tells us how to build the whole runtime environment.

---

## Stage 2 — Create the Dockerfile

### What Happens

Introduce the Dockerfile as the recipe/blueprint for the application environment.

Example structure:

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x ./scripts/setup.sh

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

A lightweight Python image can be used. A slim image is often easier for beginners than Alpine because Alpine may introduce package/build issues with some Python dependencies. Alpine can be mentioned as a smaller option, but avoid letting it distract from Docker concepts.

### What to Explain

Explain the Dockerfile line-by-line at a Docker level:

| Instruction | Docker Meaning |
|---|---|
| `FROM` | Start from a base image |
| `WORKDIR` | Set working directory inside image/container |
| `COPY` | Copy files from build context into image |
| `RUN` | Run commands while building the image |
| `EXPOSE` | Document the container port |
| `CMD` | Default command when container starts |

### Docker Concept

- Dockerfile
- Base image
- Build context
- Image layers
- Runtime command
- Container port

### Speaker Message

> The Dockerfile is the recipe. It does not run the app by itself. It tells Docker how to build the image.

---

## Stage 3 — Add `.dockerignore`

### What Happens

Create a `.dockerignore` file.

Example:

```text
.git
__pycache__
*.pyc
.venv
.env
db.sqlite3
media
staticfiles
```

### What to Explain

Docker sends a build context during image building. Without `.dockerignore`, unnecessary or sensitive files may be included.

### Docker Concept

- Build context
- Smaller builds
- Avoid leaking secrets
- Avoid copying local state into image
- Cleaner reproducibility

### Speaker Message

> We should control what enters the image. Local databases, uploaded files, secrets, and virtual environments should not be baked into the image.

---

## Stage 4 — Build the Docker Image

### What Happens

Build the image:

```bash
docker build -t recipevault .
```

### What to Explain

The Dockerfile is used to build an image.

The image now contains:

- Python runtime
- App code
- Installed dependencies
- Default startup command

### Docker Concept

- Image creation
- Build cache
- Reusable artifact
- Distributable package

### Speaker Message

> The image is the built package. It is reusable and can be run again and again as containers.

---

## Stage 5 — Run the Container

### What Happens

Run the image as a container:

```bash
docker run -p 8000:8000 recipevault
```

Open the browser.

### What to Explain

The image is not the running application. The container is the running instance.

### Docker Concept

- Image vs container
- Container lifecycle
- Port publishing
- Isolated process

### Speaker Message

> Image is the package. Container is the running copy of that package.

---

## Stage 6 — Move to Docker Compose

### Why This Stage Exists

At this point, running Docker manually becomes annoying.

You do not want to remember:

- Port mappings
- Environment variables
- Volume mounts
- Container names
- Commands
- Networks

### What Happens

Create a `docker-compose.yml` file.

Example first version:

```yaml
services:
  web:
    build: .
    ports:
      - "8000:8000"
```

Run:

```bash
docker compose up --build
```

Stop:

```bash
docker compose down
```

### What to Explain

Compose lets us define services in YAML instead of writing long `docker run` commands.

### Docker Concept

- Compose file
- Services
- Declarative configuration
- Application stack lifecycle

### Speaker Message

> Docker Compose is our system manifest. It tells Docker what services exist and how they should run.

---

## Stage 7 — Expose the App and Explain Networking

### What Happens

Use Compose ports:

```yaml
services:
  web:
    build: .
    ports:
      - "8000:8000"
```

### What to Explain

The app runs inside a container. The browser is outside the container. Publishing a port creates a path from the host to the container.

Explain:

```text
Host port 8000 → Container port 8000
```

Also introduce the idea that Docker containers have their own network space.

### Docker Concept

- Port publishing
- Host network vs container network
- Bridge network
- External access

### Speaker Message

> The app is running, but the outside world cannot reach it unless we publish a port.

---

## Stage 8 — Logs and Debugging

### What Happens

Show logs:

```bash
docker compose logs
```

Follow logs:

```bash
docker compose logs -f web
```

Show running services:

```bash
docker compose ps
```

Enter the container:

```bash
docker compose exec web sh
```

Inside the container, demonstrate simple commands:

```bash
ls
pwd
python manage.py check
```

### What to Explain

Containers are isolated, but not invisible. Docker gives us ways to inspect and debug them.

### Docker Concept

- Logs
- Container process output
- `docker compose ps`
- `docker compose exec`
- Shell access inside running containers

### Speaker Message

> If something breaks, we need to inspect the container, read its logs, and sometimes enter it.

---

## Stage 9 — Development Workflow with Bind Mounts

### Why This Stage Exists

So far, the app code is copied into the image during build. If we change code locally, the running container does not automatically change unless we rebuild.

For development, we want live updates.

### What Happens

Add a bind mount:

```yaml
services:
  web:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - .:/app
```

Now local files are mapped into the container.

### What to Demonstrate

Change a file locally and show that the running application sees the change.

### Docker Concept

- Bind mounts
- Local directory mapping
- Development workflow
- Difference between image contents and mounted files

### Speaker Message

> In production, we usually run the image as built. In development, we can mount local code into the container for faster iteration.

---

## Stage 10 — Two Environments

### What Happens

Create two different ways to run the app:

1. Normal environment on port `8000`
2. Development environment on port `8080` with bind mount/live updates

Possible approach:

- `compose.yml`
- `compose.dev.yml`
- `.env`
- `.env.dev`

Example idea:

```yaml
services:
  web:
    build: .
    ports:
      - "8080:8000"
    volumes:
      - .:/app
    env_file:
      - .env.dev
```

### Docker Concept

- Runtime configuration
- Compose override files
- Environment files
- Same image, different runtime behavior

### Speaker Message

> Docker is useful not only for deployment. It also helps create repeatable development environments.

---

## Stage 11 — Identify the Database Problem

### What Happens

Point out that the app still uses SQLite.

Current situation:

```text
RecipeVault app → SQLite file
```

Problems:

- SQLite is a file inside/local to the application environment.
- It is not ideal for a production-style multi-container system.
- If the container is recreated incorrectly, local state can be lost.
- Multiple app instances cannot safely share a local SQLite file in this architecture.

### Docker Concept

- State should be separated from app containers
- App container should be replaceable
- Database should be its own service

### Speaker Message

> The app container should not be the place where important production data lives.

---

## Stage 12 — Add PostgreSQL Container

### What Happens

Add a database service:

```yaml
services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      DB_HOST: db
      DB_NAME: recipevault
      DB_USER: recipeuser
      DB_PASSWORD: recipepass

  db:
    image: postgres:16
    environment:
      POSTGRES_DB: recipevault
      POSTGRES_USER: recipeuser
      POSTGRES_PASSWORD: recipepass
```

Initially, you may expose the database port for demonstration:

```yaml
ports:
  - "5432:5432"
```

This can later be removed to show why internal networking is better.

### What to Explain

We did not install PostgreSQL on the host machine. We are running PostgreSQL as a container.

### Docker Concept

- Multi-container application
- Using prebuilt images
- Database as a service
- Environment variables
- Service configuration

### Speaker Message

> Instead of setting up a whole database server manually, we add a database container to the application stack.

---

## Stage 13 — Add Database Volume

### Problem

If PostgreSQL stores data only inside the container filesystem, the data may be lost when the container is removed and recreated.

### What Happens

Add a named volume:

```yaml
services:
  db:
    image: postgres:16
    environment:
      POSTGRES_DB: recipevault
      POSTGRES_USER: recipeuser
      POSTGRES_PASSWORD: recipepass
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

### What to Demonstrate

1. Add data.
2. Stop/recreate containers.
3. Show data persists.

### Docker Concept

- Named volumes
- Persistent data
- Container filesystem vs volume storage
- Database persistence

### Speaker Message

> Containers are disposable. Data is not. Volumes are how Docker keeps important data outside the container lifecycle.

---

## Stage 14 — Service Dependencies

### Problem

The web app depends on the database. The database may take time to start.

If the app starts first, it may fail because the database is not ready.

### What Happens

Add `depends_on`:

```yaml
services:
  web:
    build: .
    depends_on:
      - db

  db:
    image: postgres:16
```

### What to Explain

`depends_on` controls startup order. It does not automatically guarantee that the database is fully ready to accept connections unless combined with readiness checks.

### Docker Concept

- Service dependency
- Startup order
- Compose orchestration

### Speaker Message

> The app depends on the database, so Compose should start the database before the app.

---

## Stage 15 — Healthchecks

### Problem

A container can be running while the service inside is not ready.

For example, PostgreSQL may be running but not yet ready to accept connections.

### What Happens

Add a healthcheck:

```yaml
services:
  db:
    image: postgres:16
    environment:
      POSTGRES_DB: recipevault
      POSTGRES_USER: recipeuser
      POSTGRES_PASSWORD: recipepass
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U recipeuser -d recipevault"]
      interval: 5s
      timeout: 5s
      retries: 5

  web:
    build: .
    depends_on:
      db:
        condition: service_healthy
```

### Docker Concept

- Healthcheck
- Readiness
- Stable startup
- Running vs ready

### Speaker Message

> Running is not the same as ready. Healthchecks let Docker know when a service is actually usable.

---

## Stage 16 — Restart Policies

### Problem

Containers are processes. Processes can crash. If a service fails, someone would normally need to restart it manually.

### What Happens

Add restart policies:

```yaml
services:
  web:
    restart: unless-stopped

  db:
    restart: unless-stopped
```

### Docker Concept

- Container lifecycle
- Failure recovery
- Restart policies
- Long-running services

### Speaker Message

> A restart policy tells Docker what to do when a container exits unexpectedly.

---

## Stage 17 — Internal Networking and Removing Public Database Exposure

### Current Issue

When first setting up the database, we may expose it using:

```yaml
ports:
  - "5432:5432"
```

This makes sense for demonstration, but it is not ideal for the final system.

The database does not need to be publicly reachable. Only the app needs to talk to it.

### What Happens

Remove the public database port.

Use internal service communication:

```yaml
services:
  web:
    environment:
      DB_HOST: db

  db:
    image: postgres:16
```

### What to Explain

Inside Docker Compose, services can communicate by service name.

```text
web container → db container
```

The hostname is:

```text
db
```

Also explain localhost:

```text
Inside web container, localhost = web container itself.
Inside db container, localhost = db container itself.
Your laptop localhost = your laptop.
```

### Docker Concept

- Internal Docker network
- Service discovery
- Service names as hostnames
- Reducing external exposure
- Public vs private services

### Speaker Message

> The database should live inside the Docker network. It does not need a public gate to the outside world.

---

## Stage 18 — Add Nginx as Public Reverse Proxy

### Problem

The app container should not be the only public-facing entry point. We want a web server/proxy container in front.

This is not about deeply teaching Nginx. It is about demonstrating that infrastructure components can also be containers.

### What Happens

Add an Nginx service:

```yaml
services:
  proxy:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx/default.conf:/etc/nginx/conf.d/default.conf:ro
    depends_on:
      - web

  web:
    build: .
    expose:
      - "8000"
```

### What to Explain

Only Nginx is exposed publicly. The app is available only inside the Docker network.

```text
Browser → Nginx → RecipeVault app
```

### Docker Concept

- Separate infrastructure service
- Reverse proxy container
- `ports` vs `expose`
- Public service vs internal service
- Bind-mounted configuration
- Read-only mount

### Speaker Message

> We are not adding Nginx to learn Nginx. We are adding it to show how Docker lets us run infrastructure as part of the application system.

---

## Stage 19 — Serve Media Through Shared Volume

### Problem

Recipe images/media files are currently handled by the app. In a more production-style setup, Nginx can serve media/static files directly.

### What Happens

Create a shared media volume:

```yaml
services:
  web:
    volumes:
      - media_data:/app/media

  proxy:
    image: nginx:alpine
    volumes:
      - media_data:/media:ro

volumes:
  media_data:
```

Nginx reads media from the same volume that the app writes to.

### What to Explain

The app writes uploaded recipe images. Nginx reads the files and serves them directly.

The app can have read-write access:

```text
media_data:/app/media
```

Nginx can have read-only access:

```text
media_data:/media:ro
```

### Docker Concept

- Shared volumes
- Read-write mount
- Read-only mount
- Separation of responsibility
- Persistent media storage

### Speaker Message

> One container writes the files. Another container reads and serves them. Docker volumes allow controlled sharing between containers.

---

## Stage 20 — Final Single-App Containerized System

At this stage, the system is:

```text
Browser
  ↓
Nginx container
  ↓
RecipeVault app container
  ↓
PostgreSQL container
  ↓
postgres_data volume

RecipeVault writes media → media_data volume → Nginx reads media
```

### Final Properties

- Nginx is the only public container.
- App container is internal.
- Database container is internal.
- Database data persists.
- Media files persist.
- Nginx can read media directly.
- App and database communicate inside Docker network.

### Docker Concepts Covered

- Dockerfile
- Image
- Container
- Compose service
- Port publishing
- Internal networking
- Environment variables
- Logs
- Exec
- Bind mounts
- Volumes
- Multi-container app
- Service dependency
- Healthcheck
- Restart policy
- Public/private container boundaries

### Speaker Message

> We now have a complete containerized application system, not just one container running an app.

---

## Stage 21 — Scaling the Application

### Problem

One app container is still a single app instance. If it fails or becomes overloaded, we have no additional app instance to receive traffic.

### What Happens

Run multiple app containers.

Possible approach 1:

```bash
docker compose up --scale web=2
```

Possible approach 2, easier for explicit Nginx configuration:

```yaml
services:
  web1:
    build: .
    expose:
      - "8000"

  web2:
    build: .
    expose:
      - "8000"

  proxy:
    image: nginx:alpine
```

Nginx load balances between `web1` and `web2`.

### What to Explain

The app image can create multiple running containers.

State must stay outside the app containers:

- Database state goes to PostgreSQL.
- Uploaded files go to media volume.
- App containers should be replaceable.

### Docker Concept

- Same image, multiple containers
- Horizontal scaling
- Stateless app containers
- Shared external state
- Load balancing

### Speaker Message

> The reason scaling works is that the app containers do not own the important state. They can be replaced or multiplied.

---

# 5. Final Architecture Explanation

The final architecture should be explained like this:

1. The browser sends traffic only to Nginx.
2. Nginx is the only externally exposed service.
3. Nginx forwards application requests to one of the RecipeVault app containers.
4. The app containers perform backend logic.
5. The app containers communicate with PostgreSQL over the internal Docker network.
6. PostgreSQL stores data in a persistent named volume.
7. Uploaded recipe images are written to a media volume.
8. Nginx reads media files directly from the media volume using read-only access.
9. The database is not publicly exposed.
10. The app containers are not publicly exposed.
11. Only necessary traffic is routed internally.
12. Multiple app containers can run from the same image.

Final diagram:

```text
                    Browser
                       ↓
              Public port: Nginx
                       ↓
        ┌──────────────┴──────────────┐
        ↓                             ↓
  RecipeVault web1              RecipeVault web2
        ↓                             ↓
        └──────────────┬──────────────┘
                       ↓
              PostgreSQL container
                       ↓
              postgres_data volume

Media:
RecipeVault writes → media_data volume → Nginx reads
```

---

# 6. Docker Concepts Covered

By the end, participants should understand:

1. Local setup problem
2. Reproducible environment
3. Dockerfile
4. Base image
5. Build context
6. `.dockerignore`
7. Image
8. Container
9. Image vs container
10. Container process
11. Port publishing
12. Docker Compose
13. Compose services
14. YAML-based infrastructure definition
15. Environment variables
16. `.env` files
17. Logs
18. Exec into containers
19. Bind mounts
20. Development vs normal runtime
21. Multi-container application
22. Official/prebuilt images
23. PostgreSQL container
24. Named volumes
25. Data persistence
26. Service dependencies
27. `depends_on`
28. Healthchecks
29. Restart policies
30. Docker internal networking
31. Service names as hostnames
32. Public vs private services
33. `ports` vs `expose`
34. Nginx as proxy container
35. Bind-mounted configuration files
36. Shared named volumes
37. Read-only mounts
38. Scaling app containers
39. Load balancing
40. Stateless app containers
41. External/shared state

---

# 7. Suggested Hands-On Branches

Prepare the repository with branches so participants can recover if they get stuck.

```text
main
  Local RecipeVault app with SQLite

01-dockerfile
  Dockerfile added and image can be built

02-compose-basic
  App runs with Docker Compose

03-ports-logs-exec
  Port publishing, logs, and exec demonstrated

04-dev-bind-mount
  Development bind mount and environment file setup

05-postgres
  PostgreSQL container added

06-postgres-volume
  PostgreSQL persistence added using named volume

07-depends-health-restart
  depends_on, healthcheck, and restart policies added

08-internal-network
  Database no longer publicly exposed; app uses db hostname

09-nginx-proxy
  Nginx added as public reverse proxy

10-shared-media-volume
  Media volume shared between app and Nginx

11-scale-app
  Multiple app containers behind Nginx
```

---

# 8. Suggested Timing for 1.5–2 Hours

## 0:00–0:10 — App and Problem

- Show RecipeVault locally
- Run setup script
- Run app
- Show UI/admin/media
- State “works on my machine” problem

## 0:10–0:30 — Dockerfile, Image, Container

- Explain Dockerfile
- Build image
- Run container
- Explain image vs container
- Explain port publishing

## 0:30–0:45 — Compose and Debugging

- Move to Docker Compose
- Show services
- Show logs
- Show exec

## 0:45–1:00 — Development Workflow

- Add bind mount
- Add dev environment
- Run normal and dev environments on different ports

## 1:00–1:20 — PostgreSQL and Persistence

- Add PostgreSQL container
- Explain database as a service
- Add named volume
- Demonstrate persistence

## 1:20–1:35 — Dependencies, Health, Restart, Internal Network

- Add depends_on
- Add healthcheck
- Add restart policy
- Remove public DB port
- Explain service names and internal networking

## 1:35–1:50 — Nginx and Shared Media

- Add Nginx proxy
- Explain ports vs expose
- Share media volume
- Nginx reads media directly

## 1:50–2:00 — Scaling and Recap

- Add second app instance
- Nginx load balances
- Recap final architecture
- Recap Docker concepts learned

---

# 9. Important Speaker Framing

Use this repeatedly:

> We are not adding this technology to learn the technology. We are adding it because it demonstrates a Docker concept.

Examples:

| Component | Do Not Teach As | Teach As Docker Concept |
|---|---|---|
| Django app | Django programming | App process packaged into image/container |
| setup script | Django setup | Repeatable setup step inside environment |
| requirements.txt | Python-only concept | Dependency list that motivates Dockerfile |
| Dockerfile | Random config file | Environment recipe/blueprint |
| Docker image | Running app | Built reusable package |
| Container | VM | Running instance of image |
| Compose | Tool convenience only | System manifest for services |
| PostgreSQL | Database administration | Separate service container |
| Volume | Folder only | Persistent storage outside container lifecycle |
| Nginx | Web server deep dive | Public proxy container and traffic boundary |
| Bind mount | File sync trick | Development workflow and host-container file mapping |
| Healthcheck | DB detail | Container readiness signal |
| Restart policy | Production magic | Container lifecycle recovery |
| Scaling | Performance topic only | Same image creates multiple containers |

---

# 10. Final Closing Message

End the workshop with this idea:

> A simple app becomes a deployable system when we separate code, configuration, services, networking, and storage.

Then summarize:

```text
Code → Dockerfile → Image → Container
Container → Compose service
Services → Network
State → Volumes
Config → Environment variables
Traffic → Nginx
Database → PostgreSQL container
Debugging → logs and exec
Reliability → depends_on, healthcheck, restart
Scaling → multiple app containers from the same image
```

Final statement:

> Docker is not only about running one container. It is about defining and running an application system in a repeatable way.

---

# 11. Reference Links

Use official documentation while preparing commands and explanations:

- Dockerfile overview: https://docs.docker.com/build/concepts/dockerfile/
- Dockerfile reference: https://docs.docker.com/reference/dockerfile/
- Docker Compose overview: https://docs.docker.com/compose/
- Compose file reference: https://docs.docker.com/reference/compose-file/
- Compose services: https://docs.docker.com/reference/compose-file/services/
- Compose networking: https://docs.docker.com/compose/how-tos/networking/
- Compose volumes: https://docs.docker.com/reference/compose-file/volumes/
- Startup order in Compose: https://docs.docker.com/compose/how-tos/startup-order/
