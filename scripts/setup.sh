#!/usr/bin/env bash
# Installiert HyperFrames-CLI, GSAP und Chrome Headless Shell fürs Rendern.
set -euo pipefail
cd "$(dirname "$0")/.."
npm install --no-audit --no-fund
npx hyperframes browser ensure
