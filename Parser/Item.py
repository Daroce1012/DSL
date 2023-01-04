class Item:
    def __init__(self, production, pos, lookaheads=frozenset()):
        self.Production = production
        self.Pos = pos
        self.Lookaheads = frozenset(look for look in lookaheads)

    def __str__(self):
        s = str(self.Production.Left) + " -> "
        if len(self.Production.Right) > 0:
            for i, c in enumerate(self.Production.Right):
                if i == self.Pos:
                    s += "."
                s += str(self.Production.Right[i])
            if self.Pos == len(self.Production.Right):
                s += "."
        else:
            s += "."
        s += ", " + str(self.Lookaheads)[10:-1]
        return s

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return (
                (self.Pos == other.Pos) and
                (self.Production == other.Production) and
                (set(self.Lookaheads) == set(other.Lookaheads))
        )

    def __hash__(self):
        return hash((self.Production, self.Pos, self.Lookaheads))

    @property
    def is_reduce_item(self):
        return len(self.Production.Right) == self.Pos

    @property
    def next_symbol(self):
        if self.Pos < len(self.Production.Right):
            return self.Production.Right[self.Pos]
        else:
            return None

    def next_item(self):
        if self.Pos < len(self.Production.Right):
            return Item(self.Production, self.Pos + 1, self.Lookaheads)
        else:
            return None

#Esta devuelve todas las posibles cadenas que resultan de concatenar
# _"lo que queda por leer del item tras saltarse `skip=1` símbolos"_ 
# con los posibles lookaheads. 
# Esta función nos será útil, pues sabemos que el lookahead de los items LR(1) 
# se obtiene de calcular el `first` de estas cadenas
    def preview(self, skip=1):
        return [ self.Production.Right[self.Pos + skip:] + (lookahead,) for lookahead in self.Lookaheads]

    def center(self):
        return Item(self.Production, self.Pos)
