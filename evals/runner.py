#!/usr/bin/env python3
"""Small, dependency-free eval runner for skill routing and artifacts."""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


def load(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data.get("evals"), list):
        raise ValueError("case file requires an evals array")
    return data


def validate(case: dict) -> list[str]:
    items = case["evals"]
    triggers = [item for item in items if item.get("kind", "trigger") == "trigger"]
    errors = []
    if sum(item.get("expected") is True for item in triggers) < 3:
        errors.append("need at least 3 positive trigger evals")
    if sum(item.get("expected") is False for item in triggers) < 2:
        errors.append("need at least 2 negative trigger evals")
    if not any(item.get("kind") == "artifact" for item in items):
        errors.append("need at least 1 artifact eval")
    return errors


def trigger_score(prompt: str, keywords: list[str]) -> bool:
    """Approximate routing with declared signature terms, not generic verbs."""
    words = set(re.findall(r"[a-z0-9$-]+", prompt.lower()))
    return bool(words.intersection(k.lower() for k in keywords))


def run(case_path: Path) -> tuple[int, list[str]]:
    case = load(case_path)
    root = case_path.parent.parent
    failures: list[str] = []
    checked = 0
    for item in case["evals"]:
        kind = item.get("kind", "trigger")
        checked += 1
        if kind == "trigger":
            actual = trigger_score(item["prompt"], item.get("keywords", []))
            if actual != item["expected"]:
                failures.append(f"{item['id']}: expected {item['expected']}, got {actual}")
        elif kind == "artifact":
            fixture = root / "fixtures" / item["fixture"]
            for expectation in item.get("expectations", []):
                path = fixture / expectation["path"]
                if not path.is_file():
                    failures.append(f"{item['id']}: missing {expectation['path']}")
                elif expectation["contains"] not in path.read_text(encoding="utf-8"):
                    failures.append(f"{item['id']}: {expectation['path']} lacks {expectation['contains']!r}")
        else:
            failures.append(f"{item.get('id', '<unknown>')}: unknown kind {kind!r}")
    return checked, failures


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("case", nargs="?", default="evals/cases/taskflow.json")
    args = parser.parse_args()
    try:
        case_path = Path(args.case)
        case = load(case_path)
        validation = validate(case)
        if validation:
            print("INVALID CASE")
            print("\n".join(f"- {error}" for error in validation))
            return 2
        checked, failures = run(case_path)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"EVAL ERROR: {exc}", file=sys.stderr)
        return 2
    if failures:
        print(f"FAIL ({len(failures)}/{checked})")
        print("\n".join(f"- {failure}" for failure in failures))
        return 1
    print(f"PASS ({checked} evals)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
