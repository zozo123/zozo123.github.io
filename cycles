#!/bin/sh
set -eu

repo="zozo123/wasted-cycles"
version="${WASTED_CYCLES_VERSION:-latest}"

# mktemp -d, not a predictable "$TMPDIR/wasted-cycles-$$": on a shared machine
# another user can pre-create or symlink a guessable path and swap the binary
# between extraction and execution.
if ! tmp_root="$(mktemp -d "${TMPDIR:-/tmp}/wasted-cycles.XXXXXXXX")"; then
  echo "wasted-cycles: could not create a temporary directory" >&2
  exit 1
fi
trap 'rm -rf "$tmp_root"' EXIT INT TERM

os="$(uname -s | tr '[:upper:]' '[:lower:]')"
arch="$(uname -m)"

case "$os" in
  darwin|linux) ;;
  *)
    echo "wasted-cycles: this runner supports macOS and Linux; see GitHub Releases for Windows" >&2
    exit 1
    ;;
esac

case "$arch" in
  x86_64|amd64) arch="x86_64" ;;
  arm64|aarch64) arch="arm64" ;;
  *)
    echo "wasted-cycles: unsupported architecture: $arch" >&2
    exit 1
    ;;
esac

if [ "$version" = "latest" ]; then
  # GitHub's unversioned release redirect can remain cached on the previous
  # release after the API already reports a new latest tag. A per-run query
  # keeps `curl | sh` from silently downloading yesterday's binary.
  base="https://github.com/$repo/releases/latest/download"
  cache_bust="?released=$(date +%s)"
else
  base="https://github.com/$repo/releases/download/$version"
  cache_bust=""
fi

asset="wasted-cycles_${os}_${arch}.tar.gz"

# --show-error so a failed download says why instead of exiting silently.
download() {
  if ! curl --fail --silent --show-error --location "$1" -o "$2"; then
    echo "wasted-cycles: could not download $1" >&2
    echo "wasted-cycles: see https://github.com/$repo/releases for available builds" >&2
    exit 1
  fi
}

download "$base/$asset$cache_bust" "$tmp_root/$asset"
download "$base/checksums.txt$cache_bust" "$tmp_root/checksums.txt"

# Tolerate the '*' binary-mode marker some sha256sum implementations emit.
expected="$(awk -v file="$asset" '{ sub(/^\*/, "", $2) } $2 == file { print $1 }' "$tmp_root/checksums.txt")"
if [ -z "$expected" ]; then
  echo "wasted-cycles: release checksum is missing for $asset" >&2
  exit 1
fi

if command -v shasum >/dev/null 2>&1; then
  actual="$(shasum -a 256 "$tmp_root/$asset" | awk '{print $1}')"
elif command -v sha256sum >/dev/null 2>&1; then
  actual="$(sha256sum "$tmp_root/$asset" | awk '{print $1}')"
else
  echo "wasted-cycles: sha256 tool not found" >&2
  exit 1
fi

if [ "$actual" != "$expected" ]; then
  echo "wasted-cycles: checksum verification failed" >&2
  exit 1
fi

tar -xzf "$tmp_root/$asset" -C "$tmp_root"
"$tmp_root/wasted-cycles" "$@"
