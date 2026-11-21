"""Deterministic, dependency-free bitemporal evidence admission checks.

This module does not infer historical availability from event dates.
All timestamps must be timezone-aware ISO 8601 and all source versions
must be independently archived or otherwise verifiable.
"""
from datetime import datetime
from dataclasses import dataclass
from typing import Optional


def parse_time(value: str) -> datetime:
    if not isinstance(value, str):
        raise ValueError("timestamp must be a string")
    try:
        dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except (ValueError, TypeError) as exc:
        raise ValueError("invalid ISO 8601 timestamp") from exc
    if dt.tzinfo is None or dt.utcoffset() is None:
        raise ValueError("timestamp must include timezone offset")
    return dt


@dataclass(frozen=True)
class EvidenceVersion:
    source_id: str
    version_id: str
    valid_at: str
    first_public_at: Optional[str]
    captured_at: Optional[str]
    content_sha256: str


def admit(evidence: EvidenceVersion, cutoff: str) -> tuple[bool, str]:
    """Conservative point-in-time admission, with explicit failure reason.

    'captured_at' records archival capture, not publication. A later
    capture cannot establish that an earlier version was publicly available.
    A first-public timestamp must be supported by external provenance;
    this function validates chronology only, not authenticity.
    """
    boundary = parse_time(cutoff)
    if not evidence.source_id or not evidence.version_id:
        return False, "missing_source_or_version"
    if len(evidence.content_sha256) != 64 or any(c not in "0123456789abcdef" for c in evidence.content_sha256):
        return False, "invalid_sha256"
    parse_time(evidence.valid_at)
    if evidence.first_public_at is None:
        return False, "unknown_publication_time"
    published = parse_time(evidence.first_public_at)
    if evidence.captured_at is None:
        return False, "missing_capture"
    captured = parse_time(evidence.captured_at)
    if published > captured:
        return False, "publication_after_capture"
    if published > boundary:
        return False, "future_publication"
    if captured > boundary:
        return False, "capture_after_cutoff_unverified_version"
    return True, "admitted"


if __name__ == "__main__":
    import unittest

    HASH = "a" * 64

    class Tests(unittest.TestCase):
        def record(self, **changes):
            data = dict(source_id="s", version_id="v1", valid_at="2020-01-01T00:00:00Z",
                        first_public_at="2021-01-01T00:00:00Z",
                        captured_at="2021-01-02T00:00:00Z", content_sha256=HASH)
            data.update(changes)
            return EvidenceVersion(**data)

        def test_admitted(self):
            self.assertEqual(admit(self.record(), "2022-01-01T00:00:00Z"), (True, "admitted"))

        def test_historical_validity_not_publication(self):
            self.assertEqual(admit(self.record(), "2020-06-01T00:00:00Z")[1], "future_publication")

        def test_future_capture(self):
            self.assertEqual(admit(self.record(captured_at="2023-01-01T00:00:00Z"), "2022-01-01T00:00:00Z")[1], "capture_after_cutoff_unverified_version")

        def test_missing_publication(self):
            self.assertEqual(admit(self.record(first_public_at=None), "2022-01-01T00:00:00Z")[1], "unknown_publication_time")

        def test_naive_cutoff_rejected(self):
            with self.assertRaises(ValueError):
                admit(self.record(), "2022-01-01T00:00:00")

        def test_publication_after_capture(self):
            self.assertEqual(admit(self.record(first_public_at="2021-01-03T00:00:00Z"), "2022-01-01T00:00:00Z")[1], "publication_after_capture")

        def test_invalid_digest(self):
            self.assertEqual(admit(self.record(content_sha256="bad"), "2022-01-01T00:00:00Z")[1], "invalid_sha256")

    unittest.main()
