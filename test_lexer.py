import pytest
from pycompiler import lexer

def test_lexer_parses_single_number():
    line = "5"
    
    tokens = lexer(line)

    assert tokens[0].type == "NUMBER"