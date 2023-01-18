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
func_call, expr_list, param = g.non_terminals('<func-call> <expr-list> <param>')  # Llamada de funciones y lista de expresiones
stat_list, stat = g.non_terminals('<stat_list> <stat>')            # Ordenes y listas de ordenes
if_decl, if_else_decl, for_decl = g.non_terminals('<if-decl> <if-else-decl> <for_decl>')  # Declaraciones 

redef_var, def_var, def_func, print_stat, arg_list, def_return = \
    g.non_terminals('<redef_var> <def_var> <def-func> <print-stat> <arg-list> <def-return>')          # Definiciones
patient_expr, list_expr = g.non_terminals('<patient-expr> <list-expr>')
def_name,def_age,def_sex = g.non_terminals('<def_name> <def_age> <def_sex>')
#def_attr_sex, def_attr_age,def_attr_name, def_attr_add, def_attr_len,def_attr_remove \
get_attr, set_attr, def_add_remove = g.non_terminals('<get_attr>  <set_attr> <def_add_remove>')
def_cancer, def_find = g.non_terminals('<def_cancer> <def_find>')

# Terminals
idx, num, stringx, patient, find ,ifx, elsex, forx, funcx, printx, returnx \
    = g.terminals('id number string Patient Find if else for func print return')
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
stat %= redef_var+semi,             lambda h, s: s[1]    
stat %= def_var + semi,             lambda h, s: s[1]
stat %= def_func,                   lambda h, s: s[1]
stat %= func_call + semi,           lambda h, s: s[1]
stat %= print_stat + semi,          lambda h, s: s[1]
stat %= if_decl,                    lambda h, s: s[1]
stat %= if_else_decl,               lambda h, s: s[1]
stat %= def_return + semi,          lambda h, s: s[1]
stat %= for_decl,                   lambda h, s: s[1]
stat %= get_attr + semi,            lambda h, s: s[1]
stat %= set_attr + semi,            lambda h, s: s[1]
stat %= def_add_remove+semi,        lambda h, s: s[1]
stat %= def_find     + semi,        lambda h, s: s[1]
stat %= def_cancer+ semi,           lambda h, s: s[1] 
   
   # Declaraciones 
if_decl %= ifx + o_bracket + expr + c_bracket + okey + stat_list + ckey, lambda h, s: IfExprNode(s[3], s[6])
if_else_decl %= ifx + o_bracket + expr + c_bracket + okey + stat_list + ckey + elsex + okey + stat_list + ckey, \
                lambda h, s: IfElseExprNode(s[3], s[6], s[10])
for_decl %= forx + o_bracket + idx + equal + num + semi + expr + semi + idx + plus + plus + c_bracket + okey + stat_list + ckey, \
            lambda h, s: ForNode(s[3], s[5], s[7], s[9], s[10], s[11], s[14])
for_decl %= forx + o_bracket + idx + equal + num + semi + expr + semi + idx + minus + minus + c_bracket + okey + stat_list + ckey, \
            lambda h, s: ForNode(s[3], s[5], s[7], s[9], s[10], s[11], s[14])

    # Definiciones
def_return  %= returnx + expr, lambda h, s: ReturnNode(s[2])
print_stat  %= printx + expr, lambda h, s: PrintNode(s[2])

redef_var   %= idx + equal + expr,         lambda h, s: RedefVarDeclarationNode(s[1], s[3])
def_var     %= idx  + idx + equal + expr,  lambda h, s: VarDeclarationNode(s[1],s[2], s[4])

get_attr %= idx + dot + idx, lambda h,s: GetNode(s[1],s[3])
set_attr %= idx + dot + idx + equal + expr, lambda h,s: SetNode(s[1], s[3],s[5])
def_add_remove %= idx + dot + idx + o_bracket + expr + c_bracket, lambda h,s: AddRemoveNode(s[1],s[3],s[5])

patient_expr  %= patient + o_bracket + stringx + comma + stringx +comma+ num + c_bracket, lambda h,s: PatientNode(s[3],s[5],s[7])  
def_find      %= find     + o_bracket  + idx   + comma + stringx + c_bracket, lambda h,s: FindNode(s[3], s[5])
def_cancer    %= idx + o_bracket  + idx + c_bracket, lambda h,s: CancerNode(s[1],s[3])


# def_func %= idx+funcx + idx + o_bracket + arg_list + c_bracket + okey + stat_list + ckey, \
#             lambda h, s: FuncDeclarationNode(s[1],s[3], s[5], s[8])
# arg_list %= idx, lambda h, s: [s[1]]
# arg_list %= idx + comma + arg_list, lambda h, s: [s[1]] + s[3]

func_call %= idx + o_bracket + expr_list + c_bracket, lambda h, s: CallNode(s[1], s[3])

def_func %= funcx + idx + o_bracket + arg_list + c_bracket + colon + idx + okey + stat_list + ckey, lambda h,s: FuncDeclarationNode(s[2],s[4],s[7],s[9])

arg_list %= param, lambda h,s: [ s[1] ]
arg_list %= param + comma + arg_list, lambda h,s: [ s[1] ] + s[3]

param %= idx + colon + idx, lambda h,s: [s[1],s[3]]

expr_list %= expr, lambda h, s: [s[1]]
expr_list %= expr + comma + expr_list, lambda h, s: [s[1]] + s[3]

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

expr %= patient_expr,          lambda h, s: s[1], None
expr %= list_expr,             lambda h, s: s[1], None
expr %= get_attr,              lambda h, s: s[1], None
expr %= def_cancer,            lambda h, s: s[1], None
expr %= def_find,              lambda h, s: s[1], None

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
        err.append(f'{i} -> {value} no ha sido bien definido')
    return err

d ='''
func f(n:int):int
{
 return 0;
}
print f(4);
'''
#print(execute(d))
