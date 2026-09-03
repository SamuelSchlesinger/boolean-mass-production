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

note_dir="$(cd -- "$(dirname -- "$0")" && pwd)"
note_build_dir="$(mktemp -d "${TMPDIR:-/tmp}/nondet-note.XXXXXX")"

cleanup() {
  rm -rf -- "$note_build_dir"
}
trap cleanup EXIT HUP INT TERM

export SOURCE_DATE_EPOCH=946684800
export FORCE_SOURCE_DATE=1
export TZ=UTC
export LC_ALL=C

cd -- "$note_dir"
trailer_id_code='\pdftrailerid{<\pdfmdfivesum file {nondet.tex}><\pdfmdfivesum file {nondet.tex}>}'
latexmk \
  -silent \
  -pdf \
  -interaction=nonstopmode \
  -halt-on-error \
  -usepretex="$trailer_id_code" \
  -outdir="$note_build_dir" \
  nondet.tex

warning_pattern='(LaTeX|Package [^ ]+|pdfTeX) Warning|Overfull \\hbox|Underfull \\hbox|undefined references'
if grep -Eq "$warning_pattern" "$note_build_dir/nondet.log"; then
  grep -E "$warning_pattern" "$note_build_dir/nondet.log" >&2
  printf 'Build completed with warnings; nondet.pdf was not replaced.\n' >&2
  exit 1
fi

if [[ "$mode" == check ]]; then
  if [[ ! -f "$note_dir/nondet.pdf" ]]; then
    printf 'nondet.pdf is missing; run ./build-nondet.sh and stage the result.\n' >&2
    exit 1
  fi

  if ! cmp "$note_build_dir/nondet.pdf" "$note_dir/nondet.pdf" >/dev/null 2>&1; then
    printf 'nondet.pdf is stale; run ./build-nondet.sh and stage the result.\n' >&2
    exit 1
  fi

  printf 'Verified %s is up to date.\n' "$note_dir/nondet.pdf"
  exit 0
fi

cp -- "$note_build_dir/nondet.pdf" "$note_dir/nondet.pdf"
printf 'Rendered %s\n' "$note_dir/nondet.pdf"
