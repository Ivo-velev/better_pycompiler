import pytest
from pycompiler import parse_statement

def test_end_returns_END_statement_object():
    input = "end"

    statement = parse_statement(input)

    assert statement.type == "END"

def test_while_with_expression_returns_WHILE_statement_object_with_expression():
    input = "while n 1 >="

    statement = parse_statement(input)

    assert statement.type == "WHILE"
    assert statement.expression == "n 1 >="

def test_while_returns_syntax_error():
    input = "while"

    with pytest.raises(SyntaxError):
        parse_statement(input)

def test_assignment_returns_assignment_statement_object():
    input = "n = 5"

    statement = parse_statement(input)

    assert statement.type == "ASSIGN"
    assert statement.variable == "n"
    assert statement.expression == 5

def test_invalid_assignment_returns_error():
    input = "n"
    with pytest.raises(SyntaxError):
        parse_statement(input)