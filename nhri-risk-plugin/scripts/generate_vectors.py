#!/usr/bin/env python3
"""Generate deterministic NHRI V4 regression vectors."""

from __future__ import annotations

import argparse
import json
import random
from pathlib import Path
from typing import Any, Dict, List

from nhri_risk_eval import MODELS, evaluate


def random_payload(rng: random.Random, gender: int, include_derived_bmi: bool) -> Dict[str, Any]:
    height = round(rng.uniform(145.0, 185.0), 1)
    weight = round(rng.uniform(45.0, 110.0), 1)
    bmi = round(rng.uniform(18.0, 38.0), 2)
    if include_derived_bmi:
        bmi = 0.0

    return {
        "gender": gender,
        "age": rng.randint(30, 80),
        "sbp": rng.randint(90, 185),
        "tg": round(rng.uniform(40.0, 320.0), 2),
        "ua": round(rng.uniform(2.0, 10.0), 2),
        "chol": round(rng.uniform(120.0, 320.0), 2),
        "hdlc": round(rng.uniform(25.0, 95.0), 2),
        "ldlc": round(rng.uniform(60.0, 220.0), 2),
        "glu": round(rng.uniform(70.0, 260.0), 2),
        "bmi": bmi,
        "height": height,
        "weight": weight,
        "ratio": 0.0,
        "waist": round(rng.uniform(60.0, 125.0), 2),
        "hip": round(rng.uniform(75.0, 130.0), 2),
        "hbp": rng.randint(0, 1),
        "diabetes": rng.randint(0, 1),
        "smoke": rng.randint(0, 1),
    }


def generate_vectors(per_group: int, seed: int) -> List[Dict[str, Any]]:
    rng = random.Random(seed)
    vectors: List[Dict[str, Any]] = []

    for model in MODELS:
        for gender in (1, 0):
            gender_label = "male" if gender == 1 else "female"
            for i in range(1, per_group + 1):
                include_derived_bmi = model in {"hypertension", "diabetes"} and i % 2 == 0
                payload = random_payload(rng, gender, include_derived_bmi)
                expected = evaluate(model, payload)
                vectors.append(
                    {
                        "id": f"{model}-{gender_label}-{i:03d}",
                        "model": model,
                        "input": payload,
                        "expected": expected,
                    }
                )

    return vectors


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--per-group", type=int, default=10, help="Cases per model/gender group")
    parser.add_argument("--seed", type=int, default=42, help="Random seed")
    parser.add_argument("--output", required=True, help="Output JSON path")
    args = parser.parse_args()

    vectors = generate_vectors(args.per_group, args.seed)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as handle:
        json.dump(vectors, handle, ensure_ascii=False, indent=2)

    print(f"Wrote {len(vectors)} vectors to {output_path}")


if __name__ == "__main__":
    main()
