#!/usr/bin/env bash
# Lädt die Higgsfield-Bilder (ki1–ki5) nach assets/ und baut den unscharfen CTA-Hintergrund.
# Diese Sitzung darf Higgsfield nicht erreichen → läuft in der Higgsfield-Sandbox.
set -euo pipefail
cd "$(dirname "$0")/assets"
B=https://d8j0ntlcm91z4.cloudfront.net/user_3EaPlydsH5kGn6HYj95n2mOllAM
for p in "1 174353_4a25a7e5-d8f2-46b7-9221-4fece6188538" "2 174353_efaa7e82-8f57-42b6-a67d-1942cab5ec45" \
         "3 174354_beed223d-0591-49f5-97c7-664983fcf551" "4 174354_276b9d89-5fa0-47c1-9768-963dacaef67c" \
         "5 174353_2eddecc0-5834-4cb3-b5d2-5c9617be35a5"; do
  set -- $p; curl -sf -o "ki$1.png" "$B/hf_20261029_$2.png"
done
convert ki3.png -resize 540x960 -blur 0x18 -resize 1080x1920 ki3-bg.jpg
