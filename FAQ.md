# FAQ — Resilience-Metrics

- What does the CLI output?
  - JSON analysis with summary stats per numeric column (count, mean, std, min, max, p05, p95, band, refusal_index, tracking_error, vitality).
- Quickstart?
  - `docker run --rm -v "$PWD/examples":/data eliotsystem/resilience-metrics:latest analyze --csv /data/synth.csv --out /data/analysis.json`
- Visual proofs?
  - Generate `examples/summary.svg` (no deps) and `examples/summary.png` (Matplotlib) from analysis.json.
- Support/SLA?
  - As‑is/no‑support (see EULA). Community issues only, best‑effort.
- Licensing?
  - Annual commercial “as‑is”. See EULA.md.

