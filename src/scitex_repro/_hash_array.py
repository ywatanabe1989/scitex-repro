#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Extracted from scitex-python/src/scitex/repro/_hash_array.py
from __future__ import annotations

import hashlib

import numpy as np


def hash_array(array_data: np.ndarray) -> str:
    """Generate hash for array data.

    Creates a deterministic hash for numpy arrays, useful for
    verifying data integrity and reproducibility.

    Parameters
    ----------
    array_data : np.ndarray
        Array to hash

    Returns
    -------
    str
        16-character hash string

    Examples
    --------
    >>> import numpy as np
    >>> data = np.array([1, 2, 3, 4, 5])
    >>> hash1 = hash_array(data)
    >>> hash2 = hash_array(data)
    >>> hash1 == hash2
    True
    """
    data_bytes = array_data.tobytes()
    return hashlib.sha256(data_bytes).hexdigest()[:16]
