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
printf '%s  %s\n' 479ba85f24c3d31345cf378baf1ca225229849a520add18e6524a2099888b2f7 "$frozen" | sha256sum -c -
"$gopher" regress add -tv NTSC -frames 30 -mapping F6 -notes 'G5BD ITER2 shadow frozen positive boot' "$frozen"
"$gopher" regress add -tv NTSC -frames 30 -mapping F6 -notes 'G5BD ITER3 sharefour positive boot' "$candidate"
"$gopher" regress list
db="$HOME/gopher2600/regression/db"
sha256sum "$db" > "$root/database.sha256"
"$gopher" regress run -concurrent=false -verbose
sha256sum -c "$root/database.sha256"
