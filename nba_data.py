import sqlite3

from nba_api.stats.endpoints import playergamelog
from nba_api.stats.static import players
from errors import PlayerNotFoundError, PlayerAmbiguousError, CourtVisionError
from datetime import datetime
from models import GameRow


def get_player_id(name: str) -> int:
    matches = players.find_players_by_full_name(name)
    if not matches:
        raise PlayerNotFoundError(f"No player found matching '{name}'")
    if len(matches) > 1:
        candidates = ", ".join(f"{m['full_name']} (id {m['id']})" for m in matches)
        raise PlayerAmbiguousError(
            f"'{name}' matches multiple players: {candidates}. Be more specific."
        )
    return matches[0]["id"]


def get_player_games(player_id: int, season: str) -> list[GameRow]:
    """Fetch a player's games for one season as GameRows.

    Empty list if the player logged no games that season.
    """
    log = playergamelog.PlayerGameLog(player_id=player_id, season=season, timeout=30)

    raw = log.get_normalized_dict()["PlayerGameLog"]
    return [_to_row(player_id, g, season) for g in raw]


def _to_row(player_id: int, g: dict, season:str) -> GameRow:
    """Convert one raw nba_api dict into our GameRow. The ONLY place that
    knows NBA's column names."""

    return GameRow(
        player_id=player_id,
        game_date=datetime.strptime(g["GAME_DATE"], "%b %d, %Y").date(),
        matchup=g["MATCHUP"],
        minutes=g["MIN"],
        points=g["PTS"],
        rebounds=g["REB"],
        assists=g["AST"],
        steals=g["STL"],
        blocks=g["BLK"],
        win_loss=g["WL"],
        field_goal_made=g["FGM"],
        field_goal_attempted=g["FGA"],
        field_goal_three_made=g["FG3M"],
        field_goal_three_attempted=g["FG3A"],
        free_throw_made=g["FTM"],
        free_throw_attempted=g["FTA"],
        turn_over=g["TOV"],
        season=season
    )

