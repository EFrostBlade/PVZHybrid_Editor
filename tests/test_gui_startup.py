"""Real Tk lifecycle smoke test; pure startup tests also run on Linux."""
import json
import os
from pathlib import Path
import subprocess
import sys
import unittest


@unittest.skipUnless(os.name == "nt", "Windows runtime dependencies required")
class GuiStartupTests(unittest.TestCase):
    def test_full_ui_responds_while_update_waits_and_survives_prompt_close(self):
        root = Path(__file__).resolve().parents[1]
        result = subprocess.run(
            [sys.executable, "-B", str(root / "tests/gui_startup_probe.py")],
            cwd=root, capture_output=True, encoding="utf-8", errors="replace", timeout=60,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        line = next(line for line in result.stdout.splitlines() if line.startswith("STARTUP_RESULT "))
        metrics = json.loads(line.removeprefix("STARTUP_RESULT "))
        self.assertEqual(metrics["tabs_visited"], 9)
        self.assertGreaterEqual(metrics["comboboxes"], 100)


if __name__ == "__main__":
    unittest.main()
