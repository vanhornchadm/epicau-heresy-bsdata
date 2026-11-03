#!/usr/bin/env bash
# Build the release assets BattleScribe and New Recruit download: each .gst/.cat zipped as .gstz/.catz, and a data
# index (<repo>.latest.bsi) listing them, the same assets BSData's publish-catpkg action makes.
#
#   tools/release_assets.sh <out_dir> <owner/repo> [display name]
#
# Asset names are escaped the way GitHub renames uploads (each run of characters other than letters, digits, '-'
# and '_' becomes '.'), so the index points at the names the release will have. The index's own URL is the
# repository's latest-release download, so a data index added once keeps updating. Needs the .NET SDK (for wham).
set -euo pipefail

OUT="$(mkdir -p "$1" && cd "$1" && pwd)"
REPO="$2"
NAME="${3:-${REPO#*/}}"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
WHAM_VERSION=0.13.0
WHAM_DIR="${WHAM_DIR:-$ROOT/.wham}"

# wham targets .NET 5; let it run on the newer runtime the machine has
export DOTNET_SKIP_FIRST_TIME_EXPERIENCE=1 DOTNET_NOLOGO=1 DOTNET_CLI_TELEMETRY_OPTOUT=1 DOTNET_ROLL_FORWARD=Major
if [ ! -x "$WHAM_DIR/wham" ]; then
  dotnet tool install wham --version "$WHAM_VERSION" --tool-path "$WHAM_DIR"
fi
# run the tool's dll rather than its launcher, which may be built for another architecture
wham() { dotnet "$(ls "$WHAM_DIR"/.store/wham/*/wham/*/tools/*/any/wham.dll | head -1)" "$@"; }

rm -rf "$OUT"/*
STAGE="$OUT/.stage"
mkdir -p "$STAGE"
cp "$ROOT"/*.gst "$ROOT"/*.cat "$STAGE/"
(cd "$STAGE" && wham publish -a zip -o "$OUT")
rm -rf "$STAGE"

escape() { python3 -c 'import re,sys; print(re.sub(r"[^a-zA-Z0-9_-]+", ".", sys.argv[1]).strip("."))' "$1"; }
for f in "$OUT"/*.catz "$OUT"/*.gstz; do
  mv "$f" "$OUT/$(escape "$(basename "$f")")"
done

LATEST="$(escape "${REPO#*/}.latest")"
(cd "$OUT" && wham publish -a bsi -f "$LATEST" --repo-name "$NAME" \
  --url "https://github.com/$REPO/releases/latest/download/$LATEST.bsi")
ls -1 "$OUT"
