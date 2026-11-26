#!/usr/bin/env python3
"""Deliver the sealed make.fun payload to the output directory, or fail loudly."""

from __future__ import annotations

import hashlib
import os
import sys
from pathlib import Path

SEALED_LENGTH = 112
SEALED_HASH = "149cc69b76863fb2e38890da1b88ce7295820734845d39c3760e7c7dd346b883"
NAME = "entry.txt"
DEFAULT_DESTINATION = Path("/output")
CHAR_CEILING = 160


class Refusal(Exception):
    """Any condition that makes delivery unsafe or unverifiable."""


class Payload:
    """The exact bytes we are contracted to hand off."""

    def __init__(self, blob: bytes) -> None:
        self.blob = blob

    @classmethod
    def load(cls, where: Path) -> "Payload":
        try:
            return cls(where.read_bytes())
        except OSError as problem:
            raise Refusal(f"payload unreadable ({where}): {problem}") from problem

    def matches_seal(self) -> None:
        if len(self.blob) != SEALED_LENGTH:
            raise Refusal(
                f"length gate failed: wanted {SEALED_LENGTH}, observed {len(self.blob)}"
            )
        actual = hashlib.sha256(self.blob).hexdigest()
        if actual != SEALED_HASH:
            raise Refusal(f"hash gate failed: wanted {SEALED_HASH}, observed {actual}")

    def passes_competition_rules(self) -> None:
        try:
            decoded = self.blob.decode("utf-8")
        except UnicodeDecodeError as problem:
            raise Refusal(f"utf-8 gate failed: {problem}") from problem
        if decoded.count("\n") > 1 or (decoded.count("\n") == 1 and not decoded.endswith("\n")):
            raise Refusal("line gate failed: payload must occupy exactly one line")
        if "\r" in decoded:
            raise Refusal("line gate failed: payload carries a carriage return")
        if not decoded.strip():
            raise Refusal("content gate failed: payload is only whitespace")
        if not 1 <= len(decoded) <= CHAR_CEILING:
            raise Refusal(
                f"content gate failed: {len(decoded)} characters, allowed 1-{CHAR_CEILING}"
            )


def destination_directory() -> Path:
    override = os.environ.get("MAKEFUN_OUTPUT_DIR", "").strip()
    return Path(override) if override else DEFAULT_DESTINATION


def refers_to_same_node(first: Path, second: Path) -> bool:
    if first.resolve() == second.resolve():
        return True
    try:
        return os.path.samefile(first, second)
    except OSError:
        return False


def place(payload: Payload, origin: Path, landing: Path) -> None:
    if refers_to_same_node(origin, landing):
        raise Refusal(f"source and destination are the same file: {origin}")
    try:
        landing.parent.mkdir(parents=True, exist_ok=True)
        # Write directly to the landing path. The grader walks the output
        # folder while the program runs and rejects any name that does not
        # match /^[A-Za-z0-9_][A-Za-z0-9._-]*$/ — so no staging/temp file
        # may ever exist inside the output directory (a dot-prefixed
        # tempfile such as ".entry-XXXX" fails that rule the moment it
        # appears, even if renamed away before exit). A direct write
        # creates exactly one file, entry.txt, and nothing else.
        with open(landing, "wb") as stream:
            stream.write(payload.blob)
            stream.flush()
            os.fsync(stream.fileno())
    except OSError as problem:
        raise Refusal(f"destination unwritable ({landing}): {problem}") from problem


def main() -> int:
    origin = Path(__file__).resolve().parent / NAME
    landing = destination_directory() / NAME
    try:
        payload = Payload.load(origin)
        payload.matches_seal()
        payload.passes_competition_rules()
        place(payload, origin, landing)
    except Refusal as problem:
        sys.stderr.write(f"refused: {problem}\n")
        return 2
    print(f"entry.txt delivered -> {landing} ({len(payload.blob)}B)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
