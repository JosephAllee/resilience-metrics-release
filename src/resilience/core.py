from __future__ import annotations

from typing import Any, Dict, Iterable

import numpy as np


def _safe_percentile(x: np.ndarray, q: float) -> float:
    return float(np.nanpercentile(x, q)) if x.size else float("nan")


def analyze(csv_path: str, cfg: Dict[str, Any] | None = None, *, columns: Iterable[str] | None = None) -> Dict[str, Any]:
    """Simple CSV analysis for resilience metrics (EN)."""
    data = np.genfromtxt(csv_path, delimiter=",", names=True, dtype=None, encoding=None)
    if data.size == 0:
        return {"columns": [], "summary": {}}
    if data.dtype.names is None:
        raise ValueError("CSV must have headers")

    cols: list[str] = []
    summary: Dict[str, Any] = {}
    desired = set(columns) if columns is not None else None

    for name in data.dtype.names:
        if desired is not None and name not in desired:
            continue
        # Try converting to float; skip non-numeric columns
        try:
            x = np.array(data[name], dtype=float)
        except (ValueError, TypeError):
            continue
        cols.append(name)
        m = float(np.nanmean(x))
        s = float(np.nanstd(x))
        lo, hi = m - 2.0 * s, m + 2.0 * s
        outside = np.logical_or(x < lo, x > hi)
        refusal = float(np.nanmean(outside.astype(float))) if x.size else 0.0
        dx = np.diff(x)
        track_err = float(np.nanmean(np.abs(dx))) if dx.size else 0.0
        vitality = float(s / (abs(m) + 1e-6))
        summary[name] = {
            "count": int(np.sum(np.isfinite(x))),
            "mean": m,
            "std": s,
            "min": float(np.nanmin(x)),
            "max": float(np.nanmax(x)),
            "p05": _safe_percentile(x, 5),
            "p95": _safe_percentile(x, 95),
            "band": [lo, hi],
            "refusal_index": refusal,
            "tracking_error": track_err,
            "vitality": vitality,
        }
    # If no numeric columns survived selection, fail loud and clear
    if not cols:
        if desired is not None:
            raise ValueError("No numeric columns matched --columns filter")
        raise ValueError("No numeric columns found in CSV (use --columns to specify)")

    return {"columns": cols, "summary": summary}
