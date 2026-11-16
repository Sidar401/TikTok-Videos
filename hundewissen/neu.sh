#!/usr/bin/env bash
# Neues HundeWissenTv-Video im Magazin-Stil: hundewissen/neu.sh <name>
set -euo pipefail
cd "$(dirname "$0")/.."
n="${1:?name}"; d="videos/$n"
[ -e "$d" ] && { echo "existiert: $d"; exit 1; }
bash scripts/new-video.sh "$n" >/dev/null; rm -f "$d/CLAUDE.md"
mkdir -p "$d/assets/aussie" "$d/assets/fonts"
cp brand/aussie/*.png "$d/assets/aussie/"
cp videos/hw-mag-farben/assets/fonts/* "$d/assets/fonts/"
cp hundewissen/magazin/magazin.css hundewissen/magazin/magazin.js hundewissen/rig/rig.js "$d/assets/"
echo "$d"
