#!/usr/bin/env python3
"""Read-only inventory of research regression fixtures; standard library only.

This script does not execute tests or download models. It fails closed when
the three previously cloud-validated fixtures are missing.
"""
from pathlib import Path
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[2]
FIXTURES = ROOT / "research" / "fixtures"
REQUIRED = {
    "test_protocol_146_identifiability_witness.py",
    "test_protocol_149_source_cluster_certificate.py",
    "test_protocol_150_adversarial_source_selection.py",
}

def main() -> int:
    if not FIXTURES.is_dir():
        print("ERROR: fixture directory absent", file=sys.stderr)
        return 2
    paths = sorted(FIXTURES.glob("test_*.py"))
    names = {p.name for p in paths}
    missing = sorted(REQUIRED - names)
    manifest = {
        "schema_version": 1,
        "inventory_only": True,
        "total_discovered_test_files": len(paths),
        "files": [
            {"path": p.relative_to(ROOT).as_posix(),
             "protocol": (re.search(r"protocol_(\d+)", p.name).group(1)
                          if re.search(r"protocol_(\d+)", p.name) else None)}
            for p in paths
        ],
        "previously_validated_subset": sorted(REQUIRED),
        "missing_required_files": missing,
        "full_suite_executed": False,
    }
    print(json.dumps(manifest, indent=2))
    if missing:
        print("ERROR: previously validated fixtures missing", file=sys.stderr)
        return 1
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
