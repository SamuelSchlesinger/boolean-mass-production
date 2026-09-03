#!/usr/bin/env python3
"""Static audit for the nondeterminism research corpus.

Validates: ASCII-only Markdown, no unresolved TODO markers, complete reference
definitions for [key][key] citations, and existing local Markdown link targets.

Expected output after the corpus is complete:
  audited <count> Markdown files
  corpus audit passed
"""

from __future__ import annotations

from pathlib import Path
import re


CORPUS = Path(__file__).resolve().parents[1]
REFERENCE_USE = re.compile(r"\[([A-Za-z0-9_.-]+)\]\[\1\]")
REFERENCE_DEFINITION = re.compile(
    r"^\[([A-Za-z0-9_.-]+)\]:\s+(\S+)", re.MULTILINE
)
INLINE_LINK = re.compile(r"\[[^]]+\]\(([^)]+)\)")


def main() -> None:
    failures: list[str] = []
    markdown_files = sorted(CORPUS.rglob("*.md"))
    for path in markdown_files:
        relative = path.relative_to(CORPUS)
        raw = path.read_bytes()
        try:
            text = raw.decode("ascii")
        except UnicodeDecodeError as error:
            failures.append(f"{relative}: non-ASCII byte at offset {error.start}")
            continue

        if "TODO" in text:
            failures.append(f"{relative}: unresolved TODO marker")

        definitions = dict(REFERENCE_DEFINITION.findall(text))
        for key in sorted(set(REFERENCE_USE.findall(text))):
            if key not in definitions:
                failures.append(f"{relative}: missing reference definition [{key}]")

        for target in INLINE_LINK.findall(text):
            clean_target = target.split("#", 1)[0]
            if not clean_target or "://" in clean_target or clean_target.startswith("mailto:"):
                continue
            resolved = (path.parent / clean_target).resolve()
            if not resolved.exists():
                failures.append(f"{relative}: missing local link target {target}")

    if failures:
        raise SystemExit("\n".join(failures))

    print(f"audited {len(markdown_files)} Markdown files")
    print("corpus audit passed")


if __name__ == "__main__":
    main()
