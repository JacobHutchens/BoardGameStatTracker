# Board Game Stat Tracker — Full Schema Update Summary

This document is the single reference for the MySQL database schema. It aligns with the Board Game Stat Tracker REST API (The Librarian) and supports the Kotlin app, with real-time scoring handled by a separate Elixir/WebSocket service.

**Schema name:** `BoardGameTracker`  
**Character set:** utf8  
**Engine:** InnoDB  
**Conventions:** snake_case for table and column names; 1NF, 2NF, 3NF.

---

## 1. Overview

The schema supports:

- **Authentication** — User and publisher login, JWT + refresh tokens, logout, forgot-password.
- **Reference data** — Scopes and data types for stat definitions.
- **Games and stat sets** — Games, stat set definitions per game, stat definitions (name, description, type, scope).
- **Sessions** — Create, join, list, detail, PATCH, DELETE; session key; creator; stat set; visibility; invites.
- **Session players and stats** — Players (app users or non-app names), spectators; tracked stats and player/table stat values.
- **User stats** — Per-user per-game cache (played, wins) for stats endpoints.
- **Social** — Followers, following, user search; feed from followed users’ sessions.
- **Export** — User data export with filters (games, dates, sessions, stat sets).
- **Publishers** — Publisher accounts, designer assignment, publisher auth, analytics.

---

## 2. Tables at a glance

| Table | Purpose |
|-------|--------|
| `user` | User accounts; profile (bio, avatar, designer, default_session_visibility); auth. |
| `game` | Games; name, description, player counts, can_win, created_at. |
| `scope` | Stat scope reference (e.g. player, table). |
| `data_type` | Stat data type reference (e.g. integer, string, boolean). |
| `game_tracked_stat_set` | Stat sets per game (creator user_id, set_name). |
| `game_tracked_stat` | Stat definitions in a set (stat_name, description, data_type_id, scope_id). |
| `session` | Game sessions; creator, game, stat set, session_key, times, visibility_override. |
| `session_player` | Players in a session (user or non-app name, is_spectator). |
| `session_invite` | Invited users per session (POST /sessions invitedUserIds; GET /sessions/invites). |
| `session_tracked_stat` | Stats tracked in a session (from stat set). |
| `player_stat_value` | Recorded stat values per player. |
| `table_stat_value` | Recorded stat values per session (table scope). |
| `user_game_stats_cache` | Aggregated per-user per-game stats (played, wins). |
| `follower` | Follow relationship (user_id = follower, following_user_id = followee). |
| `user_refresh_token` | User refresh tokens for /auth/refresh and logout. |
| `publisher` | Publisher accounts (publisher login). |
| `publisher_refresh_token` | Publisher refresh tokens. |
| `publisher_designer` | Designer tag assignment (publisher → user, assigned_at). |

**Total: 18 tables.**

---

## 3. Change summary (vs original baseline)

### 3.1 New tables

| Table | Purpose |
|-------|--------|
| `user_refresh_token` | Store refresh tokens for user auth; /auth/refresh, /auth/logout. |
| `publisher` | Publisher identity; /auth/publisher/login, GET /publishers/me. |
| `publisher_refresh_token` | Refresh tokens for publisher auth (tokens distinct per API). |
| `publisher_designer` | Link publishers to users with designer tag; /publishers/me/designers; session-limit exemption. |
| `session_invite` | Store invitedUserIds from POST /sessions; read by GET /sessions/invites. |

### 3.2 New columns

| Table | Column | Type | Reason |
|-------|--------|------|--------|
| `user` | `bio` | TEXT NULL | User profile (UserMe / UserPublic). |
| `user` | `avatar_url` | VARCHAR(255) NULL | User profile. |
| `user` | `designer` | TINYINT NOT NULL DEFAULT 0 | Designer flag; session-limit exemption; API responses. |
| `user` | `default_session_visibility` | VARCHAR(45) NOT NULL DEFAULT 'public' | Feed visibility default; per-session override on session. |
| `user` | — | UNIQUE on `email` | Enforce unique email (register/PATCH 409). |
| `game` | `created_at` | DATETIME NOT NULL | Game data shape createdAt. |
| `game_tracked_stat` | `description` | TEXT NULL | Stat set stat definition (StatSet.stats[].description). |
| `session` | `creator_user_id` | INT NOT NULL, FK → user | Session creator; feed “user”; authz; session quota. |
| `session` | `stat_set_id` | INT NOT NULL, FK → game_tracked_stat_set | Session uses one stat set. |
| `session` | `visibility_override` | VARCHAR(45) NULL | Per-session visibility override for feed. |
| `session_player` | `is_spectator` | TINYINT NOT NULL DEFAULT 0 | Session players shape (isSpectator). |

### 3.3 Column changes

| Table | Column | Change | Reason |
|-------|--------|--------|--------|
| `user` | `password_hash` | VARCHAR(45) → VARCHAR(255) | Fit bcrypt hashes. |

### 3.4 Removals

None. All original tables and columns remain in use.

### 3.5 Other

- **follower:** UNIQUE on `(user_id, following_user_id)` for idempotent follow.
- DDL order adjusted so referenced tables are created before dependents; FKs and indexes preserved.

---

## 4. Full table reference

### 4.1 user

| Column | Type | Nullable | Default | Notes |
|--------|------|----------|---------|-------|
| id | INT | NOT NULL | AUTO_INCREMENT | PK. |
| username | VARCHAR(45) | NOT NULL | — | UNIQUE. |
| email | VARCHAR(45) | NOT NULL | — | UNIQUE. |
| password_hash | VARCHAR(255) | NOT NULL | — | Bcrypt. |
| created_at | DATETIME | NOT NULL | — | Backend/audit; not in API response. |
| bio | TEXT | NULL | — | Profile. |
| avatar_url | VARCHAR(255) | NULL | — | Profile. |
| designer | TINYINT | NOT NULL | 0 | Designer flag. |
| default_session_visibility | VARCHAR(45) | NOT NULL | 'public' | Feed visibility default. |

**Indexes:** PK; UNIQUE(id); UNIQUE(username); UNIQUE(email).

---

### 4.2 game

| Column | Type | Nullable | Default | Notes |
|--------|------|----------|---------|-------|
| id | INT | NOT NULL | AUTO_INCREMENT | PK. |
| game_name | VARCHAR(45) | NOT NULL | — | UNIQUE. |
| max_player_count | INT | NULL | — | |
| min_player_count | INT | NULL | — | |
| description | TEXT | NOT NULL | — | |
| can_win | TINYINT | NOT NULL | 1 | |
| created_at | DATETIME | NOT NULL | — | Game.createdAt. |

**Indexes:** PK; UNIQUE(id); UNIQUE(game_name).

---

### 4.3 scope

| Column | Type | Nullable | Default | Notes |
|--------|------|----------|---------|-------|
| id | INT | NOT NULL | AUTO_INCREMENT | PK. |
| scope | VARCHAR(45) | NOT NULL | — | UNIQUE (e.g. player, table). |

**Indexes:** PK; UNIQUE(id); UNIQUE(scope).

---

### 4.4 data_type

| Column | Type | Nullable | Default | Notes |
|--------|------|----------|---------|-------|
| id | INT | NOT NULL | AUTO_INCREMENT | PK. |
| data_type | VARCHAR(45) | NULL | — | e.g. integer, string, boolean. |

**Indexes:** PK; UNIQUE(id).

---

### 4.5 game_tracked_stat_set

| Column | Type | Nullable | Default | Notes |
|--------|------|----------|---------|-------|
| id | INT | NOT NULL | AUTO_INCREMENT | PK. |
| game_id | INT | NOT NULL | — | FK → game. |
| user_id | INT | NOT NULL | — | FK → user (creator). |
| set_name | VARCHAR(45) | NOT NULL | — | |

**Indexes:** PK; UNIQUE(id); INDEX(game_id); INDEX(user_id). **FKs:** game, user.

---

### 4.6 game_tracked_stat

| Column | Type | Nullable | Default | Notes |
|--------|------|----------|---------|-------|
| id | INT | NOT NULL | AUTO_INCREMENT | PK. |
| game_tracked_stat_set_id | INT | NOT NULL | — | FK → game_tracked_stat_set. |
| stat_name | VARCHAR(45) | NOT NULL | — | |
| description | TEXT | NULL | — | StatSet.stats[].description. |
| data_type_id | INT | NOT NULL | — | FK → data_type. |
| scope_id | INT | NOT NULL | — | FK → scope. |

**Indexes:** PK; UNIQUE(id); INDEXes on FKs. **FKs:** game_tracked_stat_set, scope, data_type.

---

### 4.7 session

| Column | Type | Nullable | Default | Notes |
|--------|------|----------|---------|-------|
| id | INT | NOT NULL | AUTO_INCREMENT | PK. |
| creator_user_id | INT | NOT NULL | — | FK → user. |
| game_id | INT | NOT NULL | — | FK → game. |
| stat_set_id | INT | NOT NULL | — | FK → game_tracked_stat_set. |
| session_key | VARCHAR(6) | NOT NULL | — | UNIQUE; join code. |
| time_started | DATETIME | NOT NULL | — | |
| time_ended | DATETIME | NULL | — | NULL = active. |
| current_round | INT | NULL | — | |
| visibility_override | VARCHAR(45) | NULL | — | Per-session override. |

**Indexes:** PK; UNIQUE(id); UNIQUE(session_key); INDEX(game_id); INDEX(stat_set_id); INDEX(creator_user_id). **FKs:** user, game, game_tracked_stat_set.

---

### 4.8 session_player

| Column | Type | Nullable | Default | Notes |
|--------|------|----------|---------|-------|
| id | INT | NOT NULL | AUTO_INCREMENT | PK. |
| session_id | INT | NOT NULL | — | FK → session. |
| user_id | INT | NULL | — | FK → user; NULL = non-app player. |
| player_name | VARCHAR(45) | NOT NULL | — | |
| is_spectator | TINYINT | NOT NULL | 0 | |

**Indexes:** PK; UNIQUE(id); INDEX(user_id); INDEX(session_id). **FKs:** session, user.

---

### 4.9 session_invite

| Column | Type | Nullable | Default | Notes |
|--------|------|----------|---------|-------|
| id | INT | NOT NULL | AUTO_INCREMENT | PK. |
| session_id | INT | NOT NULL | — | FK → session. |
| user_id | INT | NOT NULL | — | FK → user (invitee). |
| invited_at | DATETIME | NOT NULL | — | |

**Indexes:** PK; UNIQUE(id); UNIQUE(session_id, user_id); INDEX(user_id). **FKs:** session, user.

---

### 4.10 session_tracked_stat

| Column | Type | Nullable | Default | Notes |
|--------|------|----------|---------|-------|
| id | INT | NOT NULL | AUTO_INCREMENT | PK. |
| session_id | INT | NOT NULL | — | FK → session. |
| stat_name | VARCHAR(45) | NOT NULL | — | |
| data_type_id | INT | NOT NULL | — | FK → data_type. |
| scope_id | INT | NOT NULL | — | FK → scope. |

**Indexes:** PK; UNIQUE(id); INDEXes on FKs. **FKs:** session, scope, data_type.

---

### 4.11 player_stat_value

| Column | Type | Nullable | Default | Notes |
|--------|------|----------|---------|-------|
| id | INT | NOT NULL | AUTO_INCREMENT | PK. |
| session_tracked_stat_id | INT | NOT NULL | — | FK → session_tracked_stat. |
| session_player_id | INT | NOT NULL | — | FK → session_player. |
| stat_value | VARCHAR(45) | NOT NULL | — | |
| recorded_at | DATETIME | NOT NULL | — | |
| round_number | INT | NULL | — | |

**Indexes:** PK; UNIQUE(id); INDEXes on FKs. **FKs:** session_tracked_stat, session_player.

---

### 4.12 table_stat_value

| Column | Type | Nullable | Default | Notes |
|--------|------|----------|---------|-------|
| id | INT | NOT NULL | AUTO_INCREMENT | PK. |
| session_tracked_stat_id | INT | NOT NULL | — | FK → session_tracked_stat. |
| session_id | INT | NOT NULL | — | FK → session. |
| stat_value | VARCHAR(45) | NOT NULL | — | |
| recorded_at | DATETIME | NOT NULL | — | |
| round_number | INT | NULL | — | |

**Indexes:** PK; UNIQUE(id); INDEXes on FKs. **FKs:** session_tracked_stat, session.

---

### 4.13 user_game_stats_cache

| Column | Type | Nullable | Default | Notes |
|--------|------|----------|---------|-------|
| id | INT | NOT NULL | AUTO_INCREMENT | PK. |
| game_id | INT | NOT NULL | — | FK → game. |
| user_id | INT | NOT NULL | — | FK → user. |
| total_times_played | INT | NOT NULL | — | |
| wins | INT | NULL | — | |

**Indexes:** PK; UNIQUE(id); INDEX(game_id); INDEX(user_id). **FKs:** game, user.

---

### 4.14 follower

| Column | Type | Nullable | Default | Notes |
|--------|------|----------|---------|-------|
| id | INT | NOT NULL | AUTO_INCREMENT | PK. |
| user_id | INT | NOT NULL | — | FK → user (follower). |
| following_user_id | INT | NOT NULL | — | FK → user (followee). |
| followed_at | DATETIME | NOT NULL | — | |

**Indexes:** PK; UNIQUE(id); UNIQUE(user_id, following_user_id); INDEX(user_id); INDEX(following_user_id). **FKs:** user (x2).

---

### 4.15 user_refresh_token

| Column | Type | Nullable | Default | Notes |
|--------|------|----------|---------|-------|
| id | INT | NOT NULL | AUTO_INCREMENT | PK. |
| user_id | INT | NOT NULL | — | FK → user. |
| token_hash | VARCHAR(255) | NOT NULL | — | |
| expires_at | DATETIME | NOT NULL | — | |
| revoked_at | DATETIME | NULL | — | Logout. |
| created_at | DATETIME | NOT NULL | — | Internal. |

**Indexes:** PK; UNIQUE(id); INDEX(user_id). **FK:** user.

---

### 4.16 publisher

| Column | Type | Nullable | Default | Notes |
|--------|------|----------|---------|-------|
| id | INT | NOT NULL | AUTO_INCREMENT | PK. |
| name | VARCHAR(255) | NOT NULL | — | |
| email | VARCHAR(255) | NOT NULL | — | UNIQUE; login; not in response. |
| password_hash | VARCHAR(255) | NOT NULL | — | |
| created_at | DATETIME | NOT NULL | — | Not in response. |

**Indexes:** PK; UNIQUE(id); UNIQUE(email).

---

### 4.17 publisher_refresh_token

| Column | Type | Nullable | Default | Notes |
|--------|------|----------|---------|-------|
| id | INT | NOT NULL | AUTO_INCREMENT | PK. |
| publisher_id | INT | NOT NULL | — | FK → publisher. |
| token_hash | VARCHAR(255) | NOT NULL | — | |
| expires_at | DATETIME | NOT NULL | — | |
| revoked_at | DATETIME | NULL | — | |
| created_at | DATETIME | NOT NULL | — | |

**Indexes:** PK; UNIQUE(id); INDEX(publisher_id). **FK:** publisher.

---

### 4.18 publisher_designer

| Column | Type | Nullable | Default | Notes |
|--------|------|----------|---------|-------|
| id | INT | NOT NULL | AUTO_INCREMENT | PK. |
| publisher_id | INT | NOT NULL | — | FK → publisher. |
| user_id | INT | NOT NULL | — | FK → user. |
| assigned_at | DATETIME | NOT NULL | — | designers[].assignedAt. |

**Indexes:** PK; UNIQUE(id); UNIQUE(publisher_id, user_id); INDEX(user_id). **FKs:** publisher, user.

---

## 5. Entity-relationship overview

- **user** — Central; profile and auth; referenced by sessions (creator), session_player, session_invite, game_tracked_stat_set, user_game_stats_cache, follower, user_refresh_token, publisher_designer.
- **game** — Referenced by game_tracked_stat_set, session, user_game_stats_cache.
- **scope**, **data_type** — Referenced by game_tracked_stat, session_tracked_stat.
- **game_tracked_stat_set** — Referenced by game_tracked_stat, session (stat_set_id).
- **game_tracked_stat** — Belongs to game_tracked_stat_set.
- **session** — Has creator_user_id → user; game_id → game; stat_set_id → game_tracked_stat_set; has session_player, session_invite, session_tracked_stat, player_stat_value, table_stat_value.
- **session_player** — session + user (optional); **session_invite** — session + user.
- **session_tracked_stat** — session + scope + data_type; feeds player_stat_value and table_stat_value.
- **user_game_stats_cache** — user + game.
- **follower** — user (follower) + user (followee).
- **user_refresh_token** — user; **publisher** — standalone; **publisher_refresh_token** — publisher; **publisher_designer** — publisher + user.

**Session visibility:** Resolved as user.default_session_visibility with optional session.visibility_override.  
**Won/lost:** Derived from player_stat_value (e.g. boolean stat player_won), not a separate column.  
**Session quota:** sessionsUsedThisWeek = count of sessions where creator_user_id = current user and time_started in current week; sessionsLimitPerWeek from app config (designers exempt).

---

## 6. API alignment summary

- **Auth:** user, user_refresh_token; publisher, publisher_refresh_token.
- **Reference:** scope, data_type (GET /scopes, GET /data-types).
- **Games:** game (GET/POST /games, GET /games/{id}); game_tracked_stat_set, game_tracked_stat (stat-sets).
- **Sessions:** session (creator_user_id, stat_set_id, visibility_override), session_invite (invites), session_player (including nonAppPlayerNames, is_spectator), session_tracked_stat, player_stat_value, table_stat_value.
- **Users:** user (profile, sessionQuota from session count, quickStats from cache); user_game_stats_cache (stats endpoints).
- **Social:** follower (followers/following/follow/unfollow); user (search).
- **Feed:** session + creator_user_id + visibility; follower.
- **Export:** session, player_stat_value, table_stat_value, etc., with filters.
- **Publishers:** publisher, publisher_designer (designers, analytics).

All documented API endpoints have a place in this schema to store and retrieve the required data.

---

## 7. Design notes

- **Normalization:** Schema is in 1NF, 2NF, 3NF; no repeating groups, partial key dependencies, or transitive dependencies in the new design.
- **Naming:** snake_case for tables and columns; schema name BoardGameTracker retained.
- **Backend-only columns (not in API request/response):** user.created_at; publisher.created_at, publisher.email; all columns of user_refresh_token and publisher_refresh_token. Used for auth, ordering, or audit only.

---

## 8. Related files

| File | Description |
|------|-------------|
| `mysql-database/create-tables.sql` | Full DDL for the schema. |
| `mysql-database/schema-update-summary.md` | This document. |
| `python-api/design-guide/api-specification.jsonld` | REST API spec (endpoints, data shapes). |
| `python-api/design-guide/api-documentation.md` | API documentation. |

---

*Created using AALang and Gab.*
