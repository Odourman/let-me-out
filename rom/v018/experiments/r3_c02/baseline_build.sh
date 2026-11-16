#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../../../" && pwd)"  # repository /rom? override below
cd "$(dirname "$0")/../.."
# source location: rom/v018, only historical comparison, no canonical changes.
python3 tools/build.py
bash tools/build_with_dasm.sh
mkdir -p experiments/r3_c02/dist
cp dist/dasm/rebuilt-v018-F6.bin experiments/r3_c02/dist/historical_v018_F6.bin
sha256sum experiments/r3_c02/dist/historical_v018_F6.bin
