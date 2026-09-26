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
cap_docs_source="../../vexy-screensese-cap/apps/web/content/docs"

case "${1:-build}" in
  build)
    if [[ ! -d "$cap_docs_source" ]]; then
      cap_docs_checkout="$(mktemp -d)"
      trap 'rm -rf "$cap_docs_checkout"' EXIT
      git clone --depth 1 --filter=blob:none --sparse https://github.com/vexyart/vexy-screensese-cap "$cap_docs_checkout/cap"
      git -C "$cap_docs_checkout/cap" sparse-checkout set apps/web/content/docs
      cap_docs_source="$cap_docs_checkout/cap/apps/web/content/docs"
    fi
    uv run --with fire import_cap_docs.py --source="$cap_docs_source"
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
