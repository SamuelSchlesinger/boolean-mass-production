#!/usr/bin/env python3
"""Package the verified manuscript as a deterministic, source-only arXiv upload."""

import gzip
import io
from pathlib import Path
import re
import subprocess
import tarfile


def main():
    root = Path(__file__).resolve().parents[1]
    subprocess.run([str(root / "build.sh"), "--check"], cwd=root, check=True)
    guide = (root / "ARXIV_SUBMISSION.md").read_text()
    abstract = re.search(r"Abstract:\n\n```text\n(.*?)\n```", guide, re.S)
    if abstract is None or not abstract.group(1).isascii() or len(abstract.group(1)) > 1920:
        raise ValueError("The submission abstract must be ASCII and at most 1920 characters.")

    source = (root / "main.tex").read_bytes()
    packed = io.BytesIO()
    with gzip.GzipFile(filename="", fileobj=packed, mode="wb", mtime=0) as compressed:
        with tarfile.open(fileobj=compressed, mode="w", format=tarfile.USTAR_FORMAT) as bundle:
            entry = tarfile.TarInfo("main.tex")
            entry.size = len(source)
            entry.mtime = 946684800
            entry.mode = 0o644
            bundle.addfile(entry, io.BytesIO(source))
    payload = packed.getvalue()
    with tarfile.open(fileobj=io.BytesIO(payload), mode="r:gz") as bundle:
        if bundle.getnames() != ["main.tex"] or bundle.extractfile("main.tex").read() != source:
            raise ValueError("The source archive failed its contents check.")
    destination = root / "output" / "exponential-range-mass-production-arxiv.tar.gz"
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(payload)
    print(f"Created {destination} ({len(payload)} bytes; main.tex only).")
    print(f"Submission abstract: {len(abstract.group(1))}/1920 ASCII characters.")


if __name__ == "__main__":
    main()
