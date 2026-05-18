---
description: |
  [TOPIC] Python Api
  [DETAILS] scitex-repro — Python API — see file body for details.
tags: [scitex-repro-python-api]
---

<!-- 02_python-api.md -->

# scitex-repro — Python API

Public symbols in `scitex_repro.__all__`:

| Symbol | Kind | One-liner |
|--------|------|-----------|
| `RandomStateManager` | class | Seeded RNG manager with named generators, verify cache, checkpoints. |
| `get` | function | Return (or lazily create) the module-level `RandomStateManager`. |
| `reset` | function | Rebuild the module-level singleton with a new seed. |
| `gen_ID` | function | Unique ID = formatted timestamp + N random alphanumerics. |
| `gen_id` | function | Lowercase alias of `gen_ID`. |
| `gen_timestamp` | function | Short filename-safe timestamp string. |
| `timestamp` | function | Alias of `gen_timestamp`. |
| `hash_array` | function | Deterministic hex hash of a numpy array. |
| `fix_seeds` | function | **Deprecated.** Back-compat wrapper that returns `RandomStateManager(seed)`. |

## Signatures

```python
class RandomStateManager:
    def __init__(self, seed: int = 42, verbose: bool = False) -> None: ...
    def __call__(self, name: str, verbose: bool | None = None) -> "numpy.random.Generator": ...
    def get_np_generator(self, name: str) -> "numpy.random.Generator": ...
    def get_sklearn_random_state(self, name: str) -> int: ...
    def get_torch_generator(self, name: str) -> "torch.Generator": ...
    def verify(self, obj: Any, name: str | None = None, verbose: bool = True) -> bool: ...
    def checkpoint(self, name: str = "checkpoint") -> dict: ...
    def restore(self, checkpoint: dict) -> None: ...
    def temporary_seed(self, seed: int): ...   # context manager
    def clear_cache(self, patterns: str | list[str] | None = None) -> int: ...

get(verbose: bool = False) -> RandomStateManager
reset(seed: int = 42, verbose: bool = False) -> RandomStateManager

gen_ID(time_format: str = "%YY-%mM-%dD-%Hh%Mm%Ss", N: int = 8) -> str
gen_id(time_format: str = "%YY-%mM-%dD-%Hh%Mm%Ss", N: int = 8) -> str
gen_timestamp() -> str
timestamp() -> str

hash_array(array_data: "numpy.ndarray") -> str

fix_seeds(seed=42, os=True, random=True, np=True, torch=True,
          tf=False, jax=False, verbose=False, **kwargs) -> RandomStateManager  # deprecated
```

`RandomStateManager.verify` stores a hash the first time it sees `name`
and compares on subsequent runs — useful as a smoke test in CI that a
pipeline's random output has not drifted.
