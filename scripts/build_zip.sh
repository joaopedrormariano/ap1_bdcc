#!/usr/bin/env bash
set -e
OUT=app.zip
rm -f "$OUT"

zip -r "$OUT" . \
  -x "*.venv/*" \
  -x "*venv/*" \
  -x "*__pycache__/*" \
  -x "*.pyc" \
  -x "db.sqlite3" \
  -x ".env" \
  -x "*.git/*" \
  -x "media/*" \
  -x "staticfiles/*" \
  -x "app.zip" \
  -x "scripts/*" \
  -x "docs/*" \
  > /dev/null

echo ">> Gerado: $OUT"
