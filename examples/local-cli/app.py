"""Literal UTF-8 JSON Lines filter. Errors can follow already-emitted matches."""

import argparse
import json
import sys

MAX_LINE = 65536


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON key")
        result[key] = value
    return result


def reject_constant(value):
    raise ValueError("nonfinite JSON number")


def matches(stream, field, value):
    number = 0
    while True:
        raw = stream.readline(MAX_LINE + 1)
        if not raw:
            return
        number += 1
        try:
            if len(raw) > MAX_LINE:
                raise ValueError("line exceeds 65536 bytes including delimiter")
            parsed = json.loads(
                raw.decode("utf-8"), object_pairs_hook=unique_object, parse_constant=reject_constant
            )
        except (ValueError, RecursionError) as exc:
            raise ValueError(f"line {number}: invalid JSON Lines input ({exc})") from exc
        if (
            isinstance(parsed, dict)
            and isinstance(parsed.get(field), str)
            and parsed[field] == value
        ):
            yield raw


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("field")
    parser.add_argument("value")
    args = parser.parse_args(argv)
    try:
        for raw in matches(sys.stdin.buffer, args.field, args.value):
            sys.stdout.buffer.write(raw)
            sys.stdout.buffer.flush()
        return 0
    except ValueError as exc:
        print(exc, file=sys.stderr)
        return 2
    except BrokenPipeError:
        # Prevent a second broken-pipe error during interpreter shutdown.
        sys.stdout = open(__import__("os").devnull, "w")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
