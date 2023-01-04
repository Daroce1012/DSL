from Parser.Symbol import Symbol, Sentence

class Production(object):
    def __init__(self, non_terminal, sentence):
        self.Left = non_terminal
        self.Right = sentence

    def __str__(self):
        return '%s := %s' % (self.Left, self.Right)

    def __repr__(self):
        return '%s -> %s' % (self.Left, self.Right)

    def __iter__(self):
        yield self.Left
        yield self.Right

    def __eq__(self, other):
        return isinstance(other, Production) and self.Left == other.Left and self.Right == other.Right

    def __hash__(self):
        return hash((self.Left, self.Right))

    @property
    def is_epsilon(self):
        return self.Right.IsEpsilon



class AttributeProduction(Production):
    def __init__(self, non_terminal, sentence, attributes):
        if not isinstance(sentence, Sentence) and isinstance(sentence, Symbol):
            sentence = Sentence(sentence)
        super(AttributeProduction, self).__init__(non_terminal, sentence)
        self.attributes = attributes

    def __str__(self):
        return '%s := %s' % (self.Left, self.Right)

    def __repr__(self):
        return '%s -> %s' % (self.Left, self.Right)

    def __iter__(self):
        yield self.Left
        yield self.Right

    @property
    def is_epsilon(self):
        return self.Right.IsEpsilon
