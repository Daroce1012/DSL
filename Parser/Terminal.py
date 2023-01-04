from .Symbol import Symbol

class Terminal(Symbol):
    def __int__(self, name, grammar):
        super().__init__(name, grammar)
        self.Productions = []

    def __str__(self):
        return self.name

    @property
    def is_terminal(self):
        return True

    @property
    def is_non_terminal(self):
        return False

    @property
    def is_epsilon(self):
        return False

class EOF(Terminal):
    def __init__(self, grammar):
        super().__init__('eof', grammar)

    def __str__(self):
        return 'eof'


