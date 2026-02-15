#!/usr/bin/env python3
"""Render NHRI evaluator outputs into markdown/text/json reports."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

MODELS = ("chd", "stroke", "hypertension", "diabetes", "mace")


class ReportError(Exception):
    pass


def parse_payload(args: argparse.Namespace) -> Dict[str, Any]:
    if args.input and args.inline_json:
        raise ReportError("Use either --input or --json, not both")
    if args.input:
        with open(args.input, "r", encoding="utf-8") as handle:
            return json.load(handle)
    if args.inline_json:
        return json.loads(args.inline_json)
    if not sys.stdin.isatty():
        return json.load(sys.stdin)
    raise ReportError("Provide --input, --json, or piped JSON")


def is_model_result(value: Any) -> bool:
    return isinstance(value, dict) and "status" in value and "riskType" in value


def detect_results(payload: Dict[str, Any], single_model_hint: str | None) -> Dict[str, Dict[str, Any]]:
    if any(key in payload for key in MODELS):
        out: Dict[str, Dict[str, Any]] = {}
        for model in MODELS:
            value = payload.get(model)
            if is_model_result(value):
                out[model] = value
        if out:
            return out

    if is_model_result(payload):
        model_name = (single_model_hint or "unknown").lower().strip()
        return {model_name: payload}

    raise ReportError("Input is not a recognizable evaluator output")


def band_for(model: str, result: Dict[str, Any]) -> str:
    if to_int(result.get("status", 1), 1) != 0:
        return "invalid"

    risk = to_float(result.get("risk", 0.0), 0.0)
    multiple_diff = to_float(result.get("multipleDiff", 0.0), 0.0)

    if model == "hypertension":
        if multiple_diff > 1.25:
            return "high"
        if multiple_diff >= 0.75:
            return "elevated"
        return "lower"

    if risk >= 20.0:
        return "high"
    if risk >= 10.0:
        return "elevated"
    return "lower"


def summary_for(band: str) -> str:
    if band == "high":
        return "High risk level. Recommend clinician review and short-interval follow-up."
    if band == "elevated":
        return "Elevated risk level. Recommend focused risk-factor management and follow-up."
    if band == "lower":
        return "Lower risk level. Continue routine monitoring and preventive care."
    return "Invalid or incomplete result. Verify inputs before interpretation."


def to_int(value: Any, default: int) -> int:
    try:
        if isinstance(value, bool):
            return int(value)
        if isinstance(value, (int, float)):
            return int(value)
        return int(str(value))
    except Exception:
        return default


def to_float(value: Any, default: float) -> float:
    try:
        if isinstance(value, (int, float)):
            return float(value)
        return float(str(value))
    except Exception:
        return default


def build_records(results: Dict[str, Dict[str, Any]]) -> List[Dict[str, Any]]:
    records: List[Dict[str, Any]] = []
    for model, result in results.items():
        band = band_for(model, result)
        records.append(
            {
                "model": model,
                "status": to_int(result.get("status", 1), 1),
                "risk": to_float(result.get("risk", 0.0), 0.0),
                "populationAvg": to_float(result.get("populationAvg", 0.0), 0.0),
                "multipleDiff": to_float(result.get("multipleDiff", 0.0), 0.0),
                "riskType": to_int(result.get("riskType", 0), 0),
                "version": to_int(result.get("version", 0), 0),
                "band": band,
                "summary": summary_for(band),
            }
        )
    return records


def aggregate(records: List[Dict[str, Any]]) -> Dict[str, Any]:
    high_count = sum(1 for item in records if item["band"] == "high")
    elevated_count = sum(1 for item in records if item["band"] == "elevated")
    lower_count = sum(1 for item in records if item["band"] == "lower")

    if high_count > 0:
        highest_band = "high"
    elif elevated_count > 0:
        highest_band = "elevated"
    elif lower_count > 0:
        highest_band = "lower"
    else:
        highest_band = "invalid"

    return {
        "highestBand": highest_band,
        "highCount": high_count,
        "elevatedCount": elevated_count,
        "lowerCount": lower_count,
    }


def render_markdown(report: Dict[str, Any], template_path: Path) -> str:
    template = template_path.read_text(encoding="utf-8")

    sections = []
    for item in report["models"]:
        sections.append(
            "\n".join(
                [
                    f"### {item['model'].upper()}",
                    f"- status: {item['status']}",
                    f"- band: {item['band']}",
                    f"- risk: {item['risk']}",
                    f"- populationAvg: {item['populationAvg']}",
                    f"- multipleDiff: {item['multipleDiff']}",
                    f"- riskType: {item['riskType']}",
                    f"- summary: {item['summary']}",
                ]
            )
        )

    overall = report["overall"]
    rendered = template
    rendered = rendered.replace("{{TITLE}}", report["title"])
    rendered = rendered.replace("{{GENERATED_AT}}", report["generatedAt"])
    rendered = rendered.replace("{{HIGHEST_BAND}}", overall["highestBand"])
    rendered = rendered.replace("{{HIGH_COUNT}}", str(overall["highCount"]))
    rendered = rendered.replace("{{ELEVATED_COUNT}}", str(overall["elevatedCount"]))
    rendered = rendered.replace("{{LOWER_COUNT}}", str(overall["lowerCount"]))
    rendered = rendered.replace("{{MODEL_SECTIONS}}", "\n\n".join(sections))
    return rendered


def render_text(report: Dict[str, Any]) -> str:
    lines = [
        report["title"],
        f"generatedAt: {report['generatedAt']}",
        f"highestBand: {report['overall']['highestBand']}",
        "",
    ]
    for item in report["models"]:
        lines.extend(
            [
                f"[{item['model']}]",
                f"status={item['status']} band={item['band']} risk={item['risk']} populationAvg={item['populationAvg']} multipleDiff={item['multipleDiff']} riskType={item['riskType']}",
                item["summary"],
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", help="Input JSON file")
    parser.add_argument("--json", dest="inline_json", help="Inline JSON input")
    parser.add_argument("--model", help="Model name for single-result input")
    parser.add_argument("--title", default="NHRI Risk Summary")
    parser.add_argument("--format", choices=("markdown", "text", "json"), default="markdown")
    parser.add_argument("--output", help="Optional output file")
    parser.add_argument("--pretty", action="store_true", help="Pretty output for JSON")
    args = parser.parse_args()

    payload = parse_payload(args)
    results = detect_results(payload, args.model)
    records = build_records(results)

    report = {
        "title": args.title,
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "models": records,
        "overall": aggregate(records),
    }

    if args.format == "json":
        text = json.dumps(report, ensure_ascii=False, indent=2 if args.pretty else None)
    elif args.format == "text":
        text = render_text(report)
    else:
        template_path = Path(__file__).resolve().parent.parent / "assets" / "report-template.md"
        text = render_markdown(report, template_path)

    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(text, encoding="utf-8")
        print(f"Report written to {output_path}")
    else:
        print(text)


if __name__ == "__main__":
    main()
