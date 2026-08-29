import sqlite3
from models import GameRow
from datetime import date, datetime

DB_PATH = "courtvision.db"  # local disk db for test/dev


def get_connection():
    return sqlite3.connect(DB_PATH)


def create_tables(conn):
    conn.execute("""
        CREATE TABLE IF NOT EXISTS games (
            player_id INTEGER,
            game_date TEXT,
            matchup TEXT,
            minutes REAL,
            points INTEGER,
            rebounds INTEGER,
            assists INTEGER,
            steals INTEGER,
            blocks INTEGER,
            win_loss TEXT,
            field_goal_made INTEGER,
            field_goal_attempted INTEGER,
            field_goal_three_made INTEGER,
            field_goal_three_attempted INTEGER,
            free_throw_made INTEGER,
            free_throw_attempted INTEGER,
            turn_over INTEGER,
            season TEXT,
            PRIMARY KEY (player_id, game_date)
        )

        
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS fetches (
            player_id INTEGER NOT NULL,
            season TEXT NOT NULL,
            fetched_at TEXT NOT NULL,
            PRIMARY KEY (player_id, season)
        )
    """)
    conn.commit()


def save_fetch(conn, player_id: int, season: str) -> None:
    conn.execute(
        "INSERT OR REPLACE INTO fetches (player_id, season, fetched_at) VALUES (?, ?, ?)",
        (player_id, season, datetime.now().isoformat()),
    )
    conn.commit()


def get_fetch(conn, player_id: int, season: str) -> datetime | None:
    row = conn.execute(
        "SELECT fetched_at FROM fetches WHERE player_id = ? AND season = ?",
        (player_id, season),
    ).fetchone()

    if row is None:
        return None
    return datetime.fromisoformat(row[0])


def save_games(conn, games: list[GameRow]) -> None:
    conn.executemany(
        "INSERT OR REPLACE INTO games VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
        [g.to_row() for g in games],
    )


def delete_games(conn, player_id: int, season: str) -> None:
    """Delete all cached games for one player-season. Scoped to
    (player_id, season) so refreshing one season leaves other cached
    seasons intact."""
    conn.execute(
        "DELETE FROM games WHERE player_id = ? AND season = ?",
        (player_id, season),
    )


def get_games(conn, playerid: int, season: str) -> list[GameRow]:

    rows = conn.execute(
        "SELECT * FROM games WHERE player_id = ? AND season = ?", (playerid, season)
    ).fetchall()

    return [
        GameRow(
            row[0],
            date.fromisoformat(row[1]),
            row[2],
            row[3],
            row[4],
            row[5],
            row[6],
            row[7],
            row[8],
            row[9],
            row[10],
            row[11],
            row[12],
            row[13],
            row[14],
            row[15],
            row[16],
            row[17],
        )
        for row in rows
    ]

