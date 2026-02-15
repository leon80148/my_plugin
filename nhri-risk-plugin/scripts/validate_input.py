#!/usr/bin/env python3
"""Validate NHRI V4 inputs for one or all models."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any, Dict, List

MODELS = ("chd", "stroke", "hypertension", "diabetes", "mace")

ERRORS = {
    "AGE_REQUIRED": ("age", "age must be > 0"),
    "SBP_REQUIRED": ("sbp", "sbp must be > 0"),
    "HDLC_REQUIRED": ("hdlc", "hdlc must be > 0"),
    "WAIST_REQUIRED": ("waist", "waist must be > 0"),
    "CHOL_REQUIRED": ("chol", "chol must be > 0"),
    "TG_REQUIRED": ("tg", "tg must be > 0"),
    "GLU_REQUIRED": ("glu", "glu must be > 0"),
    "LDLC_REQUIRED": ("ldlc", "ldlc must be > 0"),
    "BMI_OR_HW_REQUIRED": (
        "bmi,height,weight",
        "bmi > 0 or both height and weight must be > 0",
    ),
}


class ValidationError(Exception):
    pass


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


def normalize(payload: Dict[str, Any]) -> Dict[str, Any]:
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


def add_error(error_list: List[Dict[str, str]], code: str) -> None:
    field, message = ERRORS[code]
    error_list.append({"code": code, "field": field, "message": message})


def validate_model(model: str, data: Dict[str, Any]) -> Dict[str, Any]:
    model_name = model.lower().strip()
    if model_name not in MODELS:
        raise ValidationError(f"Unsupported model: {model}")

    male = data["gender"] == 1
    errors: List[Dict[str, str]] = []

    if data["age"] <= 0:
        add_error(errors, "AGE_REQUIRED")

    if model_name == "chd":
        if data["hdlc"] <= 0:
            add_error(errors, "HDLC_REQUIRED")
        if data["waist"] <= 0:
            add_error(errors, "WAIST_REQUIRED")
        if not male:
            if data["sbp"] <= 0:
                add_error(errors, "SBP_REQUIRED")
            if data["chol"] <= 0:
                add_error(errors, "CHOL_REQUIRED")
            if data["tg"] <= 0:
                add_error(errors, "TG_REQUIRED")

    elif model_name == "stroke":
        if data["sbp"] <= 0:
            add_error(errors, "SBP_REQUIRED")
        if male:
            if data["glu"] <= 0:
                add_error(errors, "GLU_REQUIRED")
            if data["tg"] <= 0:
                add_error(errors, "TG_REQUIRED")
        else:
            if data["waist"] <= 0:
                add_error(errors, "WAIST_REQUIRED")

    elif model_name == "hypertension":
        if data["sbp"] <= 0:
            add_error(errors, "SBP_REQUIRED")
        if not (data["bmi"] > 0 or (data["height"] > 0 and data["weight"] > 0)):
            add_error(errors, "BMI_OR_HW_REQUIRED")
        if male:
            if data["hdlc"] <= 0:
                add_error(errors, "HDLC_REQUIRED")
            if data["ldlc"] <= 0:
                add_error(errors, "LDLC_REQUIRED")
        else:
            if data["tg"] <= 0:
                add_error(errors, "TG_REQUIRED")
            if data["glu"] <= 0:
                add_error(errors, "GLU_REQUIRED")

    elif model_name == "diabetes":
        if data["glu"] <= 0:
            add_error(errors, "GLU_REQUIRED")
        if data["tg"] <= 0:
            add_error(errors, "TG_REQUIRED")
        if not (data["bmi"] > 0 or (data["height"] > 0 and data["weight"] > 0)):
            add_error(errors, "BMI_OR_HW_REQUIRED")
        if male:
            if data["chol"] <= 0:
                add_error(errors, "CHOL_REQUIRED")
        else:
            if data["waist"] <= 0:
                add_error(errors, "WAIST_REQUIRED")
            if data["hdlc"] <= 0:
                add_error(errors, "HDLC_REQUIRED")

    elif model_name == "mace":
        if data["sbp"] <= 0:
            add_error(errors, "SBP_REQUIRED")
        if data["hdlc"] <= 0:
            add_error(errors, "HDLC_REQUIRED")
        if data["waist"] <= 0:
            add_error(errors, "WAIST_REQUIRED")
        if not male and data["chol"] <= 0:
            add_error(errors, "CHOL_REQUIRED")

    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "normalizedInput": data,
    }


def parse_payload(args: argparse.Namespace) -> Dict[str, Any]:
    if args.input and args.inline_json:
        raise ValidationError("Use either --input or --json, not both")
    if args.input:
        with open(args.input, "r", encoding="utf-8") as handle:
            return json.load(handle)
    if args.inline_json:
        return json.loads(args.inline_json)
    if not sys.stdin.isatty():
        return json.load(sys.stdin)
    raise ValidationError("Provide --input, --json, or piped JSON")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", choices=MODELS, help="Validate a single model")
    parser.add_argument("--input", help="Path to payload JSON")
    parser.add_argument("--json", dest="inline_json", help="Inline payload JSON")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print output")
    args = parser.parse_args()

    payload = parse_payload(args)
    normalized = normalize(payload)

    if args.model:
        output: Any = validate_model(args.model, normalized)
    else:
        output = {model: validate_model(model, normalized) for model in MODELS}

    if args.pretty:
        print(json.dumps(output, ensure_ascii=False, indent=2))
    else:
        print(json.dumps(output, ensure_ascii=False))


if __name__ == "__main__":
    main()
