from AST.Context import *
from defined import *

class Node:
    def check_semantic(self, context, errors):
        pass

class ProgramNode(Node):
    def __init__(self, declarations):
        self.declarations = declarations
        self.context = Context()

    def run(self):
        errors = []
        ans = []
        for node in self.declarations:
            node.check_semantic(self.context, errors)
            if isinstance(node, DeclarationNode):
                node.execute(self.context, errors, ans)
        return errors, ans


class DeclarationNode(Node):
    def execute(self, context, errors, ans):
        pass


class ExpressionNode(Node):
    def evaluate(self, context, errors, ans):
        pass


class ClassDeclarationNode(DeclarationNode):
    def __init__(self, idx, features):
        self.idx = idx
        self.features = features

    def check_semantic(self, context, errors):
        pass

    def execute(self, context, errors, ans):
        pass


class PatientNode(ExpressionNode):
    def __init__(self, name,sex,age):
        self.name = name
        self.sex = sex
        self.age = age
        self.symptoms =[]

    def check_semantic(self, context, errors):
        pass

    def evaluate(self, context, errors, ans):
        patient = Patient(self.name,self.sex,self.age)
        return patient



class AddNode(DeclarationNode):
    def __init__(self, name_patient, element):
        self.name_patient = name_patient
        self.element = element

    def check_semantic(self, context, errors):
        if not context.check_var_defined(self.name_patient):
            errors.append(f'Patient {self.name_patient} no definida :(')

    def execute(self, context, errors, ans):
        if len(errors) != 0:
            return
        patient = context.get_local_variable_info(self.name_patient)
        element = self.element.evaluate(context, errors, ans)
        patient.add(element) 

class LenNode(ExpressionNode):
    def __init__(self, name_patient):
        self.name_patient = name_patient

    def check_semantic(self, context, errors):
        if not context.check_var_defined(self.name_patient):
            errors.append(f'Patient {self.name_patient} no definida :(')

    def evaluate(self, context, errors, ans):
        if len(errors) != 0:
            return
        patient = context.get_local_variable_info(self.name_patient)
        return patient.len()

class RemoveNode(DeclarationNode):
    def __init__(self, name_patient, element):
        self.name_patient = name_patient
        self.element = element

    def check_semantic(self, context, errors):
        if not context.check_var_defined(self.name_patient):
            errors.append(f'Patient {self.name_patient} no definida :(')

    def execute(self, context, errors, ans):
        if len(errors) != 0:
            return
        patient = context.get_local_variable_info(self.name_patient)
        element = self.element.evaluate(context, errors, ans)
        patient.remove(element) 

#Atributos
    

class NameNode(DeclarationNode):
    def __init__(self, name_patient, name):
        self.name_patient = name_patient
        self.name = name
    def check_semantic(self, context, errors):
        if not context.check_var_defined(self.name_patient):
            errors.append(f'Patient {self.name_patient} no definido :(')

    def execute(self, context, errors, ans):
        if len(errors) != 0:
            return
        patient = context.get_local_variable_info(self.name_patient)
        patient.name = self.name.evaluate(context, errors, ans)

class AgeNode(DeclarationNode):
    def __init__(self, name_patient, age):
        self.name_patient = name_patient
        self.age = age
    def check_semantic(self, context, errors):
        if not context.check_var_defined(self.name_patient):
            errors.append(f'Patient {self.name_patient} no definido :(')

    def execute(self, context, errors, ans):
        if len(errors) != 0:
            return
        patient = context.get_local_variable_info(self.name_patient)
        patient.age = self.age.evaluate(context, errors, ans)
        
class SexNode(DeclarationNode):
    def __init__(self, name_patient, sex):
        self.name_patient = name_patient
        self.sex = sex
    def check_semantic(self, context, errors):
        if not context.check_var_defined(self.name_patient):
            errors.append(f'Patient {self.name_patient} no definido :(')

    def execute(self, context, errors, ans):
        if len(errors) != 0:
            return
        patient = context.get_local_variable_info(self.name_patient)
        patient.sex = self.sex.evaluate(context, errors, ans)
        

class FuncDeclarationNode(DeclarationNode):
    def __init__(self, idx, params, stat_list):
        self.idx = idx
        self.params = params
        self.stat_list = stat_list

    def check_semantic(self, context, errors):
        if context.check_func_defined(self.idx, len(self.params)):
            errors.append(f'Función {self.idx} ya declarada :(')
        else:
            context.def_function(self)

    def execute(self, context, errors, ans):
        pass


class ReturnNode(DeclarationNode):
    def __init__(self, expr):
        self.expr = expr

    def check_semantic(self, context, errors):
        self.expr.check_semantic(context, errors)

    def execute(self, context, errors, ans):
        pass


class AttrDeclarationNode(DeclarationNode):
    def __init__(self, idx):
        self.id = idx

class VarDeclarationNode(DeclarationNode):
    def __init__(self, idx, expr):
        self.idx = idx
        self.expr = expr

    def check_semantic(self, context, errors):
        pass

    def execute(self, context, errors, ans):
        if len(errors) != 0:
            return
        if context.check_var_defined(self.idx):
            errors.append(f'Variable {self.idx} ya definida :(')
        if isinstance(self.expr, ExpressionNode):
            context.def_var(self.idx, self.expr.evaluate(context, errors, ans))
        else:
            context.def_var(self.idx, self.expr)

class ForNode(DeclarationNode):
    def __init__(self, idx, idx_value, expr, idx_counter, counter_one, counter_two, body):
        self.idx = idx
        self.idx_value = idx_value
        self.expr = expr
        self. idx_counter = idx_counter
        self.counter_one = counter_one
        self.counter_two = counter_two
        self.counter = "" + counter_one + counter_two
        self.body = body

    def check_semantic(self, context, errors):
        if self.idx != self.idx_counter:
            errors.append(f'El id {self.idx} debe ser igual a {self.idx_counter}')
        if self.counter_one != self.counter_two:
            errors.append(f'El {self.counter_one} debe ser igual a {self.counter_two}')
        child = context.create_child_context()
        child.def_var(self.idx, self.idx_value)
        for i in self.body:
            i.check_semantic(child, errors)

    def execute(self, context, errors, ans):
        if len(errors) != 0:
            return
        child = context.create_child_context()
        child.def_var(self.idx, self.idx_value)
        while self.expr.evaluate(child, errors, ans):
            for i in self.body:
                i.execute(child, errors, ans)
            if self.counter == "++":
                value = child.get_local_variable_info(self.idx) + 1
            else:
                value = child.get_local_variable_info(self.idx) - 1
            child.redef_var(self.idx, value)

#Ver si funciona y hacer asi el del bool y str
class IntVarDeclarationNode(DeclarationNode):
    def __init__(self, idx, expr):
        self.idx = idx
        self.expr = expr

    def check_semantic(self, context, errors):
        pass

    def execute(self, context, errors, ans):
        if len(errors) != 0:
            return
        if context.check_var_defined(self.idx):
            errors.append(f'Variable {self.idx} ya definida :(')
        if isinstance(self.expr, ExpressionNode):
            value = self.expr.evaluate(context, errors, ans)
            if not isinstance(value,int):
                errors.append(f'variable: {self.idx} no puede convertirse a entero')
            else : context.def_var(self.idx, value)
        else:
            context.def_var(self.idx, self.expr)

class StrVarDeclarationNode(DeclarationNode):
    def __init__(self, idx, expr):
        self.idx = idx
        self.expr = expr

    def check_semantic(self, context, errors):
        pass

    def execute(self, context, errors, ans):
        if len(errors) != 0:
            return
        if context.check_var_defined(self.idx):
            errors.append(f'Variable {self.idx} ya definida :(')
        if isinstance(self.expr, ExpressionNode):
            value = self.expr.evaluate(context, errors, ans)
            if not isinstance(value,str):
                errors.append(f'variable: {self.idx} no puede convertirse a string')
            else : context.def_var(self.idx, value)
        else:
            context.def_var(self.idx, self.expr)

class BoolVarDeclarationNode(DeclarationNode):
    def __init__(self, idx, expr):
        self.idx = idx
        self.expr = expr

    def check_semantic(self, context, errors):
        pass

    def execute(self, context, errors, ans):
        if len(errors) != 0:
            return
        if context.check_var_defined(self.idx):
            errors.append(f'Variable {self.idx} ya definida :(')
        if isinstance(self.expr, ExpressionNode):
            value = self.expr.evaluate(context, errors, ans)
            if not isinstance(value,bool):
                errors.append(f'variable: {self.idx} no puede convertirse a bool')
            else : context.def_var(self.idx, value)
        else:
            context.def_var(self.idx, self.expr)
            
class PatientVarDeclarationNode(DeclarationNode):
    def __init__(self, idx, expr):
        self.idx = idx
        self.expr = expr

    def check_semantic(self, context, errors):
        pass

    def execute(self, context, errors, ans):
        if len(errors) != 0:
            return
        if context.check_var_defined(self.idx):
            errors.append(f'Variable {self.idx} ya definida :(')
        if isinstance(self.expr, ExpressionNode):
            value = self.expr.evaluate(context, errors, ans)
            if not isinstance(value,Patient):
                errors.append(f'variable: {self.idx} no puede convertirse a Patient')
            else : context.def_var(self.idx, value)
        else:
            context.def_var(self.idx, self.expr)


class IfExprNode(DeclarationNode):
    def __init__(self, eva_expr, body):
        self.eva_expr = eva_expr
        self.body = body

    def check_semantic(self, context, errors):
        self.eva_expr.check_semantic(context, errors)

    def execute(self, context, errors, ans):
        if len(errors) != 0:
            return
        result = self.eva_expr.evaluate(context, errors, ans)
        if result:
            for i in self.body:
                i.execute(context, errors, ans)


class IfElseExprNode(DeclarationNode):
    def __init__(self, eva_expr, one_body, two_body):
        self.eva_expr = eva_expr
        self.one_body = one_body
        self.two_body = two_body

    def check_semantic(self, context, errors):
        self.eva_expr.check_semantic(context, errors)

    def execute(self, context, errors, ans):
        if len(errors) != 0:
            return
        result = self.eva_expr.evaluate(context, errors, ans)
        if result:
            for i in self.one_body:
                i.execute(context, errors, ans)
        else:
            for i in self.two_body:
                i.execute(context, errors, ans)


class CallNode(ExpressionNode):
    def __init__(self, idx, args):
        self.idx = idx
        self.args = args

    def check_semantic(self, context, errors):
        if not context.check_func_defined(self.idx, len(self.args)):
            errors.append(f'Función {self.idx} no definida :(')

    def evaluate(self, context, errors, ans):
        if len(errors) != 0:
            return
        func = context.get_local_function_info(self.idx, len(self.args))
        child = context.create_child_context()
        for i, p in enumerate(func.params):
            child.def_var(p, self.args[i].evaluate(context, errors, ans))
        for stat in func.stat_list:
            if isinstance(stat, ReturnNode):
                return stat.expr.evaluate(child, errors, ans)
            stat.execute(child, errors, ans)
        return None


class AtomicNode(ExpressionNode):
    def evaluate(self, context, errors, ans):
        pass


class BinaryNode(ExpressionNode):
    def evaluate(self, context, errors, ans):
        pass


class ConstantNumNode(AtomicNode):
    def __init__(self, value):
        self.value = value

    def check_semantic(self, context, errors):
        pass

    def evaluate(self, context, errors, ans):
        return self.value


class ConstantStrNode(AtomicNode):
    def __init__(self, value):
        self.value = value

    def check_semantic(self, context, errors):
        pass

    def evaluate(self, context, errors, ans):
        return self.value


class ConstantBoolNode(AtomicNode):
    def __init__(self, value):
        self.value = value

    def check_semantic(self, context, errors):
        pass

    def evaluate(self, context, errors, ans):
        return self.value


class VariableNode(AtomicNode):
    def __init__(self, idx):
        self.idx = idx

    def check_semantic(self, context, errors):
        if not context.check_var_defined(self.idx):
            errors.append(f'Variable {self.idx} no definida :(')

    def evaluate(self, context, errors, ans):
        var = context.get_local_variable_info(self.idx)
        if var is None:
            errors.append(f'Variable {self.idx} no definida :(')
            return
        return var


class AndNode(BinaryNode):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def evaluate(self, context, errors, ans):
        if len(errors) != 0:
            return
        lvalue = self.left.evaluate(context, errors, ans)
        rvalue = self.right.evaluate(context, errors, ans)
        if isinstance(lvalue, ExpressionNode):
            lvalue = lvalue.evaluate(context, errors, ans)
        if isinstance(rvalue, ExpressionNode):
            rvalue = rvalue.evaluate(context, errors, ans)
        _type = [int, bool]
        if not _type.__contains__(type(lvalue)) or not _type.__contains__(type(rvalue)):
            errors.append(f'Operación "and" entre un tipo {type(lvalue)} y un tipo {type(rvalue)} no definida :( ')
            return
        return lvalue and rvalue


class OrNode(BinaryNode):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def evaluate(self, context, errors, ans):
        if len(errors) != 0:
            return
        lvalue = self.left.evaluate(context, errors, ans)
        rvalue = self.right.evaluate(context, errors, ans)
        if isinstance(lvalue, ExpressionNode):
            lvalue = lvalue.evaluate(context, errors, ans)
        if isinstance(rvalue, ExpressionNode):
            rvalue = rvalue.evaluate(context, errors, ans)
        _type = [int, bool]
        if not _type.__contains__(type(lvalue)) or not _type.__contains__(type(rvalue)):
            errors.append(f'Operación "or" entre un tipo {type(lvalue)} y un tipo {type(rvalue)} no definida :( ')
            return
        return lvalue or rvalue


class PlusNode(BinaryNode):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def evaluate(self, context, errors, ans):
        if len(errors) != 0:
            return
        lvalue = self.left.evaluate(context, errors, ans)
        rvalue = self.right.evaluate(context, errors, ans)
        if isinstance(lvalue, ExpressionNode):
            lvalue = lvalue.evaluate(context, errors, ans)
        if isinstance(rvalue, ExpressionNode):
            rvalue = rvalue.evaluate(context, errors, ans)
        _type = [int, float]
        if not _type.__contains__(type(lvalue)) or not _type.__contains__(type(rvalue)):
            errors.append(f'Operación "+" entre un tipo {type(lvalue)} y un tipo {type(rvalue)} no definida :( ')
            return
        return lvalue + rvalue


class MinusNode(BinaryNode):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def evaluate(self, context, errors, ans):
        if len(errors) != 0:
            return
        lvalue = self.left.evaluate(context, errors, ans)
        rvalue = self.right.evaluate(context, errors, ans)
        if isinstance(lvalue, ExpressionNode):
            lvalue = lvalue.evaluate(context, errors, ans)
        if isinstance(rvalue, ExpressionNode):
            rvalue = rvalue.evaluate(context, errors, ans)
        _type = [int, float]
        if not _type.__contains__(type(lvalue)) or not _type.__contains__(type(rvalue)):
            errors.append(f'Operación "-" entre un tipo {type(lvalue)} y un tipo {type(rvalue)} no definida :( ')
            return
        return lvalue - rvalue


class StarNode(BinaryNode):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def evaluate(self, context, errors, ans):
        if len(errors) != 0:
            return
        lvalue = self.left.evaluate(context, errors, ans)
        rvalue = self.right.evaluate(context, errors, ans)
        if isinstance(lvalue, ExpressionNode):
            lvalue = lvalue.evaluate(context, errors, ans)
        if isinstance(rvalue, ExpressionNode):
            rvalue = rvalue.evaluate(context, errors, ans)
        _type = [int, float]
        if not _type.__contains__(type(lvalue)) or not _type.__contains__(type(rvalue)):
            errors.append(f'Operación "*" entre un tipo {type(lvalue)} y un tipo {type(rvalue)} no definida :( ')
            return
        return lvalue * rvalue


class DivNode(BinaryNode):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def evaluate(self, context, errors, ans):
        if len(errors) != 0:
            return
        lvalue = self.left.evaluate(context, errors, ans)
        rvalue = self.right.evaluate(context, errors, ans)
        if isinstance(lvalue, ExpressionNode):
            lvalue = lvalue.evaluate(context, errors, ans)
        if isinstance(rvalue, ExpressionNode):
            rvalue = rvalue.evaluate(context, errors, ans)
        _type = [int, float]
        if not _type.__contains__(type(lvalue)) or not _type.__contains__(type(rvalue)):
            errors.append(f'Operación "/" entre un tipo {type(lvalue)} y un tipo {type(rvalue)} no definida :( ')
            return
        return lvalue / rvalue


class LeqNode(ExpressionNode):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def evaluate(self, context, errors, ans):
        if len(errors) != 0:
            return
        lvalue = self.left.evaluate(context, errors, ans)
        rvalue = self.right.evaluate(context, errors, ans)
        if isinstance(lvalue, ExpressionNode):
            lvalue = lvalue.evaluate(context, errors, ans)
        if isinstance(rvalue, ExpressionNode):
            rvalue = rvalue.evaluate(context, errors, ans)
        _type = [int, float]
        if not _type.__contains__(type(lvalue)) or not _type.__contains__(type(rvalue)):
            errors.append(f'Operación "<=" entre un tipo {type(lvalue)} y un tipo {type(rvalue)} no definida :( ')
            return
        return lvalue <= rvalue


class GeqNode(ExpressionNode):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def evaluate(self, context, errors, ans):
        if len(errors) != 0:
            return
        lvalue = self.left.evaluate(context, errors, ans)
        rvalue = self.right.evaluate(context, errors, ans)
        if isinstance(lvalue, ExpressionNode):
            lvalue = lvalue.evaluate(context, errors, ans)
        if isinstance(rvalue, ExpressionNode):
            rvalue = rvalue.evaluate(context, errors, ans)
        _type = [int, float]
        if not _type.__contains__(type(lvalue)) or not _type.__contains__(type(rvalue)):
            errors.append(f'Operación ">=" entre un tipo {type(lvalue)} y un tipo {type(rvalue)} no definida :( ')
            return
        return lvalue >= rvalue


class EqualNode(ExpressionNode):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def evaluate(self, context, errors, ans):
        if len(errors) != 0:
            return
        lvalue = self.left.evaluate(context, errors, ans)
        rvalue = self.right.evaluate(context, errors, ans)
        if isinstance(lvalue, ExpressionNode):
            lvalue = lvalue.evaluate(context, errors, ans)
        if isinstance(rvalue, ExpressionNode):
            rvalue = rvalue.evaluate(context, errors, ans)
        _type = [int, float]
        if not _type.__contains__(type(lvalue)) or not _type.__contains__(type(rvalue)):
            errors.append(f'Operación "==" entre un tipo {type(lvalue)} y un tipo {type(rvalue)} no definida :( ')
            return
        return lvalue == rvalue


class NotNode(ExpressionNode):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def evaluate(self, context, errors, ans):
        if len(errors) != 0:
            return
        lvalue = self.left.evaluate(context, errors, ans)
        rvalue = self.right.evaluate(context, errors, ans)
        if isinstance(lvalue, ExpressionNode):
            lvalue = lvalue.evaluate(context, errors, ans)
        if isinstance(rvalue, ExpressionNode):
            rvalue = rvalue.evaluate(context, errors, ans)
        _type = [int, float]
        if not _type.__contains__(type(lvalue)) or not _type.__contains__(type(rvalue)):
            errors.append(f'Operación "!=" entre un tipo {type(lvalue)} y un tipo {type(rvalue)} no definida :( ')
            return
        return lvalue != rvalue


class LessNode(ExpressionNode):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def evaluate(self, context, errors, ans):
        if len(errors) != 0:
            return
        lvalue = self.left.evaluate(context, errors, ans)
        rvalue = self.right.evaluate(context, errors, ans)
        if isinstance(lvalue, ExpressionNode):
            lvalue = lvalue.evaluate(context, errors, ans)
        if isinstance(rvalue, ExpressionNode):
            rvalue = rvalue.evaluate(context, errors, ans)
        _type = [int, float]
        if not _type.__contains__(type(lvalue)) or not _type.__contains__(type(rvalue)):
            errors.append(f'Operación "<" entre un tipo {type(lvalue)} y un tipo {type(rvalue)} no definida :( ')
            return
        return lvalue < rvalue


class GreaterNode(ExpressionNode):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def evaluate(self, context, errors, ans):
        if len(errors) != 0:
            return
        lvalue = self.left.evaluate(context, errors, ans)
        rvalue = self.right.evaluate(context, errors, ans)
        if isinstance(lvalue, ExpressionNode):
            lvalue = lvalue.evaluate(context, errors, ans)
        if isinstance(rvalue, ExpressionNode):
            rvalue = rvalue.evaluate(context, errors, ans)
        _type = [int, float]
        if not _type.__contains__(type(lvalue)) or not _type.__contains__(type(rvalue)):
            errors.append(f'Operación ">" entre un tipo {type(lvalue)} y un tipo {type(rvalue)} no definida :( ')
            return
        return lvalue > rvalue


class ListExprNode(ExpressionNode):
    def __init__(self, list_expr):
        self.list_expr = list_expr

    def check_semantic(self, context, errors):
        pass

    def evaluate(self, context, errors, ans):
        if len(errors) != 0:
            return
        listx = []
        for i in self.list_expr:
            listx.append(i.evaluate(context, errors, ans))
        return listx


class ListGetNode(ExpressionNode):
    def __init__(self, name, pos):
        self.name = name
        self.pos = pos

    def check_semantic(self, context, errors):
        if not context.check_var_defined(self.name):
            errors.append(f'Lista {self.name} no definida :(')
            return
        pos = self.pos.evaluate(context, errors, None)
        if pos < 0 or pos >= len(context.get_local_variable_info(self.name)):
            errors.append(f'Posición {pos} fuera de rango :(')

    def evaluate(self, context, errors, ans):
        if len(errors) != 0:
            return
        listx = context.get_local_variable_info(self.name)
        pos = self.pos.evaluate(context, errors, ans)
        if len(errors) == 0:
            return listx[pos]
        return None


class PrintNode(DeclarationNode):
    def __init__(self, expr):
        self.expr = expr

    def check_semantic(self, context, errors):
        self.expr.check_semantic(context, errors)

    def execute(self, context, errors, ans):
        if len(errors) != 0:
            return
        result = self.expr.evaluate(context, errors, ans)
        if not len(errors):
            ans.append(result)


class FindNode(ExpressionNode):
    def __init__(self, patient, condition):
        self.patient = patient
        self.condition = condition

    def check_semantic(self, context, errors):
        if not context.check_var_defined(self.patient):
            errors.append(f'Patient {self.patient} no definido :(')

    def evaluate(self, context, errors, ans):
        patient = context.get_local_variable_info(self.patient)
       # condition = self.condition.evaluate(context, errors, ans)
        if len(errors) != 0:
            return
        return Find(patient,self.condition)

class BreastCancerNode(ExpressionNode):
    def __init__(self, patient):
        self.patient = patient

    def check_semantic(self, context, errors):
        if not context.check_var_defined(self.patient):
            errors.append(f'Patient {self.patient} no definido :(')

    def evaluate(self, context, errors, ans):
        patient = context.get_local_variable_info(self.patient)
        if len(errors) != 0:
            return
        return BreastCancer(patient)

class OvarianCancerNode(ExpressionNode):
    def __init__(self, patient):
        self.patient = patient

    def check_semantic(self, context, errors):
        if not context.check_var_defined(self.patient):
            errors.append(f'Patient {self.patient} no definido :(')

    def evaluate(self, context, errors, ans):
        patient = context.get_local_variable_info(self.patient)
        if len(errors) != 0:
            return
        return OvarianCancer(patient)

class PancreaticCancerNode(ExpressionNode):
    def __init__(self, patient):
        self.patient = patient

    def check_semantic(self, context, errors):
        if not context.check_var_defined(self.patient):
            errors.append(f'Patient {self.patient} no definido :(')

    def evaluate(self, context, errors, ans):
        patient = context.get_local_variable_info(self.patient)
        if len(errors) != 0:
            return
        return PancreaticCancer(patient)

class GetNameNode(ExpressionNode):
    def __init__(self, patient):
        self.patient = patient

    def check_semantic(self, context, errors):
        if not context.check_var_defined(self.patient):
            errors.append(f'Patient {self.patient} no definido :(')

    def evaluate(self, context, errors, ans):
        patient = context.get_local_variable_info(self.patient)
        if len(errors) != 0:
            return
        return patient.name
class GetSexNode(ExpressionNode):
    def __init__(self, patient):
        self.patient = patient

    def check_semantic(self, context, errors):
        if not context.check_var_defined(self.patient):
            errors.append(f'Patient {self.patient} no definido :(')

    def evaluate(self, context, errors, ans):
        patient = context.get_local_variable_info(self.patient)
        if len(errors) != 0:
            return
        return patient.sex
class GetAgeNode(ExpressionNode):
    def __init__(self, patient):
        self.patient = patient

    def check_semantic(self, context, errors):
        if not context.check_var_defined(self.patient):
            errors.append(f'Patient {self.patient} no definido :(')

    def evaluate(self, context, errors, ans):
        patient = context.get_local_variable_info(self.patient)
        if len(errors) != 0:
            return
        return patient.age

