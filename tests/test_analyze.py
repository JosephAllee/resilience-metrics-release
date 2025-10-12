from __future__ import annotations

import csv
import sys
import tempfile
import unittest
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

import numpy as np

TESTS_DIR = Path(__file__).resolve().parent
SRC_PATH = TESTS_DIR.parent / "src" / "resilience"

CORE_SPEC = spec_from_file_location("resilience.core", SRC_PATH / "core.py")
if CORE_SPEC is None or CORE_SPEC.loader is None:
    raise ImportError("Impossible de charger resilience.core depuis le squelette local")
core_module = module_from_spec(CORE_SPEC)
sys.modules[CORE_SPEC.name] = core_module
CORE_SPEC.loader.exec_module(core_module)

analyze = core_module.analyze


class TestResilienceAnalyze(unittest.TestCase):
    def _write_csv(self, rows: list[tuple[float, str]]) -> Path:
        fd, path_str = tempfile.mkstemp(suffix=".csv")
        Path(path_str).unlink(missing_ok=True)  # we will rewrite via csv module
        path = Path(path_str)
        with path.open("w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["value", "label"])
            for val, label in rows:
                writer.writerow([val, label])
        return path

    def test_analyze_numeric_column(self) -> None:
        rows = [(float(v), "ok") for v in np.linspace(0.0, 1.0, num=10)]
        path = self._write_csv(rows)
        try:
            res = analyze(str(path))
        finally:
            path.unlink(missing_ok=True)

        self.assertIn("columns", res)
        self.assertIn("summary", res)
        self.assertIn("value", res["columns"])
        self.assertNotIn("label", res["columns"])

        summary = res["summary"].get("value")
        self.assertIsNotNone(summary)

        expected_keys = {
            "count",
            "mean",
            "std",
            "min",
            "max",
            "p05",
            "p95",
            "band",
            "refusal_index",
            "tracking_error",
            "vitality",
        }
        self.assertTrue(expected_keys.issubset(summary.keys()))

        numeric_keys = expected_keys - {"band"}
        for key in numeric_keys:
            self.assertIsInstance(summary[key], (int, float))

        band = summary["band"]
        self.assertIsInstance(band, list)
        self.assertEqual(len(band), 2)
        self.assertTrue(all(isinstance(v, (int, float)) for v in band))


if __name__ == "__main__":
    unittest.main()
