class Symbol(object):
    def __init__(self, name, grammar):
        self.name = name
        self.grammar = grammar

    def __repr__(self):
        return repr(self.name)

    def __str__(self):
        return self.name

    def __add__(self, other):
        if isinstance(other, Symbol):
            return Sentence(self, other)
        raise TypeError(other)

    def __or__(self, other):
        if isinstance(other, Sentence):
            return SentenceList(Sentence(self), other)
        raise TypeError(other)

    def __len__(self):
        return 1

    @property
    def is_epsilon(self):
        return False

class Sentence(object):
    def __init__(self, *args):
        self._symbols = tuple(x for x in args if not x.is_epsilon)
        self.hash = hash(self._symbols)

    def __len__(self):
        return len(self._symbols)

    def __add__(self, other):
        if isinstance(other, Symbol):
            return Sentence(*(self._symbols + (other,)))
        if isinstance(other, Sentence):
            return Sentence(*(self._symbols + other._symbols))

    def __or__(self, other):
        if isinstance(other, Sentence):
            return SentenceList(self, other)
        if isinstance(other, Symbol):
            return SentenceList(self, Sentence(other))

    def __str__(self):
        return ("%s " * len(self._symbols) % tuple(self._symbols)).strip()

    def __iter__(self):
        return iter(self._symbols)

    def __getitem__(self, index):
        return self._symbols[index]

    def __eq__(self, other):
        return self._symbols == other._symbols

    def __hash__(self):
        return self.hash

    @property
    def is_epsilon(self):
        return False


class SentenceList(object):
    def __init__(self, *args):
        self._sentences = list(args)

    def add(self, symbol):
        if not symbol and (symbol is None or not symbol.is_epsilon):
            raise ValueError(symbol)
        self._sentences.append(symbol)

    def __or__(self, other):
        if isinstance(other, Sentence):
            self.add(other)
            return self

        if isinstance(other, Symbol):
            return self | Sentence(other)

    def __iter__(self):
        return iter(self._sentences)
