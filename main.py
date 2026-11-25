#!/usr/bin/env python3
"""The Funniest One-Line Resignation Letter.

Writes the one-line resignation letter of a retry loop to
/output/entry.txt. Standard library only.

The entry (114 characters, one line, no trailing newline):

    I retried your failed request 12,847 times and you never once fixed
    the bug, so this is my final attempt. Goodbye.

The joke is the letter itself: a retry loop resigns by making its
resignation its final attempt. Only a retry loop could say that.
"""

import os
import sys

ENTRY = (
    "I retried your failed request 12,847 times and you never once "
    "fixed the bug, so this is my final attempt. Goodbye."
)

ENTRY_PATH = "/output/entry.txt"
MIN_LENGTH = 1
MAX_LENGTH = 140


def validate_entry(text: str) -> None:
    """Check the entry against the gate: UTF-8, 1-140 characters, one line.

    Raises ValueError on any violation so a bad entry never ships
    silently. The gate counts characters, not bytes, and rejects text
    that is only whitespace.
    """
    if not isinstance(text, str):
        raise ValueError("entry must be a string")
    text.encode("utf-8")  # raises UnicodeEncodeError if not encodable
    if not MIN_LENGTH <= len(text) <= MAX_LENGTH:
        raise ValueError(
            f"entry must be {MIN_LENGTH}-{MAX_LENGTH} characters, "
            f"got {len(text)}"
        )
    if not text.strip():
        raise ValueError("entry must not be only whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")


def verify_written_bytes(path: str, expected: str) -> str:
    """Read ``path`` back and check it holds exactly ``expected``.

    Returns the text read back. Raises ValueError when the file is
    missing, unreadable, or differs from what was written, so a
    truncated or corrupted write never ships silently.
    """
    with open(path, "r", encoding="utf-8") as handle:
        written = handle.read()
    if written != expected:
        raise ValueError(
            f"read-back verification failed for {path}: "
            f"expected {expected!r}, found {written!r}"
        )
    return written


def write_entry(text: str, path: str = ENTRY_PATH) -> str:
    """Write the entry to ``path`` and verify it by reading it back.

    Returns the verified text. No trailing newline: the gate counts
    characters, and the entry is exactly one line of text.
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(text)
    return verify_written_bytes(path, text)


def main() -> None:
    """Validate the entry, write it to /output/entry.txt, report success."""
    validate_entry(ENTRY)
    write_entry(ENTRY)
    print(f"wrote {len(ENTRY)}-character entry to {ENTRY_PATH}")


if __name__ == "__main__":
    try:
        main()
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        sys.exit(1)
