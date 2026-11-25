"""Test the restricted CI test entry point."""

import io
import runpy
import shutil
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stderr
from pathlib import Path
from unittest.mock import patch

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
                stderr = io.StringIO()
                with patch.object(sys, "argv", [str(RUNTESTS), argument]), patch(
                    "nose2.discover"
                ) as discover, redirect_stderr(stderr):
                    with self.assertRaises(SystemExit) as error:
                        runpy.run_path(str(RUNTESTS), run_name="__main__")
                self.assertEqual(error.exception.code, 2)
                self.assertIn("unsupported", stderr.getvalue().lower())
                discover.assert_not_called()
        result = subprocess.run(
            [str(RUNTESTS), "--plugin=other"], cwd=ROOT, capture_output=True, text=True
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

    def test_rejects_missing_test_method(self):
        result = subprocess.run(
            [str(RUNTESTS), "tests.test_exceptions.TestJsonSchema.test_missing"],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("unsupported", result.stderr.lower())

    def test_returns_failure_from_an_executed_test(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            shutil.copy2(RUNTESTS, root / "runtests")
            (root / "tests").mkdir()
            (root / "tests" / "__init__.py").touch()
            (root / "tests" / "test_failure.py").write_text(
                "import unittest\n"
                "class TestFailure(unittest.TestCase):\n"
                "    def test_failure(self):\n"
                '        self.fail("intentional failure")\n'
            )
            result = subprocess.run(
                [str(root / "runtests"), "tests.test_failure.TestFailure.test_failure"],
                cwd=root,
                capture_output=True,
                text=True,
            )
        self.assertEqual(result.returncode, 1)
        self.assertIn("intentional failure", result.stderr)

    def test_rejects_test_method_on_non_test_class(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            shutil.copy2(RUNTESTS, root / "runtests")
            (root / "tests").mkdir()
            (root / "tests" / "__init__.py").touch()
            (root / "tests" / "test_example.py").write_text(
                "class Helper:\n"
                "    @staticmethod\n"
                "    def test_action():\n"
                '        print("unexpected execution")\n'
                "class helper:\n"
                "    @staticmethod\n"
                "    def test_action():\n"
                '        print("unexpected execution")\n'
            )
            for name in ("Helper", "helper"):
                with self.subTest(name=name):
                    result = subprocess.run(
                        [
                            str(root / "runtests"),
                            f"tests.test_example.{name}.test_action",
                        ],
                        cwd=root,
                        capture_output=True,
                        text=True,
                    )
                    self.assertEqual(result.returncode, 2)
                    self.assertIn("unsupported", result.stderr.lower())
                    self.assertNotIn("unexpected execution", result.stdout)

    def test_rejects_callable_in_place_of_test_module(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            shutil.copy2(RUNTESTS, root / "runtests")
            (root / "tests").mkdir()
            (root / "tests" / "__init__.py").write_text(
                'def test_action(): print("unexpected execution")\n'
            )
            result = subprocess.run(
                [str(root / "runtests"), "tests.test_action"],
                cwd=root,
                capture_output=True,
                text=True,
            )
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertNotIn("unexpected execution", result.stdout)
