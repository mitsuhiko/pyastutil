# -*- coding: utf-8 -*-
"""
    astutil.debug
    ~~~~~~~~~~~~~

    Simple debug helpers

    :copyright: (c) Copyright 2011 by Armin Ronacher.
    :license: BSD, see LICENSE for more details.
"""
import sys
from .sexpr import to_sexpr


def debug_print_ast(node, highlight=True):
    """Pretty prints the s-expression of an ast node."""
    from pprint import pformat
    if highlight:
        try:
            from pygments import highlight
            from pygments.formatters import TerminalFormatter
            from pygments.lexers import PythonLexer
        except ImportError:
            highlight = False
    indented = pformat(to_sexpr(node))
    if highlight:
        indented = highlight(indented, formatter=TerminalFormatter(),
                             lexer=PythonLexer()).rstrip()
    print >> sys.stderr, indented
