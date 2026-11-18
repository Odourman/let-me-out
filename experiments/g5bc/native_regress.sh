#!/usr/bin/env bash
set -euo pipefail
frozen=$(realpath "$1")
candidate=$(realpath "$2")
root=$(realpath -m "$3")
test ! -e "$root"
mkdir -p "$root"/{home,cwd}
export HOME="$root/home" XDG_CONFIG_HOME="$root/home"
cd "$root/cwd"
gopher=/workspace/.g5ar-env01/bin/gopher2600
printf '%s  %s\n' 7c77fcba29b460547f35c4667d637f1f0ff14e94be3b93290d1d4a8b85cacccd "$frozen" | sha256sum -c -
"$gopher" regress add -tv NTSC -frames 30 -mapping F6 -notes 'G5BB positive boot / same-Y' "$frozen"
"$gopher" regress add -tv NTSC -frames 30 -mapping F6 -notes 'G5BC positive boot / generalized same-Y' "$candidate"
"$gopher" regress list
db="$HOME/gopher2600/regression/db"
sha256sum "$db" > "$root/database.sha256"
"$gopher" regress run -concurrent=false -verbose
sha256sum -c "$root/database.sha256"
