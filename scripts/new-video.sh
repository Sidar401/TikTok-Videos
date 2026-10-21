#!/usr/bin/env bash
# Neues Hochformat-Video (1080x1920) unter videos/<name> anlegen.
# GSAP wird lokal kopiert, weil CDNs in der Cloud-Umgebung gesperrt sind.
set -euo pipefail
cd "$(dirname "$0")/.."
name="${1:?Usage: scripts/new-video.sh <name>}"
dir="videos/$name"
HYPERFRAMES_SKIP_SKILLS=1 npx hyperframes init "$dir" --resolution portrait --non-interactive
cp node_modules/gsap/dist/gsap.min.js "$dir/"
sed -i 's#https://cdn.jsdelivr.net/npm/gsap@[0-9.]*/dist/gsap.min.js#gsap.min.js#' "$dir/index.html"
echo "Fertig: $dir"
