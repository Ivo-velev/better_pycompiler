class Token:
    def __init__(self, type, value, line):
        self.type = type
        self.value = value
        self.line = line

def lexer(input):
    lines = input.splitlines()
    tokens = []
    for count, line in enumerate(lines):
        chars = line.split()
        line_number = count+1
        for char in chars:
            if char.isnumeric():
                tokens.append(Token(type="NUMBER", value=int(char), line=line_number))
            elif char in ["while", "end"]:
                tokens.append(Token(type="KEYWORD", value=char, line=line_number))
            elif char.isalpha():
                tokens.append(Token(type="IDENT", value=char, line=line_number))
            elif char == "=":
                tokens.append(Token(type="ASSIGN", value=char, line=line_number))
            elif char in ["+", "-", "*", ">="]:
                tokens.append(Token(type="OPERATOR", value=char, line=line_number))
            else:
                raise SyntaxError("Unexpected character '%s'" % char)
    return tokens