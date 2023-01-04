from Parser.ShiftReduceParser import ShiftReduce
from Parser.Tools import *
from Parser.Grammar import *
from Parser.State import *
from Parser.Item import *


class LR1Parser(ShiftReduce):
    def build_parsing_table(self):
        g = self.g.augmented_grammar(True)
        automata = self.build_automata(g)
        for i, node in enumerate(automata):
            node.idx = i
        for node in automata:
            idx = node.idx
            for item in node.state:
                p = item.Production
                if item.is_reduce_item:
                    if p.Left == g.Start_symbol:
                        self._register(self.action, (idx, self.g.Eof.name), (ShiftReduce.OK, None))
                    else:
                        for c in item.Lookaheads:
                            self._register(self.action, (idx, c.name), (ShiftReduce.REDUCE, p))
                else:
                    if item.next_symbol.is_terminal:
                        self._register(self.action, (idx, item.next_symbol.name),
                                       (ShiftReduce.SHIFT, node[item.next_symbol.name][0].idx))
                    else:
                        self._register(self.goto, (idx, item.next_symbol.name), node[item.next_symbol.name][0].idx)
                pass

    def build_automata(self, g):
        assert len(g.Start_symbol.Productions) == 1, 'Grammar must be augmented'
        firsts = compute_firsts(g)
        firsts[g.Eof] = ContainerSet(g.Eof)
        start_production = g.Start_symbol.Productions[0]
        start_item = Item(start_production, 0, lookaheads=(g.Eof,))
        start = frozenset([start_item])
        closure = self.closure_lr1(start, firsts)
        automata = State(frozenset(closure), True)
        pending = [start]
        visited = {start: automata}
        while pending:
            current = pending.pop()
            current_state = visited[current]
            for symbol in g.Terminals + g.Non_terminals:
                #  (Get/Build `next_state`)
                a = self.goto_lr1(current_state.state, symbol, firsts, True)
                if not a:
                    continue
                try:
                    next_state = visited[a]
                except KeyError:
                    next_state = State(frozenset(self.goto_lr1(current_state.state, symbol, firsts)), True)
                    visited[a] = next_state
                    pending.append(a)
                current_state.add_transition(symbol.name, next_state)
        automata.set_formatter(multiline_formatter)
        return automata

    def goto_lr1(self, items, symbol, firsts=None, just_kernel=False):
        assert just_kernel or firsts is not None, '`firsts` must be provided if `just_kernel=False`'
        items = frozenset(item.next_item() for item in items if item.next_symbol == symbol)
        return items if just_kernel else self.closure_lr1(items, firsts)

    def closure_lr1(self, items, firsts):
        closure = ContainerSet(*items)
        changed = True
        while changed:
            new_items = ContainerSet()
            # por cada item hacer expand y añadirlo a new_items
            for item in closure:
                e = self.expand(item, firsts)
                new_items.extend(e)
            changed = closure.update(new_items)
        return self.compress(closure)

    @staticmethod
    def compress(items):
        centers = {}
        for item in items:
            center = item.center()
            try:
                lookaheads = centers[center]
            except KeyError:
                centers[center] = lookaheads = set()
            lookaheads.update(item.Lookaheads)
        return {Item(x.Production, x.Pos, set(lookahead)) for x, lookahead in centers.items()}

    @staticmethod
    def expand(item, firsts):
        next_symbol = item.next_symbol
        if next_symbol is None or not next_symbol.is_non_terminal:
            return []
        lookaheads = ContainerSet()
        #  (Compute lookahead for child items)
        # calcular el first a todos los preview posibles
        for p in item.preview():
            for first in compute_local_first(firsts, p):
                lookaheads.add(first)
        _list = []
        for production in next_symbol.Productions:
            _list.append(Item(production, 0, lookaheads))
        return _list

    @staticmethod
    def _register(table, key, value):
        table[key] = value
