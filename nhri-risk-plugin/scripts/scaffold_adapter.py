#!/usr/bin/env python3
"""Scaffold NHRI API adapter templates for selected platform."""

from __future__ import annotations

import argparse
from pathlib import Path

TEMPLATES = {
    "fastapi": ("fastapi_app.py.tpl", "app.py"),
    "express": ("express_app.js.tpl", "app.js"),
    "spring": ("spring_risk_controller.java.tpl", "RiskController.java"),
}


def render_template(
    template_text: str,
    service_name: str,
    route_prefix: str,
    java_package: str,
) -> str:
    return (
        template_text.replace("{{SERVICE_NAME}}", service_name)
        .replace("{{ROUTE_PREFIX}}", route_prefix)
        .replace("{{JAVA_PACKAGE}}", java_package)
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--platform", required=True, choices=sorted(TEMPLATES.keys()))
    parser.add_argument("--output", required=True, help="Output directory")
    parser.add_argument("--service-name", default="nhri-risk-api")
    parser.add_argument("--route-prefix", default="/risk")
    parser.add_argument("--java-package", default="com.example.nhri")
    args = parser.parse_args()

    script_dir = Path(__file__).resolve().parent
    assets_dir = script_dir.parent / "assets"

    source_name, target_name = TEMPLATES[args.platform]
    source_path = assets_dir / source_name

    if not source_path.exists():
        raise FileNotFoundError(f"Template not found: {source_path}")

    rendered = render_template(
        source_path.read_text(encoding="utf-8"),
        service_name=args.service_name,
        route_prefix=args.route_prefix,
        java_package=args.java_package,
    )

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    target_path = output_dir / target_name
    target_path.write_text(rendered, encoding="utf-8")

    print(f"Scaffolded {args.platform} adapter to {target_path}")


if __name__ == "__main__":
    main()
