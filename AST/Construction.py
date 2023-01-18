from Parser.ShiftReduceParser import ShiftReduce

def construction_ast(parser_lr1, operations, tokens):
    if not parser_lr1 or not operations or not tokens:
        return  # Nada que eval!!!!
    right_parse = iter(parser_lr1)
    tokens = iter(tokens)
    stack = []
    for operation in operations:
        if operation == ShiftReduce.SHIFT:
            token = next(tokens)
            stack.append(token.value)
        elif operation == ShiftReduce.REDUCE:
            production = next(right_parse)
            head, body = production
            attributes = production.attributes
            assert all(rule is None for rule in attributes[1:]), 'There must be only synteticed attributes.'
            rule = attributes[0]
            if len(body):
                synteticed = [None] + stack[-len(body):]
                value = rule(None, synteticed)
                stack[-len(body):] = [value]           #Solo se inicializa el nodo
            else:
                stack.append(rule(None, None))
        else:
            raise Exception('error')
    # queda la raiz del AST, el node Program, y 'eof', el token final.
    return stack[0]
