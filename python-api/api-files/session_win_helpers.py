"""
Shared helpers for deriving per-player won/lost from tracked stats.
Uses conventional stat names (e.g. player_won, won) per design guide.
"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db_models import SessionTrackedStat, PlayerStatValue

# Conventional stat names for "player won" (case-insensitive).
WIN_STAT_NAMES = ("player_won", "won")


async def get_win_tracked_stat_id(db: AsyncSession, session_id: int) -> int | None:
    """Return the SessionTrackedStat id for the win stat in this session, or None if none found."""
    stmt = select(SessionTrackedStat).where(SessionTrackedStat.session_id == session_id)
    result = await db.execute(stmt)
    for row in result.scalars().all():
        if row.stat_name and row.stat_name.strip().lower() in WIN_STAT_NAMES:
            return row.id
    return None


async def get_player_won_value(
    db: AsyncSession, session_player_id: int, win_tracked_stat_id: int
) -> bool | None:
    """Return True/False from the player's value for the win stat, or None if no value recorded."""
    stmt = select(PlayerStatValue).where(
        PlayerStatValue.session_player_id == session_player_id,
        PlayerStatValue.session_tracked_stat_id == win_tracked_stat_id,
    )
    result = await db.execute(stmt)
    row = result.scalars().first()
    if not row or not row.stat_value:
        return None
    raw = row.stat_value.strip().lower()
    if raw in ("true", "1", "yes"):
        return True
    return False
