from Parser.Symbol import*
from Parser.Production import*

class NonTerminal(Symbol):
    def __init__(self, name, grammar):
        super().__init__(name, grammar)
        self.Productions = []

    def __str__(self):
        return self.name

    def __mod__(self, other):
        if isinstance(other, Sentence):
            p = Production(self, other)
            self.grammar.add_production(p)
            return self
        if isinstance(other, tuple):
            if len(other) == 2:
                other += (None,) * len(other[0])
            # Debe definirse una regla por cada símbolo de la producción
            if isinstance(other[0], Symbol) or isinstance(other[0], Sentence):
                p = AttributeProduction(self, other[0], other[1:])
            else:
                raise Exception("")
            self.grammar.add_production(p)
            return self
        if isinstance(other, Symbol):
            p = Production(self, Sentence(other))
            self.grammar.add_production(p)
            return self
        if isinstance(other, SentenceList):
            for s in other:
                p = Production(self, s)
                self.grammar.add_production(p)
            return self
        raise TypeError(other)

    @property
    def is_terminal(self):
        return False

    @property
    def is_non_terminal(self):
        return True

    @property
    def is_epsilon(self):
        return False
