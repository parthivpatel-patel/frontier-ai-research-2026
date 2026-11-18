#!/usr/bin/env python3
"""Check a freeze attestation against immutable Git object content.

This checks Git object identity and manifest bytes, NOT trustworthy freeze time.
Run in a cloud CI checkout with full Git history (fetch-depth: 0).
Usage: python research/tools/check_git_freeze_provenance.py ATTESTATION
"""
import hashlib
import json
import pathlib
import re
import subprocess
import sys


def git(*args):
    return subprocess.run(["git", *args], check=True, stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE).stdout


def check(attestation_path):
    errors = []
    try:
        att = json.loads(pathlib.Path(attestation_path).read_text(encoding="utf-8"))
        if not isinstance(att, dict):
            return ["attestation must be a JSON object"]
        commit = att.get("git_commit", "")
        path = att.get("manifest_path", "")
        digest = att.get("sha256", "")
        if not isinstance(commit, str) or not re.fullmatch(r"[0-9a-f]{40}", commit):
            return ["git_commit must be a full lowercase SHA-1 commit ID"]
        if not isinstance(path, str) or not path or path.startswith("/") or ".." in pathlib.PurePosixPath(path).parts:
            return ["manifest_path must be a safe repository-relative path"]
        if not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest):
            return ["sha256 must be a lowercase SHA-256 digest"]
        resolved = git("rev-parse", "--verify", commit + "^{commit}").decode().strip()
        if resolved != commit:
            errors.append("git_commit does not resolve to the specified commit")
        historical = git("show", commit + ":" + path)
        if hashlib.sha256(historical).hexdigest() != digest:
            errors.append("manifest in attested commit does not match attested digest")
        current = pathlib.Path(path).read_bytes()
        if current != historical:
            errors.append("working-tree manifest differs from attested Git object")
    except (OSError, ValueError, subprocess.CalledProcessError, UnicodeDecodeError) as exc:
        errors.append("provenance verification failed: " + str(exc))
    return errors


def main(argv):
    if len(argv) != 2:
        print(__doc__.strip())
        return 2
    errors = check(argv[1])
    for error in errors:
        print("FAIL:", error)
    if errors:
        return 1
    print("PASS: Git object and byte identity only; freeze timing is NOT independently proven")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
