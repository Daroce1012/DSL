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
            if len(errors)>0: return errors,ans
            if isinstance(node, DeclarationNode) and (isinstance(node,IfElseExprNode) or isinstance(node,IfExprNode) or isinstance(node,ReturnNode) or isinstance(node,ForNode)  ):
                errors.append(f' La instruccion no puede ser declarada fuera del cuerpo de una funcion \n ');
                return errors,ans
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




class GetNode(ExpressionNode):
    def __init__(self, var,attr):
        self.var = var
        self.attr = attr
        
    def check_semantic(self, context, errors):
        if not context.check_var_defined(self.var):  # Si la variable no esta definida
            errors.append(f'La variable {self.var} no esta definida ')
        elif not hasattr(context.get_local_variable_info(self.var),self.attr):      #Verifica si la variable contiene ese atributo o propiedad
            errors.append(f' La variable {self.var} no contiene el atributo {self.attr} ') # Si la variable no contiene esa propiedad

    def evaluate(self, context, errors, ans):
        var = context.get_local_variable_info(self.var)
        if len(errors) != 0:
            return
        return getattr(var,self.attr)

    
class SetNode(DeclarationNode):
    def __init__(self, var, attr,exp):
        self.var = var
        self.attr = attr
        self.exp = exp

    def check_semantic(self, context, errors):
        if not context.check_var_defined(self.var):  # Si la variable no esta definida
            errors.append(f'La variable {self.var} no esta definida ')    
        elif not hasattr(context.get_local_variable_info(self.var),self.attr):
            errors.append(f' La variable {self.var} no contiene el atributo {self.attr} ') # Si la variable no contiene esa propiedad

    def execute(self, context, errors, ans):
        if len(errors) != 0:
            return
        var = context.get_local_variable_info(self.var)
        element = self.exp.evaluate(context, errors, ans)
        setattr(var,self.attr,element)


class AddRemoveNode(DeclarationNode):
    def __init__(self, name_patient,func, element):
        self.name_patient = name_patient
        self.element = element
        self.func  = func

    def check_semantic(self, context, errors):
        if not context.check_var_defined(self.name_patient):
            errors.append(f'Patient {self.name_patient} no definida ')
        if self.func != "add" and self.func != "remove":
            errors.append(f'Patient {self.name_patient} no contiene a {self.func} ')  
        
    def execute(self, context, errors, ans):
        if len(errors) != 0:
            return
        patient = context.get_local_variable_info(self.name_patient)
        element = self.element.evaluate(context, errors, ans)
        if self.func == "remove":
            if patient.len > 0:patient.remove(element)
            else: errors.append(f'Patient {patient.name} no tiene sintomas que eliminar')
        else: patient.add(element)     
        

class FuncDeclarationNode(DeclarationNode):
    def __init__(self, idx, params, return_type, stat_list):
        self.idx = idx
        self.params = params       # paramas es una lista de listas que contiene en 0 el nombre y en 1 el tipo
        self.stat_list = stat_list # body
        self.type = return_type    # tipo de retorno de la funcion

    def check_semantic(self, context, errors):
        if context.check_func_defined(self.idx, len(self.params)):
            errors.append(f'Función {self.idx} ya declarada ')
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
        value = self.expr.evaluate(context, errors, ans)
        if not len(errors):
            context.return_local_func.append(value)
        pass
        


class AttrDeclarationNode(DeclarationNode):
    def __init__(self, idx):
        self.id = idx

#Arreglar este nodo
class VarDeclarationNode(DeclarationNode):
    def __init__(self,type ,idx, expr):
        self.idx = idx
        self.expr = expr
        self.type = type

    def check_semantic(self, context, errors):
        if context.check_var_defined(self.idx):
            errors.append(f'Variable {self.idx} ya definida ')
        # Falta verificar el tipado

    def execute(self, context, errors, ans):
        if len(errors) != 0:
            return
        if isinstance(self.expr, ExpressionNode):
            value = self.expr.evaluate(context, errors, ans)
            context.def_var(self.idx, value,self.type)
        
        else:
            context.def_var(self.idx, self.expr,self.type)

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

class RedefVarDeclarationNode(DeclarationNode):
    def __init__(self, idx, expr):
        self.idx = idx
        self.expr = expr

    def check_semantic(self, context, errors):
        pass

    def execute(self, context, errors, ans):
        if len(errors) != 0:
            return
        if context.check_var_defined(self.idx):
            var = context.get_local_variable_info(self.idx)
            if isinstance(self.expr, ExpressionNode):
                value = self.expr.evaluate(context, errors, ans)
                if type(var) is not type(value):
                    errors.append(f'variable: {self.idx} no puede convertirse')
                else : context.redef_var(self.idx, value)
        else:
            errors.append(f'Variable {self.idx} no ha sido definida ')



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
            errors.append(f'Función {self.idx} no definida ')
    
    def execute(self, context, errors, ans): # Si se llama a una funcion como orden o declaracion entonces no hace nada 
        pass
    
    def evaluate(self, context, errors, ans):
        if len(errors) != 0:
            return
        func = context.get_function_info(self.idx, len(self.args))
        child = context.create_child_context() # Context de la funcion llamada
        for i, p in enumerate(func.params):
            child.def_var(p[0], self.args[i].evaluate(context, errors, ans),p[1]) #Se crean variables para guardar los parametros de entrada
        for stat in func.stat_list:
            stat.execute(child, errors, ans)
            returns = child.return_local_func
            if len(returns) > 0: return returns[0]
            
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
            errors.append(f'Variable {self.idx} no definida ')

    def evaluate(self, context, errors, ans):
        var = context.get_local_variable_info(self.idx)
        if var is None:
            errors.append(f'Variable {self.idx} no definida ')
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
            errors.append(f'Operación "and" entre un tipo {type(lvalue)} y un tipo {type(rvalue)} no definida  ')
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
            errors.append(f'Operación "or" entre un tipo {type(lvalue)} y un tipo {type(rvalue)} no definida  ')
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
            errors.append(f'Operación "+" entre un tipo {type(lvalue)} y un tipo {type(rvalue)} no definida  ')
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
            errors.append(f'Operación "-" entre un tipo {type(lvalue)} y un tipo {type(rvalue)} no definida  ')
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
            errors.append(f'Operación "*" entre un tipo {type(lvalue)} y un tipo {type(rvalue)} no definida  ')
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
            errors.append(f'Operación "/" entre un tipo {type(lvalue)} y un tipo {type(rvalue)} no definida  ')
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
            errors.append(f'Operación "<=" entre un tipo {type(lvalue)} y un tipo {type(rvalue)} no definida  ')
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
            errors.append(f'Operación ">=" entre un tipo {type(lvalue)} y un tipo {type(rvalue)} no definida  ')
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
            errors.append(f'Operación "==" entre un tipo {type(lvalue)} y un tipo {type(rvalue)} no definida  ')
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
            errors.append(f'Operación "!=" entre un tipo {type(lvalue)} y un tipo {type(rvalue)} no definida  ')
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
            errors.append(f'Operación "<" entre un tipo {type(lvalue)} y un tipo {type(rvalue)} no definida  ')
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
            errors.append(f'Operación ">" entre un tipo {type(lvalue)} y un tipo {type(rvalue)} no definida  ')
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
            errors.append(f'Patient {self.patient} no definido ')

    def evaluate(self, context, errors, ans):
        patient = context.get_local_variable_info(self.patient)
       # condition = self.condition.evaluate(context, errors, ans)
        if len(errors) != 0:
            return
        return Find(patient,self.condition)

class CancerNode(ExpressionNode):
    def __init__(self,cancer ,patient):
        self.patient = patient
        self.cancer = cancer

    def check_semantic(self, context, errors):
        if not context.check_var_defined(self.patient):
            errors.append(f'Patient {self.patient} no definido ')
        if self.cancer != "BreastCancer" and self.cancer != "OvarianCancer" and self.cancer != "PancreaticCancer":
            errors.append(f'{self.cancer} no existe')  
      
    def evaluate(self, context, errors, ans):
        patient = context.get_local_variable_info(self.patient)
        if len(errors) != 0:
            return
        if self.cancer =="BreastCancer": 
            return BreastCancer(patient)
        elif self.cancer =="OvarianCancer":
            return OvarianCancer(patient)
        else: return PancreaticCancer(patient) 

