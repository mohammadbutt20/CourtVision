import sqlite3
from models import GameRow

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
    conn.commit()


def save_games(conn, games: list[GameRow]) -> None:
    conn.executemany(
        "INSERT OR REPLACE INTO games VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
        [g.to_row() for g in games],
    )
    conn.commit()