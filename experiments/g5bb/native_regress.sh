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
printf '%s  %s\n' 793cb44d5a763e6f744c2dfacd8440eb39e2cea014127bd22399eec6345c9526 "$frozen" | sha256sum -c -
"$gopher" regress add -tv NTSC -frames 30 -mapping F6 -notes 'G5BA positive boot / close2' "$frozen"
"$gopher" regress add -tv NTSC -frames 30 -mapping F6 -notes 'G5BB positive boot / repaired same-Y' "$candidate"
"$gopher" regress list
db="$HOME/gopher2600/regression/db"
sha256sum "$db" > "$root/database.sha256"
"$gopher" regress run -concurrent=false -verbose
sha256sum -c "$root/database.sha256"
