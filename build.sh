#!/usr/bin/env bash
# this_file: build.sh
# Build or serve the Vexy Screensese docs site (ProperDocs + MaterialX).
#
# Usage:
#   ./build.sh build   # import Cap docs, build ./docs, add .nojekyll
#   ./build.sh serve   # local dev server with live reload
set -euo pipefail

cd "$(dirname "$0")/src_docs"

UV_ARGS=(uv run --with properdocs --with mkdocs-materialx)

case "${1:-build}" in
  build)
    uv run --with fire import_cap_docs.py
    "${UV_ARGS[@]}" properdocs build -f properdocs.yml -d ../docs --strict
    touch ../docs/.nojekyll
    echo "Built ./docs"
    ;;
  serve)
    "${UV_ARGS[@]}" properdocs serve -f properdocs.yml -a localhost:8000 -o
    ;;
  *)
    echo "Usage: $0 [build|serve]" >&2
    exit 1
    ;;
esac
