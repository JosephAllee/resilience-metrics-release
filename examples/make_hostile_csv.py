#!/usr/bin/env python3
"""
Generate a stress-test CSV with noise, gaps (NaNs), and outliers.

Usage:
  python examples/make_hostile_csv.py --out examples/hostile.csv --rows 2000
"""
import argparse
import csv
import numpy as np


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', default='examples/hostile.csv')
    ap.add_argument('--rows', type=int, default=2000)
    ap.add_argument('--seed', type=int, default=0)
    args = ap.parse_args()

    rng = np.random.default_rng(args.seed)
    t = np.arange(args.rows)
    x = 0.7 + 0.2*np.sin(2*np.pi*t/200) + 0.02*rng.standard_normal(args.rows)

    # Inject gaps (NaNs)
    missing_idx = rng.choice(args.rows, size=int(0.02*args.rows), replace=False)
    x[missing_idx] = np.nan

    # Inject outliers
    out_idx = rng.choice(args.rows, size=int(0.01*args.rows), replace=False)
    x[out_idx] += rng.choice([+3.0, -3.0], size=len(out_idx))

    with open(args.out, 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['value'])
        for v in x:
            w.writerow(['' if np.isnan(v) else float(v)])
    print(f"Wrote {args.out} with {args.rows} rows (with NaNs/outliers)")


if __name__ == '__main__':
    main()

