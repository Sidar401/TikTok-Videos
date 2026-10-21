#!/usr/bin/env bash
# Neues Video im Kanal-Stil anlegen: kopiert vorlage/ nach videos/<name>/.
set -euo pipefail
cd "$(dirname "$0")/.."
name="${1:?Usage: scripts/new-video.sh <name>}"
dir="videos/$name"
[ -e "$dir" ] && { echo "Existiert schon: $dir"; exit 1; }
mkdir -p videos
cp -r vorlage "$dir"
rm -rf "$dir/.hyperframes"
sed -i "s/\"name\": *\"[^\"]*\"/\"name\": \"$name\"/" "$dir/package.json"
echo "Fertig: $dir"
