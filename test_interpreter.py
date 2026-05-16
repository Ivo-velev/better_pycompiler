import pytest
from pycompiler import interpreter

def test_assignment_returns_correct_variable_store():
    input = "n = 5"

    result = interpreter(input)

    assert result["n"] == 5