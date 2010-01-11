import argparse

from scion.parse import get_syntax_tree
from scion.codegen import eval_toplevel

parser = argparse.ArgumentParser(description='A scheme-like language that uses JSON instead of S-Expressions')
parser.add_argument('infile', type=str)
parser.add_argument('-d', '--dis', action='store_true', default=False,
                    help='Print the disassembly of the generated code.')

def main():
    args = parser.parse_args()
    ast = get_syntax_tree(args.infile)
    eval_toplevel(ast, args)
    
