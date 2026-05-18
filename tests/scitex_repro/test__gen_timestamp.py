#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Time-stamp: "2026-05-18"
# File: tests/scitex_repro/test__gen_timestamp.py

"""Tests for timestamp generation functionality.

All tests follow the SciTeX no-mocks + AAA + single-assert testing
discipline (see scitex general skills 02_package_12_no-mocks.md and
02_package_13_test-quality.md). Deterministic-timestamp tests inject a
hand-rolled `now_fn` fake rather than patching `datetime` globally.
"""

import re
import time
from datetime import datetime

import pytest

from scitex_repro import gen_timestamp, timestamp


# ----- helpers ---------------------------------------------------------------

def _fixed_now(year, month, day, hour, minute, second=30):
    fixed = datetime(year, month, day, hour, minute, second)
    return lambda: fixed


_PATTERN = r"\d{4}-\d{4}-\d{4}"


# ----- basic format ----------------------------------------------------------

def test_gen_timestamp_returns_a_string_instance():
    # Arrange
    # (no inputs)
    # Act
    result = gen_timestamp()
    # Assert
    assert isinstance(result, str)


def test_gen_timestamp_matches_dashed_four_four_four_pattern():
    # Arrange
    pattern = _PATTERN
    # Act
    result = gen_timestamp()
    # Assert
    assert re.match(pattern, result)


def test_gen_timestamp_has_exact_length_of_fourteen_characters():
    # Arrange
    # (no inputs)
    # Act
    result = gen_timestamp()
    # Assert
    assert len(result) == 14


# ----- format-detail decomposition ------------------------------------------

def test_gen_timestamp_splits_into_three_dash_separated_parts():
    # Arrange
    # (no inputs)
    # Act
    parts = gen_timestamp().split("-")
    # Assert
    assert len(parts) == 3


def test_gen_timestamp_year_part_has_four_digits():
    # Arrange
    # (no inputs)
    # Act
    year_part = gen_timestamp().split("-")[0]
    # Assert
    assert len(year_part) == 4


def test_gen_timestamp_year_part_is_all_digits():
    # Arrange
    # (no inputs)
    # Act
    year_part = gen_timestamp().split("-")[0]
    # Assert
    assert year_part.isdigit()


def test_gen_timestamp_year_part_is_in_reasonable_range():
    # Arrange
    # (no inputs)
    # Act
    year = int(gen_timestamp().split("-")[0])
    # Assert
    assert 2020 <= year <= 2099


def test_gen_timestamp_month_day_part_has_four_digits():
    # Arrange
    # (no inputs)
    # Act
    month_day = gen_timestamp().split("-")[1]
    # Assert
    assert len(month_day) == 4


def test_gen_timestamp_month_day_part_is_all_digits():
    # Arrange
    # (no inputs)
    # Act
    month_day = gen_timestamp().split("-")[1]
    # Assert
    assert month_day.isdigit()


def test_gen_timestamp_hour_minute_part_has_four_digits():
    # Arrange
    # (no inputs)
    # Act
    hour_minute = gen_timestamp().split("-")[2]
    # Assert
    assert len(hour_minute) == 4


def test_gen_timestamp_hour_minute_part_is_all_digits():
    # Arrange
    # (no inputs)
    # Act
    hour_minute = gen_timestamp().split("-")[2]
    # Assert
    assert hour_minute.isdigit()


# ----- deterministic timestamp via injected now_fn (no mocks) ---------------

def test_gen_timestamp_uses_injected_now_fn_for_specific_datetime():
    # Arrange
    now_fn = _fixed_now(2025, 6, 2, 15, 30)
    # Act
    result = gen_timestamp(now_fn=now_fn)
    # Assert
    assert result == "2025-0602-1530"


@pytest.mark.parametrize(
    "year,month,day,hour,minute,expected",
    [
        (2025, 1, 1, 0, 0, "2025-0101-0000"),
        (2025, 12, 31, 23, 59, "2025-1231-2359"),
        (2025, 2, 9, 9, 5, "2025-0209-0905"),
        (2025, 10, 10, 10, 10, "2025-1010-1010"),
    ],
)
def test_gen_timestamp_formats_edge_case_datetimes_correctly(
    year, month, day, hour, minute, expected
):
    # Arrange
    now_fn = _fixed_now(year, month, day, hour, minute)
    # Act
    result = gen_timestamp(now_fn=now_fn)
    # Assert
    assert result == expected


# ----- consistency over rapid calls -----------------------------------------

def test_gen_timestamp_keeps_pattern_consistent_across_two_rapid_calls():
    # Arrange
    pattern = _PATTERN
    # Act
    ts1 = gen_timestamp()
    time.sleep(0.05)
    ts2 = gen_timestamp()
    matches = bool(re.match(pattern, ts1)) and bool(re.match(pattern, ts2))
    # Assert
    assert matches


# ----- current-time correctness ---------------------------------------------

def test_gen_timestamp_year_matches_current_wall_clock_year():
    # Arrange
    now = datetime.now()
    # Act
    year_in_ts = int(gen_timestamp()[:4])
    # Assert
    assert year_in_ts == now.year


def test_gen_timestamp_month_matches_current_wall_clock_month():
    # Arrange
    now = datetime.now()
    # Act
    month_in_ts = int(gen_timestamp()[5:7])
    # Assert
    assert month_in_ts == now.month


def test_gen_timestamp_day_matches_current_wall_clock_day():
    # Arrange
    now = datetime.now()
    # Act
    day_in_ts = int(gen_timestamp()[7:9])
    # Assert
    assert day_in_ts == now.day


def test_gen_timestamp_hour_minute_within_one_minute_of_now():
    # Arrange
    now = datetime.now()
    # Act
    ts = gen_timestamp()
    h = int(ts[10:12])
    m = int(ts[12:14])
    diff = abs((now.hour * 60 + now.minute) - (h * 60 + m))
    # Assert
    assert diff <= 1


# ----- alias ----------------------------------------------------------------

def test_timestamp_is_alias_pointing_to_gen_timestamp():
    # Arrange
    # (no inputs)
    # Act
    is_alias = timestamp is gen_timestamp
    # Assert
    assert is_alias


def test_timestamp_alias_matches_dashed_pattern():
    # Arrange
    pattern = _PATTERN
    # Act
    result = timestamp()
    # Assert
    assert re.match(pattern, result)


# ----- month padding via injected now_fn ------------------------------------

@pytest.mark.parametrize("month", list(range(1, 10)))
def test_gen_timestamp_zero_pads_single_digit_month_part(month):
    # Arrange
    now_fn = _fixed_now(2025, month, 15, 12, 30)
    expected = f"0{month}"
    # Act
    month_part = gen_timestamp(now_fn=now_fn)[5:7]
    # Assert
    assert month_part == expected


# ----- day padding via injected now_fn --------------------------------------

@pytest.mark.parametrize("day", list(range(1, 10)))
def test_gen_timestamp_zero_pads_single_digit_day_part(day):
    # Arrange
    now_fn = _fixed_now(2025, 6, day, 12, 30)
    expected = f"0{day}"
    # Act
    day_part = gen_timestamp(now_fn=now_fn)[7:9]
    # Assert
    assert day_part == expected


# ----- hour/minute padding via injected now_fn ------------------------------

@pytest.mark.parametrize(
    "hour,minute,expected",
    [
        (0, 0, "0000"),
        (5, 7, "0507"),
        (9, 9, "0909"),
        (10, 5, "1005"),
        (23, 59, "2359"),
    ],
)
def test_gen_timestamp_zero_pads_hour_and_minute_correctly(
    hour, minute, expected
):
    # Arrange
    now_fn = _fixed_now(2025, 6, 15, hour, minute)
    # Act
    hhmm_part = gen_timestamp(now_fn=now_fn)[10:14]
    # Assert
    assert hhmm_part == expected


# ----- filename-usage smoke -------------------------------------------------

def test_gen_timestamp_output_contains_no_filename_unsafe_chars():
    # Arrange
    forbidden = set('<>:"|?*')
    # Act
    chars_in_filename = set(f"experiment_{gen_timestamp()}.csv")
    # Assert
    assert not (chars_in_filename & forbidden)


if __name__ == "__main__":
    import os
    pytest.main([os.path.abspath(__file__)])
