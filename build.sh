#!/usr/bin/env bash
set -euo pipefail

usage() {
  printf 'Usage: %s [--check]\n' "${0##*/}" >&2
}

mode="write"
case "${1:-}" in
  "") ;;
  --check) mode="check" ;;
  -h|--help)
    usage
    exit 0
    ;;
  *)
    usage
    exit 2
    ;;
esac

if (( $# > 1 )); then
  usage
  exit 2
fi

paper_dir="$(cd -- "$(dirname -- "$0")" && pwd)"
paper_build_dir="$(mktemp -d "${TMPDIR:-/tmp}/sharing-paper.XXXXXX")"

cleanup() {
  rm -rf -- "$paper_build_dir"
}
trap cleanup EXIT HUP INT TERM

# Keep the checked-in PDF byte-for-byte reproducible across builds.  The fixed
# epoch affects PDF metadata only; the manuscript date remains set in main.tex.
export SOURCE_DATE_EPOCH=946684800
export FORCE_SOURCE_DATE=1
export TZ=UTC
export LC_ALL=C

cd -- "$paper_dir"
trailer_id_code='\pdftrailerid{<\pdfmdfivesum file {main.tex}><\pdfmdfivesum file {main.tex}>}'
latexmk \
  -silent \
  -pdf \
  -interaction=nonstopmode \
  -halt-on-error \
  -usepretex="$trailer_id_code" \
  -outdir="$paper_build_dir" \
  main.tex

warning_pattern='(LaTeX|Package [^ ]+|pdfTeX) Warning|Overfull \\hbox|Underfull \\hbox|undefined references'
if grep -Eq "$warning_pattern" "$paper_build_dir/main.log"; then
  grep -E "$warning_pattern" "$paper_build_dir/main.log" >&2
  printf 'Build completed with warnings; main.pdf was not replaced.\n' >&2
  exit 1
fi

if [[ "$mode" == check ]]; then
  if [[ ! -f "$paper_dir/main.pdf" ]]; then
    printf 'main.pdf is missing; run ./build.sh and stage the result.\n' >&2
    exit 1
  fi

  if ! cmp "$paper_build_dir/main.pdf" "$paper_dir/main.pdf" >/dev/null 2>&1; then
    printf 'main.pdf is stale; run ./build.sh and stage the result.\n' >&2
    exit 1
  fi

  printf 'Verified %s is up to date.\n' "$paper_dir/main.pdf"
  exit 0
fi

cp -- "$paper_build_dir/main.pdf" "$paper_dir/main.pdf"

printf 'Rendered %s\n' "$paper_dir/main.pdf"
