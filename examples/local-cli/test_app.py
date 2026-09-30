import io
import subprocess
import sys
import unittest
from pathlib import Path

from app import matches


class FilterTests(unittest.TestCase):
    def test_exact_bytes_and_no_coercion(self):
        wanted = ' {"kind": "猫", "extra": 1}\r\n'.encode()
        final = '{"kind":"猫"}'.encode()
        stream = io.BytesIO(wanted + b'{"kind":3}\nnull\n' + final)
        self.assertEqual(list(matches(stream, "kind", "猫")), [wanted, final])

    def test_literal_top_level(self):
        stream = io.BytesIO(b'{"k":"a.*"}\n{"k":"abc"}\n{"nested":{"k":"a.*"}}\n')
        self.assertEqual(list(matches(stream, "k", "a.*")), [b'{"k":"a.*"}\n'])

    def test_lazy_first_match(self):
        class Stream:
            def readline(self, size):
                if hasattr(self, "read"):
                    raise AssertionError("Read ahead before first match")
                self.read = True
                return b'{"k":"yes"}\n'

        self.assertEqual(next(matches(Stream(), "k", "yes")), b'{"k":"yes"}\n')

    def test_bad_lines(self):
        for raw in [
            b"\n",
            b"\xff\n",
            b'{"x":1,"x":2}\n',
            b'{"x":Infinity}\n',
            b" " * 65537,
            b"[" * 2000,
            b"{\n",
        ]:
            with self.subTest(raw=raw[:30]), self.assertRaisesRegex(ValueError, "line 2"):
                list(matches(io.BytesIO(b"null\n" + raw), "k", "v"))

    def test_cli_partial_output_and_status(self):
        result = subprocess.run(
            [sys.executable, str(Path(__file__).with_name("app.py")), "k", "v"],
            input=b'{"k":"v"}\nnot-json\n',
            capture_output=True,
        )
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, b'{"k":"v"}\n')
        self.assertIn(b"line 2", result.stderr)
        self.assertNotIn(b"Traceback", result.stderr)

    def test_cli_empty_success(self):
        result = subprocess.run(
            [sys.executable, str(Path(__file__).with_name("app.py")), "k", "v"],
            input=b"",
            capture_output=True,
        )
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout, b"")


if __name__ == "__main__":
    unittest.main()
