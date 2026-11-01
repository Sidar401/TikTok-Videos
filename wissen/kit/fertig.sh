#!/usr/bin/env bash
# Ton mischen + prüfen + rendern: wissen/kit/fertig.sh <name>
set -uo pipefail
cd "$(dirname "$0")/../../videos/$1"
python3 -I ../../wissen/kit/mix.py cues.json assets/sfx.wav 30
npx hyperframes lint 2>&1 | grep -E " error" | head -3
npx hyperframes render --quality delivery --output "../../renders/$1.mp4" 2>&1 | grep -E "MB|rror"
