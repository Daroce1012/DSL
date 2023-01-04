from .Terminal import Terminal
from .Symbol import Sentence

class Epsilon(Terminal, Sentence):
    def __init__(self, grammar):
        super().__init__('epsilon', grammar)

    def __hash__(self):
        return hash("")

    def __len__(self):
        return 0

    def __str__(self):
        return "e"

    def __repr__(self):
        return 'epsilon'

    def __iter__(self):
        yield from ()

    def __add__(self, other):
        return other

    def __eq__(self, other):
        return isinstance(other, (Epsilon,))

    @property
    def is_epsilon(self):
        return True
