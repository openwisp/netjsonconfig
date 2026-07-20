import unittest
from io import BytesIO

from netjsonconfig.backends.base.backend import BaseBackend
from netjsonconfig.backends.base.parser import BaseParser
from netjsonconfig.backends.base.renderer import BaseRenderer
from netjsonconfig.exceptions import ValidationError
from netjsonconfig.schema import schema


class BaseBackendWithSchema(BaseBackend):
    schema = schema


class TestBase(unittest.TestCase):
    """
    tests for netjsonconfig.backends.base
    """

    def test_generate(self):
        b = BaseBackend({})
        with self.assertRaises(NotImplementedError):
            b.generate()

    def test_cleanup(self):
        b = BaseBackend({})
        r = BaseRenderer(b)
        self.assertEqual(r.cleanup(""), "")

    def test_parse_text_not_implemented(self):
        with self.assertRaises(NotImplementedError):
            BaseParser("")

    def test_parse_tar_not_implemented(self):
        with self.assertRaises(NotImplementedError):
            BaseParser(BytesIO())

    def test_base_backend_parse_not_implemented(self):
        with self.assertRaises(NotImplementedError):
            BaseBackend(native="")

    def test_validate_file_paths(self):
        b = BaseBackendWithSchema(
            {
                "files": [
                    {"path": "/etc/config/network", "mode": "0644", "contents": ""},
                    {"path": "etc/openvpn/client.conf", "mode": "0644", "contents": ""},
                    {"path": "{{cert_path_abc123}}", "mode": "0644", "contents": ""},
                    {
                        "path": "/etc/{{cert_path_abc123}}",
                        "mode": "0644",
                        "contents": "",
                    },
                ]
            }
        )
        b.validate()

    def test_validate_file_paths_rejects_invalid_paths(self):
        invalid_paths = [
            "tmp/x; reboot",
            "../../../etc/passwd",
            "tmp/a b",
            "tmp/file\n",
            "tmp/$(reboot)",
            "//etc/passwd",
            "///etc/passwd",
            "tmp//file",
            "tmp/./file",
            "tmp/{file}",
            "tmp/{{file}",
            "tmp/file}}",
        ]
        for path in invalid_paths:
            with self.subTest(path=path):
                b = BaseBackendWithSchema(
                    {"files": [{"path": path, "mode": "0644", "contents": ""}]}
                )
                with self.assertRaises(ValidationError) as context:
                    b.validate()
                self.assertIn("Invalid file path", context.exception.message)
