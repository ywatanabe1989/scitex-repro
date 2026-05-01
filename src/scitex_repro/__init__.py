#!/usr/bin/env python3
"""
scitex-repro — Reproducibility utilities for scientific computing.

Provides tools for reproducible scientific computing:
- Random state management (RandomStateManager)
- ID generation (gen_ID)
- Timestamp generation (gen_timestamp)
- Array hashing (hash_array)
"""

from __future__ import annotations

# ID and timestamp utilities
from ._gen_ID import gen_ID, gen_id
from ._gen_timestamp import gen_timestamp, timestamp

# Hash utilities
from ._hash_array import hash_array

# Random state management
from ._RandomStateManager import RandomStateManager, get, reset


# Legacy function for backward compatibility
def fix_seeds(
    seed=42,
    os=True,
    random=True,
    np=True,
    torch=True,
    tf=False,
    jax=False,
    verbose=False,
    **kwargs,
):
    """
    Deprecated: Use RandomStateManager instead.

    This function maintains backward compatibility with the old fix_seeds API.
    """
    import warnings

    warnings.warn(
        "fix_seeds is deprecated. Use scitex_repro.RandomStateManager instead.",
        DeprecationWarning,
        stacklevel=2,
    )
    return RandomStateManager(seed=seed, verbose=verbose)


__all__ = [
    "__version__",
    # ID and timestamp utilities
    "gen_ID",
    "gen_id",
    "gen_timestamp",
    "timestamp",
    # Hash utilities
    "hash_array",
    # Random state management
    "RandomStateManager",
    "get",
    "reset",
    # Legacy (deprecated)
    "fix_seeds",
]

try:
    from importlib.metadata import version as _v, PackageNotFoundError
    try:
        __version__ = _v("scitex-repro")
    except PackageNotFoundError:
        __version__ = "0.0.0+local"
    del _v, PackageNotFoundError
except ImportError:  # pragma: no cover — only on ancient Pythons
    __version__ = "0.0.0+local"