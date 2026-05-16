class CompilerError(Exception):
    def __init__(self, message, line=None):
        self.message = message
        self.line = line
        super().__init__(f"Error (line {line}): {message}" if line else f"Error: {message}")

class UndefinedVariableError(CompilerError): pass
class StackUnderflowError(CompilerError): pass

class Token:
    def __init__(self, type, value, line):
        self.type = type
        self.value = value
        self.line = line

class Statement:
    def __init__(self, type, variable=None, expression=None):
        self.type = type
        self.variable = variable
        self.expression = expression

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

def evaluate(tokens, variables=None):
    if variables is None:
        variables = {}
    stack = []
    for token in tokens:
        if token.type == "NUMBER":
            stack.append(token.value)
        elif token.type == "IDENT":
            if token.value in variables:
                stack.append(variables[token.value])
            else:
                raise UndefinedVariableError(f"Undefined variable '{token.value}'", token.line)
        elif token.type == "OPERATOR":
            try:
                rhs = stack.pop()
                lhs = stack.pop()
            except IndexError:
                raise StackUnderflowError(f"Not enough values for operator '{token.value}'", token.line)

            if token.value == "+":
                stack.append(lhs + rhs)
            elif token.value == "-":
                stack.append(lhs - rhs)
            elif token.value == "*":
                stack.append(lhs * rhs)
            elif token.value == ">=":
                stack.append(1 if lhs >= rhs else 0)
    return stack[0]

def parse_statement(line):
    parts = line.split()
    if "end" == parts[0]:
        return Statement(type="END")
    elif "while" == parts[0]:
        if len(parts) < 2:
            raise(SyntaxError("Missing condition after while"))
        expression = " ".join(parts[1:])
        return Statement(type="WHILE", expression=expression)
    else:
        try:
            variable, expression = line.split("=", 1)
        except ValueError:
            raise(SyntaxError(f"Invalid statement: '{line}'"))
        variable = variable.strip()
        expression = expression.strip()
        if expression.isnumeric():
            expression = int(expression)
        return Statement(type="ASSIGN", variable=variable, expression=expression)

def interpreter(input):
    lines = input.splitlines()
    var_store = {}
    for line in lines:
        statement = parse_statement(line)
        if statement.type == "ASSIGN":
            var_store[statement.variable] = statement.expression
    return var_store