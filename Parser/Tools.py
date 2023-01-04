class ContainerSet:
    def __init__(self, *values, contains_epsilon=False):
        self.set = set(values)
        self.contains_epsilon = contains_epsilon

    def add(self, value):
        n = len(self.set)
        self.set.add(value)
        return n != len(self.set)

    def extend(self, values):
        change = False
        for value in values:
            change |= self.add(value)
        return change

    def set_epsilon(self, value=True):
        last = self.contains_epsilon
        self.contains_epsilon = value
        return last != self.contains_epsilon

    def update(self, other):
        n = len(self.set)
        self.set.update(other.set)
        return n != len(self.set)

    def epsilon_update(self, other):
        return self.set_epsilon(self.contains_epsilon | other.contains_epsilon)

    def hard_update(self, other):
        return self.update(other) | self.epsilon_update(other)

    def __len__(self):
        return len(self.set) + int(self.contains_epsilon)

    def __iter__(self):
        return iter(self.set)


# Computes First(alpha), given First(Vt) and First(Vn)
# alpha in (Vt U Vn)*
def compute_local_first(firsts, alpha):
    first_alpha = ContainerSet()
    try:
        alpha_is_epsilon = alpha.is_epsilon
    except:
        alpha_is_epsilon = False
    if alpha_is_epsilon:
        first_alpha.set_epsilon()
    else:
        for item in alpha:
            first_symbol = firsts[item]
            first_alpha.update(first_symbol)
            if not first_symbol.contains_epsilon:
                break
        else:
            first_alpha.set_epsilon()
    return first_alpha


# Computes First(Vt) U First(Vn) U First(alpha)
# P: X -> alpha
def compute_firsts(g):
    firsts = {}
    change = True
    # init First(Vt)
    for terminal in g.Terminals:
        firsts[terminal] = ContainerSet(terminal)
    # init First(Vn)
    for non_terminal in g.Non_terminals:
        firsts[non_terminal] = ContainerSet()
    while change:
        change = False
        # P: X -> alpha
        for production in g.Productions:
            x = production.Left
            alpha = production.Right
            first_x = firsts[x]
            # init First(alpha)
            try:
                first_alpha = firsts[alpha]
            except:
                first_alpha = firsts[alpha] = ContainerSet()
            local_first = compute_local_first(firsts, alpha)
            # update First(X) and First(alpha) from CurrentFirst(alpha)
            change |= first_alpha.hard_update(local_first)
            change |= first_x.hard_update(local_first)

    # First(Vt) + First(Vt) + First(RightSides)
    return firsts
