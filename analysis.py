from datetime import date, datetime, timedelta
from cache import get_fetch, get_games, save_games, save_fetch, delete_games
from nba_data import get_player_games
from models import GameRow

MAX_AGE = timedelta(days=1)


def current_season() -> str:
    today = datetime.today()

    if today.month >= 10:
        start_year = today.year
    else:
        start_year = today.year - 1

    end_year = start_year + 1
    return f"{start_year}-{str(end_year)[2:]}"


def is_fresh(conn, player_id: int, season: str) -> bool:
    """Past seasons are always fresh; the current season is fresh only if
    it was fetched within MAX_AGE."""

    fetched_at = get_fetch(conn, player_id, season)

    if fetched_at is None:
        return False  # never fetched, regardless of season

    if season != current_season():
        return True  # have it, and it can never change

    return datetime.now() - fetched_at < MAX_AGE


def get_player_data(conn, player_id: int, season: str) -> list[GameRow]:
    """Return a player's games for a season, refreshing the cache if stale.

    Cold start and stale both take the same path: fetch from the API,
    blow away the cached player-season, reinsert, and stamp the receipt.
    A fresh cache skips all of that and reads straight through.
    """
    if not is_fresh(conn, player_id, season):
        games = get_player_games(player_id, season)

        delete_games(conn, player_id, season)
        save_games(conn, games)
        save_fetch(conn, player_id, season)
        conn.commit()

    return get_games(conn, player_id, season)
