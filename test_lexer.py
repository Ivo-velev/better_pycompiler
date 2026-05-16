import pytest
from pycompiler import lexer

def test_lexer_parses_single_number():
    line = "5"
    
    tokens = lexer(line)

    assert tokens[0].type == "NUMBER"
    assert tokens[0].value == 5
    assert tokens[0].line == 1

def test_lexer_parses_single_indentifier():
    line = "n"

    tokens = lexer(line)

    assert tokens[0].type == "IDENT"
    assert tokens[0].value == "n"
    assert tokens[0].line == 1

def test_lexer_parses_keyword():
    line = "while"

    tokens = lexer(line)

    assert tokens[0].type == "KEYWORD"
    assert tokens[0].value == "while"
    assert tokens[0].line == 1

def test_lexer_parser_numbers_on_seperate_lines():
    input = "5\n5"

    tokens = lexer(input)

    assert len(tokens) == 2

    assert tokens[0].type == "NUMBER"
    assert tokens[0].value == 5
    assert tokens[0].line == 1
    assert tokens[1].type == "NUMBER"
    assert tokens[1].value == 5
    assert tokens[1].line == 2

def test_lexer_parses_assign():
    input = "="

    tokens = lexer(input)

    assert tokens[0].type == "ASSIGN"
    assert tokens[0].value == "="
    assert tokens[0].line == 1

@pytest.mark.parametrize("operator", ["+", "-", "*", ">="])
def test_lexer_parses_operator(operator):
    tokens = lexer(operator)

    assert tokens[0].type == "OPERATOR"
    assert tokens[0].value == operator
    assert tokens[0].line == 1

def test_unknown_char_raises_syntax_error():
    input = "@"

    with pytest.raises(SyntaxError):
        lexer(input)

def test_lexer_parses_assignment():
    input = "n = 5"

    tokens = lexer(input)

    assert tokens[0].type == "IDENT"
    assert tokens[0].value == "n"
    assert tokens[0].line == 1

    assert tokens[1].type == "ASSIGN"
    assert tokens[1].value == "="
    assert tokens[1].line == 1

    assert tokens[2].type == "NUMBER"
    assert tokens[2].value == 5
    assert tokens[2].line == 1

def test_lexer_parses_print_as_a_keyword():
    input = "print"

    tokens = lexer(input)

    assert tokens[0].type == "KEYWORD"

def test_lexer_parses_if_as_a_keyword():
    input = "if 1 1 >="

    tokens = lexer(input)

    assert tokens[0].type == "KEYWORD"

def test_lexer_parses_else_as_a_keyword():
    input = "else"

    tokens = lexer(input)

    assert tokens[0].type == "KEYWORD"