# Board Game Stat Tracker — REST API Documentation

**API name:** The Librarian  
**Base URL:** Use version prefix (e.g. `/v1/`).  
**Client:** Kotlin Android app; future web and iPhone. Real-time live scoring is handled by a separate Elixir/WebSocket service.  
**Format:** JSON. Send `Accept: application/json`; responses use `Content-Type: application/json` (UTF-8).

---

## 1. Overview

This API provides authentication, user and publisher management, games, stat sets, sessions (create/join/list/end; live scoring is via WebSocket), followers, following feed, session history, stats, export, and publisher dashboard. One endpoint per logical operation is used where possible (e.g. a single session-details endpoint for history, feed, and room).

### Design assumptions

- **Session limit:** Enforced on create (403 when at weekly limit). Quota exposed in current user profile. Designers (users with designer flag) are exempt.
- **Win/loss:** From a per-player boolean tracked stat (e.g. `player_won`). "Won"/"Lost" in responses are derived from that stat.
- **Reference data:** `GET /scopes` and `GET /data-types` are read-only; new values can be added via DB.
- **Feed visibility:** User-level default (public/private) plus per-session override. New users default to public.
- **Publisher:** Separate login and resources; multiple user accounts can be linked to one publisher.

---

## 2. Authentication

All authenticated requests use: `Authorization: Bearer <accessToken>`. Publisher tokens are distinct (publisher-scoped).

| Method | Endpoint | Description | Request body | Response | Status codes |
|--------|----------|-------------|--------------|----------|--------------|
| POST | `/auth/login` | User login | `{ "emailOrUsername", "password" }` | `{ "accessToken", "refreshToken", "expiresIn", "user": { "id", "username", "email", "designer" } }` | 200, 401 |
| POST | `/auth/register` | User registration | `{ "username", "email", "password" }` | Same shape as login (201 + tokens) | 201, 400, 409 |
| POST | `/auth/publisher/login` | Publisher login (e.g. for future web) | `{ "emailOrUsername", "password" }` or publisher-specific | `{ "accessToken", "refreshToken", "expiresIn", "publisher": { "id", "name", ... } }` | 200, 401 |
| POST | `/auth/refresh` | Refresh access token | `{ "refreshToken" }` | `{ "accessToken", "expiresIn" }` | 200, 401 |
| POST | `/auth/forgot-password` | Request password reset | `{ "email" }` | 200 + message (no leak if email missing) | 200 |
| POST | `/auth/logout` | Invalidate refresh token (optional) | — or `{ "refreshToken" }` | — | 204 |

- **409** on register: duplicate username or email.
- **Username availability:** `GET /users/check-username?username=<value>` → 200 `{ "available": true|false }`.

---

## 3. Reference data

| Method | Endpoint | Description | Response |
|--------|----------|-------------|----------|
| GET | `/scopes` | List scopes (e.g. player, table) | `{ "scopes": [ { "id", "scope" } ] }` |
| GET | `/data-types` | List data types (e.g. integer, string, boolean) | `{ "dataTypes": [ { "id", "dataType" } ] }` |

Auth may be optional for onboarding; otherwise same as rest of API.

---

## 4. Games

| Method | Endpoint | Description | Request | Response | Status codes |
|--------|----------|-------------|---------|----------|--------------|
| GET | `/games` | List games | Query: `filter=my|all|recent`, `search`, `page`, `limit` | `{ "games": [...], "total", "page" }` | 200 |
| GET | `/games/{gameId}` | Game details | — | Game + stat sets summary + my stats (when authenticated) | 200, 404 |
| POST | `/games` | Create game | Body: `{ "gameName", "description", "minPlayerCount", "maxPlayerCount", "canWin" }` | 201 + full game | 201, 400, 409 |

- **Filter:** `my` = user has played/created; `all` = all games; `recent` = e.g. last 30 days.
- **409:** Duplicate game name (or return existing per product choice).
- **Game list** with `search` also serves duplicate check / search (no separate `/games/search` required).

---

## 5. Stat sets

Stat sets are scoped to a game.

| Method | Endpoint | Description | Request | Response | Status codes |
|--------|----------|-------------|---------|----------|--------------|
| GET | `/games/{gameId}/stat-sets` | List stat sets for game | — | `{ "statSets": [ { "id", "setName", "stats": [ { "statName", "dataTypeId", "scopeId" } ] } ] }` | 200, 404 |
| GET | `/games/{gameId}/stat-sets/{statSetId}` | Stat set details | — | Full stat set with stat definitions | 200, 404 |
| POST | `/games/{gameId}/stat-sets` | Create stat set (or build on existing) | Body: `{ "setName", "stats": [...] }` or `{ "setName", "sourceStatSetId" }` | 201 + stat set | 201, 400, 404, 422 |

- Use **sourceStatSetId** to create a new stat set by copying an existing one.

---

## 6. Sessions

Sessions are created and managed via REST; live score updates use the Elixir WebSocket service. Session list is canonical: one endpoint for both active sessions and history.

| Method | Endpoint | Description | Request | Response | Status codes |
|--------|----------|-------------|---------|----------|--------------|
| GET | `/sessions` | List sessions (active or history) | Query: `active=true|false`, `from`, `to`, `gameId`, `page`, `limit` | `{ "sessions": [...], "total", "page" }` | 200 |
| GET | `/sessions/{sessionId}` | Session details | — | Session + game + stat set + players + tracked stats + visibility + won/lost per player | 200, 403, 404 |
| POST | `/sessions` | Create session | Body: `{ "gameId", "statSetId", "invitedUserIds": [], "nonAppPlayerNames": [] }` | 201 + `{ "sessionId", "sessionKey", ... }` | 201, 403, 404, 409, 422 |
| PATCH | `/sessions/{sessionId}` | End session / update | Body: e.g. `{ "timeEnded", "visibilityOverride" }` or `{ "status": "ended" }` | 200 + session | 200, 403, 404, 422 |
| DELETE | `/sessions/{sessionId}` | Delete session | — | — | 204, 403, 404 |
| POST | `/sessions/join` | Join by session key | Body: `{ "sessionKey" }` | 200 + session (id, key, game, etc.) | 200, 404, 409 |
| GET | `/sessions/invites` | List session invites for current user | Query: `pending=true|false`, `page`, `limit` | `{ "invites": [...], "total", "page" }` | 200, 401 |

- **Session list:** Use `active=true` for active sessions (e.g. Live Sessions list); `active=false` for history. Same endpoint.
- **403 on POST /sessions:** User at weekly session limit (designers exempt).
- **Join:** Idempotent — if caller already in session, return 200 with current session. 404 = session not found; 409 = full, already ended, or other conflict.
- **Session invites:** Returns invites where current user is the invitee. `pending=true` (default) filters to invites for active sessions where user hasn't joined yet; `pending=false` returns all invites (including for ended sessions or already joined). Each invite includes: `{ "id", "sessionId", "invitedAt", "session": { ... } }` with session details (game, creator, timeStarted, etc.).
- **Session quota** is included in `GET /users/me` as `sessionQuota: { "sessionsUsedThisWeek", "sessionsLimitPerWeek" }` (designers: limit null or unlimited sentinel). Optional: `GET /users/me/session-quota` for lightweight polling.

---

## 7. Users and profile

| Method | Endpoint | Description | Request | Response | Status codes |
|--------|----------|-------------|---------|----------|--------------|
| GET | `/users/me` | Current user profile + quota | — | User + `sessionQuota`; optional `quickStats` (totalGames, winRate, sessionsThisWeek, favoriteGame) | 200, 401 |
| PATCH | `/users/me` | Update profile | Body: partial `{ "username", "email", "bio", "avatarUrl" }` | 200 + user | 200, 400, 401, 409, 422 |
| GET | `/users/{userId}` | Other user profile (public) | — | Public fields: username, bio, avatar, designer, stats summary | 200, 404 |
| GET | `/users/check-username?username=<value>` | Username availability | — | `{ "available": true|false }` | 200 |

- **409** on PATCH: duplicate username or email.
- Check username before register or edit via `/users/check-username`.

---

## 8. User stats

| Method | Endpoint | Description | Response | Status codes |
|--------|----------|-------------|----------|--------------|
| GET | `/users/me/stats` | Current user full stats | Per-game: played, wins, etc. | 200, 401 |
| GET | `/users/{userId}/stats` | Another user's stats | For profile view | 200, 404 |
| GET | `/games/{gameId}/stats` | Current user's stats for that game | played, wins, win rate, etc. | 200, 401, 404 |

---

## 9. Social (followers, following, user search)

| Method | Endpoint | Description | Request | Response | Status codes |
|--------|----------|-------------|---------|----------|--------------|
| GET | `/users/{userId}/followers` | List followers | Query: `page`, `limit`, optional `search` | `{ "followers": [...], "total", "page" }` | 200, 404 |
| GET | `/users/{userId}/following` | List following | Same | Same shape | 200, 404 |
| POST | `/users/{userId}/follow` | Follow user | — | 204 or 200 | 200, 204, 404 |
| DELETE | `/users/{userId}/follow` | Unfollow | — | — | 204, 404 |
| GET | `/users/search` | Search users | Query: `q`, `page`, `limit` | `{ "users": [...], "total", "page" }` | 200 |

- **q** is the search query string (invite flow, find users to follow).
- Follow is idempotent.

---

## 10. Following feed

| Method | Endpoint | Description | Request | Response | Status codes |
|--------|----------|-------------|---------|----------|--------------|
| GET | `/feed` | Sessions from followed users | Query: `page`, `limit`, optional `since` | `{ "sessions": [ { "id", "game", "user", "result", "playedAt", "visibility", ... } ], "total", "page" }` | 200, 401 |

- Only sessions visible to current user (visibility = user default + per-session override). `result` = derived won/lost.

---

## 11. Export

| Method | Endpoint | Description | Request | Response | Status codes |
|--------|----------|-------------|---------|----------|--------------|
| GET | `/users/me/export` | Export stats (primary) | Query: `gameIds`, `from`, `to`, `sessionIds`, `statSetIds`, `preview=true` | If `preview=true`: `{ "sessionCount", "statValueCount", "estimatedSizeBytes" }`; else export JSON/stream | 200, 401, 422 |
| POST | `/users/me/export` | Export with complex filters | Body: `{ "gameIds", "from", "to", "sessionIds", "statSetIds", "preview": true }` | Same | 200, 401, 422 |

- **Primary:** GET with query params. Use POST for very long filter lists.
- **422:** Invalid filter (e.g. invalid date range).

---

## 12. Publishers

Requires publisher authentication. Multiple user accounts can be linked to one publisher.

| Method | Endpoint | Description | Request | Response | Status codes |
|--------|----------|-------------|---------|----------|--------------|
| GET | `/publishers/me` | Publisher profile | — | `{ "id", "name", "designerTagCount", "assignedCount", ... }` | 200, 401 |
| GET | `/publishers/me/designers` | Users assigned designer tag | Query: `page`, `limit` | `{ "designers": [ { "userId", "username", "assignedAt" } ], "total", "page" }` | 200, 401 |
| GET | `/publishers/me/analytics` | Dashboard data | Query: optional date range | Aggregates (sessions by designers, games created, etc.) | 200, 401 |
| POST | `/publishers/me/designers` | Assign designer tag | Body: `{ "userId" }` | 201 or 204 | 201, 204, 400, 401, 404, 409 |
| DELETE | `/publishers/me/designers/{userId}` | Revoke designer tag | — | — | 204, 401, 404 |

---

## 13. Data shapes (summary)

- **Game:** `id`, `gameName`, `description`, `minPlayerCount`, `maxPlayerCount`, `canWin`, `createdAt`. Optional in context: `playCount`, `lastPlayedAt`.
- **Stat set:** `id`, `gameId`, `setName`, `userId` (creator), `stats`: array of `{ id, statName, description, dataTypeId, scopeId }`.
- **Session:** `id`, `sessionKey`, `gameId`, `game` (summary), `statSetId`, `statSet` (summary), `timeStarted`, `timeEnded`, `currentRound`, `visibility`, `players`: array of `{ sessionPlayerId, userId, playerName, isSpectator, won }`, `trackedStats`, optional stat values.
- **Session invite:** `id`, `sessionId`, `invitedAt`, `session` (summary with game, creator, timeStarted, etc.).
- **User (me):** `id`, `username`, `email`, `bio`, `avatarUrl`, `designer`, `sessionQuota`, `defaultSessionVisibility`; optional `quickStats`.
- **User (public):** `id`, `username`, `avatarUrl`, `bio`, `designer`, optional stats summary.
- **Error body:** `{ "error": { "code", "message" }, "details": [] }`.

### HTTP status codes

| Code | Meaning |
|------|---------|
| 200 | OK |
| 201 | Created |
| 204 | No Content |
| 400 | Bad Request (malformed) |
| 401 | Unauthorized |
| 403 | Forbidden (e.g. session limit) |
| 404 | Not Found |
| 409 | Conflict (duplicate, join conflict) |
| 422 | Unprocessable Entity (validation/semantic) |
| 5xx | Server error |

---

## 14. Security

- **Authentication:** JWT in `Authorization: Bearer <token>`. Publisher tokens are distinct (publisher scope).
- **Authorization:** Resource-level (e.g. only session creator/participant can end/delete; only publisher can access `/publishers/me`; only user can PATCH `/users/me`).
- **HTTPS:** Required in production.
- **CORS:** Configure for Kotlin app and future web origin.
- **Rate limiting:** Recommended for auth and export.
- **Sensitive data:** No passwords in responses; password reset via token/side-channel.
- **Content:** `Accept: application/json`; `Content-Type: application/json` (charset utf-8).

---

## 15. Growability

- **Versioning:** URL prefix (e.g. `/v1/`) for future `/v2/` without breaking clients.
- **Extensibility:** Optional JSON fields; clients ignore unknown fields. New scopes/data types via DB and existing endpoints.
- **Backward compatibility:** Add optional request/response fields; avoid removing or changing semantics in same major version.
- **Pagination:** List endpoints use `page` and `limit` (or `cursor` and `limit`) consistently.

---

*Created using AALang and Gab.*
