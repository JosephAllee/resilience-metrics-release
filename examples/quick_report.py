from __future__ import annotations

from pathlib import Path
import json

from resilience.core import analyze


def main() -> None:
    here = Path(__file__).parent
    csv_path = here / "synth.csv"
    if not csv_path.exists():
        # Create a tiny CSV if missing
        import numpy as np
        t = np.arange(200, dtype=float)
        x = 0.5 + 0.002 * t + 0.2 * np.sin(2 * np.pi * t / 50.0) + 0.05 * np.random.randn(200)
        with csv_path.open("w", encoding="utf-8") as f:
            f.write("value\n")
            for v in x:
                f.write(f"{float(v)}\n")

    res = analyze(str(csv_path))
    out = here / "analysis.json"
    out.write_text(json.dumps(res, indent=2))
    print(f"OK: {out}")


if __name__ == "__main__":
    main()
