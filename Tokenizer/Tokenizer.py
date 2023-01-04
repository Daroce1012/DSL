from typing import NamedTuple
import re


class Token(NamedTuple):
    type: str
    value: str


def tokenize(code):
    ret = []
    
    keywords = {'int','str','print','input', 'if', 'else', 'for','func' ,'patient', 'Simulate',
                'return', '<=', '>=', '==', '!=', '<', '>', 'and', 'or','Add','Len','Find'}
    
    token_specification = [
        ('eof', r'eof'),               # eof
        ('int', r'int'),               # int    
        ('str', r'str'),               # str    
        ('patient', r'patient'),       # Patient
        ('if',  r'if'),                # if
        ('else', r'else'),             # else
        ('for', r'for'),               # for
        ('func',r'func'),              # func
       
        # Comparison operators
        ('leq', r'<='),                # less than or equal
        ('geq', r'>='),                # greater than or equal
        ('equal', r'=='),              # equal
        ('not', r'!='),                # not equal
        ('less', r'[<]'),              # less than
        ('greater', r'[>]'),           # greater than

        ('o_bracket', r'\('),          # (
        ('c_bracket', r'\)'),          # )
        ('o_curlybrackets',r'\{'),     # {
        ('c_curlybrackets',r'\}'),     # }
        
        ('comma', r','),               # comma
        ('semi', r';'),                # ;
       #('colon', r':'),               # colon
       #('quotation',r'"'),            # quotation 

        # Logic operators
        ('and', r'and'),               # and
        ('or', r'or'),                 # or

        ('print', r'print'),           # print
        ('input', r'input'),           # input

        ('number', r'\d+(\.\d*)?'),    # Integer or decimal number
        ('id', r'[A-Za-z]+'),          # Identifiers
        ('assign', r'='),              # Assignment operator
        
        
        # Arithmetic operators
        ('plus', r'[+]'),              # plus
        ('minus', r'[\-]'),            # minus
        ('mul', r'[*]'),               # mul
        ('div', r'[/]'),               # div

        ('newline',  r'\n'),           # Line endings
        ('skip',     r'[ \t]+'),       # Skip over spaces and tabs
        ('mismatch', r'.'),            # Any other character
    ]
    tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
    code += ' eof'
    for mo in re.finditer(tok_regex, code):
        kind = mo.lastgroup
        value = mo.group()
        if kind == 'number':
            value = int(value)
        elif kind == 'id' and value in keywords:
            kind = value
        elif kind == 'newline':
            continue
        elif kind == 'skip':
            continue
        elif kind == 'mismatch':
            raise RuntimeError(f'{value!r} unexpected')
        ret.append(Token(kind, value))
    return ret


# statements = '''
#     If (5 >= 6 )
#     {
#         str total = 4 ;
#     }
        
# '''

#print(tokenize(statements))
