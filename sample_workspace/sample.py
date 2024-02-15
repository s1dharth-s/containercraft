def mypy_example(a: str) -> int:
    """
    Shows working of mypy for type checking.
    """
    return a + 2  # Unsupported operand types for + ("str" and "int")


def mypy_corrected(a: str) -> int:
    return int(a) + 2  # Corrected


def test_mypy_corrected(a: str):
    assert mypy_corrected("3") == 5
