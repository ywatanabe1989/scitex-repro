---
description: |
  [TOPIC] Installation
  [DETAILS] pip install scitex-repro. Pure-Python; numpy required, torch/tensorflow auto-detected and seeded only when present.
tags: [scitex-repro-installation]
---

# Installation

## Standard

```bash
pip install scitex-repro
```

Required: `numpy`. Optional (auto-detected at seed time):
`torch`, `tensorflow` — seeded only if importable.

## Verify

```bash
python -c "import scitex_repro; print(scitex_repro.__version__)"
python -c "from scitex_repro import RandomStateManager, gen_ID, hash_array; print('ok')"
```

## Editable install (development)

```bash
git clone https://github.com/ywatanabe1989/scitex-repro
cd scitex-repro
pip install -e .
```

## Used by

Pulled in by `scitex` umbrella; also usable standalone for any experiment
needing seed-everything semantics or deterministic run IDs.
