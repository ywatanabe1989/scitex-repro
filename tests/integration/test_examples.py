"""Smoke test: every example script under examples/ runs to completion."""

import subprocess
import sys
from pathlib import Path

import pytest

EXAMPLES = sorted(Path(__file__).resolve().parents[2].joinpath("examples").glob("*.py"))


def test_examples_directory_contains_scripts_to_run():
    # Arrange
    examples = EXAMPLES
    # Act
    count = len(examples)
    # Assert
    assert count > 0, "No example scripts found under examples/"


@pytest.mark.parametrize("example_path", EXAMPLES, ids=lambda p: p.name)
def test_example_script_runs_to_completion(tmp_path, example_path):
    # Arrange
    cmd = [sys.executable, str(example_path)]
    # Act
    r = subprocess.run(
        cmd,
        cwd=tmp_path,
        capture_output=True,
        text=True,
        timeout=120,
    )
    # Assert
    assert r.returncode == 0, (
        f"{example_path.name} failed:\nSTDOUT:\n{r.stdout}\nSTDERR:\n{r.stderr}"
    )
