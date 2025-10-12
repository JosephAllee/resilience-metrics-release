from __future__ import annotations

from pathlib import Path

import numpy as np


def make_synth(T: int = 200, drift: float = 0.002, noise: float = 0.05) -> np.ndarray:
    t = np.arange(T, dtype=float)
    x = 0.5 + drift * t + 0.2 * np.sin(2 * np.pi * t / 50.0) + noise * np.random.randn(T)
    return x.astype(np.float32)


if __name__ == "__main__":
    out = Path(__file__).with_name("synth.csv")
    series = make_synth()
    with out.open("w", encoding="utf-8") as f:
        f.write("value\n")
        for v in series:
            f.write(f"{float(v)}\n")
    print(f"Wrote {out} with {len(series)} rows")
