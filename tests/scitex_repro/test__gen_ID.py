#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Time-stamp: "2026-05-18"
# File: tests/scitex_repro/test__gen_ID.py

"""Tests for unique ID generation functionality.

All tests follow the SciTeX no-mocks + AAA + single-assert testing
discipline (see scitex general skills 02_package_12_no-mocks.md and
02_package_13_test-quality.md). Deterministic-timestamp tests inject a
hand-rolled `now_fn` fake rather than patching `datetime` globally.
"""

import re
import string
import time
from datetime import datetime

import pytest

from scitex_repro import gen_id


# ----- helpers ---------------------------------------------------------------

def _fixed_now(year=2025, month=6, day=2, hour=15, minute=30, second=45):
    """Return a zero-arg callable yielding the fixed datetime.

    Honest fake — exposes only `.strftime(fmt)` because that is the
    only method `gen_id` calls on `now_fn()`. No mock magic.
    """
    fixed = datetime(year, month, day, hour, minute, second)
    return lambda: fixed


# ----- basic format ----------------------------------------------------------

def test_gen_id_default_output_contains_underscore_separator():
    # Arrange
    # (no inputs — default call)
    # Act
    id_str = gen_id()
    # Assert
    assert "_" in id_str


def test_gen_id_default_output_splits_into_two_parts():
    # Arrange
    # (no inputs — default call)
    # Act
    parts = gen_id().split("_")
    # Assert
    assert len(parts) == 2


def test_gen_id_default_random_part_has_length_eight():
    # Arrange
    # (no inputs — default call)
    # Act
    random_part = gen_id().split("_")[1]
    # Assert
    assert len(random_part) == 8


def test_gen_id_default_random_part_is_alphanumeric():
    # Arrange
    # (no inputs — default call)
    # Act
    random_part = gen_id().split("_")[1]
    # Assert
    assert random_part.isalnum()


# ----- default time format ---------------------------------------------------

def test_gen_id_default_timestamp_matches_yymmdd_hms_pattern():
    # Arrange
    pattern = r"\d{4}Y-\d{2}M-\d{2}D-\d{2}h\d{2}m\d{2}s"
    # Act
    timestamp_part = gen_id().split("_")[0]
    # Assert
    assert re.match(pattern, timestamp_part)


# ----- custom time format ----------------------------------------------------

def test_gen_id_with_short_format_returns_eight_digit_timestamp_length():
    # Arrange
    fmt = "%Y%m%d"
    # Act
    timestamp_part = gen_id(time_format=fmt).split("_")[0]
    # Assert
    assert len(timestamp_part) == 8


def test_gen_id_with_short_format_returns_only_digits_in_timestamp():
    # Arrange
    fmt = "%Y%m%d"
    # Act
    timestamp_part = gen_id(time_format=fmt).split("_")[0]
    # Assert
    assert timestamp_part.isdigit()


def test_gen_id_with_dashed_format_matches_iso_prefix_pattern():
    # Arrange
    fmt = "%Y-%m-%d_%H:%M"
    pattern = r"\d{4}-\d{2}-\d{2}"
    # Act
    timestamp_part = gen_id(time_format=fmt).split("_")[0]
    # Assert
    assert re.match(pattern, timestamp_part)


# ----- custom random length --------------------------------------------------

@pytest.mark.parametrize("n", [1, 4, 16, 32])
def test_gen_id_random_part_length_matches_requested_n(n):
    # Arrange
    requested = n
    # Act
    random_part = gen_id(N=requested).split("_")[1]
    # Assert
    assert len(random_part) == requested


@pytest.mark.parametrize("n", [1, 4, 16, 32])
def test_gen_id_random_part_is_alphanumeric_for_various_n(n):
    # Arrange
    requested = n
    # Act
    random_part = gen_id(N=requested).split("_")[1]
    # Assert
    assert random_part.isalnum()


# ----- zero random length ----------------------------------------------------

def test_gen_id_with_zero_n_ends_with_underscore():
    # Arrange
    # (no inputs)
    # Act
    id_str = gen_id(N=0)
    # Assert
    assert id_str.endswith("_")


def test_gen_id_with_zero_n_splits_into_two_parts_with_empty_random():
    # Arrange
    # (no inputs)
    # Act
    parts = gen_id(N=0).split("_")
    # Assert
    assert parts[1] == ""


# ----- uniqueness ------------------------------------------------------------

def test_gen_id_generates_unique_ids_across_one_hundred_calls():
    # Arrange
    n_samples = 100
    # Act
    ids = [gen_id() for _ in range(n_samples)]
    # Assert
    assert len(set(ids)) == n_samples


# ----- random character composition -----------------------------------------

def test_gen_id_random_part_uses_only_ascii_letters_and_digits():
    # Arrange
    valid_chars = set(string.ascii_letters + string.digits)
    sample = gen_id(N=200)
    # Act
    random_chars = set(sample.split("_")[1])
    # Assert
    assert random_chars.issubset(valid_chars)


# ----- deterministic timestamp via injected now_fn (no mocks) ---------------

def test_gen_id_uses_injected_now_fn_for_default_format():
    # Arrange
    now_fn = _fixed_now(2025, 6, 2, 15, 30, 45)
    # Act
    timestamp_part = gen_id(now_fn=now_fn).split("_")[0]
    # Assert
    assert timestamp_part == "2025Y-06M-02D-15h30m45s"


def test_gen_id_uses_injected_now_fn_for_custom_short_format():
    # Arrange
    now_fn = _fixed_now(2025, 6, 2, 15, 30, 45)
    # Act
    timestamp_part = gen_id(time_format="%Y%m%d_%H%M%S", now_fn=now_fn).split("_")[0]
    # Assert
    assert timestamp_part == "20250602"


# ----- backward-compatibility alias ------------------------------------------

def test_gen_id_legacy_alias_is_same_function_object():
    # Arrange
    from scitex_repro import gen_ID
    # Act
    is_alias = gen_ID is gen_id
    # Assert
    assert is_alias


def test_gen_id_legacy_alias_produces_underscore_separated_output():
    # Arrange
    from scitex_repro import gen_ID
    # Act
    id_str = gen_ID()
    # Assert
    assert "_" in id_str


def test_gen_id_legacy_alias_produces_default_eight_char_random_part():
    # Arrange
    from scitex_repro import gen_ID
    # Act
    random_part = gen_ID().split("_")[1]
    # Assert
    assert len(random_part) == 8


# ----- rapid generation precision -------------------------------------------

def test_gen_id_rapid_calls_produce_unique_ids_via_random_suffix():
    # Arrange
    n_samples = 10
    # Act
    ids = []
    for _ in range(n_samples):
        ids.append(gen_id(time_format="%Y%m%d_%H%M%S"))
        time.sleep(0.005)
    # Assert
    assert len(set(ids)) == n_samples


def test_gen_id_rapid_calls_keep_default_eight_char_random_suffix():
    # Arrange
    n_samples = 10
    # Act
    ids = [gen_id(time_format="%Y%m%d_%H%M%S") for _ in range(n_samples)]
    suffix_lengths = {len(i.split("_")[-1]) for i in ids}
    # Assert
    assert suffix_lengths == {8}


# ----- empty / special time formats -----------------------------------------

def test_gen_id_with_empty_time_format_has_empty_timestamp_part():
    # Arrange
    fmt = ""
    # Act
    parts = gen_id(time_format=fmt).split("_")
    # Assert
    assert parts[0] == ""


def test_gen_id_with_empty_time_format_preserves_random_part_length():
    # Arrange
    fmt = ""
    # Act
    parts = gen_id(time_format=fmt).split("_")
    # Assert
    assert len(parts[1]) == 8


def test_gen_id_special_time_format_preserves_prefix_literal_chars():
    # Arrange
    fmt = "exp-%Y-%m-%d"
    # Act
    timestamp_part = gen_id(time_format=fmt).split("_")[0]
    # Assert
    assert timestamp_part.startswith("exp-")


def test_gen_id_special_time_format_matches_combined_prefix_pattern():
    # Arrange
    fmt = "exp-%Y-%m-%d"
    pattern = r"exp-\d{4}-\d{2}-\d{2}"
    # Act
    timestamp_part = gen_id(time_format=fmt).split("_")[0]
    # Assert
    assert re.match(pattern, timestamp_part)


# ----- large random length --------------------------------------------------

def test_gen_id_with_large_n_returns_correct_random_part_length():
    # Arrange
    n_chars = 1000
    # Act
    random_part = gen_id(N=n_chars).split("_")[1]
    # Assert
    assert len(random_part) == n_chars


def test_gen_id_with_large_n_random_part_is_alphanumeric():
    # Arrange
    n_chars = 1000
    # Act
    random_part = gen_id(N=n_chars).split("_")[1]
    # Assert
    assert random_part.isalnum()


if __name__ == "__main__":
    import os
    pytest.main([os.path.abspath(__file__)])
