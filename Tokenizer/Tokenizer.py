from typing import NamedTuple
import re

class Token(NamedTuple):
    type: str
    value: str


def tokenize(code):
    result = [] # Devuelve un array con todos los tokens
    errors = [] # Contiene los errores del tokenizer
    
    tokens = {
        'eof'    : r'eof',               # eof
        'int'    : r'int',               # int    
        'str'    : r'str',               # str    
        'bool'   : r'bool',              # bool
        'Patient': r'Patient',           # Patient
        'if'     : r'if',                # if
        'else'   : r'else',              # else
        'for'    : r'for',               # for
        'func'   : r'func',              # func
        
        'name'            : r'name',     # name the patient  
        'sex'             : r'sex',      # sex the patient
        'age'             : r'age',      #  age the patient
        'add'             : r'add',      #  add the patient
        'remove'          : r'remove',   #  remove the patient
        'len'             : r'len',      #  len the patient
        'Find'            : r'Find',     
        'BreastCancer'    : r'BreastCancer',
        'OvarianCancer'   : r'OvarianCancer',
        'PancreaticCancer': r'PancreaticCancer',
       
        # Comparison operators
        'leq'    : r'<=',                # less than or equal
        'geq'    : r'>=',                # greater than or equal
        'equal'  : r'==',                # equal
        'not'    : r'!=',                # not equal
        'less'   : r'[<]',               # less than
        'greater': r'[>]',               # greater than

        'o_bracket': r'\(',              # (
        'c_bracket': r'\)',              # )
        'o_key'    : r'\{',              # {
        'c_key'    : r'\}',              # }
        
        'comma'    : r',',               # comma
        'semi'     : r';',               # ;
        #'colon': r':',                  # :
        #'quotation':r'"',               # "
        'dot'      : r'\.',              # . 
        
        # Logic operators
        'and'      : r'and',             # and
        'or'       : r'or',              # or
        'return'   : r'return',          # return
        'print'    : r'print',           # print
        #'input'   : r'input',           # input

        'comment'  : r'[\#](\w+)#|[\#](\w+)[ \t]+(\w+)#|'   ,
        'number'   : r'\d+(\.\d*)?',     # Integer or decimal number
        'string'   : r'[\"](\w+)[\"]|[\"](\w+)[ \t]+(\w+)[\"]',
        'true'     : r'True',
        'false'    : r'False',
        'id'       : r'[A-Za-z]+',       # Identifiers
        'assign'   : r'=',               # Assignment operator
        
        # Arithmetic operators
        'plus'     : r'[+]',             # plus
        'minus'    : r'[\-]',            # minus
        'mul'      : r'[*]',             # mul
        'div'      : r'[/]',             # div

        'newline'  : r'\n',              # Line endings
        'skip'     : r'[ \t]+',          # Skip over spaces and tabs
        'salt'     : r'\r',
        'mismatch' : r'.',               # Any other character
        }
    
    
    token_type = list(tokens.items())
    keys = tokens.keys()
    tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_type)
    code += ' eof'
    for mo in re.finditer(tok_regex, code):
        kind = mo.lastgroup
        value = mo.group()
        if kind == 'number':
            value = int(value)
        elif kind == 'true' or kind == 'false':
            value = eval(value)    
        elif kind == 'string':
            value = eval(value)
        elif kind == 'id' and value in keys:
            kind = value
        elif kind == 'newline'or kind == 'comment' or kind == 'skip' or kind =='salt':
            continue
        elif kind == 'mismatch':
            errors.append(f'{value!r} unexpected')
        result.append(Token(kind, value))
    return errors,result



