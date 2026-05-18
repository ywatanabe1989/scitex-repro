#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Time-stamp: "2024-11-07 17:44:32 (ywatanabe)"
# Extracted from scitex-python/src/scitex/repro/_gen_timestamp.py

from datetime import datetime as _datetime


def gen_timestamp(*, now_fn=None):
    """Generate a timestamp string for file naming.

    Returns a timestamp in the format YYYY-MMDD-HHMM, suitable for
    creating unique filenames or version identifiers.

    Parameters
    ----------
    now_fn : callable, optional
        Zero-argument callable returning a `datetime`-like object with
        `.strftime()`. Defaults to `datetime.now`. Injection point for
        deterministic tests — pass a fake that returns a fixed datetime
        instead of mocking `datetime` globally.

    Returns
    -------
    str
        Timestamp string in format "YYYY-MMDD-HHMM"

    Examples
    --------
    >>> timestamp = gen_timestamp()
    >>> print(timestamp)
    '2025-0531-1230'

    >>> filename = f"experiment_{gen_timestamp()}.csv"
    >>> print(filename)
    'experiment_2025-0531-1230.csv'
    """
    if now_fn is None:
        now_fn = _datetime.now
    return now_fn().strftime("%Y-%m%d-%H%M")


timestamp = gen_timestamp
