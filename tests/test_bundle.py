import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from SMDesigner import r2r


class BundleTests(unittest.TestCase):
    def test_wsl_uses_linux_platform(self):
        with patch.object(r2r.platform, 'system', return_value='Linux'), patch.object(r2r.platform, 'machine', return_value='x86_64'):
            self.assertEqual(r2r.bundle_platform(), 'linux-x86_64')

    def test_arm_alias(self):
        with patch.object(r2r.platform, 'system', return_value='Linux'), patch.object(r2r.platform, 'machine', return_value='aarch64'):
            self.assertEqual(r2r.bundle_platform(), 'linux-arm64')

    def test_bundle_precedes_path_and_override_precedes_bundle(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder)
            binary=root/'_vendor'/'test-platform'/'r2r'
            binary.parent.mkdir(parents=True)
            binary.write_text('#!/bin/sh\nexit 0\n');binary.chmod(0o755)
            override=root/'custom';override.write_text('#!/bin/sh\nexit 0\n');override.chmod(0o755)
            with patch.object(r2r, '__file__', str(root/'r2r.py')), patch.object(r2r, 'bundle_platform', return_value='test-platform'), patch.object(r2r.shutil,'which',return_value='/bad/system/r2r'), patch.dict(os.environ, {}, clear=True):
                self.assertEqual(r2r.resolve_r2r(),str(binary))
                with patch.dict(os.environ, {'SMDESIGNER_R2R':str(override)}):
                    self.assertEqual(r2r.resolve_r2r(),str(override.resolve()))

    def test_invalid_override_is_not_silently_ignored(self):
        with patch.dict(os.environ, {'SMDESIGNER_R2R':'/nonexistent/smd-r2r'}):
            with self.assertRaisesRegex(RuntimeError,'not executable'):
                r2r.resolve_r2r()
