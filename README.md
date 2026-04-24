# scitex-repro

Reproducibility utilities for SciTeX: random state management, ID generation, timestamps, and array hashing.

> **Interfaces:** Python ⭐⭐⭐ (primary) · CLI — · MCP — · Skills ⭐⭐ · Hook — · HTTP —

## Problem and Solution


| # | Problem | Solution |
|---|---------|----------|
| 1 | **"Seed everything" requires 5+ lines of boilerplate** -- `random.seed()` + `np.random.seed()` + `torch.manual_seed()` + `torch.cuda.manual_seed_all()` + `tf.random.set_seed()` + `os.environ[PYTHONHASHSEED]` | **`RandomStateManager(seed=42)`** -- one call seeds every framework detected in the env; `.reset()` rewinds mid-experiment |
| 2 | **Experiment run directories collide** -- two parallel runs overwrite each other | **`gen_ID()` + `hash_array()`** -- unique directory names like `20260423_2155_abc12345`; deterministic array fingerprints for integrity checks |

