from sample import mypy_corrected, mypy_example


def test_mypy_example():
    assert (
        mypy_example("3") == 5
    )  # Test will fail: Unsupported operand types for + ("str" and "int")


def test_mypy_corrected():
    assert mypy_corrected("3") == 5  # Test will pass
