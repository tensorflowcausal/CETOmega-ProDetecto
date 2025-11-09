# === CETΩ Verification Pipeline ===
# Targets:
#   make frg             -> evolve kernel (FRG)
#   make bench           -> run bench (Hankel-PSD/causality) if available
#   make ringdown        -> model comparison CET vs GR vs GR+echoes
#   make ringdown_per_event -> same with per-event CET shifts + bootstrap
#   make all             -> FRG -> bench -> ringdown -> report

PYTHON ?= python

# Paths
KERNEL_IN  ?= kernels/kernel_example.json
KERNEL_OUT ?= kernels/kernel_evolved.json
FRG        ?= CETOmega_FRGsolver.py
BENCH      ?= CETOmega_bench_v1.py
RINGDOWN   ?= CETOmega_RingdownStats.py
DATA       ?= ringdown.csv
PER_EVENT  ?= cet_shifts_by_event.csv
REPORT     ?= reports/ringdown_report.json
REPORT_BOOT?= reports/ringdown_report_boot.json

# FRG params
STEPS ?= 500
DELL  ?= 0.01
ALPHA ?= 1.0
SIGMA ?= 1.0
C0    ?= 0.0
TAU   ?= 0.0

frg:
	$(PYTHON) $(FRG) --in $(KERNEL_IN) --out $(KERNEL_OUT) --steps $(STEPS) --dell $(DELL) --alpha $(ALPHA) --sigma $(SIGMA) --c0 $(C0) --tau $(TAU) --keep-norm --export-F --wmin 0.0 --wmax 10.0 --wpts 512

bench:
	@if [ -f "$(BENCH)" ]; then \
	  echo "[bench] Running bench on $(KERNEL_OUT)"; \
	  $(PYTHON) $(BENCH) --json $(KERNEL_OUT) --out reports/bench_out/; \
	else \
	  echo "[bench] Skipped (CETOmega_bench_v1.py not found)."; \
	fi

ringdown:
	$(PYTHON) $(RINGDOWN) --data $(DATA) --cet-json $(KERNEL_OUT) --out $(REPORT)

ringdown_per_event:
	$(PYTHON) $(RINGDOWN) --data $(DATA) --cet-delta-csv $(PER_EVENT) --boots 1000 --seed 123 --out $(REPORT_BOOT)

report:
	@echo "=== CETΩ Ringdown Decision (see README_ringdown.md for criteria) ==="
	@cat $(REPORT) 2>/dev/null || true
	@cat $(REPORT_BOOT) 2>/dev/null || true

all: frg bench ringdown report

.PHONY: frg bench ringdown ringdown_per_event report all

# Quantum Zeno targets
ZENO_DATA ?= quantum/zeno.csv
ZENO_OUT  ?= reports/zeno_report.json
ZENO_OUTB ?= reports/zeno_report_boot.json
ZENO      ?= CETOmega_QuantumZenoStats.py

quantum:
	$(PYTHON) $(ZENO) --data $(ZENO_DATA) --cet-json $(KERNEL_OUT) --out $(ZENO_OUT)

quantum_boot:
	$(PYTHON) $(ZENO) --data $(ZENO_DATA) --cet-json $(KERNEL_OUT) --boots 1000 --seed 42 --out $(ZENO_OUTB)
