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
    assert statement.expression == "5"

def test_invalid_assignment_returns_error():
    input = "n"
    with pytest.raises(SyntaxError):
        parse_statement(input)

def test_print_returns_PRINT_statement_object():
    input = "print n"

    statement = parse_statement(input)

    assert statement.type == "PRINT"
    assert statement.expression == "n"

def test_print_without_expression_returns_syntax_error():
    input = "print"
    with pytest.raises(SyntaxError):
        parse_statement(input)

def test_if_with_expression_returns_IF_statement_object_with_expression():
    input = "if n 1 >="

    statement = parse_statement(input)

    assert statement.type == "IF"
    assert statement.expression == "n 1 >="

def test_if_without_expression_raises_syntax_error():
    input = "if"

    with pytest.raises(SyntaxError):
        parse_statement(input)

def test_else_returns_ELSE_statement_object():
    input = "else"

    statement = parse_statement(input)

    assert statement.type == "ELSE"

def test_else_with_expression_returns_syntax_error():
    input = "else 1 1 >="
    with pytest.raises(SyntaxError):
        parse_statement(input)