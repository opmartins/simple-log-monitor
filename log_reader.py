"""CLI to count log occurrences per rule defined in a YAML file."""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from collections import OrderedDict
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

import re
import yaml


def parse_args(argv: Iterable[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Count log matches for regex rules defined in a YAML file."
    )
    parser.add_argument(
        "log_file",
        type=Path,
        help="Path to the log file to scan",
    )
    parser.add_argument(
        "rules_file",
        type=Path,
        help="Path to the YAML file describing regex rules",
    )
    return parser.parse_args(argv)


def load_rules(rules_path: Path) -> List[Tuple[str, re.Pattern[str]]]:
    """Load rules from YAML preserving order and compile regex patterns."""
    if not rules_path.is_file():
        raise SystemExit(f"Rules file not found: {rules_path}")

    with rules_path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)

    if not isinstance(data, list):
        raise SystemExit("Rules file must contain a list of rule objects")

    compiled_rules: List[Tuple[str, re.Pattern[str]]] = []
    for index, item in enumerate(data, start=1):
        if not isinstance(item, dict) or "regex" not in item:
            raise SystemExit(
                f"Invalid rule at position {index}: expected mapping with a 'regex' key"
            )
        name = str(item.get("name", f"rule_{index}"))
        pattern = re.compile(str(item["regex"]))
        compiled_rules.append((name, pattern))

    if not compiled_rules:
        raise SystemExit("No rules found in rules file")

    return compiled_rules


def count_matches(log_path: Path, rules: List[Tuple[str, re.Pattern[str]]]) -> Dict[str, int]:
    if not log_path.is_file():
        raise SystemExit(f"Log file not found: {log_path}")

    counts: Dict[str, int] = OrderedDict((name, 0) for name, _ in rules)
    with log_path.open("r", encoding="utf-8") as handle:
        for line in handle:
            for name, pattern in rules:
                if pattern.search(line):
                    counts[name] += 1
    return counts


def persist_results(log_path: Path, counts: Dict[str, int]) -> None:
    metrics_dir = Path("metrics")
    processed_dir = Path("processed")
    metrics_dir.mkdir(parents=True, exist_ok=True)
    processed_dir.mkdir(parents=True, exist_ok=True)

    metrics_path = metrics_dir / log_path.name
    with metrics_path.open("w", encoding="utf-8") as handle:
        json.dump(counts, handle, indent=2)

    destination = processed_dir / log_path.name
    shutil.move(str(log_path), destination)


def main(argv: Iterable[str] | None = None) -> int:
    args = parse_args(argv)
    log_path = args.log_file
    rules = load_rules(args.rules_file)
    counts = count_matches(log_path, rules)
    for name, total in counts.items():
        print(f"{name}: {total}")

    persist_results(log_path, counts)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
