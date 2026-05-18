#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Time-stamp: "2026-05-18"
# File: tests/scitex_repro/test__hash_array.py

"""Tests for hash_array function.

All tests follow the SciTeX no-mocks + AAA + single-assert testing
discipline (see scitex general skills 02_package_12_no-mocks.md and
02_package_13_test-quality.md).
"""

import numpy as np
import pytest

from scitex_repro import hash_array


# ----- basic behaviour -------------------------------------------------------

def test_hash_array_function_is_callable_at_module_level():
    # Arrange
    # (no inputs)
    # Act
    is_callable = callable(hash_array)
    # Assert
    assert is_callable


def test_hash_array_returns_string_for_simple_1d_array():
    # Arrange
    arr = np.array([1, 2, 3, 4, 5])
    # Act
    result = hash_array(arr)
    # Assert
    assert isinstance(result, str)


def test_hash_array_returns_sixteen_char_digest_for_1d_array():
    # Arrange
    arr = np.array([1, 2, 3, 4, 5])
    # Act
    result = hash_array(arr)
    # Assert
    assert len(result) == 16


def test_hash_array_returns_sixteen_char_digest_for_2d_array():
    # Arrange
    arr = np.array([[1, 2], [3, 4]])
    # Act
    result = hash_array(arr)
    # Assert
    assert len(result) == 16


def test_hash_array_returns_sixteen_char_digest_for_float_array():
    # Arrange
    arr = np.array([1.1, 2.2, 3.3])
    # Act
    result = hash_array(arr)
    # Assert
    assert len(result) == 16


# ----- determinism -----------------------------------------------------------

def test_hash_array_returns_identical_hash_for_same_array_object():
    # Arrange
    arr = np.array([1, 2, 3, 4, 5])
    # Act
    hashes = (hash_array(arr), hash_array(arr))
    # Assert
    assert hashes[0] == hashes[1]


def test_hash_array_returns_different_hash_for_one_element_change():
    # Arrange
    arr1 = np.array([1, 2, 3, 4, 5])
    arr2 = np.array([1, 2, 3, 4, 6])
    # Act
    hashes = (hash_array(arr1), hash_array(arr2))
    # Assert
    assert hashes[0] != hashes[1]


def test_hash_array_returns_identical_hash_for_array_copy():
    # Arrange
    arr1 = np.array([1, 2, 3, 4, 5])
    arr2 = arr1.copy()
    # Act
    hashes = (hash_array(arr1), hash_array(arr2))
    # Assert
    assert hashes[0] == hashes[1]


# ----- dtype variations ------------------------------------------------------

@pytest.mark.parametrize(
    "arr",
    [
        np.array([1, 2, 3], dtype=np.int32),
        np.array([1.0, 2.0, 3.0], dtype=np.float64),
        np.array([1 + 2j, 3 + 4j], dtype=np.complex128),
        np.array([True, False, True]),
    ],
    ids=["int32", "float64", "complex128", "bool"],
)
def test_hash_array_returns_sixteen_char_digest_for_various_dtypes(arr):
    # Arrange
    array_in = arr
    # Act
    result = hash_array(array_in)
    # Assert
    assert len(result) == 16


# ----- shape variations ------------------------------------------------------

@pytest.mark.parametrize(
    "arr",
    [
        np.array([1, 2, 3, 4, 5]),
        np.array([[1, 2], [3, 4], [5, 6]]),
        np.array([[[1, 2], [3, 4]], [[5, 6], [7, 8]]]),
        np.array([42]),
        np.array([]),
    ],
    ids=["1d", "2d", "3d", "single-element", "empty"],
)
def test_hash_array_returns_sixteen_char_digest_for_various_shapes(arr):
    # Arrange
    array_in = arr
    # Act
    result = hash_array(array_in)
    # Assert
    assert len(result) == 16


# ----- sensitivity -----------------------------------------------------------

def test_hash_array_treats_element_order_as_significant():
    # Arrange
    arr1 = np.array([1, 2, 3])
    arr2 = np.array([3, 2, 1])
    # Act
    hashes = (hash_array(arr1), hash_array(arr2))
    # Assert
    assert hashes[0] != hashes[1]


def test_hash_array_ignores_shape_when_underlying_bytes_match():
    # Arrange
    arr1 = np.array([1, 2, 3, 4])
    arr2 = np.array([[1, 2], [3, 4]])
    # Act
    hashes = (hash_array(arr1), hash_array(arr2))
    # Assert
    assert hashes[0] == hashes[1]


def test_hash_array_treats_dtype_as_significant_for_byte_layout():
    # Arrange
    arr1 = np.array([1, 2, 3], dtype=np.int32)
    arr2 = np.array([1, 2, 3], dtype=np.int64)
    # Act
    hashes = (hash_array(arr1), hash_array(arr2))
    # Assert
    assert hashes[0] != hashes[1]


def test_hash_array_detects_sub_epsilon_value_changes():
    # Arrange
    arr1 = np.array([1.0, 2.0, 3.0])
    arr2 = np.array([1.0, 2.0, 3.0000001])
    # Act
    hashes = (hash_array(arr1), hash_array(arr2))
    # Assert
    assert hashes[0] != hashes[1]


# ----- reproducibility integration ------------------------------------------

def test_hash_array_matches_for_reproduced_random_data_with_same_seed():
    # Arrange
    from scitex_repro import RandomStateManager
    mgr1 = RandomStateManager(seed=42, verbose=False)
    data1 = mgr1("data").random(100)
    mgr2 = RandomStateManager(seed=42, verbose=False)
    data2 = mgr2("data").random(100)
    # Act
    hashes = (hash_array(data1), hash_array(data2))
    # Assert
    assert hashes[0] == hashes[1]


def test_hash_array_differs_for_random_data_with_different_seeds():
    # Arrange
    from scitex_repro import RandomStateManager
    mgr1 = RandomStateManager(seed=42, verbose=False)
    data1 = mgr1("data").random(100)
    mgr2 = RandomStateManager(seed=123, verbose=False)
    data2 = mgr2("data").random(100)
    # Act
    hashes = (hash_array(data1), hash_array(data2))
    # Assert
    assert hashes[0] != hashes[1]


# ----- edge cases ------------------------------------------------------------

def test_hash_array_returns_sixteen_char_digest_for_large_random_array():
    # Arrange
    arr = np.random.rand(10000)
    # Act
    result = hash_array(arr)
    # Assert
    assert len(result) == 16


def test_hash_array_returns_sixteen_char_digest_for_array_containing_nan():
    # Arrange
    arr = np.array([1.0, np.nan, 3.0])
    # Act
    result = hash_array(arr)
    # Assert
    assert len(result) == 16


def test_hash_array_returns_sixteen_char_digest_for_array_containing_inf():
    # Arrange
    arr = np.array([1.0, np.inf, -np.inf])
    # Act
    result = hash_array(arr)
    # Assert
    assert len(result) == 16


def test_hash_array_returns_identical_digest_for_two_equal_nan_arrays():
    # Arrange
    arr1 = np.array([1.0, np.nan, 3.0])
    arr2 = np.array([1.0, np.nan, 3.0])
    # Act
    hashes = (hash_array(arr1), hash_array(arr2))
    # Assert
    assert hashes[0] == hashes[1]


# ----- integration workflows ------------------------------------------------

def test_hash_array_workflow_preserves_hash_when_data_is_unchanged():
    # Arrange
    data = np.array([1, 2, 3, 4, 5])
    original_hash = hash_array(data)
    _ = data * 2  # processing does not mutate data
    # Act
    new_hash = hash_array(data)
    # Assert
    assert new_hash == original_hash


def test_hash_array_workflow_changes_hash_after_data_transformation():
    # Arrange
    data = np.array([1, 2, 3, 4, 5])
    original_hash = hash_array(data)
    processed = data * 2
    # Act
    processed_hash = hash_array(processed)
    # Assert
    assert processed_hash != original_hash


def test_hash_array_experiment_workflow_matches_under_same_seed():
    # Arrange
    from scitex_repro import RandomStateManager, gen_id
    _ = gen_id(N=6)
    mgr = RandomStateManager(seed=42, verbose=False)
    results = mgr("experiment").random(100)
    results_hash = hash_array(results)
    mgr2 = RandomStateManager(seed=42, verbose=False)
    verified = mgr2("experiment").random(100)
    # Act
    verified_hash = hash_array(verified)
    # Assert
    assert results_hash == verified_hash


if __name__ == "__main__":
    import os
    pytest.main([os.path.abspath(__file__)])
