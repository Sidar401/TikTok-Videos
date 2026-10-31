#!/usr/bin/env bash
# Lädt die Higgsfield-Clips eines Produkts in alle seine Videos: scripts/hole_clips.sh shop/<produkt>
# (Braucht Zugriff auf Higgsfield; sonst in der Higgsfield-Sandbox ausführen.)
set -euo pipefail
cd "$(dirname "$0")/.."
p="${1:?Usage: scripts/hole_clips.sh shop/<produkt>}"
mkdir -p "$p/clips"
grep -v '^#' "$p/clips.txt" | while read -r n url _; do
  [ -s "$p/clips/$n.mp4" ] || curl -sf -o "$p/clips/$n.mp4" "$url"
done
for cfg in "$p"/*.json; do
  name=$(python3 -c "import json,sys;print(json.load(open(sys.argv[1]))['name'])" "$cfg")
  mkdir -p "videos/$name/assets/clips" && cp "$p"/clips/*.mp4 "videos/$name/assets/clips/"
done
echo "Clips geladen: $p"
