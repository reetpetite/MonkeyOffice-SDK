from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location(
    "validate_evidence", ROOT / "tools" / "validate_evidence.py"
)
assert SPEC is not None and SPEC.loader is not None
validate_evidence = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validate_evidence)


class EvidenceValidationTests(unittest.TestCase):
    def test_canonical_level_registry_is_valid(self) -> None:
        registry = validate_evidence.load_json(validate_evidence.LEVELS_PATH)
        self.assertEqual(validate_evidence.validate_level_registry(registry), [])

    def test_missing_evidence_file_is_reported(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "registry.json"
            path.write_text(
                json.dumps(
                    {
                        "items": [
                            {
                                "status": "verified",
                                "evidence": ["evidence/does-not-exist.md"],
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )
            errors, checked = validate_evidence.validate_registry_links(
                path, "items", set(validate_evidence.EXPECTED_ORDER)
            )
        self.assertEqual(checked, 1)
        self.assertTrue(any("Datei fehlt" in error for error in errors))

    def test_unknown_evidence_level_is_reported(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "registry.json"
            path.write_text(
                json.dumps(
                    {
                        "items": [
                            {
                                "status": "implementation",
                                "evidence": ["evidence/README.md"],
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )
            errors, checked = validate_evidence.validate_registry_links(
                path, "items", set(validate_evidence.EXPECTED_ORDER)
            )
        self.assertEqual(checked, 1)
        self.assertTrue(any("unbekannte Evidenzstufe" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
