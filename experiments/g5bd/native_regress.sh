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
printf '%s  %s\n' 0f1c83bab54f4a1089461f7ac721d8c6e46f59f3a984938939a223af5083cd14 "$frozen" | sha256sum -c -
"$gopher" regress add -tv NTSC -frames 30 -mapping F6 -notes 'G5BC positive boot / same-Y' "$frozen"
"$gopher" regress add -tv NTSC -frames 30 -mapping F6 -notes 'G5BD phaseprobe positive boot / same-Y' "$candidate"
"$gopher" regress list
db="$HOME/gopher2600/regression/db"
sha256sum "$db" > "$root/database.sha256"
"$gopher" regress run -concurrent=false -verbose
sha256sum -c "$root/database.sha256"
