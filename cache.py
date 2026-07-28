import sqlite3
from models import GameRow
from datetime import date, datetime

DB_PATH = "courtvision.db"


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
            PRIMARY KEY (player_id, game_date)
        )

        
    """)
    conn.execute("""
            CREATE TABLE IF NOT EXISTS fetches (
                player_id INTEGER PRIMARY KEY,
                fetched_at TEXT
            )
    """)
    conn.commit()


def save_fetch(conn, player_id: int) -> None:
    conn.execute(
        "INSERT OR REPLACE INTO fetches VALUES (?, ?)",
        (player_id, datetime.now().isoformat()),
    )
    conn.commit()


def get_fetch(conn, player_id: int) -> datetime | None:
    row = conn.execute(
        "SELECT fetched_at FROM fetches WHERE player_id = ?", (player_id,)
    ).fetchone()

    if row is None:
        return None
    return datetime.fromisoformat(row[0])


def save_games(conn, games: list[GameRow]) -> None:
    conn.executemany(
        "INSERT OR REPLACE INTO games VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
        [g.to_row() for g in games],
    )
    conn.commit()


def get_games(conn, playerid: int) -> list[GameRow]:

    rows = conn.execute(
        "SELECT * FROM games WHERE player_id = ?", (playerid,)
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
        )
        for row in rows
    ]
