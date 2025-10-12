#!/usr/bin/env python3
"""
Generate a minimal SVG (summary.svg) from examples/analysis.json.
Uses only the Python standard library (no external deps).

Usage:
  python examples/quick_svg.py
"""
from __future__ import annotations

import json
from pathlib import Path


def load_metrics(path: Path) -> dict:
    data = json.loads(path.read_text())
    # Assume at least one column; take the first
    cols = data.get("columns", [])
    if not cols:
        raise SystemExit("analysis.json contains no columns")
    col = cols[0]
    summary = data.get("summary", {}).get(col, {})
    return {
        "mean": float(summary.get("mean", 0.0)),
        "std": float(summary.get("std", 0.0)),
        "refusal_index": float(summary.get("refusal_index", 0.0)),
        "tracking_error": float(summary.get("tracking_error", 0.0)),
        "vitality": float(summary.get("vitality", 0.0)),
    }


def render_svg(values: dict, out_path: Path) -> None:
    # Simple bar scaling
    keys = ["mean", "std", "refusal_index", "tracking_error", "vitality"]
    series = [values.get(k, 0.0) for k in keys]
    vmax = max(series) if series else 1.0
    if vmax <= 0:
        vmax = 1.0

    width, height = 640, 300
    margin_left, margin_right = 80, 20
    margin_top, margin_bottom = 30, 40
    chart_w = width - margin_left - margin_right
    chart_h = height - margin_top - margin_bottom

    bar_w = chart_w / (len(keys) * 1.5)
    gap = bar_w / 2

    def yscale(v: float) -> float:
        return chart_h * (v / vmax)

    def esc(txt: str) -> str:
        return (txt
                .replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;"))

    # Simple palette
    colors = {
        "mean": "#4e79a7",
        "std": "#f28e2b",
        "refusal_index": "#e15759",
        "tracking_error": "#76b7b2",
        "vitality": "#59a14f",
    }

    # Build the SVG
    parts = []
    parts.append(f"<svg xmlns='http://www.w3.org/2000/svg' width='{width}' height='{height}' viewBox='0 0 {width} {height}'>")
    parts.append(f"<rect width='{width}' height='{height}' fill='white'/>")
    # Axes
    x0 = margin_left
    y0 = height - margin_bottom
    parts.append(f"<line x1='{x0}' y1='{y0}' x2='{x0 + chart_w}' y2='{y0}' stroke='#333' stroke-width='1'/>")
    parts.append(f"<line x1='{x0}' y1='{y0}' x2='{x0}' y2='{margin_top}' stroke='#333' stroke-width='1'/>")
    # Graduation max
    parts.append(f"<text x='{x0 - 8}' y='{margin_top + 4}' text-anchor='end' font-size='12' fill='#333'>{vmax:.2f}</text>")
    parts.append(f"<text x='{x0 - 8}' y='{y0}' text-anchor='end' font-size='12' fill='#333'>0</text>")

    # Title
    parts.append("<text x='50%' y='18' text-anchor='middle' font-size='14' font-weight='bold' fill='#222'>Resilience-Metrics — Summary</text>")

    # Bars
    x = x0 + gap
    for k, v in zip(keys, series):
        h = yscale(v)
        y = y0 - h
        parts.append(f"<rect x='{x:.1f}' y='{y:.1f}' width='{bar_w:.1f}' height='{h:.1f}' fill='{colors[k]}'/>")
        # Value above bar
        parts.append(f"<text x='{x + bar_w/2:.1f}' y='{y - 4:.1f}' text-anchor='middle' font-size='11' fill='#222'>{v:.3f}</text>")
        # Label below (rotate if long)
        label = esc(k)
        parts.append(f"<text x='{x + bar_w/2:.1f}' y='{y0 + 14:.1f}' text-anchor='middle' font-size='12' fill='#333'>{label}</text>")
        x += bar_w + gap

    parts.append("</svg>")
    out_path.write_text("\n".join(parts))


def main() -> None:
    root = Path(__file__).resolve().parent
    analysis = root / "analysis.json"
    if not analysis.exists():
        raise SystemExit(f"File not found: {analysis}. Generate it first with resiliencectl.")
    vals = load_metrics(analysis)
    out = root / "summary.svg"
    render_svg(vals, out)
    print(f"OK: SVG written to {out}")


if __name__ == "__main__":
    main()
