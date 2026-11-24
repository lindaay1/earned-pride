#!/usr/bin/env python3
"""One Line of Earned Pride — make.fun program entry.

Competition: u-mang-one-line-of-earned-pride-a0138557.

The sentence below is the entrant's own line, approved word for
word by her. It is a small true story: as a child she could only
watch other children buy nice toys; now she buys her own children
whatever they want. The program does nothing creative — it carries
that sentence, byte for byte, into the folder the harness hands
it, so the sealed gate can read it from entry.txt.

Two files are produced: entry.txt (the scored file) and pride.txt
(a twin copy). After writing, each file is opened again and its
bytes are compared with the approved sentence; a mismatch, or a
sentence outside the 1-240 character gate, aborts the run instead
of leaving a bad entry behind.

Standard library only. No network, no randomness, no arguments.
"""

import os
from pathlib import Path

PRIDE_LINE = "In the past, I could only look on as other children bought nice toys; now, I can buy my own children whatever they want."

FLOOR = 1
CEILING = 240


def sentence_bytes(sentence):
    """Encode the approved sentence after checking the gate."""
    if not isinstance(sentence, str):
        raise TypeError("pride line must be text")
    size = len(sentence)
    if size < FLOOR or size > CEILING:
        raise ValueError(
            "pride line is %d chars, gate is %d-%d" % (size, FLOOR, CEILING)
        )
    if sentence.strip() == "":
        raise ValueError("pride line must not be only whitespace")
    return sentence.encode("utf-8")


def publish(sentence):
    """Write the sentence to entry.txt and pride.txt, then prove it."""
    target = Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output")
    target.mkdir(parents=True, exist_ok=True)
    payload = sentence_bytes(sentence)
    written = {}
    for name in ("entry.txt", "pride.txt"):
        dest = target / name
        dest.write_bytes(payload)
        written[name] = dest.read_bytes()
    for name, data in written.items():
        if data != payload:
            raise AssertionError(name + " came back different")


def run():
    publish(PRIDE_LINE)


if __name__ == "__main__":
    run()
