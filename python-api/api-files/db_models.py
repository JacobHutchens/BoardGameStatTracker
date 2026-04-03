from datetime import datetime
from typing import Optional

from sqlmodel import Field, Relationship, SQLModel


# ---------------------------------------------------------------------------
# User and authentication models
# ---------------------------------------------------------------------------


class User(SQLModel, table=True):
    __tablename__ = "user"

    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, max_length=45)
    email: str = Field(index=True, max_length=45)
    password_hash: str = Field(max_length=255)
    created_at: datetime
    bio: Optional[str] = None
    avatar_url: Optional[str] = Field(default=None, max_length=255)
    designer: bool = Field(default=False)
    default_session_visibility: str = Field(default="public", max_length=45)
    # Added via migration add_user_time_zone.sql
    time_zone: Optional[str] = Field(default=None, max_length=64)

    # Relationships
    games_stat_sets: list["GameTrackedStatSet"] = Relationship(back_populates="user")
    sessions_created: list["Session"] = Relationship(back_populates="creator_user")
    session_players: list["SessionPlayer"] = Relationship(back_populates="user")
    session_invites: list["SessionInvite"] = Relationship(back_populates="user")
    user_game_stats: list["UserGameStatsCache"] = Relationship(back_populates="user")
    followers: list["Follower"] = Relationship(
        back_populates="user", sa_relationship_kwargs={"foreign_keys": "[Follower.user_id]"}
    )
    following: list["Follower"] = Relationship(
        back_populates="following_user", sa_relationship_kwargs={"foreign_keys": "[Follower.following_user_id]"}
    )
    refresh_tokens: list["UserRefreshToken"] = Relationship(back_populates="user")
    publisher_links: list["PublisherDesigner"] = Relationship(back_populates="user")


class UserRefreshToken(SQLModel, table=True):
    __tablename__ = "user_refresh_token"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    token_hash: str = Field(max_length=255)
    expires_at: datetime
    revoked_at: Optional[datetime] = None
    created_at: datetime

    user: Optional[User] = Relationship(back_populates="refresh_tokens")


class Publisher(SQLModel, table=True):
    __tablename__ = "publisher"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=255)
    email: str = Field(max_length=255, index=True)
    password_hash: str = Field(max_length=255)
    created_at: datetime

    refresh_tokens: list["PublisherRefreshToken"] = Relationship(back_populates="publisher")
    designers: list["PublisherDesigner"] = Relationship(back_populates="publisher")


class PublisherRefreshToken(SQLModel, table=True):
    __tablename__ = "publisher_refresh_token"

    id: Optional[int] = Field(default=None, primary_key=True)
    publisher_id: int = Field(foreign_key="publisher.id")
    token_hash: str = Field(max_length=255)
    expires_at: datetime
    revoked_at: Optional[datetime] = None
    created_at: datetime

    publisher: Optional[Publisher] = Relationship(back_populates="refresh_tokens")


class PublisherDesigner(SQLModel, table=True):
    __tablename__ = "publisher_designer"

    id: Optional[int] = Field(default=None, primary_key=True)
    publisher_id: int = Field(foreign_key="publisher.id")
    user_id: int = Field(foreign_key="user.id")
    assigned_at: datetime

    publisher: Optional[Publisher] = Relationship(back_populates="designers")
    user: Optional[User] = Relationship(back_populates="publisher_links")


# ---------------------------------------------------------------------------
# Reference data models (scopes, data types)
# ---------------------------------------------------------------------------


class Scope(SQLModel, table=True):
    __tablename__ = "scope"

    id: Optional[int] = Field(default=None, primary_key=True)
    scope: str = Field(max_length=45, index=True)

    game_tracked_stats: list["GameTrackedStat"] = Relationship(back_populates="scope")
    session_tracked_stats: list["SessionTrackedStat"] = Relationship(back_populates="scope")


class DataType(SQLModel, table=True):
    __tablename__ = "data_type"

    id: Optional[int] = Field(default=None, primary_key=True)
    data_type: Optional[str] = Field(default=None, max_length=45)

    game_tracked_stats: list["GameTrackedStat"] = Relationship(back_populates="data_type")
    session_tracked_stats: list["SessionTrackedStat"] = Relationship(back_populates="data_type")


# ---------------------------------------------------------------------------
# Game and tracked stat-set models
# ---------------------------------------------------------------------------


class Game(SQLModel, table=True):
    __tablename__ = "game"

    id: Optional[int] = Field(default=None, primary_key=True)
    game_name: str = Field(max_length=45, index=True)
    max_player_count: Optional[int] = None
    min_player_count: Optional[int] = None
    description: str
    can_win: bool = Field(default=True)
    created_at: datetime

    stat_sets: list["GameTrackedStatSet"] = Relationship(back_populates="game")
    sessions: list["Session"] = Relationship(back_populates="game")
    user_game_stats: list["UserGameStatsCache"] = Relationship(back_populates="game")


class GameTrackedStatSet(SQLModel, table=True):
    __tablename__ = "game_tracked_stat_set"

    id: Optional[int] = Field(default=None, primary_key=True)
    game_id: int = Field(foreign_key="game.id")
    user_id: int = Field(foreign_key="user.id")
    set_name: str = Field(max_length=45)

    game: Optional[Game] = Relationship(back_populates="stat_sets")
    user: Optional[User] = Relationship(back_populates="games_stat_sets")
    stats: list["GameTrackedStat"] = Relationship(back_populates="stat_set")
    sessions: list["Session"] = Relationship(back_populates="stat_set")


class GameTrackedStat(SQLModel, table=True):
    __tablename__ = "game_tracked_stat"

    id: Optional[int] = Field(default=None, primary_key=True)
    game_tracked_stat_set_id: int = Field(foreign_key="game_tracked_stat_set.id")
    stat_name: str = Field(max_length=45)
    description: Optional[str] = None
    data_type_id: int = Field(foreign_key="data_type.id")
    scope_id: int = Field(foreign_key="scope.id")

    stat_set: Optional[GameTrackedStatSet] = Relationship(back_populates="stats")
    data_type: Optional[DataType] = Relationship(back_populates="game_tracked_stats")
    scope: Optional[Scope] = Relationship(back_populates="game_tracked_stats")


# ---------------------------------------------------------------------------
# Session, invites, and player participation models
# ---------------------------------------------------------------------------


class Session(SQLModel, table=True):
    __tablename__ = "session"

    id: Optional[int] = Field(default=None, primary_key=True)
    creator_user_id: int = Field(foreign_key="user.id")
    game_id: int = Field(foreign_key="game.id")
    stat_set_id: int = Field(foreign_key="game_tracked_stat_set.id")
    session_key: str = Field(max_length=6, index=True)
    time_started: datetime
    time_ended: Optional[datetime] = None
    current_round: Optional[int] = None
    visibility_override: Optional[str] = Field(default=None, max_length=45)

    creator_user: Optional[User] = Relationship(back_populates="sessions_created")
    game: Optional[Game] = Relationship(back_populates="sessions")
    stat_set: Optional[GameTrackedStatSet] = Relationship(back_populates="sessions")
    players: list["SessionPlayer"] = Relationship(back_populates="session")
    invites: list["SessionInvite"] = Relationship(back_populates="session")
    tracked_stats: list["SessionTrackedStat"] = Relationship(back_populates="session")
    table_stat_values: list["TableStatValue"] = Relationship(back_populates="session")


class SessionPlayer(SQLModel, table=True):
    __tablename__ = "session_player"

    id: Optional[int] = Field(default=None, primary_key=True)
    session_id: int = Field(foreign_key="session.id")
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    player_name: str = Field(max_length=45)
    is_spectator: bool = Field(default=False)

    session: Optional[Session] = Relationship(back_populates="players")
    user: Optional[User] = Relationship(back_populates="session_players")
    player_stat_values: list["PlayerStatValue"] = Relationship(back_populates="session_player")


class SessionInvite(SQLModel, table=True):
    __tablename__ = "session_invite"

    id: Optional[int] = Field(default=None, primary_key=True)
    session_id: int = Field(foreign_key="session.id")
    user_id: int = Field(foreign_key="user.id")
    invited_at: datetime

    session: Optional[Session] = Relationship(back_populates="invites")
    user: Optional[User] = Relationship(back_populates="session_invites")


class SessionTrackedStat(SQLModel, table=True):
    __tablename__ = "session_tracked_stat"

    id: Optional[int] = Field(default=None, primary_key=True)
    session_id: int = Field(foreign_key="session.id")
    stat_name: str = Field(max_length=45)
    data_type_id: int = Field(foreign_key="data_type.id")
    scope_id: int = Field(foreign_key="scope.id")

    session: Optional[Session] = Relationship(back_populates="tracked_stats")
    data_type: Optional[DataType] = Relationship(back_populates="session_tracked_stats")
    scope: Optional[Scope] = Relationship(back_populates="session_tracked_stats")
    player_stat_values: list["PlayerStatValue"] = Relationship(back_populates="session_tracked_stat")
    table_stat_values: list["TableStatValue"] = Relationship(back_populates="session_tracked_stat")


class PlayerStatValue(SQLModel, table=True):
    __tablename__ = "player_stat_value"

    id: Optional[int] = Field(default=None, primary_key=True)
    session_tracked_stat_id: int = Field(foreign_key="session_tracked_stat.id")
    session_player_id: int = Field(foreign_key="session_player.id")
    stat_value: str = Field(max_length=45)
    recorded_at: datetime
    round_number: Optional[int] = None

    session_tracked_stat: Optional[SessionTrackedStat] = Relationship(back_populates="player_stat_values")
    session_player: Optional[SessionPlayer] = Relationship(back_populates="player_stat_values")


class TableStatValue(SQLModel, table=True):
    __tablename__ = "table_stat_value"

    id: Optional[int] = Field(default=None, primary_key=True)
    session_tracked_stat_id: int = Field(foreign_key="session_tracked_stat.id")
    session_id: int = Field(foreign_key="session.id")
    stat_value: str = Field(max_length=45)
    recorded_at: datetime
    round_number: Optional[int] = None

    session_tracked_stat: Optional[SessionTrackedStat] = Relationship(back_populates="table_stat_values")
    session: Optional[Session] = Relationship(back_populates="table_stat_values")


# ---------------------------------------------------------------------------
# Aggregated stats and social models
# ---------------------------------------------------------------------------


class UserGameStatsCache(SQLModel, table=True):
    __tablename__ = "user_game_stats_cache"

    id: Optional[int] = Field(default=None, primary_key=True)
    game_id: int = Field(foreign_key="game.id")
    user_id: int = Field(foreign_key="user.id")
    total_times_played: int
    wins: Optional[int] = None

    game: Optional[Game] = Relationship(back_populates="user_game_stats")
    user: Optional[User] = Relationship(back_populates="user_game_stats")


class Follower(SQLModel, table=True):
    __tablename__ = "follower"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    following_user_id: int = Field(foreign_key="user.id")
    followed_at: datetime

    user: Optional[User] = Relationship(
        back_populates="followers", sa_relationship_kwargs={"foreign_keys": "[Follower.user_id]"}
    )
    following_user: Optional[User] = Relationship(
        back_populates="following", sa_relationship_kwargs={"foreign_keys": "[Follower.following_user_id]"}
    )

