#!/usr/bin/env python3
"""NHRI risk model V4 evaluator (reference implementation)."""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path
from typing import Any, Dict

VERSION = 4
AGE_MIN = 35
AGE_MAX = 70
MODELS = ("chd", "stroke", "hypertension", "diabetes", "mace")

ARRAY_NAMES = {
    "chd": ("Average_CHD_Male", "Average_CHD_Female"),
    "stroke": ("Average_Stroke_Male", "Average_Stroke_Female"),
    "mace": ("Average_MACE_Male", "Average_MACE_Female"),
    "diabetes": ("Average_Diabetes_Male", "Average_Diabetes_Female"),
    "hypertension": ("Average_Hypertension_Male", "Average_Hypertension_Female"),
}

DEFAULT_POPULATION_PATH = (
    Path(__file__).resolve().parent.parent / "references" / "population-averages.json"
)


def java_round(value: float) -> int:
    if value >= 0:
        return int(math.floor(value + 0.5))
    return int(math.ceil(value - 0.5))


def round2(value: float) -> float:
    return java_round(value * 100.0) / 100.0


def prob_to_percent(probability: float) -> float:
    return java_round(probability * 10000.0) / 100.0


def load_population_arrays(path: str | Path = DEFAULT_POPULATION_PATH) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as handle:
        payload = json.load(handle)
    return payload["populationAverageArrays"]


def as_int(payload: Dict[str, Any], key: str) -> int:
    try:
        return int(payload.get(key, 0) or 0)
    except (TypeError, ValueError):
        return 0


def as_float(payload: Dict[str, Any], key: str) -> float:
    try:
        return float(payload.get(key, 0.0) or 0.0)
    except (TypeError, ValueError):
        return 0.0


def normalize_input(payload: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "gender": as_int(payload, "gender"),
        "age": as_int(payload, "age"),
        "sbp": as_int(payload, "sbp"),
        "tg": as_float(payload, "tg"),
        "ua": as_float(payload, "ua"),
        "chol": as_float(payload, "chol"),
        "hdlc": as_float(payload, "hdlc"),
        "ldlc": as_float(payload, "ldlc"),
        "glu": as_float(payload, "glu"),
        "bmi": as_float(payload, "bmi"),
        "height": as_float(payload, "height"),
        "weight": as_float(payload, "weight"),
        "ratio": as_float(payload, "ratio"),
        "waist": as_float(payload, "waist"),
        "hip": as_float(payload, "hip"),
        "hbp": as_int(payload, "hbp"),
        "diabetes": as_int(payload, "diabetes"),
        "smoke": as_int(payload, "smoke"),
    }


def make_output() -> Dict[str, Any]:
    return {
        "status": 0,
        "error": "",
        "message": "",
        "risk": 0.0,
        "populationAvg": 0.0,
        "multipleDiff": 0.0,
        "riskType": 0,
        "version": 0,
    }


def fail(output: Dict[str, Any], condition: bool, message: str) -> None:
    if not condition:
        output["status"] = 1
        output["error"] = message


def compute_bmi(weight: float, height_cm: float) -> float:
    if height_cm <= 0:
        return 0.0
    bmi = weight / ((height_cm / 100.0) ** 2)
    return round2(bmi)


def validate(model: str, data: Dict[str, Any], output: Dict[str, Any]) -> None:
    fail(output, data["age"] > 0, "age must be > 0")

    if model == "chd":
        fail(output, data["hdlc"] > 0, "hdlc must be > 0")
        fail(output, data["waist"] > 0, "waist must be > 0")
        if data["gender"] != 1:
            fail(output, data["sbp"] > 0, "female sbp must be > 0")
            fail(output, data["chol"] > 0, "female chol must be > 0")
            fail(output, data["tg"] > 0, "female tg must be > 0")
        return

    if model == "stroke":
        fail(output, data["sbp"] > 0, "sbp must be > 0")
        if data["gender"] == 1:
            fail(output, data["glu"] > 0, "male glu must be > 0")
            fail(output, data["tg"] > 0, "male tg must be > 0")
        else:
            fail(output, data["waist"] > 0, "female waist must be > 0")
        return

    if model == "hypertension":
        fail(output, data["sbp"] > 0, "sbp must be > 0")
        has_bmi_or_hw = data["bmi"] > 0 or (data["height"] > 0 and data["weight"] > 0)
        fail(output, has_bmi_or_hw, "bmi > 0 or both height and weight are required")
        if data["gender"] == 1:
            fail(output, data["hdlc"] > 0, "male hdlc must be > 0")
            fail(output, data["ldlc"] > 0, "male ldlc must be > 0")
        else:
            fail(output, data["tg"] > 0, "female tg must be > 0")
            fail(output, data["glu"] > 0, "female glu must be > 0")
        return

    if model == "diabetes":
        fail(output, data["glu"] > 0, "glu must be > 0")
        fail(output, data["tg"] > 0, "tg must be > 0")
        has_bmi_or_hw = data["bmi"] > 0 or (data["height"] > 0 and data["weight"] > 0)
        fail(output, has_bmi_or_hw, "bmi > 0 or both height and weight are required")
        if data["gender"] == 1:
            fail(output, data["chol"] > 0, "male chol must be > 0")
        else:
            fail(output, data["waist"] > 0, "female waist must be > 0")
            fail(output, data["hdlc"] > 0, "female hdlc must be > 0")
        return

    if model == "mace":
        fail(output, data["sbp"] > 0, "sbp must be > 0")
        fail(output, data["hdlc"] > 0, "hdlc must be > 0")
        fail(output, data["waist"] > 0, "waist must be > 0")
        if data["gender"] != 1:
            fail(output, data["chol"] > 0, "female chol must be > 0")
        return


def compute_z_and_s0(model: str, male: bool, data: Dict[str, Any]) -> tuple[float, float]:
    age_log = math.log10(float(data["age"]))

    if model == "chd":
        if male:
            z = (
                8.3077 * (age_log - 1.7056)
                + 0.6715 * (float(data["hbp"]) - 0.3485)
                + 0.0163 * (data["waist"] - 82.0694)
                - 0.0081 * (data["hdlc"] - 53.06)
            )
            return z, 0.8936
        ratio = data["chol"] / data["hdlc"]
        z = (
            9.3891 * (age_log - 1.6886)
            + 0.0425 * (data["waist"] - 76.36177)
            + 0.0015 * (float(data["sbp"]) - 123.379)
            + 0.3581 * (ratio - 3.5753)
            + 0.0001 * (data["tg"] - 107.9153)
        )
        return z, 0.9405

    if model == "stroke":
        if male:
            z = (
                8.9714 * (age_log - 1.7093)
                + 0.0238 * (float(data["sbp"]) - 128.6824)
                + 0.0046 * (data["glu"] - 100.2177)
                + 0.0017 * (data["tg"] - 127.9926)
            )
            return z, 0.87
        z = (
            5.1186 * (age_log - 1.6963)
            + 0.7794 * (float(data["smoke"]) - 0.0522)
            + 0.023 * (data["waist"] - 77.1681)
            + 0.4908 * (float(data["hbp"]) - 0.342)
            + 0.581 * (float(data["diabetes"]) - 0.0914)
            + 0.0139 * (float(data["sbp"]) - 126.0013)
        )
        return z, 0.91

    if model == "hypertension":
        if male:
            z = (
                6.6698 * (age_log - 1.6973)
                + 0.0224 * (float(data["sbp"]) - 117.5462)
                + 0.0368 * (data["bmi"] - 23.1587)
                - 0.0113 * (data["hdlc"] - 53.37)
                + 0.0008 * (data["ldlc"] - 116.9147)
            )
            return z, 0.65
        z = (
            4.1239 * (age_log - 1.6789)
            + 0.0647 * (data["bmi"] - 24.0371)
            + 0.3866 * (float(data["smoke"]) - 0.051)
            + 0.0313 * (float(data["sbp"]) - 115.6778)
            + 0.0024 * (data["tg"] - 105.1218)
            + 0.003 * (data["glu"] - 96.3894)
        )
        return z, 0.6

    if model == "diabetes":
        if male:
            z = (
                4.3665 * (age_log - 1.7126)
                + 0.1281 * (data["bmi"] - 23.8756)
                + 0.0332 * (data["glu"] - 94.1031)
                + 0.002 * (data["chol"] - 196.9184)
                + 0.0024 * (data["tg"] - 127.0042)
            )
            return z, 0.79
        z = (
            2.8928 * (age_log - 1.6939)
            + 0.0723 * (data["bmi"] - 24.6413)
            + 0.0195 * (data["waist"] - 76.6563)
            + 0.0334 * (data["glu"] - 95.0456)
            + 0.0016 * (data["tg"] - 111.8046)
            - 0.009 * (data["hdlc"] - 59.737)
        )
        return z, 0.76

    if model == "mace":
        if male:
            z = (
                7.3146 * (age_log - 1.7056)
                + 0.0114 * (data["waist"] - 82.0694)
                + 0.027 * (float(data["sbp"]) - 127.0251)
                - 0.0045 * (data["hdlc"] - 53.06)
            )
            return z, 0.82
        ratio = data["chol"] / data["hdlc"]
        z = (
            6.8833 * (age_log - 1.6886)
            + 0.1923 * (float(data["smoke"]) - 0.0462)
            + 0.0257 * (data["waist"] - 76.3618)
            + 0.0128 * (float(data["sbp"]) - 123.379)
            + 0.3054 * (ratio - 3.5753)
        )
        return z, 0.9036

    raise ValueError(f"Unsupported model: {model}")


def population_avg_percent(
    model: str,
    male: bool,
    age: int,
    population_arrays: Dict[str, Any],
) -> float:
    if age < AGE_MIN or age > AGE_MAX:
        return 0.0
    key = ARRAY_NAMES[model][0 if male else 1]
    return prob_to_percent(float(population_arrays[key][age - AGE_MIN]))


def evaluate(
    model: str,
    payload: Dict[str, Any],
    population_arrays: Dict[str, Any] | None = None,
) -> Dict[str, Any]:
    normalized_model = model.lower().strip()
    if normalized_model not in MODELS:
        raise ValueError(f"model must be one of: {', '.join(MODELS)}")

    arrays = population_arrays or load_population_arrays()
    data = normalize_input(payload)
    output = make_output()

    validate(normalized_model, data, output)
    if output["status"] == 1:
        return output

    output["version"] = VERSION

    if normalized_model in {"hypertension", "diabetes"} and data["bmi"] <= 0:
        data["bmi"] = compute_bmi(data["weight"], data["height"])

    male = data["gender"] == 1
    z_value, s0 = compute_z_and_s0(normalized_model, male, data)
    risk_probability = 1.0 - math.pow(s0, math.exp(z_value))
    risk = prob_to_percent(risk_probability)

    population_avg = population_avg_percent(normalized_model, male, data["age"], arrays)
    multiple_diff = 0.0
    if population_avg > 0:
        multiple_diff = round2((risk / population_avg) * 100.0)

    risk_type = 0
    if normalized_model == "hypertension":
        if multiple_diff > 1.25:
            risk_type = 2
        elif multiple_diff >= 0.75:
            risk_type = 1
    else:
        if risk >= 20.0:
            risk_type = 2
        elif risk >= 10.0:
            risk_type = 1

    output["risk"] = risk
    output["populationAvg"] = population_avg
    output["multipleDiff"] = multiple_diff
    output["riskType"] = risk_type
    return output


def evaluate_all(
    payload: Dict[str, Any],
    population_arrays: Dict[str, Any] | None = None,
) -> Dict[str, Dict[str, Any]]:
    arrays = population_arrays or load_population_arrays()
    return {model: evaluate(model, payload, arrays) for model in MODELS}


def parse_payload(args: argparse.Namespace) -> Dict[str, Any]:
    if args.input and args.inline_json:
        raise ValueError("Use either --input or --json, not both.")
    if args.input:
        with open(args.input, "r", encoding="utf-8") as handle:
            return json.load(handle)
    if args.inline_json:
        return json.loads(args.inline_json)
    if not sys.stdin.isatty():
        return json.load(sys.stdin)
    raise ValueError("Provide --input, --json, or piped JSON from stdin.")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", choices=MODELS, help="Evaluate only one model")
    parser.add_argument("--input", help="Path to JSON payload")
    parser.add_argument("--json", dest="inline_json", help="Inline JSON payload")
    parser.add_argument(
        "--population-arrays",
        default=str(DEFAULT_POPULATION_PATH),
        help="Path to population average arrays JSON",
    )
    parser.add_argument("--pretty", action="store_true", help="Pretty-print output")
    args = parser.parse_args()

    payload = parse_payload(args)
    arrays = load_population_arrays(args.population_arrays)

    if args.model:
        result: Any = evaluate(args.model, payload, arrays)
    else:
        result = evaluate_all(payload, arrays)

    if args.pretty:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
