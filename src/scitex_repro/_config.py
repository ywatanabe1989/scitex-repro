#!/usr/bin/env python3
"""Local config helper replacing scitex.config.get_paths dependency.

Uses SCITEX_DIR env var or defaults to ~/.scitex/.
"""
from __future__ import annotations

import os
from pathlib import Path


class _Paths:
    """Minimal path manager for scitex-repro."""

    def __init__(self, base_dir: str | None = None):
        if base_dir is not None:
            self._base_dir = Path(base_dir)
        else:
            self._base_dir = Path(
                os.environ.get("SCITEX_DIR", Path.home() / ".scitex")
            )

    @property
    def rng(self) -> Path:
        """Random number generator state directory."""
        return self._base_dir / "rng"


_default_paths: _Paths | None = None


def get_paths(base_dir: str | None = None) -> _Paths:
    """Get path manager instance.

    Parameters
    ----------
    base_dir : str, optional
        Explicit base directory.  If None, returns cached default instance
        using ``SCITEX_DIR`` env-var or ``~/.scitex/``.
    """
    global _default_paths

    if base_dir is not None:
        return _Paths(base_dir)

    if _default_paths is None:
        _default_paths = _Paths()

    return _default_paths
