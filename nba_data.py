from nba_api.stats.endpoints import playergamelog
from nba_api.stats.static import players


class PlayerNotFoundError(ValueError):
    pass

class PlayerAmbiguousError(ValueError):
    pass

class InsufficientGamesError(ValueError):
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

    print(matches)
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