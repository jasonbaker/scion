from copy import copy
from dis import dis

import peak.util.assembler as assem

from scion.options import get_dis_printer
from scion.parse import list_sexp

dis = None

def eval_toplevel(sexps, args):
    """
    Evaluate the code from an AST.
    """
    global dis
    dis = get_dis_printer(args)
    c = assem.Code()
    for sexp in sexps:
        eval_sexp(sexp, c)
    return_val(c)

    dis(c.code(), 'Toplevel function:')
    locals_dict = copy(locals())
    locals_dict['foo-bar'] = 1
    exec(c.code(), globals(), locals())

def eval_sexp(sexp, c):
    """
    Recursively evaluate an s-expression.
    """
    if isinstance(sexp, str):
        if is_string(sexp):
            string(sexp, c)
        else:
            variable(sexp, c)
    elif isinstance(sexp, list):
        funcall(sexp, c)
    elif isinstance(sexp, (int, float, str)):
        atom(sexp, c)

def funcall(sexp, c):
    """
    Evaluate a function call.
    """
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
    elif func_name == 'if':
        if_stmt(sexp, c)
    elif func_name == 'def':
        def_stmt(sexp, c)
    else:
        c( assem.Call( assem.Local(func_name), sexp))

def binary_op(op, sexp, c):
    """
    Evaluate a binary operator.
    """
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
    """
    Evaluate an atomic s-expression.
    """
    c.LOAD_CONST(sexp)

def string(sexp, c):
    """
    Evaluate a string.
    """
    sexp = sexp.strip('"\'').rstrip('"\'')
    atom(sexp, c)

def assign(sexp, c):
    """
    Handle the = form.
    """
    var_name, value = sexp
    eval_sexp(value, c)
    c( assem.LocalAssign(var_name) )

def is_string(sexp):
    """
    Determine whether this s-expression is a string or an identifier.
    """
    return sexp.startswith('"') and sexp.endswith('"')

def variable(sexp, c):
    """
    Handle a variable lookup.
    """
    c( assem.Local(sexp) )

def if_stmt(sexp, c):
    """
    Handle an if statement.
    """
    skip = assem.Label()
    eval_sexp(sexp[0], c)
    forward = c.JUMP_IF_FALSE()
    c.POP_TOP()
    eval_sexp(sexp[1], c)
    c( skip.JUMP_FORWARD )
    forward()
    c.POP_TOP()
    eval_sexp(sexp[2], c)
    c( skip.JUMP_FORWARD )
    c( skip )

def def_stmt(sexp, c):
    """
    Handle a function definition.
    """
    sub_block = c.nested()
    name = sexp[0]
    sub_block.co_name = name
    args = sexp[1]
    sub_block.co_argcount=len(args)
    sub_block.co_varnames = args
    # Unpack the code out of the list
    sub_block_code, = sexp[2:]
    eval_sexp(sub_block_code, sub_block)
    return_val(sub_block)
    dis(sub_block.code(), 'Function %s:' % name)
    print
    c.LOAD_CONST(sub_block.code())
    c.MAKE_FUNCTION(0)
    c( assem.LocalAssign(name) )

def return_val(c):
    """
    Return a value from code c.  This will return None if there
    is nothing on the return stack.  If there is more than one item
    on the return stack, pop it down to one.

    TODO:  Verify that this is the correct behavior if there is more
    than one item on the stack.
    """
    if not c.stack_size:
        c.LOAD_CONST(None)
    elif c.stack_size > 1:
        for i in xrange(c.stack_size):
            c.POP_TOP()
    c.RETURN_VALUE()
