# The Librarian — REST API (Stub)

Board Game Stat Tracker REST API. Stub implementation with mock data; all routes under `/v1`. Stub auth accepts any Bearer token.

## Requirements

- Python 3.11+
- See `requirements.txt` for dependencies.

## Setup

1. **Database:** Set `DATABASE_URL` in the environment (e.g. in a `.env` file in `api-files` or `python-api`). Example for local MySQL: `DATABASE_URL=mysql+aiomysql://user:password@127.0.0.1:3306/BoardGameTracker`. The app does not use a default URL with credentials; you must provide it.

2. From the **python-api** directory (parent of `api-files`), create a virtual environment and install dependencies:

   ```bash
   cd python-api
   python -m venv .venv
   .venv\Scripts\activate   # Windows
   # source .venv/bin/activate   # macOS/Linux
   pip install -r api-files/requirements.txt
   ```

3. Run the app from the **api-files** directory so that imports resolve correctly.

## Run

From the **api-files** directory:

```bash
cd python-api/api-files
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

- API base:     `http://127.0.0.1:8000`
- OpenAPI docs: `http://127.0.0.1:8000/docs`
- ReDoc:        `http://127.0.0.1:8000/redoc`

## Behaviour

- **Auth:** Any `Authorization: Bearer <token>` is accepted (stub). Reference data (`/v1/scopes`, `/v1/data-types`) is public.
- **Pagination:** List endpoints use `page` (default 1) and `limit` (default 20, max 50).
- **Games:** `POST /v1/games` returns **200** when a new game is created and **211** when a game with the same name already exists (error body includes details).
- **Visibility:** Only `public` and `private` for now (expandable later).

## Generated files

- `main.py` — FastAPI app, `/v1` prefix, exception handlers, router includes
- `dependencies.py` — Stub auth, pagination params
- `schemas_common.py` — Error body, pagination
- `auth/`, `reference/`, `games/`, `stat_sets/`, `sessions/`, `users/`, `stats/`, `social/`, `feed/`, `export/`, `publishers/` — Routers and schemas per domain

Created using AALang and Gab.
