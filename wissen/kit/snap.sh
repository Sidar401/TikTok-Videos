#!/usr/bin/env bash
# Standbilder: wissen/kit/snap.sh <name> <zeiten,komma,getrennt>
cd "$(dirname "$0")/../../videos/$1" && npx hyperframes lint 2>&1 | grep -E " error" | head -3; npx hyperframes snapshot --at "$2" 2>&1 | grep contact
