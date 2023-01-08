from Parser.Grammar import Grammar
from AST.Construction import *
from Parser.Parser import LR1Parser
from Tokenizer.Tokenizer import tokenize
from AST.Nodes import *
import os 
# Inicializa la gramatica
g = Grammar()

# Non Terminals

program = g.non_terminal('<program>', start_symbol=True)  
expr, term, factor, atom = g.non_terminals('<expr> <term> <factor> <atom>') 
func_call, expr_list = g.non_terminals('<func-call> <expr-list>')  # Llamada de funciones y lista de expresiones
stat_list, stat = g.non_terminals('<stat_list> <stat>')            # Ordenes y listas de ordenes
if_decl, if_else_decl, for_decl = g.non_terminals('<if-decl> <if-else-decl> <for_decl>')  # Declaraciones 

int_var,str_var,bool_var,patient_var, def_func, print_stat, arg_list, def_return = \
    g.non_terminals('<int-var> <str-var> <patient-var> <bool-var> <def-func> <print-stat> <arg-list> <def-return>')          # Definiciones
patient_expr, list_expr = g.non_terminals('<patient-expr> <list-expr>')

def_name,def_age,def_sex = g.non_terminals('<def_name> <def_age> <def_sex>')

def_attr_sex, def_attr_age,def_attr_name, def_attr_add, def_attr_len,def_attr_remove \
    = g.non_terminals('<def_attr_sex>  <def_attr_age> <def_attr_name> <def_attr_add> <def_attr_len> <def_attr_remove>')

def_find, def_breast_cancer,def_ovarian_cancer,def_pancreatic_cancer \
    = g.non_terminals('<def_find> <def_breast_cancer> <def_ovarian_cancer> <def_pancreatic_cancer>')

# Terminals
idx, num, stringx, ifx, elsex, forx, intx, strx, boolx, funcx, printx, returnx \
    = g.terminals('id number string if else for int str bool func print return')
    
patient, name, sex, age, addx, removex, lenx, find, breast_cancer, ovarian_cancer, pancreatic_cancer \
    = g.terminals('Patient name sex age add remove len Find BreastCancer OvarianCancer PancreaticCancer')    

dot, semi, comma, colon, okey, ckey, o_bracket, c_bracket \
    = g.terminals('dot semi comma colon o_key c_key o_bracket c_bracket')
equal, plus, minus, star, div, andx, orx, true, false\
    = g.terminals('assign plus minus mul div and or true false')
leq, geq, equalx, notx, less, greater = g.terminals('leq geq equal not less greater')

# Productions
program %= stat_list,          lambda h, s: ProgramNode(s[1])
   # Lista de ordenes
stat_list %= stat,             lambda h, s: [s[1]]
stat_list %= stat + stat_list, lambda h, s: [s[1]] + s[2]
    # Ordenes
stat %= str_var + semi,             lambda h, s: s[1]
stat %= int_var + semi,             lambda h, s: s[1]
stat %= bool_var+ semi,             lambda h, s: s[1]
stat %= patient_var + semi,         lambda h, s: s[1]    
stat %= def_func,                   lambda h, s: s[1]
stat %= print_stat + semi,          lambda h, s: s[1]
stat %= if_decl,                    lambda h, s: s[1]
stat %= if_else_decl,               lambda h, s: s[1]
stat %= def_return + semi,          lambda h, s: s[1]
stat %= for_decl,                   lambda h, s: s[1]
stat %= def_name + semi,            lambda h, s: s[1]
stat %= def_age  + semi,            lambda h, s: s[1]
stat %= def_sex  + semi,            lambda h, s: s[1]
stat %= def_attr_add + semi,        lambda h, s: s[1]
stat %= def_attr_remove + semi,     lambda h, s: s[1]
stat %= def_attr_len + semi,        lambda h, s: s[1]
stat %= def_attr_name + semi,       lambda h, s: s[1]
stat %= def_attr_age + semi,        lambda h, s: s[1]
stat %= def_attr_sex + semi,        lambda h, s: s[1]
stat %= def_find     + semi,        lambda h, s: s[1]
stat %= def_breast_cancer+ semi,    lambda h, s: s[1] 
stat %= def_ovarian_cancer+ semi,   lambda h, s: s[1]
stat %= def_pancreatic_cancer+ semi,lambda h, s: s[1]
stat %= patient_expr,               lambda h, s: s[1]
   
   # Declaraciones 
if_decl %= ifx + o_bracket + expr + c_bracket + okey + stat_list + ckey, lambda h, s: IfExprNode(s[3], s[6])
if_else_decl %= ifx + o_bracket + expr + c_bracket + okey + stat_list + ckey + elsex + okey + stat_list + ckey, \
                lambda h, s: IfElseExprNode(s[3], s[6], s[10])
for_decl %= forx + o_bracket + idx + equal + num + semi + expr + semi + idx + plus + plus + c_bracket + okey + stat_list + ckey, \
            lambda h, s: ForNode(s[3], s[5], s[7], s[9], s[10], s[11], s[14])
for_decl %= forx + o_bracket + idx + equal + num + semi + expr + semi + idx + minus + minus + c_bracket + okey + stat_list + ckey, \
            lambda h, s: ForNode(s[3], s[5], s[7], s[9], s[10], s[11], s[14])

    # Definiciones
def_return %= returnx + expr, lambda h, s: ReturnNode(s[2])
print_stat %= printx + expr, lambda h, s: PrintNode(s[2])

int_var     %= intx  + idx + equal + expr, lambda h, s: IntVarDeclarationNode(s[2], s[4])
bool_var    %= boolx + idx + equal + expr, lambda h, s: BoolVarDeclarationNode(s[2], s[4])
str_var     %= strx  + idx + equal + expr, lambda h, s: StrVarDeclarationNode(s[2], s[4])
patient_var %= patient + idx + equal + patient_expr, lambda h, s: PatientVarDeclarationNode(s[2], s[4])
list_expr   %= o_bracket + expr_list + c_bracket,lambda h, s: ListExprNode(s[2])

def_name %= idx + dot + name, lambda h,s: GetNameNode(s[1])
def_age  %= idx + dot + age,  lambda h,s: GetAgeNode(s[1])
def_sex  %= idx + dot + sex,  lambda h,s: GetSexNode(s[1])
def_attr_name   %= idx + dot + name + equal + expr, lambda h,s: NameNode(s[1], s[5])
def_attr_age    %= idx + dot + age  + equal + expr, lambda h,s: AgeNode(s[1], s[5])
def_attr_sex    %= idx + dot + sex  + equal + expr, lambda h,s: SexNode(s[1], s[5])
def_attr_add    %= idx + dot + addx + o_bracket  + expr + c_bracket, lambda h,s: AddNode(s[1], s[5])
def_attr_len    %= idx + dot + lenx + o_bracket  + c_bracket, lambda h,s: LenNode(s[1])
def_attr_remove %= idx + dot + removex + o_bracket + expr + c_bracket, lambda h,s: RemoveNode(s[1], s[5])

patient_expr          %= patient + o_bracket + stringx + comma + stringx +comma+ num + c_bracket, lambda h,s: PatientNode(s[3],s[5],s[7])  
def_find              %= find     + o_bracket  + idx   + comma + stringx + c_bracket, lambda h,s: FindNode(s[3], s[5])
def_breast_cancer     %= breast_cancer    + o_bracket  + idx + c_bracket, lambda h,s: BreastCancerNode(s[3])
def_ovarian_cancer    %= ovarian_cancer   + o_bracket  + idx + c_bracket, lambda h,s: OvarianCancerNode(s[3])
def_pancreatic_cancer %= pancreatic_cancer+ o_bracket  + idx + c_bracket, lambda h,s: PancreaticCancerNode(s[3])

def_func %= funcx + idx + o_bracket + arg_list + c_bracket + okey + stat_list + ckey, \
            lambda h, s: FuncDeclarationNode(s[2], s[4], s[7])

arg_list %= idx, lambda h, s: [s[1]]
arg_list %= idx + comma + arg_list, lambda h, s: [s[1]] + s[3]

expr %= idx + o_bracket + expr + c_bracket, lambda h, s: ListGetNode(s[1], s[3])

expr %= expr + plus  + term,   lambda h, s: PlusNode(s[1], s[3])
expr %= expr + minus + term,   lambda h, s: MinusNode(s[1], s[3])
term %= term + star  + factor, lambda h, s: StarNode(s[1], s[3])
term %= term + div   + factor, lambda h, s: DivNode(s[1], s[3])

expr %= expr + leq     + term, lambda h, s: LeqNode(s[1], s[3])
expr %= expr + geq     + term, lambda h, s: GeqNode(s[1], s[3])
expr %= expr + equalx  + term, lambda h, s: EqualNode(s[1], s[3])
expr %= expr + notx    + term, lambda h, s: NotNode(s[1], s[3])
expr %= expr + less    + term, lambda h, s: LessNode(s[1], s[3])
expr %= expr + greater + term, lambda h, s: GreaterNode(s[1], s[3])

expr %= expr + andx + term, lambda h, s: AndNode(s[1], s[3])
expr %= expr + orx  + term, lambda h, s: OrNode(s[1], s[3])

expr %= list_expr,             lambda h, s: s[1], None
expr %= def_name,              lambda h, s: s[1], None
expr %= def_sex,               lambda h, s: s[1], None
expr %= def_age,               lambda h, s: s[1], None
expr %= def_attr_len,          lambda h, s: s[1], None
expr %= def_breast_cancer,     lambda h, s: s[1], None
expr %= def_ovarian_cancer,    lambda h, s: s[1], None
expr %= def_pancreatic_cancer, lambda h, s: s[1], None
expr %= def_find,              lambda h, s: s[1], None
#expr %= def_attr_add,          lambda h, s: s[1], None

expr   %= term,   lambda h, s: s[1], None
term   %= factor, lambda h, s: s[1]
factor %= atom,   lambda h, s: s[1]
factor %= o_bracket + expr + c_bracket, lambda h, s: s[2]


atom %= stringx,  lambda h, s: ConstantStrNode(s[1])
atom %= num,      lambda h, s: ConstantNumNode(s[1])
atom %= true,     lambda h, s: ConstantBoolNode(s[1])
atom %= false,    lambda h, s: ConstantBoolNode(s[1])
atom %= idx,      lambda h, s: VariableNode(s[1])
atom %= func_call,lambda h, s: s[1]

func_call %= idx + o_bracket + expr_list + c_bracket, lambda h, s: CallNode(s[1], s[3])

expr_list %= expr, lambda h, s: [s[1]]
expr_list %= expr + comma + expr_list, lambda h, s: [s[1]] + s[3]


parser = LR1Parser(g)

def execute(code):
    if code=='':
        return
    errors_tokenizer, tokens = tokenize(code)
    errors_output = ""
    ans = ""
    for i in range(len(errors_tokenizer)):
        errors_output+=errors_tokenizer[i]
        if i < len(errors_tokenizer)-1:
            errors_output+="\n"
            
    errors, parse, operations = parser([i.type for i in tokens], ope=True)
    errors_pars = errors_parser(errors, tokens)
    for i in range(len(errors_pars)):
        errors_output+=errors_pars[i]
        if i < len(errors_pars)-1:
            errors_output+="\n"

    if errors_tokenizer==[] and errors_pars==[]:
        ast = construction_ast(parse, operations, tokens)
        errors_ast, answer = ast.run()

        for i in range(len(errors_ast)):
            errors_output+=errors_ast[i]
            if i < len(errors_ast)-1:
                errors_output+="\n"


        for a in answer:
            ans+=str(a) + "\n"

    res =  str(errors_output) + str(ans)

    return res    
    
def errors_parser(errors, tokens):
    err = []
    for i in errors:
        value = ''
        for t in tokens:
            if t.type == i:
                value = t.value
                break
        if i == 'eof':
            err.append(f'{i} -> fin de cadena no válida')
        err.append(f'{i} -> {value} no ha sido bien definido :(')
    return err


def Read():
    archive = open("code.txt")
    text = ''
    line = archive.readline()
    while(line):
        text+=line
        line = archive.readline() 
    archive.close()
    return text


# Declaracion de variables y uso de sus propiedades
b = ''' Patient p = Patient ("Roberto","m",45);
p.name  = "Petra";
p.sex = "f";
print p.sex;
p.age = 30;
print p.age;
p.add("secrecion");
print Find(p,"secrecion");
print BreastCancer(p); 
print OvarianCancer(p);
print PancreaticCancer(p);
p.remove("secrecion");
print Find(p,"secrecion");
print p.len();
'''
a ='''
Patient p = Patient ("Roberto","m",45);
p.add("dolor"); 
func Cabeza(p)
{
   if Find(p,"dolor"){
       return True;
   }
} 
print Cabeza(p);
'''

fac = '''
func fac(n){
    if(n <= 1){
        int x = 1;
    }
    else{
        int x = n*fac(n-1);
    }    
    return x;
}
print fac(5);
'''


p = '''
func f (a,b){ int c = a+b; return c; }
print f( 5, 7);

'''
#
print(execute(a))