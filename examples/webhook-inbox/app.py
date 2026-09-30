"""Educational signed inbox; its wire format is not a provider protocol."""

import hashlib
import hmac
import json
import re
import sqlite3
import time


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("Duplicate JSON key")
        result[key] = value
    return result


def reject_constant(value):
    raise ValueError("Nonfinite JSON number")


def signature(secret, event_id, body, timestamp):
    message = str(timestamp).encode("ascii") + b"." + event_id.encode("ascii") + b"." + body
    return hmac.new(secret, message, hashlib.sha256).hexdigest()


class Inbox:
    def __init__(self, path, secret):
        if not isinstance(secret, bytes) or len(secret) < 32:
            raise ValueError("Provide at least 32 secret bytes")
        self.secret = secret
        self.db = sqlite3.connect(path)
        self.db.execute(
            "CREATE TABLE IF NOT EXISTS events "
            "(event_id TEXT PRIMARY KEY, body BLOB NOT NULL, digest TEXT NOT NULL)"
        )
        self.db.commit()

    def receive(self, event_id, body, timestamp, signed, now=None):
        if not isinstance(event_id, str) or not re.fullmatch(r"[A-Za-z0-9_-]{1,128}", event_id):
            raise ValueError("Invalid event ID")
        if not isinstance(body, bytes) or len(body) > 1024 * 1024:
            raise ValueError("Expected bytes up to 1 MiB")
        if type(timestamp) is not int or not 0 <= timestamp <= 9999999999:
            raise ValueError("Invalid timestamp")
        clock = time.time() if now is None else now
        if abs(clock - timestamp) > 300:
            raise ValueError("Expired or future timestamp")
        if not isinstance(signed, str) or not re.fullmatch(r"[0-9a-f]{64}", signed):
            raise ValueError("Invalid signature")
        expected = signature(self.secret, event_id, body, timestamp)
        if not hmac.compare_digest(signed, expected):
            raise ValueError("Signature mismatch")
        try:
            payload = json.loads(
                body.decode("utf-8"),
                object_pairs_hook=unique_object,
                parse_constant=reject_constant,
            )
        except (UnicodeError, json.JSONDecodeError, RecursionError) as exc:
            raise ValueError("Invalid JSON body") from exc
        if not isinstance(payload, dict):
            raise ValueError("Expected a JSON object")
        digest = hashlib.sha256(body).hexdigest()
        with self.db:
            cursor = self.db.execute(
                "INSERT INTO events VALUES (?, ?, ?) ON CONFLICT(event_id) DO NOTHING",
                (event_id, body, digest),
            )
            stored = self.db.execute(
                "SELECT body FROM events WHERE event_id=?", (event_id,)
            ).fetchone()[0]
            if stored != body:
                raise ValueError("Event ID conflicts with existing body")
        return "stored" if cursor.rowcount else "duplicate"

    def get(self, event_id):
        row = self.db.execute("SELECT body FROM events WHERE event_id=?", (event_id,)).fetchone()
        return row[0] if row else None

    def close(self):
        self.db.close()
