#!/usr/bin/env bash
# Let Me Out! v0.18 diagnostic tools bootstrap, tested target Ubuntu 24.04 LTS.
set -euo pipefail
if ! command -v apt-get >/dev/null 2>&1; then
  echo 'ERROR: requires apt-get on Ubuntu/Debian Linux.' >&2; exit 2
fi
sudo apt-get update
sudo apt-get install -y dasm stella xvfb
printf '\nInstalled package versions:\n'
dpkg-query -W -f='${binary:Package}\t${Version}\n' dasm stella xvfb
command -v dasm
command -v stella
