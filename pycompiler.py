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
            elif char in ["while", "end", "print", "if", "else"]:
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
    elif "print" == parts[0]:
        if len(parts) < 2:
            raise(SyntaxError("Missing expression after print"))
        expression = " ".join(parts[1:])
        return Statement(type="PRINT", expression=expression)
    else:
        try:
            variable, expression = line.split("=", 1)
        except ValueError:
            raise(SyntaxError(f"Invalid statement: '{line}'"))
        variable = variable.strip()
        expression = expression.strip()
        return Statement(type="ASSIGN", variable=variable, expression=expression)

def interpreter(input):
    lines = input.splitlines()
    line_stack = []
    var_store = {}
    pc = 0
    while pc < len(lines):
        line = lines[pc]
        statement = parse_statement(line)
        if statement.type == "ASSIGN":
            tokenised_expression = lexer(statement.expression)
            evaluated_result = evaluate(tokenised_expression, var_store)
            var_store[statement.variable] = evaluated_result
        elif statement.type == "PRINT":
            tokenised_expression = lexer(statement.expression)
            evaluated_result = evaluate(tokenised_expression, var_store)
            print(evaluated_result)
        elif statement.type == "WHILE":
            tokenised_expression = lexer(statement.expression)
            evaluated_result = evaluate(tokenised_expression, var_store)
            if evaluated_result == 1:
                line_stack.append(pc)
            else:
                depth = 1
                while depth > 0:
                    pc += 1
                    if lines[pc].startswith("while"):
                        depth += 1
                    elif lines[pc].startswith("end"):
                        depth -= 1
        elif statement.type == "END":
            pc = line_stack.pop()
            continue
        pc += 1
    return var_store