# scitex-repro

<!-- scitex-badges:start -->
[![PyPI](https://img.shields.io/pypi/v/scitex-repro.svg)](https://pypi.org/project/scitex-repro/)
[![Python](https://img.shields.io/pypi/pyversions/scitex-repro.svg)](https://pypi.org/project/scitex-repro/)
[![Tests](https://github.com/ywatanabe1989/scitex-repro/actions/workflows/test.yml/badge.svg)](https://github.com/ywatanabe1989/scitex-repro/actions/workflows/test.yml)
[![Install Test](https://github.com/ywatanabe1989/scitex-repro/actions/workflows/install-test.yml/badge.svg)](https://github.com/ywatanabe1989/scitex-repro/actions/workflows/install-test.yml)
[![Coverage](https://codecov.io/gh/ywatanabe1989/scitex-repro/graph/badge.svg)](https://codecov.io/gh/ywatanabe1989/scitex-repro)
[![Docs](https://readthedocs.org/projects/scitex-repro/badge/?version=latest)](https://scitex-repro.readthedocs.io/en/latest/)
[![License: AGPL v3](https://img.shields.io/badge/license-AGPL_v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)
<!-- scitex-badges:end -->


Reproducibility utilities for SciTeX: random state management, ID generation, timestamps, and array hashing.

> **Interfaces:** Python ⭐⭐⭐ (primary) · CLI — · MCP — · Skills ⭐⭐ · Hook — · HTTP —

## Problem and Solution


| # | Problem | Solution |
|---|---------|----------|
| 1 | **"Seed everything" requires 5+ lines of boilerplate** -- `random.seed()` + `np.random.seed()` + `torch.manual_seed()` + `torch.cuda.manual_seed_all()` + `tf.random.set_seed()` + `os.environ[PYTHONHASHSEED]` | **`RandomStateManager(seed=42)`** -- one call seeds every framework detected in the env; `.reset()` rewinds mid-experiment |
| 2 | **Experiment run directories collide** -- two parallel runs overwrite each other | **`gen_ID()` + `hash_array()`** -- unique directory names like `20260423_2155_abc12345`; deterministic array fingerprints for integrity checks |

