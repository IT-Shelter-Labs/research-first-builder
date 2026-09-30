"""Render an edited walkthrough from actual included artifacts, not a session recording.

Development-only dependency: Pillow. Reads the verified team-chat records; no invented tests.
"""

import json
import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / "examples" / "team-chat"
WIDTH, HEIGHT = 1280, 720
BG, INK, MUTED, GREEN = "#101915", "#eff7ef", "#adc4b2", "#9ff0af"


def font(size):
    return ImageFont.load_default(size=size)


def frame(index, title, kicker, lines, foot):
    picture = Image.new("RGB", (WIDTH, HEIGHT), BG)
    draw = ImageDraw.Draw(picture)
    draw.text((60, 42), "IT SHELTER  /  RESEARCH FIRST BUILDER", fill=GREEN, font=font(22))
    draw.text((60, 110), title, fill=INK, font=font(42))
    draw.text((60, 178), kicker, fill=MUTED, font=font(23))
    y = 255
    for label, body in lines:
        draw.text((60, y), label, fill=GREEN, font=font(25))
        y += 40
        for row in textwrap.wrap(body, width=80):
            draw.text((60, y), row, fill=INK, font=font(24))
            y += 34
        y += 23
    draw.text((60, 652), foot, fill=MUTED, font=font(18))
    for step in range(4):
        draw.rounded_rectangle(
            (1110 + step * 29, 654, 1128 + step * 29, 664),
            radius=4,
            fill=GREEN if step <= index else "#314239",
        )
    return picture


def main():
    data = json.loads((EXAMPLE / "evidence.json").read_text(encoding="utf-8"))
    state = json.loads((EXAMPLE / "run.json").read_text(encoding="utf-8"))
    if state["stage"] != "COMPLETE" or any(
        c["required"] and c["result"] != "PASS" for c in data["verification"]
    ):
        raise SystemExit("Example lacks recorded passing checks; verify before creating demo")
    claims = {c["id"]: c for c in data["claims"]}
    decisions = {d["id"]: d for d in data["decisions"]}
    base = "Edited artifact walkthrough | Actual team-chat example | Not an agent-session recording"
    frames = [
        frame(
            0,
            "Start with a real constraint",
            "A small team-chat storage core",
            [
                ("REQ-001", data["requirements"][0]["text"]),
                (
                    "SCOPE",
                    "One process. Local database. No federation, HTTP, auth or push service.",
                ),
            ],
            base,
        ),
        frame(
            1,
            "Inspect before adopting",
            "Pinned primary sources, scoped claims",
            [
                ("VERIFIED - documented", claims["EV-001"]["statement"]),
                ("VERIFIED - implementation", claims["EV-002"]["statement"]),
                ("INFERENCE", claims["EV-005"]["statement"]),
            ],
            base,
        ),
        frame(
            2,
            "Make rejection visible",
            "Scale fit and user requirements decide",
            [
                ("ADOPT", decisions["DEC-001"]["candidate"]),
                (
                    "REJECT",
                    "Logless retention conflicts with durability. Federation is outside scope.",
                ),
                (
                    "DEFER",
                    "Separate delivery/background infrastructure: revisit when actually needed.",
                ),
            ],
            base,
        ),
        frame(
            3,
            "Build, then verify",
            "Actual checks saved against the implementation snapshot",
            [
                (
                    "CHECK-002 / PASS",
                    "5 behavior tests: reopen persistence, room ordering/isolation, text safety and bounds.",
                ),
                (
                    "CHECK-003 / PASS",
                    "Complete-file diff review: rejected/deferred complexity is absent.",
                ),
                (
                    "CONTRACT_CHECKED",
                    "Offline consistency check. Source truth and authorization require separate review.",
                ),
            ],
            base,
        ),
    ]
    output = ROOT / "media" / "demo.gif"
    output.parent.mkdir(exist_ok=True)
    frames[0].save(
        output, save_all=True, append_images=frames[1:], duration=4000, loop=0, optimize=False
    )
    with Image.open(output) as check:
        assert check.size == (WIDTH, HEIGHT) and check.n_frames == 4
    print("Created 1280x720 GIF, 4 frames / 16 seconds, from recorded example artifacts.")


if __name__ == "__main__":
    main()
