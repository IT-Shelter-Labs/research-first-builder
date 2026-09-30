"""Educational local storage core, not a chat server."""

import sqlite3


class ChatStore:
    def __init__(self, path):
        self.db = sqlite3.connect(path)
        self.db.execute(
            "CREATE TABLE IF NOT EXISTS messages "
            "(id INTEGER PRIMARY KEY, room TEXT NOT NULL, "
            "sender TEXT NOT NULL, body TEXT NOT NULL)"
        )
        self.db.execute("CREATE INDEX IF NOT EXISTS room_history ON messages(room, id)")
        self.db.commit()

    @staticmethod
    def text(value, maximum):
        if not isinstance(value, str) or not value.strip() or len(value) > maximum:
            raise ValueError("Expected nonempty bounded text")
        return value

    def send(self, room, sender, body):
        values = (self.text(room, 32), self.text(sender, 64), self.text(body, 2000))
        with self.db:
            cursor = self.db.execute(
                "INSERT INTO messages(room, sender, body) VALUES (?, ?, ?)", values
            )
        return cursor.lastrowid

    def history(self, room, after=0, limit=100):
        self.text(room, 32)
        if type(after) is not int or after < 0 or type(limit) is not int or not 1 <= limit <= 100:
            raise ValueError("Expected after >= 0 and limit in 1..100")
        return self.db.execute(
            "SELECT id, sender, body FROM messages WHERE room=? AND id>? ORDER BY id LIMIT ?",
            (room, after, limit),
        ).fetchall()

    def close(self):
        self.db.close()
