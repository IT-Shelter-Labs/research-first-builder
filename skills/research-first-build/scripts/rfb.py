#!/usr/bin/env python3
"""Offline checks and managed-table rendering for Research First Builder.

Python 3.11+, standard library only. No network or subprocess execution.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from urllib.parse import quote, urlsplit

VERSION = "0.1.0"
MAX_BYTES = 2 * 1024 * 1024
SKILL_ROOT = Path(__file__).resolve().parents[1]
GROUPS = (
    "requirements",
    "references",
    "sources",
    "claims",
    "decisions",
    "plan_units",
    "verification",
)
REPORT_BLOCKS = {
    "RESEARCH.md": ("references", "sources", "evidence", "decisions"),
    "PLAN.md": ("plan",),
    "VERIFICATION.md": ("checks",),
}
LABELS = {
    "VERIFIED_SOURCE": "VERIFIED · documented",
    "OPEN_SOURCE_IMPLEMENTATION": "VERIFIED · implementation",
    "OBSERVED_PUBLIC_BEHAVIOR": "OBSERVED",
    "INFERENCE": "INFERENCE",
    "USER_REQUIREMENT": "REQUIREMENT",
}


class ContractError(Exception):
    """A readable user-data error, not an internal traceback."""


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def canonical(value: object) -> str:
    return json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


def digest(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def unique_object(pairs: list[tuple[str, object]]) -> dict:
    result = {}
    for key, value in pairs:
        if key in result:
            raise ContractError(f"Duplicate JSON key: {key}")
        result[key] = value
    return result


def read_text(path: Path) -> str:
    try:
        if not path.is_file():
            raise ContractError(f"Missing file: {path.name}")
        if path.stat().st_size > MAX_BYTES:
            raise ContractError(f"File exceeds {MAX_BYTES} bytes: {path.name}")
        return path.read_text(encoding="utf-8-sig").replace("\r\n", "\n")
    except (OSError, UnicodeError) as exc:
        raise ContractError(f"Cannot read {path.name}: {exc}") from exc


def load_json(path: Path) -> dict:
    try:
        data = json.loads(
            read_text(path),
            object_pairs_hook=unique_object,
            parse_constant=lambda x: (_ for _ in ()).throw(
                ContractError(f"Non-finite JSON number: {x}")
            ),
        )
    except (ValueError, RecursionError) as exc:
        raise ContractError(f"Invalid JSON in {path.name}: {exc}") from exc
    if not isinstance(data, dict):
        raise ContractError(f"{path.name} must contain a JSON object")
    return data


def safe_path(root: Path, relative: str) -> Path:
    """Only plain relative POSIX file paths; reject symlinks and junction escape."""
    if not isinstance(relative, str) or not relative or len(relative) > 240:
        raise ContractError("Expected a nonempty relative file path (up to 240 chars)")
    if "\\" in relative or ":" in relative or "\x00" in relative:
        raise ContractError(f"Unsafe file path: {relative!r}")
    pieces = relative.split("/")
    if any(p in ("", ".", "..") for p in pieces) or PurePosixPath(relative).is_absolute():
        raise ContractError(f"Unsafe file path: {relative!r}")
    root = root.resolve()
    candidate = root.joinpath(*pieces)
    current = root
    for piece in pieces:
        current = current / piece
        if current.is_symlink():
            raise ContractError(f"Symlink file path is not allowed: {relative}")
    if not candidate.resolve().is_relative_to(root):
        raise ContractError(f"File path escapes the run directory: {relative}")
    return candidate


def timestamp(value: object) -> bool:
    if not isinstance(value, str):
        return False
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        return "T" in value and parsed.tzinfo is not None
    except ValueError:
        return False


def url(value: object) -> bool:
    if not isinstance(value, str):
        return False
    try:
        parsed = urlsplit(value)
        return (
            parsed.scheme in ("http", "https")
            and bool(parsed.hostname)
            and not parsed.username
            and not parsed.password
            and not any(ch.isspace() for ch in value)
        )
    except ValueError:
        return False


def structure(data: object, schema: dict, full: dict, at: str = "$") -> list[str]:
    """Validate only the bounded vocabulary used by our bundled schema.

    This is not a general-purpose JSON Schema implementation.
    """
    if "$ref" in schema:
        name = schema["$ref"].removeprefix("#/$defs/")
        return structure(data, full["$defs"][name], full, at)
    errors = []
    kind = schema.get("type")
    matches = {
        "object": isinstance(data, dict),
        "array": isinstance(data, list),
        "string": isinstance(data, str),
        "boolean": type(data) is bool,
        "integer": type(data) is int,
    }
    if kind and not matches.get(kind, False):
        return [f"{at}: expected {kind}"]
    if "const" in schema and data != schema["const"]:
        errors.append(f"{at}: unsupported value {data!r}; expected {schema['const']!r}")
    if "enum" in schema and data not in schema["enum"]:
        errors.append(f"{at}: expected one of {', '.join(map(str, schema['enum']))}")
    if isinstance(data, dict):
        props = schema.get("properties", {})
        for name in schema.get("required", []):
            if name not in data:
                errors.append(f"{at}.{name}: required")
        if schema.get("additionalProperties") is False:
            for name in sorted(set(data) - set(props)):
                errors.append(f"{at}.{name}: unknown field")
        for name, value in data.items():
            if name in props:
                errors.extend(structure(value, props[name], full, f"{at}.{name}"))
    elif isinstance(data, list):
        if len(data) < schema.get("minItems", 0):
            errors.append(f"{at}: too few items")
        if len(data) > schema.get("maxItems", 100):
            errors.append(f"{at}: too many items")
        if schema.get("uniqueItems") and len(set(map(canonical, data))) != len(data):
            errors.append(f"{at}: duplicate items")
        for idx, value in enumerate(data[:100]):
            errors.extend(structure(value, schema["items"], full, f"{at}[{idx}]"))
    elif isinstance(data, str):
        if any(0xD800 <= ord(character) <= 0xDFFF for character in data):
            errors.append(f"{at}: invalid Unicode surrogate in JSON string")
        if len(data.strip()) < schema.get("minLength", 0):
            errors.append(f"{at}: must not be blank")
        if len(data) > schema.get("maxLength", 8000):
            errors.append(f"{at}: too long")
        if "pattern" in schema and re.fullmatch(schema["pattern"], data) is None:
            errors.append(f"{at}: invalid identifier")
        fmt = schema.get("format")
        if fmt == "uri" and not url(data):
            errors.append(f"{at}: expected an HTTP(S) URL without credentials")
        if fmt == "date-time" and not timestamp(data):
            errors.append(f"{at}: expected ISO 8601 timestamp with timezone")
    return errors


def indexes(data: dict) -> tuple[dict[str, dict], list[str]]:
    groups = {}
    errors = []
    for group in GROUPS:
        groups[group] = {}
        for record in data[group]:
            identifier = record["id"]
            if identifier in groups[group]:
                errors.append(f"{group}: duplicate ID {identifier}")
            groups[group][identifier] = record
    return groups, errors


def contract(data: dict, root: Path) -> list[str]:
    """Semantic *structure*: links, coverage and recorded inspection conditions."""
    schema = load_json(SKILL_ROOT / "assets" / "evidence.schema.json")
    errors = structure(data, schema, schema)
    if errors:
        return errors[:100]
    ix, errors = indexes(data)

    def link(record: dict, field: str, target: str, required: bool = False) -> None:
        label = record.get("id", "question")
        if required and not record[field]:
            errors.append(f"{label}.{field}: at least one link required")
        for identifier in record[field]:
            if identifier not in ix[target]:
                errors.append(f"{label}.{field}: unknown {identifier}")

    def exists(relative: str, label: str, prefix: str) -> None:
        try:
            if not relative.startswith(prefix + "/"):
                raise ContractError(f"Expected a file below {prefix}/")
            content = read_text(safe_path(root, relative))
            if not content.strip():
                errors.append(f"{label}: evidence file is blank")
        except ContractError as exc:
            errors.append(f"{label}: {exc}")

    coverage = data["coverage"]
    expected = {"quick": (2, 3), "default": (3, 5), "deep": (3, 7)}
    low, high = expected[coverage["depth"]]
    if not low <= len(data["references"]) <= high and not coverage["reference_exception"].strip():
        errors.append("coverage.reference_exception: explain reference count outside chosen depth")
    if not any(d["outcome"] == "REJECT" for d in data["decisions"]):
        if not coverage["rejection_note"].strip():
            errors.append("coverage.rejection_note: explain why there is no substantive rejection")
    for ref in data["references"]:
        lic = ref["license_record"]
        if lic["status"] == "INSPECTED" and not url(lic["locator"]):
            errors.append(f"{ref['id']}: inspected license needs its source URL")
        if lic["reuse_mode"] == "PATTERN_ONLY" and lic["code_copied"]:
            errors.append(f"{ref['id']}: PATTERN_ONLY conflicts with copied code")
        if lic["reuse_mode"] == "SOURCE_REUSE":
            if lic["status"] != "INSPECTED" or not lic["reuse_review"].strip():
                errors.append(
                    f"{ref['id']}: source reuse requires inspected rights and reuse review"
                )
    for source in data["sources"]:
        if source["reference_id"] not in ix["references"]:
            errors.append(f"{source['id']}: unknown {source['reference_id']}")
        status = source["inspection_status"]
        loc = source["locator"]
        if status == "UNAVAILABLE":
            if not source["limitations"]:
                errors.append(f"{source['id']}: unavailable source needs a reason")
            if source["note_path"]:
                exists(source["note_path"], source["id"], "sources")
            continue
        exists(source["note_path"], source["id"], "sources")
        if not loc["location"].strip():
            errors.append(f"{source['id']}: heading/symbol/lines/action locator required")
        if source["kind"] == "IMPLEMENTATION" and status == "INSPECTED":
            if not re.fullmatch(r"[a-fA-F0-9]{40}|[a-fA-F0-9]{64}", loc["revision"]):
                errors.append(
                    f"{source['id']}: inspected implementation needs immutable commit SHA"
                )
            if not loc["path"].strip():
                errors.append(f"{source['id']}: implementation path required")
    for claim in data["claims"]:
        kind = claim["class"]
        link(claim, "source_ids", "sources")
        link(claim, "premise_claim_ids", "claims")
        link(claim, "requirement_ids", "requirements")
        if kind == "USER_REQUIREMENT":
            if not claim["requirement_ids"]:
                errors.append(f"{claim['id']}: user claim needs requirement links")
            if any(
                ix["requirements"].get(r, {}).get("origin") == "ASSUMPTION"
                for r in claim["requirement_ids"]
            ):
                errors.append(f"{claim['id']}: assumption cannot be labelled USER_REQUIREMENT")
        elif kind == "INFERENCE":
            if not (claim["source_ids"] or claim["premise_claim_ids"] or claim["requirement_ids"]):
                errors.append(f"{claim['id']}: inference needs premises")
        else:
            if not claim["source_ids"]:
                errors.append(f"{claim['id']}: verified/observed claim needs source links")
            expected_kind = {
                "VERIFIED_SOURCE": "DOCUMENTATION",
                "OPEN_SOURCE_IMPLEMENTATION": "IMPLEMENTATION",
                "OBSERVED_PUBLIC_BEHAVIOR": "OBSERVATION",
            }[kind]
            for src_id in claim["source_ids"]:
                src = ix["sources"].get(src_id)
                if src and (
                    src["kind"] != expected_kind or src["inspection_status"] != "INSPECTED"
                ):
                    errors.append(f"{claim['id']}: {src_id} is not inspected {expected_kind}")
        if kind != "INFERENCE" and claim["premise_claim_ids"]:
            errors.append(f"{claim['id']}: derived premises belong to INFERENCE")
    # Cycle detection: a chain of inferences must eventually reach raw evidence.
    visiting, visited = set(), set()

    def visit(identifier: str) -> None:
        if identifier in visiting:
            errors.append(f"{identifier}: circular claim premises")
            return
        if identifier in visited or identifier not in ix["claims"]:
            return
        visiting.add(identifier)
        for premise in ix["claims"][identifier]["premise_claim_ids"]:
            visit(premise)
        visiting.remove(identifier)
        visited.add(identifier)

    for identifier in ix["claims"]:
        visit(identifier)
    for decision in data["decisions"]:
        link(decision, "requirement_ids", "requirements", True)
        link(decision, "evidence_ids", "claims", True)
        if not decision["alternatives"]:
            errors.append(f"{decision['id']}: record a simpler/direct alternative")
    for step in data["plan_units"]:
        link(step, "requirement_ids", "requirements", True)
        link(step, "decision_ids", "decisions", True)
        link(step, "acceptance_checks", "verification", True)
        for dec_id in step["decision_ids"]:
            if ix["decisions"].get(dec_id, {}).get("outcome") != "ADOPT":
                errors.append(
                    f"{step['id']}: rejected/deferred {dec_id} cannot be planned for build"
                )
        for check_id in step["acceptance_checks"]:
            check = ix["verification"].get(check_id)
            if check and (
                not check["required"]
                or not set(step["requirement_ids"]).issubset(check["requirement_ids"])
                or not set(step["decision_ids"]).issubset(check["decision_ids"])
            ):
                errors.append(
                    f"{step['id']}: {check_id} must cover this step's requirements/decisions"
                )
    for check in data["verification"]:
        link(check, "requirement_ids", "requirements")
        link(check, "decision_ids", "decisions")
        if check["method"] == "COMMAND" and not check["command"].strip():
            errors.append(f"{check['id']}: record the command, not a made-up execution")
        if check["result"] in ("PASS", "FAIL"):
            exists(check["evidence_path"], check["id"], "checks")
            if not check["tested_snapshot"].strip() or not timestamp(check["checked_at"]):
                errors.append(f"{check['id']}: actual result needs snapshot and timestamp")
        elif check["result"] == "NOT_RUN":
            if any(check[f] for f in ("evidence_path", "tested_snapshot", "checked_at")):
                errors.append(f"{check['id']}: NOT_RUN cannot have an execution receipt")
        elif check["evidence_path"]:
            exists(check["evidence_path"], check["id"], "checks")
    for question in data["questions"]:
        link(question, "evidence_ids", "claims")
        if question["status"] == "ANSWERED" and not (
            question["evidence_ids"] and question["resolution"].strip()
        ):
            errors.append("question: ANSWERED needs linked evidence and resolution")
    for req_id in ix["requirements"]:
        if not any(req_id in d["requirement_ids"] for d in data["decisions"]):
            errors.append(f"{req_id}: no linked decision")
        if not any(req_id in p["requirement_ids"] for p in data["plan_units"]):
            errors.append(f"{req_id}: no linked plan step")
        if not any(
            c["required"] and c["method"] != "SOURCE_AUDIT" and req_id in c["requirement_ids"]
            for c in data["verification"]
        ):
            errors.append(f"{req_id}: no required acceptance check")
    for dec_id, decision in ix["decisions"].items():
        if decision["outcome"] == "ADOPT":
            if not any(dec_id in p["decision_ids"] for p in data["plan_units"]):
                errors.append(f"{dec_id}: adopted decision has no plan step")
            if not any(
                c["required"] and c["method"] != "SOURCE_AUDIT" and dec_id in c["decision_ids"]
                for c in data["verification"]
            ):
                errors.append(f"{dec_id}: adopted decision has no required check")
    return errors[:100]


def cell(value: object) -> str:
    """Keep untrusted content inside a Markdown cell; no embedded directives."""
    if isinstance(value, tuple):
        label, target = value
        return f"[{cell(label)}]({quote(target, safe='/:%?#=&+@,~')})"
    if isinstance(value, list):
        return ", ".join(cell(item) for item in value) or "—"
    text = str(value)
    for before, after in (
        ("&", "&amp;"),
        ("<", "&lt;"),
        (">", "&gt;"),
        ("|", r"\|"),
        ("[", r"\["),
        ("]", r"\]"),
        (chr(96), "&#96;"),
    ):
        text = text.replace(before, after)
    return text.replace("\n", "<br>").replace("\r", "")


def table(headers: list[str], rows: list[list[object]]) -> str:
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    lines.extend("| " + " | ".join(cell(v) for v in row) + " |" for row in rows)
    return "\n".join(lines)


def blocks(data: dict) -> dict[str, str]:
    notes = {s["id"]: s["note_path"] for s in data["sources"]}
    return {
        "references": table(
            ["ID", "Reference", "Why relevant", "Mismatch", "License / reuse"],
            [
                [
                    r["id"],
                    (r["canonical_url"], r["canonical_url"]),
                    r["relevance"],
                    r["mismatch"],
                    f"{r['license_record']['status']} · "
                    f"{r['license_record']['spdx'] or 'unknown'} · "
                    f"{r['license_record']['reuse_mode']}",
                ]
                for r in data["references"]
            ],
        ),
        "sources": table(
            ["ID / note", "Primary source", "Locator", "Inspection"],
            [
                [
                    (s["id"], s["note_path"]) if s["note_path"] else s["id"],
                    ("original", s["url"]),
                    " · ".join(
                        v
                        for v in (
                            s["locator"]["revision"],
                            s["locator"]["path"],
                            s["locator"]["location"],
                        )
                        if v
                    ),
                    s["inspection_status"],
                ]
                for s in data["sources"]
            ],
        ),
        "evidence": table(
            ["ID", "Claim", "Class", "Sources / premises", "Scope"],
            [
                [
                    c["id"],
                    c["statement"],
                    LABELS[c["class"]],
                    [
                        (identifier, notes[identifier]) if notes.get(identifier) else identifier
                        for identifier in c["source_ids"]
                    ]
                    + c["premise_claim_ids"]
                    + c["requirement_ids"],
                    c["scope"],
                ]
                for c in data["claims"]
            ],
        ),
        "decisions": table(
            ["ID", "Choice", "Outcome", "Evidence", "Reason / complexity", "Revisit"],
            [
                [
                    d["id"],
                    d["candidate"],
                    d["outcome"],
                    d["evidence_ids"],
                    d["rationale"] + " Complexity: " + d["complexity_cost"],
                    d["revisit_trigger"],
                ]
                for d in data["decisions"]
            ],
        ),
        "plan": table(
            ["ID", "Outcome", "Requirements", "Decisions", "Acceptance"],
            [
                [
                    p["id"],
                    p["outcome"],
                    p["requirement_ids"],
                    p["decision_ids"],
                    p["acceptance_checks"],
                ]
                for p in data["plan_units"]
            ],
        ),
        "checks": table(
            ["ID", "Criterion", "Result", "Method", "Evidence", "Tested snapshot"],
            [
                [
                    c["id"],
                    c["criterion"],
                    c["result"],
                    c["method"],
                    ("output", c["evidence_path"]) if c["evidence_path"] else "—",
                    c["tested_snapshot"] or "—",
                ]
                for c in data["verification"]
            ],
        ),
    }


def markers(name: str) -> tuple[str, str]:
    return f"<!-- rfb:{name}:start -->", f"<!-- rfb:{name}:end -->"


def update_block(text: str, name: str, content: str) -> str:
    start, end = markers(name)
    if text.count(start) != 1 or text.count(end) != 1:
        raise ContractError(f"Expected exactly one managed block: {name}")
    left, tail = text.split(start, 1)
    _old, right = tail.split(end, 1) if end in tail else ("", "")
    if not right and end not in tail:
        raise ContractError(f"Malformed managed block: {name}")
    return f"{left}{start}\n{content}\n{end}{right}"


def rendered(root: Path, data: dict, create: bool = False) -> dict[str, str]:
    generated = blocks(data)
    outputs = {}
    for filename, names in REPORT_BLOCKS.items():
        path = safe_path(root, filename)
        if path.exists() or not create:
            text = read_text(path)
        else:
            text = read_text(
                SKILL_ROOT / "assets" / "templates" / filename.replace(".md", ".template.md")
            )
        for name in names:
            text = update_block(text, name, generated[name])
        outputs[filename] = text
    return outputs


def planning_fingerprint(root: Path, data: dict) -> str:
    planning = {k: v for k, v in data.items() if k != "verification"}
    planning["checks"] = [
        {
            k: c[k]
            for k in (
                "id",
                "requirement_ids",
                "decision_ids",
                "required",
                "method",
                "criterion",
                "command",
            )
        }
        for c in data["verification"]
    ]
    note_hashes = {}
    for src in data["sources"]:
        if src["note_path"]:
            note_hashes[src["note_path"]] = digest(read_text(safe_path(root, src["note_path"])))
    # Prebuild audit receipts are inputs; changing them invalidates readiness.
    audit = []
    for check in data["verification"]:
        if check["method"] == "SOURCE_AUDIT":
            audit.append(check)
            if check["evidence_path"]:
                note_hashes[check["evidence_path"]] = digest(
                    read_text(safe_path(root, check["evidence_path"]))
                )
    return digest(
        canonical(
            {
                "planning": planning,
                "source_notes": note_hashes,
                "audit": audit,
                "research": read_text(safe_path(root, "RESEARCH.md")),
                "plan": read_text(safe_path(root, "PLAN.md")),
            }
        )
    )


def atomic_write(root: Path, relative: str, content: str) -> None:
    target = safe_path(root, relative)
    if not target.parent.is_dir():
        raise ContractError(f"Parent directory does not exist: {relative}")
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            newline="\n",
            dir=target.parent,
            prefix=".rfb-",
            delete=False,
        ) as handle:
            temporary = Path(handle.name)
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        safe_path(root, relative)  # Recheck immediately before replacement.
        os.replace(temporary, target)
    except OSError as exc:
        raise ContractError(f"Cannot atomically write {relative}: {exc}") from exc
    finally:
        if temporary and temporary.exists():
            temporary.unlink()


def read_run(root: Path, data: dict) -> dict:
    path = safe_path(root, "run.json")
    if not path.exists():
        return {
            "schema_version": 1,
            "run_id": data["run_id"],
            "stage": "PLANNED",
            "prebuild_receipt": None,
            "postbuild_receipt": None,
        }
    state = load_json(path)
    if state.get("schema_version") != 1 or state.get("run_id") != data["run_id"]:
        raise ContractError("run.json has an unknown schema or mismatched run_id")
    if state.get("stage") not in {"PLANNED", "PREBUILD_CHECKED", "COMPLETE"}:
        raise ContractError("run.json has an unknown stage; preserve it and review")
    for key in ("prebuild_receipt", "postbuild_receipt"):
        if state.get(key) is not None and not isinstance(state[key], dict):
            raise ContractError(f"run.json.{key}: expected receipt object or null")
    return state


def check_run(root: Path, data: dict, stage: str, snapshot: str = "") -> list[str]:
    errors = contract(data, root)
    if errors:
        return errors
    if stage == "postbuild" and data["intent"] == "research-only":
        return ["Research-only is a handoff, not a completed build; use prebuild instead"]
    expected = rendered(root, data)
    for filename, content in expected.items():
        if read_text(safe_path(root, filename)) != content:
            errors.append(f"{filename}: managed blocks are stale; run render")
    if stage == "contract":
        return errors
    for question in data["questions"]:
        if question["critical"] and question["status"] == "OPEN":
            errors.append(f"Critical research question is open: {question['question']}")
    audits = [c for c in data["verification"] if c["method"] == "SOURCE_AUDIT" and c["required"]]
    if not audits or any(c["result"] != "PASS" for c in audits):
        errors.append("Prebuild needs a required PASS source audit with saved inspection notes")
    if not any(
        c["class"] in ("VERIFIED_SOURCE", "OPEN_SOURCE_IMPLEMENTATION", "OBSERVED_PUBLIC_BEHAVIOR")
        for c in data["claims"]
    ):
        errors.append(
            "Prebuild needs at least one inspected external claim; assumptions alone are not research"
        )
    if stage == "postbuild":
        if not snapshot.strip():
            errors.append(
                "Current snapshot missing: supply --snapshot from an actual host inspection"
            )
        state = read_run(root, data)
        receipt = state.get("prebuild_receipt")
        if not receipt or receipt.get("fingerprint") != planning_fingerprint(root, data):
            errors.append("Prebuild receipt missing or stale; review changes, then check prebuild")
        for check in data["verification"]:
            if not check["required"]:
                continue
            if check["result"] != "PASS":
                errors.append(f"{check['id']}: required check is {check['result']}, not PASS")
            if check["method"] != "SOURCE_AUDIT" and check["tested_snapshot"] != snapshot:
                errors.append(f"{check['id']}: tested snapshot differs from current snapshot")
        for dec in data["decisions"]:
            if dec["outcome"] in ("REJECT", "DEFER"):
                if not any(
                    c["required"]
                    and c["method"] == "DIFF_REVIEW"
                    and dec["id"] in c["decision_ids"]
                    for c in data["verification"]
                ):
                    errors.append(
                        f"{dec['id']}: rejected/deferred complexity needs required diff review"
                    )
    return errors[:100]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Offline artifact contract checks. PASS does not prove factual truth.",
        epilog="No network, subprocesses, permission grants, or host installation.",
    )
    parser.add_argument("--version", action="version", version=f"rfb {VERSION}")
    commands = parser.add_subparsers(dest="command", required=True)
    starter = commands.add_parser(
        "init", help="Create incomplete research templates in an empty directory"
    )
    starter.add_argument("run_dir", type=Path)
    starter.add_argument("--intent", choices=("full", "research-only"), default="full")
    for action in ("check", "render"):
        cmd = commands.add_parser(action)
        cmd.add_argument("run_dir", type=Path, help="Explicit artifact directory")
        if action == "check":
            cmd.add_argument(
                "--stage", choices=("contract", "prebuild", "postbuild"), default="contract"
            )
            cmd.add_argument(
                "--snapshot", default="", help="Actual current implementation snapshot"
            )
            cmd.add_argument("--json", action="store_true", help="Machine-readable result")
    args = parser.parse_args(argv)
    try:
        root = args.run_dir.resolve()
        if args.command == "init":
            if root.exists() and (not root.is_dir() or any(root.iterdir())):
                raise ContractError(
                    "init requires a new or empty directory; existing artifacts are preserved"
                )
            if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", root.name) or len(root.name) > 64:
                raise ContractError(
                    "Task directory name must be a lowercase task-slug, up to 64 characters"
                )
            data = load_json(SKILL_ROOT / "assets" / "evidence.template.json")
            data.update(run_id=root.name, intent=args.intent)
            templates = {
                name: read_text(
                    SKILL_ROOT / "assets" / "templates" / name.replace(".md", ".template.md")
                )
                for name in REPORT_BLOCKS
            }
            root.mkdir(parents=True, exist_ok=True)
            for folder in ("sources", "checks"):
                (root / folder).mkdir()
            atomic_write(root, "evidence.json", json.dumps(data, indent=2) + "\n")
            for name, content in templates.items():
                atomic_write(root, name, content)
            print(
                "Created incomplete templates. No research, source audit or checks have been performed."
            )
            return 0
        if not root.is_dir():
            raise ContractError("Run directory does not exist")
        data = load_json(safe_path(root, "evidence.json"))
        problems = contract(data, root)
        if args.command == "render":
            if problems:
                raise ContractError("\n".join(problems))
            # Validate all destinations/blocks/state before touching any file.
            outputs = rendered(root, data, create=True)
            state = read_run(root, data)
            for filename, content in outputs.items():
                atomic_write(root, filename, content)
            state["rendered_at"] = utc_now()
            if state.get("prebuild_receipt") and (
                state["prebuild_receipt"].get("fingerprint") != planning_fingerprint(root, data)
            ):
                state["stage"] = "PLANNED"
                state["prebuild_receipt"] = None
            # Rendering is never a new verification receipt.
            state["postbuild_receipt"] = None
            if state["stage"] == "COMPLETE":
                state["stage"] = "PREBUILD_CHECKED" if state["prebuild_receipt"] else "PLANNED"
            atomic_write(root, "run.json", json.dumps(state, indent=2, ensure_ascii=False) + "\n")
            print("Rendered managed tables; narrative preserved. No checks were executed.")
            return 0
        problems = check_run(root, data, args.stage, args.snapshot)
        if not problems and args.stage in ("prebuild", "postbuild"):
            state = read_run(root, data)
            receipt = {"fingerprint": planning_fingerprint(root, data), "checked_at": utc_now()}
            if args.stage == "prebuild":
                state["prebuild_receipt"] = receipt
                state["postbuild_receipt"] = None
                state["stage"] = "PREBUILD_CHECKED"
            else:
                check_hashes = {
                    c["evidence_path"]: digest(read_text(safe_path(root, c["evidence_path"])))
                    for c in data["verification"]
                    if c["evidence_path"]
                }
                receipt.update(
                    {
                        "snapshot": args.snapshot,
                        "evidence_hash": digest(canonical(data)),
                        "check_outputs": check_hashes,
                        "verification_hash": digest(read_text(safe_path(root, "VERIFICATION.md"))),
                    }
                )
                state["postbuild_receipt"] = receipt
                state["stage"] = "COMPLETE"
            atomic_write(root, "run.json", json.dumps(state, indent=2, ensure_ascii=False) + "\n")
        report = {
            "status": "FAIL" if problems else "CONTRACT_CHECKED",
            "stage": args.stage,
            "errors": problems,
            "limits": "Not a source truth check, write barrier, or authorization token.",
        }
        if args.json:
            print(json.dumps(report, ensure_ascii=False, indent=2))
        elif problems:
            print(f"FAIL ({args.stage}):")
            for problem in problems:
                print(f"  - {problem}")
        else:
            print(
                f"CONTRACT_CHECKED ({args.stage}). Recorded source audit checked structurally; "
                "factual truth and authorization remain outside this checker."
            )
        return 1 if problems else 0
    except (ContractError, OSError, RecursionError) as exc:
        if getattr(args, "json", False):
            print(json.dumps({"status": "FAIL", "errors": [str(exc)]}, ensure_ascii=False))
        else:
            print(f"rfb: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
