class ShiftReduce:
    SHIFT = 'SHIFT'
    REDUCE = 'REDUCE'
    OK = 'OK'

    def __init__(self, g):
        self.g = g
        self.action = {}
        self.goto = {}
        self.build_parsing_table()

    def build_parsing_table(self):
        pass

    def __call__(self, tokens, ope=False):
        stack = [0]
        cursor = 0
        output = []
        operations = []
        errors = []

        while True:
            state = stack[-1]
            lookahead = tokens[cursor]
            try:
                action, tag = self.action[state, lookahead]
                # Shift case
                if action == self.SHIFT:
                    operations.append(self.SHIFT)
                    stack.append(tag)
                    cursor += 1

                # Reduce case
                elif action == self.REDUCE:
                    operations.append(self.REDUCE)
                    output.append(tag)
                    for _ in tag.Right:
                        stack.pop()
                    a = self.goto[stack[-1], tag.Left.name]
                    stack.append(a)

                # OK case
                elif action == self.OK:
                    return errors, output, operations if ope else output
                # Invalid case
                else:
                    raise NameError
            except KeyError:
                errors.append(tokens[cursor])
                return errors, output, operations if ope else output
