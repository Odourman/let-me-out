#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
python3 tools/build.py
python3 tools/verify_preflight.py
sha256sum dist/LetMeOut_Diagnostic_NTSC_F6_v018.bin
