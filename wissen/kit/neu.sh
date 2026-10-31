#!/usr/bin/env bash
# Neues Wissens-Video: wissen/kit/neu.sh <name>  -> videos/<name>/ mit kit.js/kit.css
set -euo pipefail
cd "$(dirname "$0")/../.."
n="${1:?name}"; d="videos/$n"
[ -e "$d" ] && { echo "existiert: $d"; exit 1; }
cp -r vorlage "$d"; rm -rf "$d/.hyperframes" "$d/assets/beagle.png" "$d/assets/fonts" "$d/CLAUDE.md"
sed -i "s/\"name\": *\"[^\"]*\"/\"name\": \"$n\"/" "$d/package.json"; sed -i "s/\"_vorlage\"/\"$n\"/g" "$d/meta.json"
cp wissen/kit/kit.js wissen/kit/kit.css "$d/assets/"
echo "$d"
