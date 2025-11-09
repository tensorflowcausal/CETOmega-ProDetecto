#!/usr/bin/env bash
set -euo pipefail

PYTHON=${PYTHON:-python}
FRG=${FRG:-CETOmega_FRGsolver.py}
BENCH=${BENCH:-CETOmega_bench_v1.py}
RINGDOWN=${RINGDOWN:-CETOmega_RingdownStats.py}

KERNEL_IN=${KERNEL_IN:-kernels/kernel_example.json}
KERNEL_OUT=${KERNEL_OUT:-kernels/kernel_evolved.json}

DATA=${DATA:-ringdown.csv}
PER_EVENT=${PER_EVENT:-cet_shifts_by_event.csv}

echo "[1/4] FRG evolve -> ${KERNEL_OUT}"
$PYTHON "$FRG" --in "$KERNEL_IN" --out "$KERNEL_OUT" \
  --steps 500 --dell 0.01 --alpha 1.0 --sigma 1.0 --c0 0.0 --tau 0.0 \
  --keep-norm --export-F --wmin 0.0 --wmax 10.0 --wpts 512

echo "[2/4] Bench (if available)"
if [ -f "$BENCH" ]; then
  mkdir -p reports/bench_out
  $PYTHON "$BENCH" --json "$KERNEL_OUT" --out reports/bench_out/
else
  echo "[bench] Skipped (CETOmega_bench_v1.py not found)"
fi

echo "[3/4] Ringdown stats (CET vs GR vs GR+echoes)"
mkdir -p reports
$PYTHON "$RINGDOWN" --data "$DATA" --cet-json "$KERNEL_OUT" --out reports/ringdown_report.json

echo "[4/4] Ringdown stats per-event (with bootstrap)"
$PYTHON "$RINGDOWN" --data "$DATA" --cet-delta-csv "$PER_EVENT" --boots 1000 --seed 123 --out reports/ringdown_report_boot.json

echo "Done. See 'reports/'"
