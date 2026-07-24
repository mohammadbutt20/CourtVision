from nba_api.stats.endpoints import playergamelog
from nba_api.stats.static import players


class PlayerNotFoundError(ValueError):
    pass


class PlayerAmbiguousError(ValueError):
    pass


class InsufficientGamesError(ValueError):
    pass


class InvalidStatCategoryError(KeyError):
    pass


def get_player_id(name: str) -> int:
    """Search for a player's NBA ID by name.
    Args:
        name: A player's full name (e.g. `"LeBron James"`).
    Returns:
        The player's NBA ID.
    Raises:
        PlayerNotFoundError: No player matched `name`.
        PlayerAmbiguousError: More than one player matched `name`.
    """
    matches = players.find_players_by_full_name(name)

    # No matches found
    if not matches:
        raise PlayerNotFoundError(f"No player found matching '{name}'")
    # More than one match found
    if len(matches) > 1:
        candidates = ", ".join(f"{m['full_name']} (id {m['id']})" for m in matches)
        raise PlayerAmbiguousError(
            f"'{name}' matches multiple players: {candidates}. Be more specific."
        )
    # Return ID of singular match
    return matches[0]["id"]


def get_player_games(player_id: int, season: str) -> list[dict]:
    """Get all games for a player during a given season.
    Args:
        player_id: A player's given ID (`"LeBron James" = 2544`).
    Returns:
        List of games in a dict format
    """

    game_log = playergamelog.PlayerGameLog(player_id=player_id, season=season)
    result_set = game_log.get_dict()["resultSets"][0]
    headers = result_set["headers"]
    return [dict(zip(headers, row)) for row in result_set["rowSet"]]


def extract_stat(games: list[dict], stat_category: str) -> list[object]:
    """Get data from games
    Args: 
        games: list of zipped dicts with 'catagory: value'
        stat_category: stat line desired (Ex: "REB", "PTS", "FT", "MIN"...)
    Returns:
        List of extracted data from games
    Raises:
        InvalidStatCategoryError: Invalid stat_category provided.
    """

    try:
        return [game[stat_category.upper()] for game in games]
    except KeyError:
        raise InvalidStatCategoryError(
            f"{stat_category!r} not found. Available: {sorted(games[0])}"
        ) from None


