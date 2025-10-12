#!/usr/bin/env python3
"""
Generate a PNG (summary.png) from examples/analysis.json using Matplotlib.

Usage:
  pip install matplotlib
  python examples/quick_png.py
"""
from __future__ import annotations

import json
from pathlib import Path
import matplotlib
matplotlib.use("Agg")  # non-interactive backend
import matplotlib.pyplot as plt


def load_values(path: Path) -> dict:
    data = json.loads(path.read_text())
    cols = data.get("columns", [])
    if not cols:
        raise SystemExit("analysis.json contains no columns")
    col = cols[0]
    s = data.get("summary", {}).get(col, {})
    return {
        "mean": float(s.get("mean", 0.0)),
        "std": float(s.get("std", 0.0)),
        "refusal_index": float(s.get("refusal_index", 0.0)),
        "tracking_error": float(s.get("tracking_error", 0.0)),
        "vitality": float(s.get("vitality", 0.0)),
    }


def main() -> None:
    root = Path(__file__).resolve().parent
    analysis = root / "analysis.json"
    if not analysis.exists():
        raise SystemExit(f"File not found: {analysis}. Generate it first with resiliencectl.")
    vals = load_values(analysis)
    keys = ["mean", "std", "refusal_index", "tracking_error", "vitality"]
    series = [vals[k] for k in keys]

    fig, ax = plt.subplots(figsize=(6, 3.2), dpi=150)
    bars = ax.bar(keys, series, color=["#4e79a7", "#f28e2b", "#e15759", "#76b7b2", "#59a14f"]) 
    ax.set_title("Resilience-Metrics — Summary", fontsize=12)
    ax.set_ylabel("Value (relative scale)")
    ax.grid(axis="y", linestyle=":", alpha=0.4)
    for b, v in zip(bars, series):
        ax.text(b.get_x() + b.get_width()/2, b.get_height(), f"{v:.3f}", ha="center", va="bottom", fontsize=9)
    fig.tight_layout()
    out = root / "summary.png"
    fig.savefig(out)
    print(f"OK: PNG written to {out}")


if __name__ == "__main__":
    main()
