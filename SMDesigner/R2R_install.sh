#!/bin/sh
# Explicit, user-local installation. Never invoked automatically by SMDesigner.
set -eu
prefix="${R2R_PREFIX:-$HOME/.local}"
work_dir=$(mktemp -d)
trap 'rm -rf "$work_dir"' EXIT HUP INT TERM
cd "$work_dir"
curl --fail --location --retry 3 --output R2R-1.0.6.tgz https://sourceforge.net/projects/weinberg-r2r/files/R2R-1.0.6.tgz/download
tar -xzf R2R-1.0.6.tgz
cd R2R-1.0.6
./configure --prefix="$prefix"
make
make install
printf 'R2R built and installed in %s/bin. Add it to PATH, then run SMDesigner test to validate.\n' "$prefix"
