import peak.util.assembler as assem

from copy import copy

from options import get_dis_printer

def eval_toplevel(sexps, args):
    dis = get_dis_printer(args)
    c = assem.Code()
    for sexp in sexps:
        eval_sexp(sexp, c)
    if c.stack_size == 0:
        c.LOAD_CONST(None)
    c.RETURN_VALUE()
    dis(c.code())
    locals_dict = copy(locals())
    locals_dict['foo-bar'] = 1
    exec(c.code(), globals(), locals())

def eval_sexp(sexp, c):
    if isinstance(sexp, str):
        if is_string(sexp):
            string(sexp, c)
        else:
            variable(sexp, c)
    elif isinstance(sexp, list):
        func(sexp, c)
    elif isinstance(sexp, (int, float, str)):
        atom(sexp, c)

def func(sexp, c):
    func_name = sexp.pop(0)
    if func_name == 'print':
        for subsexp in sexp:
            eval_sexp(subsexp, c)
            c.PRINT_ITEM()
            c.PRINT_NEWLINE()
    elif func_name in ['+', '-', '*', '/', '%']:
        binary_op(func_name, sexp, c)
    elif func_name == '=':
        assign(sexp, c)
    else:
        c( assem.Call( assem.Global(func_name), sexp))

def binary_op(op, sexp, c):
    op_mapping = {
        '+' : c.BINARY_ADD,
        '-' : c.BINARY_SUBTRACT,
        '/' : c.BINARY_DIVIDE,
        '*' : c.BINARY_MULTIPLY,
        '%' : c.BINARY_MODULO
        }
    lh = sexp.pop(0)
    eval_sexp(lh, c)
    rh = sexp.pop(0)
    eval_sexp(rh, c)
    op_mapping[op]()
    for sub_sexp in sexp:
        eval_sexp(sub_sexp, c)
        op_mapping[op]()

def atom(sexp, c):
    c.LOAD_CONST(sexp)

def string(sexp, c):
    sexp = sexp.strip('"\'').rstrip('"\'')
    atom(sexp, c)

def assign(sexp, c):
    var_name, value = sexp
    eval_sexp(value, c)
    c( assem.LocalAssign(var_name) )

def is_string(sexp):    
    return sexp.startswith('"') and sexp.endswith('"')

def variable(sexp, c):
    c( assem.Local(sexp) )
