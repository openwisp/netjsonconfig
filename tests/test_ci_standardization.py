"""Test the restricted CI test entry point."""

import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RUNTESTS = ROOT / "runtests"


class TestCiStandardization(unittest.TestCase):
    def test_rejects_unsupported_arguments(self):
        for argument in (
            "--plugin=other",
            "--config=other.cfg",
            "os.system",
            "tests.test_exceptions.TestJsonSchema.setUpClass",
            "tests.test_exceptions.Draft4Validator",
            "tests.test_exceptions;id",
        ):
            with self.subTest(argument=argument):
                result = subprocess.run(
                    [str(RUNTESTS), argument], cwd=ROOT, capture_output=True, text=True
                )
                self.assertEqual(result.returncode, 2)
                self.assertIn("unsupported", result.stderr.lower())

    def test_runs_a_selected_test_with_safe_flags(self):
        result = subprocess.run(
            [
                str(RUNTESTS),
                "-v",
                "tests.test_exceptions.TestJsonSchema.test_spam_object",
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Ran 1 test", result.stderr)

    def test_returns_failure_from_runner(self):
        result = subprocess.run(
            [str(RUNTESTS), "tests.test_exceptions.TestJsonSchema.test_missing"],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("test_missing", result.stderr)
