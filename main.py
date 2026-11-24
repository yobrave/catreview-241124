#!/usr/bin/env python3
"""Produce the cat's one-star review for the make.fun judge.

entry.txt holds the review the cat wants on record. This builder reads
that file, keeps only its first non-empty line, checks the review fits
the 1..200 character window the gate allows, then copies it where the
grader expects it. Any failure lands as JSON on stdout, never silent.
"""
import json
import os
import sys

BOUNTY_SLUG = "u-motasimfuad-make-the-ai-judge-laugh-cat-reviews-its-42a34990"
CHAR_LIMIT = 200


def source_line():
    folder = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(folder, "entry.txt"), encoding="utf-8") as fh:
        raw = fh.read()
    for row in raw.replace("\r\n", "\n").split("\n"):
        row = row.strip()
        if row:
            return row
    return ""


def deliver(line):
    target = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(target, exist_ok=True)
    with open(os.path.join(target, "entry.txt"), "w",
              encoding="utf-8", newline="\n") as fh:
        fh.write(line + "\n")


def announce(state, **facts):
    facts["state"] = state
    facts["slug"] = BOUNTY_SLUG
    print(json.dumps(facts))
    return 0 if state == "delivered" else 2


def guard():
    try:
        review = source_line()
    except OSError:
        return announce("no_file", hint="entry.txt must sit beside main.py")
    span = len(review)
    if span < 1 or span > CHAR_LIMIT:
        return announce("out_of_range", chars=span, allowed=CHAR_LIMIT)
    deliver(review)
    return announce("delivered", chars=span)


if __name__ == "__main__":
    sys.exit(guard())
