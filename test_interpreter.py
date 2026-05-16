import pytest
from pycompiler import interpreter

def test_assignment_returns_correct_variable_store():
    input = "n = 5"

    result = interpreter(input)

    assert result["n"] == 5

def test_assignment_of_math_expression_returns_correct_variable_store():
    input = "n = 2 2 +"

    result = interpreter(input)

    assert result["n"] == 4

def test_two_assignment_returns_correct_variable_store():
    input = "n = 5\nm = 4"

    result = interpreter(input)

    assert result["n"] == 5
    assert result["m"] == 4

def test_two_assignments_with_math_expression_returns_correct_variable_store():
    input = "n = 5 1 +\nm = 4 1 +"

    result = interpreter(input)

    assert result["n"] == 6
    assert result["m"] == 5

def test_while_loop_returns_correct_variable_store():
    input = "n = 1\nwhile n 1 >=\nn = 0\nend"

    result = interpreter(input)

    assert result["n"] == 0

def test_while_loop_that_never_runs_returns_correct_variable_store():
    input = "n = 0\nwhile n 1 >=\nn = 5\nend"

    result = interpreter(input)

    assert result["n"] == 0

def test_nested_while_loops_return_correct_variable_store():
    input = "n = 2\nm = 2\nwhile n 1 >=\nwhile m 1 >=\nm = m 1 -\nend\nn = n 1 -\nend"

    result = interpreter(input)

    assert result["n"] == 0
    assert result["m"] == 0

def test_print_statement_prints_5(capsys):
    input = "n = 5\nprint n"

    interpreter(input)

    captured = capsys.readouterr()

    assert captured.out.strip() == "5"