import pytest
from pycompiler import lexer, evaluate, UndefinedVariableError, StackUnderflowError


def test_single_number_token_returns_value():
    tokens = lexer("5")

    evaluation = evaluate(tokens)

    assert evaluation == 5

def test_variable_returns_value():
    tokens = lexer("n")
    variables = {"n": 5}

    evaluation = evaluate(tokens, variables)

    assert evaluation == 5

def test_raise_undefined_error_if_variable_not_found():
    tokens = lexer("n")

    with pytest.raises(UndefinedVariableError):
        evaluate(tokens)


def test_1_plus_1_returns_2():
    tokens = lexer("1 1 +")

    evaluation = evaluate(tokens)

    assert evaluation == 2

def test_1_minus_1_returns_0():
    tokens = lexer("1 1 -")

    evaluation = evaluate(tokens)

    assert evaluation == 0

def test_2_times_2_returns_4():
    tokens = lexer("2 2 *")

    evaluation = evaluate(tokens)

    assert evaluation == 4

def test_5_greater_than_or_equal_to_1_returns_true():
    tokens = lexer("5 1 >=")

    evaluation = evaluate(tokens)

    assert evaluation == 1

def test_1_greater_than_or_equal_to_5_returns_false():
    tokens = lexer("1 5 >=")

    evaluation = evaluate(tokens)

    assert evaluation == 0

def test_raises_error_if_only_operator_is_given():
    tokens = lexer("+")

    with pytest.raises(StackUnderflowError):
        evaluate(tokens)