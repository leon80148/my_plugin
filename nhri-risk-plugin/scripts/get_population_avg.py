#!/usr/bin/env python3
"""Lookup NHRI V4 population average risk by model, gender, and age."""

import argparse
import json
from pathlib import Path

ARRAY_PREFIX = {
    "chd": "Average_CHD",
    "stroke": "Average_Stroke",
    "hypertension": "Average_Hypertension",
    "diabetes": "Average_Diabetes",
    "mace": "Average_MACE",
}


def parse_gender(raw: str) -> str:
    value = raw.strip().lower()
    if value in {"1", "male", "m"}:
        return "Male"
    if value in {"0", "female", "f"}:
        return "Female"
    raise ValueError("gender must be male/female or 1/0")


def java_round(value: float) -> int:
    if value >= 0:
        return int(value + 0.5)
    return int(value - 0.5)


def to_percent(probability: float) -> float:
    return java_round(probability * 10000.0) / 100.0


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", required=True, choices=sorted(ARRAY_PREFIX.keys()))
    parser.add_argument("--gender", required=True, help="male/female or 1/0")
    parser.add_argument("--age", required=True, type=int)
    parser.add_argument(
        "--arrays",
        default=str(Path(__file__).resolve().parent.parent / "references" / "population-averages.json"),
        help="Path to population average JSON",
    )
    args = parser.parse_args()

    with open(args.arrays, "r", encoding="utf-8") as handle:
        payload = json.load(handle)

    arrays = payload["populationAverageArrays"]
    sex = parse_gender(args.gender)
    key = f"{ARRAY_PREFIX[args.model]}_{sex}"

    if args.age < 35 or args.age > 70:
        print("0")
        return

    value = arrays[key][args.age - 35]
    print(to_percent(value))


if __name__ == "__main__":
    main()
