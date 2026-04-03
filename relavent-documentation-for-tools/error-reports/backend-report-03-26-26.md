## Backend Timeout & DB Connection Report (2026-03-26)

### Summary

User registration from the Android app reaches the Python REST API but the request hangs until the client times out. Server logs show repeated database connection failures when handling `POST /v1/auth/register`, caused by an unreachable MySQL host.

### Evidence from Logs

- Client-side behavior:
  - User fills registration form and taps **Create Account**.
  - After a long wait, the app reports a timeout.
- Server-side logs (FastAPI + SQLAlchemy + aiomysql):
  - `TimeoutError: [Errno 110] Connection timed out`
  - `pymysql.err.OperationalError: (2003, "Can't connect to MySQL server on '167.172.207.98'")`
  - Traceback shows the error occurring while handling `auth.router.register(...)` when executing a database query through `session.execute(stmt)`.

### Relevant Backend Code

- `python-api/api-files/database.py`
  - Reads `DATABASE_URL` from the environment and creates the async engine:
    - `DATABASE_URL=mysql+aiomysql://jacob:J%40cob76247@167.172.207.98:3306/BoardGameTracker`
  - Uses `create_async_engine(DATABASE_URL, pool_pre_ping=True, ...)` and exposes `async_session_maker` and `get_session()`.
- `python-api/api-files/auth/router.py`
  - `@router.post("/register", ...) async def register(body: RegisterRequest, session: AsyncSession = Depends(get_session))`
  - Registration performs a SELECT to check for existing users and then inserts a new user; both depend on a healthy DB connection.
- `python-api/api-files/main.py`
  - Uses `check_db_connection()` in `/health` and shares the same engine.

### Root Cause (Backend)

1. **MySQL host unreachable from API runtime**
   - `DATABASE_URL` points to `167.172.207.98:3306`.
   - `aiomysql` attempts to open a TCP connection and times out (`Errno 110`), which then surfaces as a SQLAlchemy `OperationalError (2003)`.
   - This indicates that, from wherever the API is running (local machine, server, container), it cannot successfully reach that MySQL host/port (firewall, DNS, networking, or service address mismatch).

2. **Request-level timeout experienced by the client**
   - The registration endpoint waits on the DB connection until it errors/timeouts.
   - The Android client has finite network timeouts; by the time the backend either fails or hangs, the client surfaces this as a generic “timeout” to the user.

### Recommended Backend Fixes

1. **Verify and correct `DATABASE_URL`**
   - Confirm that:
     - The MySQL server is actually running at `167.172.207.98` on port `3306`.
     - Credentials (`user`, `password`, database name) match the DB configuration.
   - If the API is in Docker or another container, ensure:
     - The host is reachable from inside the container (use a service name or internal IP, not necessarily the public IP).
     - The Docker network permits traffic to the DB (correct network, no blocked ports).

2. **Check firewall and network routing**
   - On the host where MySQL runs:
     - Ensure port `3306` is open to the machine that runs the API (or to its Docker network).
   - On any cloud environment (if applicable):
     - Verify security groups / inbound rules allow connections from the API host to `167.172.207.98:3306`.

3. **Run a direct connectivity test from the API environment**
   - From the same machine / container where `uvicorn main:app` is running:
     - Test TCP connectivity to `167.172.207.98:3306` (e.g. `nc -vz 167.172.207.98 3306` or an equivalent tool).
   - If this fails, fix networking first (host, firewall, or routing) before revisiting the API.

4. **Consider using a local or Dockerized DB for development**
   - For local/dev work, it may be simpler to:
     - Run MySQL locally (e.g. `127.0.0.1:3306`) and set `DATABASE_URL` accordingly.
     - Or run MySQL in Docker on the same Docker network as the FastAPI container, referencing it by service name.
   - Update `.env` under `python-api/api-files` with a `DATABASE_URL` that reflects this topology.

5. **Fail fast and return a clearer HTTP response**
   - Currently, failed DB connections bubble up as a timeout that the client experiences as “no response”.
   - Improvements:
     - Tighten DB connection timeouts (e.g. via MySQL driver / SQLAlchemy options) so failures happen quickly.
     - Optionally wrap connection failures for critical endpoints in a controlled exception and return:
       - `503 Service Unavailable` with an error body like `{ "error": { "code": "database_unavailable", "message": "The database is currently unreachable." }, "details": [] }`.
   - This would let the Android app distinguish “backend is down” from auth or validation problems and present a friendlier message.

6. **Monitor `/health` to detect DB outages**
   - The `/health` endpoint already calls `check_db_connection()` and returns 503 when the DB is disconnected.
   - Use this endpoint:
     - In monitoring to detect when DB connectivity is lost.
     - Optionally in the client (or a small admin tool) to confirm backend readiness before attempting expensive operations like registration.

### Client Impact & Current Behavior

- The Android client:
  - Successfully validates registration inputs and sends a `POST /v1/auth/register` request.
  - Encodes the body correctly and waits for the server.
  - Encounters a network timeout because the backend blocks on DB connection.
- This is **not** a client-side contract issue anymore (payload is correct); it is a backend infrastructure/configuration problem.

### Next Steps

1. Fix DB connectivity:
   - Ensure `DATABASE_URL` points to a reachable MySQL instance and networking allows the connection.
2. Once DB is reachable:
   - Re-run registration and confirm:
     - The user is written to the DB.
     - The API returns `201 Created` with tokens.
3. Optionally:
   - Add better error mapping in the API to surface DB outages as 5xx with a clear error code.
   - Use `/health` in CI/monitoring and possibly in client-side diagnostics.

