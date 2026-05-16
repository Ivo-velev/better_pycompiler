class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

def lexer(line):
    chars = line.split()
    tokens = []
    for char in chars:
        if char.isnumeric():
            tokens.append(Token(type="NUMBER", value=int(char)))
    return tokens