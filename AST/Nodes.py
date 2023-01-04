class Node:
    def evaluate(self):
        raise NotImplementedError()


class ProgramNode(Node):
    def __init__(self, declarations):
        self.declarations = declarations

    def evaluate(self):
        pass


class DeclarationNode(Node):
    pass

    def evaluate(self):
        pass


class ExpressionNode(Node):
    pass

    def evaluate(self):
        pass


class ClassDeclarationNode(DeclarationNode):
    def __init__(self, idx, features, parent=None):
        self.id = idx
        self.parent = parent
        self.features = features


class FuncDeclarationNode(DeclarationNode):
    def __init__(self, idx, params, body):
        self.id = idx
        self.params = params
        self.body = body


class AttrDeclarationNode(DeclarationNode):
    def __init__(self, idx, typex):
        self.id = idx
        self.type = typex


class VarDeclarationNode(ExpressionNode):
    def __init__(self, idx, expr):
        self.id = idx
        self.expr = expr


class AssignNode(ExpressionNode):
    def __init__(self, idx, expr):
        self.id = idx
        self.expr = expr


class CallNode(ExpressionNode):
    def __init__(self, idx, args):
        self.id = idx
        self.args = args


class AtomicNode(ExpressionNode):
    def __init__(self, lex):
        self.lex = lex

    def evaluate(self):
        pass


class BinaryNode(ExpressionNode):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def evaluate(self):
        lvalue = self.left.evaluate()
        rvalue = self.right.evaluate()
        return self.operate(lvalue, rvalue)

    @staticmethod
    def operate(lvalue, rvalue):
        raise NotImplementedError()


class ConstantNumNode(AtomicNode):
    pass


class VariableNode(AtomicNode):
    pass


class InstantiateNode(AtomicNode):
    pass


class PlusNode(BinaryNode):
    pass


class MinusNode(BinaryNode):
    pass


class StarNode(BinaryNode):
    pass


class DivNode(BinaryNode):
    pass


class PrintNode(DeclarationNode):
    def __init__(self, expr):
        self.expr = expr
