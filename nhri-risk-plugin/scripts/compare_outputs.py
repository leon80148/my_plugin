#!/usr/bin/env python3
"""Compare NHRI V4 expected vectors against actual outputs."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List, Tuple

INT_FIELDS = {"status", "riskType", "version"}
FLOAT_FIELDS = {"risk", "populationAvg", "multipleDiff"}
DEFAULT_FIELDS = ["status", "risk", "populationAvg", "multipleDiff", "riskType", "version"]


def load_json(path: str | Path) -> Any:
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def extract_result(item: Dict[str, Any]) -> Dict[str, Any]:
    for key in ("output", "actual", "result", "expected"):
        if isinstance(item.get(key), dict):
            return item[key]
    return item if isinstance(item, dict) else {}


def to_int(value: Any) -> int:
    if isinstance(value, bool):
        return int(value)
    if isinstance(value, (int, float)):
        return int(value)
    return int(str(value))


def to_float(value: Any) -> float:
    if isinstance(value, (int, float)):
        return float(value)
    return float(str(value))


def compare_records(
    expected_result: Dict[str, Any],
    actual_result: Dict[str, Any],
    fields: List[str],
    tolerance: float,
) -> List[str]:
    errors: List[str] = []

    for field in fields:
        expected_value = expected_result.get(field)
        actual_value = actual_result.get(field)

        try:
            if field in INT_FIELDS:
                if to_int(expected_value) != to_int(actual_value):
                    errors.append(
                        f"{field}: expected {expected_value}, actual {actual_value}"
                    )
            elif field in FLOAT_FIELDS:
                if abs(to_float(expected_value) - to_float(actual_value)) > tolerance:
                    errors.append(
                        f"{field}: expected {expected_value}, actual {actual_value}"
                    )
            else:
                if expected_value != actual_value:
                    errors.append(
                        f"{field}: expected {expected_value}, actual {actual_value}"
                    )
        except Exception:
            errors.append(f"{field}: expected {expected_value}, actual {actual_value}")

    return errors


def build_index(rows: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    index: Dict[str, Dict[str, Any]] = {}
    for row in rows:
        row_id = row.get("id")
        if isinstance(row_id, str):
            index[row_id] = extract_result(row)
    return index


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--expected", required=True, help="Expected vectors JSON")
    parser.add_argument("--actual", required=True, help="Actual outputs JSON")
    parser.add_argument(
        "--tolerance",
        type=float,
        default=1e-9,
        help="Floating point tolerance",
    )
    parser.add_argument(
        "--fields",
        default=",".join(DEFAULT_FIELDS),
        help="Comma-separated fields to compare",
    )
    parser.add_argument("--report", help="Optional mismatch report path")
    args = parser.parse_args()

    expected_rows = load_json(args.expected)
    actual_rows = load_json(args.actual)

    if not isinstance(expected_rows, list) or not isinstance(actual_rows, list):
        raise ValueError("Both expected and actual files must contain JSON arrays")

    fields = [field.strip() for field in args.fields.split(",") if field.strip()]
    actual_index = build_index(actual_rows)

    mismatches: List[Dict[str, Any]] = []
    missing_ids: List[str] = []

    for expected_row in expected_rows:
        row_id = expected_row.get("id")
        if not isinstance(row_id, str):
            continue

        expected_result = extract_result(expected_row)
        actual_result = actual_index.get(row_id)

        if actual_result is None:
            missing_ids.append(row_id)
            continue

        errors = compare_records(expected_result, actual_result, fields, args.tolerance)
        if errors:
            mismatches.append({"id": row_id, "errors": errors})

    total = len(expected_rows)
    missing = len(missing_ids)
    failed = len(mismatches)
    passed = total - missing - failed

    print(f"Total: {total}")
    print(f"Passed: {passed}")
    print(f"Missing IDs: {missing}")
    print(f"Mismatched: {failed}")

    if missing_ids:
        print("Missing ID examples:")
        for row_id in missing_ids[:10]:
            print(f"  - {row_id}")

    if mismatches:
        print("Mismatch examples:")
        for mismatch in mismatches[:10]:
            print(f"  - {mismatch['id']}")
            for error in mismatch["errors"][:6]:
                print(f"    * {error}")

    if args.report:
        report_payload = {
            "summary": {
                "total": total,
                "passed": passed,
                "missing": missing,
                "mismatched": failed,
            },
            "missingIds": missing_ids,
            "mismatches": mismatches,
        }
        report_path = Path(args.report)
        report_path.parent.mkdir(parents=True, exist_ok=True)
        with open(report_path, "w", encoding="utf-8") as handle:
            json.dump(report_payload, handle, ensure_ascii=False, indent=2)
        print(f"Report written to {report_path}")

    if missing_ids or mismatches:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
