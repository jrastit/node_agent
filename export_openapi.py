#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

from node_agent.myapp import init_app


def main():
    parser = argparse.ArgumentParser(
        description="Export FastAPI OpenAPI schema for frontend generation"
    )
    parser.add_argument(
        "output",
        nargs="?",
        default="swagger.json",
        help="Output path for the OpenAPI JSON file (default: swagger.json)",
    )
    args = parser.parse_args()

    app = init_app(init_db=False)
    schema = app.openapi()

    output_path = Path(args.output).expanduser().resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(schema, indent=2), encoding="utf-8")

    print(f"OpenAPI exported to {output_path}")


if __name__ == "__main__":
    main()
