import tempfile
import unittest
from pathlib import Path

from app import Inbox, signature


class InboxTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.path = Path(self.temp.name) / "inbox.db"
        self.secret = b"test-only-key-do-not-deploy-12345678"
        self.inbox = Inbox(self.path, self.secret)
        self.now = 1700000000

    def tearDown(self):
        self.inbox.close()
        self.temp.cleanup()

    def receive(self, body=b'{"event":"hello"}', event="evt_1", stamp=None, signed=None):
        stamp = self.now if stamp is None else stamp
        signed = signature(self.secret, event, body, stamp) if signed is None else signed
        return self.inbox.receive(event, body, stamp, signed, now=self.now)

    def test_duplicate_and_persistence(self):
        body = '{"value":"Привет"}'.encode()
        self.assertEqual(self.receive(body), "stored")
        self.assertEqual(self.receive(body), "duplicate")
        self.inbox.close()
        self.inbox = Inbox(self.path, self.secret)
        self.assertEqual(self.inbox.get("evt_1"), body)
        self.assertEqual(self.receive(body), "duplicate")

    def test_conflicting_id_does_not_overwrite(self):
        self.receive()
        with self.assertRaisesRegex(ValueError, "conflicts"):
            self.receive(b'{"changed":true}')
        self.assertEqual(self.inbox.get("evt_1"), b'{"event":"hello"}')

    def test_signature_binds_body_id_and_timestamp(self):
        signed = signature(self.secret, "evt_1", b"{}", self.now)
        for body, event, stamp in [
            (b'{"x":1}', "evt_1", self.now),
            (b"{}", "evt_2", self.now),
            (b"{}", "evt_1", self.now + 1),
        ]:
            with self.subTest(event=event, stamp=stamp), self.assertRaises(ValueError):
                self.receive(body, event, stamp, signed)
        self.assertIsNone(self.inbox.get("evt_1"))

    def test_time_window(self):
        for offset in [-301, 301]:
            with self.subTest(offset=offset), self.assertRaises(ValueError):
                self.receive(stamp=self.now + offset)
        self.assertEqual(self.receive(stamp=self.now - 300), "stored")

    def test_invalid_json_and_bounds(self):
        for body in [
            b"[]",
            b"no",
            b"\xff",
            b'{"x":1,"x":2}',
            b'{"x":NaN}',
            b" " * (1024 * 1024 + 1),
            b"[" * 2000,
        ]:
            with self.subTest(body=body[:30]), self.assertRaises(ValueError):
                self.receive(body)
            self.assertIsNone(self.inbox.get("evt_1"))

    def test_boundary_validation(self):
        for identifier in ["", "a.b", "x" * 129]:
            with self.assertRaises(ValueError):
                self.receive(event=identifier)
        for stamp in [True, -1, 10000000000]:
            with self.assertRaises(ValueError):
                self.receive(stamp=stamp)
        for signed in ["", "x" * 64, "a" * 63]:
            with self.assertRaises(ValueError):
                self.receive(signed=signed)


if __name__ == "__main__":
    unittest.main()
