# SmartES — Personal Ecosystem Platform

SmartES is a modular, self-hosted personal ecosystem platform built to evolve over many years — starting as a browser-based dashboard and eventually expanding into a full cross-device ecosystem with native agents and an AI assistant layer.

This project prioritizes maintainability, modularity, security, and long-term extensibility over speed of delivery.

---

## Development Layers

### Layer 1 — Browser-Based Web Ecosystem (current focus)
A fully browser-accessible control panel. No native apps, no device agents yet. This layer is being built to allow future layers to plug in without major rewrites.

### Layer 2 — Device Agent Ecosystem (not started)
Native Android/Windows agents reporting system info (battery, storage, CPU, RAM, etc.) through APIs only. Business logic stays server-side.

### Layer 3 — AI Ecosystem (not started)
An AI assistant layer that consumes APIs (never touches the database directly) to search, automate, and answer questions across the ecosystem.

---

## Tech Stack

**Backend:** Python, Django, Django REST Framework, Django Channels (planned)
**Frontend:** Plain HTML, CSS, JavaScript — no frontend framework, no TypeScript
**Databases:**
- **MySQL** — structured relational data (users, auth, files metadata, folders, notes, sessions, permissions)
- **MongoDB** — high-volume/flexible data (activity logs, audit logs, future telemetry, future AI memory)
**Storage:** Local filesystem, abstracted behind a storage backend layer (`cloud/storage.py`) so future providers (S3, etc.) can be swapped in without touching business logic
**Communication:** REST APIs, WebSockets (planned for Messaging), MQTT (reserved for future device agents)

---

## Features Built So Far

- **Dashboard** — live stats bar (files, notes, sessions, devices online) + module card grid
- **Notes** — create, pin/unpin, delete
- **Personal Cloud** — nested folders, file upload/download with live progress (speed, ETA, cancel), image preview, storage abstraction layer
- **Clipboard Hub** — clipboard history, save-as-snippet, one-click copy to device clipboard
- **Device Sessions** — tracks every browser/device login, live online/offline status, remote logout, IP/browser/OS detection
- **Activity Feed** — every meaningful action (file uploads, note edits, logins, etc.) logged to MongoDB with full device context (who, what, from which device/browser/IP, when — in local timezone)

## Not Yet Built

- Messaging Center (deferred — will introduce Django Channels/WebSockets)
- Project Workspace (tasks + attachments)
- Download Center (external download queue/history)
- Settings (account & security page)
- Search (cross-module search)
- Layer 2 (device agents) and Layer 3 (AI assistant)

---

## Project Structure
BijayES Ecosystem/

├── bijayes_server/       # Django project settings, root urls, asgi/wsgi

    ├── core/                 # Shared utilities: Mongo connection layer, activity logging

    ├── dashboard/            # Dashboard home page, stats aggregation

    ├── notes/                # Notes module

    ├── cloud/                # Personal Cloud: folders, files, storage abstraction

    ├── clipboard/            # Clipboard Hub module

    ├── device_sessions/      # Browser/device session tracking (NOT Layer 2 device agents)

    ├── devices/              # Reserved for Layer 2 native device agents (not yet built)

    ├── activity/             # Activity Feed (reads from MongoDB)

    ├── api/                  # Shared/future API endpoints
    
    ├── templates/            # All HTML templates, organized by app

    ├── static/               # CSS, JS, images

    ├── media/                # User-uploaded files (gitignored)

    └── manage.py



**Note on naming:** `device_sessions` (browser/login tracking, Layer 1) and `devices` (physical device agents, Layer 2) are intentionally separate apps — don't confuse them.

---

## Local Setup

1. Clone the repo and create a virtual environment:
```bash
   git clone https://github.com/bijayshankarj/SmartES
   cd "BijayES Ecosystem"
   python -m venv virt
   virt\Scripts\activate
   pip install -r requirements.txt
```

2. Install and run **MySQL** locally. Create the database:
```sql
   CREATE DATABASE smartes_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   CREATE USER 'smartes_user'@'localhost' IDENTIFIED BY 'your-password';
   GRANT ALL PRIVILEGES ON smartes_db.* TO 'smartes_user'@'localhost';
   FLUSH PRIVILEGES;
```

3. Install and run **MongoDB Community Server** locally (runs as a Windows service by default).

4. Create a `.env` file in the project root:
```env
   DB_NAME=smartes_db
   DB_USER=smartes_user
   DB_PASSWORD=your-password
   DB_HOST=localhost
   DB_PORT=3306

   MONGO_HOST=localhost
   MONGO_PORT=27017
   MONGO_DB_NAME=smartes_logs
```

5. Run migrations and start the server:
```bash
   python manage.py migrate
   python manage.py createsuperuser
   python manage.py runserver
```

6. Visit `http://localhost:8000`, log in, and explore.

---

## Design Principles Followed

- Every user-owned model is scoped with `get_object_or_404(Model, pk=pk, owner=request.user)` — no cross-user data leaks, even via guessed URLs.
- All configuration (DB credentials, hosts) lives in environment variables, never hardcoded.
- Storage access always goes through `cloud/storage.py`, never Django's storage classes directly — keeps future storage-provider swaps isolated to one file.
- All Mongo access goes through `core/mongo.py`'s `get_collection()` — a single point of control for the document store.
- Every meaningful user action logs to `core/activity.py`'s `log_activity(request, action, details)` — always pass the full `request` object, not just `request.user`, so device context is captured automatically.
- Timezone: `TIME_ZONE = "Asia/Kolkata"`, `USE_TZ = True` — data stored in UTC, displayed in IST.

---

## Git Workflow

```bash
git status              # see what changed
git add .                # stage everything
git commit -m "message"  # snapshot
git push                 # back up to GitHub
```

Working solo on `main` — no branching strategy needed yet.

---

## Roadmap (next up)

1. Messaging Center — Django Channels, in-memory channel layer for now, Redis later if scaling beyond one process
2. Project Workspace
3. Download Center
4. Settings page
5. Cross-module Search
6. Layer 2: Device Agents
7. Layer 3: AI Assistant