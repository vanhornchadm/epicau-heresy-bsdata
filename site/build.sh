#!/usr/bin/env bash
# Build the Quartz site into site/public.
#
#   site/build.sh            build once
#   site/build.sh --serve    build and preview at http://localhost:8080, rebuilding on changes
#
# Fetches the pinned Quartz release into site/.quartz on first run (and when QUARTZ_VERSION
# changes), copies this folder's quartz.config.ts and quartz.layout.ts over its own, then
# generates the Markdown from the data files with build_content.py. Needs git, Node 22+ and Python 3.
set -euo pipefail

QUARTZ_VERSION=v4.5.2
SITE="$(cd "$(dirname "$0")" && pwd)"
Q="$SITE/.quartz"

if [ "$(cat "$Q/.version" 2>/dev/null)" != "$QUARTZ_VERSION" ]; then
  rm -rf "$Q"
  git -c advice.detachedHead=false clone --quiet --depth 1 --branch "$QUARTZ_VERSION" \
    https://github.com/jackyzha0/quartz.git "$Q"
  rm -rf "$Q/.git" "$Q/content" "$Q/docs"
  (cd "$Q" && npm ci --no-audit --no-fund)
  echo "$QUARTZ_VERSION" > "$Q/.version"
fi

cp "$SITE/quartz.config.ts" "$SITE/quartz.layout.ts" "$Q/"
python3 "$SITE/build_content.py" "$SITE/content"
cd "$Q"
npx quartz build --directory "$SITE/content" --output "$SITE/public" "$@"
