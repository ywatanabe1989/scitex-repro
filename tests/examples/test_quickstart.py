"""PS303 example mirror stub: ensure examples/quickstart.py is syntactically valid."""

import subprocess
import sys
from pathlib import Path

EXAMPLE = Path(__file__).resolve().parents[2] / "examples" / "quickstart.py"


def test_quickstart_example_file_exists_on_disk():
    # Arrange
    example_path = EXAMPLE
    # Act
    exists = example_path.exists()
    # Assert
    assert exists, f"missing example: {example_path}"


def test_quickstart_example_compiles_without_syntax_errors():
    # Arrange
    example_path = EXAMPLE
    # Act
    result = subprocess.run(
        [sys.executable, "-m", "py_compile", str(example_path)],
        capture_output=True,
        text=True,
    )
    # Assert
    assert result.returncode == 0, f"py_compile failed: {result.stderr}"
