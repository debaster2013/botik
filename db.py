import sqlite3
from config import DB_PATH


class Database:
    def __init__(self, db_path: str = DB_PATH):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self._init_tables()

    def _init_tables(self):
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS stats (
                chat_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                username TEXT,
                messages_count INTEGER DEFAULT 0,
                PRIMARY KEY (chat_id, user_id)
            )
            """
        )
        self.conn.commit()

    def add_message(self, chat_id: int, user_id: int, username: str | None):
        self.cursor.execute(
            """
            INSERT INTO stats (chat_id, user_id, username, messages_count)
            VALUES (?, ?, ?, 1)
            ON CONFLICT(chat_id, user_id) DO UPDATE SET
                username = COALESCE(excluded.username, stats.username),
                messages_count = stats.messages_count + 1
            """,
            (chat_id, user_id, username or "без_ника"),
        )
        self.conn.commit()

    def get_top_users(self, chat_id: int, limit: int = 10) -> list[tuple[str, int]]:
        self.cursor.execute(
            """
            SELECT username, messages_count FROM stats
            WHERE chat_id = ?
            ORDER BY messages_count DESC
            LIMIT ?
            """,
            (chat_id, limit),
        )
        return self.cursor.fetchall()

    def get_user_stats(self, chat_id: int, user_id: int) -> tuple[str, int] | None:
        self.cursor.execute(
            """
            SELECT username, messages_count FROM stats
            WHERE chat_id = ? AND user_id = ?
            """,
            (chat_id, user_id),
        )
        return self.cursor.fetchone()
