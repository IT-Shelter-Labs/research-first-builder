import tempfile
import unittest
from pathlib import Path

from app import ChatStore


class ChatTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.path = Path(self.temp.name) / "chat.db"
        self.store = ChatStore(self.path)

    def tearDown(self):
        self.store.close()
        self.temp.cleanup()

    def test_persistence(self):
        identifier = self.store.send("general", "Ada", "Привет 🐈")
        self.store.close()
        self.store = ChatStore(self.path)
        self.assertEqual(self.store.history("general"), [(identifier, "Ada", "Привет 🐈")])

    def test_room_order_cursor_and_limit(self):
        first = self.store.send("one", "A", "first")
        self.store.send("two", "B", "private")
        second = self.store.send("one", "C", "second")
        self.assertEqual(self.store.history("one", limit=1), [(first, "A", "first")])
        self.assertEqual(self.store.history("one", after=first), [(second, "C", "second")])
        self.assertEqual(self.store.history("missing"), [])

    def test_sql_like_text_preserved(self):
        value = "'; DROP TABLE messages; --"
        self.store.send(value, "A", value)
        self.assertEqual(self.store.history(value)[0][2], value)
        self.store.send("one", "A", "still works")

    def test_invalid_text_never_written(self):
        for values in [
            ("", "A", "ok"),
            ("one", " ", "ok"),
            ("one", "A", ""),
            ("x" * 33, "A", "ok"),
            ("one", "x" * 65, "ok"),
            ("one", "A", "x" * 2001),
            ("one", "A", None),
        ]:
            with self.subTest(values=str(values)[:50]), self.assertRaises(ValueError):
                self.store.send(*values)
        self.assertEqual(self.store.history("one"), [])

    def test_history_bounds(self):
        for params in [(-1, 1), (True, 1), (0, 0), (0, 101), (0, True), (0, 1.0)]:
            with self.subTest(params=params), self.assertRaises(ValueError):
                self.store.history("one", *params)


if __name__ == "__main__":
    unittest.main()
