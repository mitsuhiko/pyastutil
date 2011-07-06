# -*- coding: utf-8 -*-
"""
    astutil.sexpr
    ~~~~~~~~~~~~~

    Conversion from and to s-expressions.

    :copyright: (c) Copyright 2011 by Armin Ronacher.
    :license: BSD, see LICENSE for more details.
"""
import ast
from .mapping import lookup_node


def to_sexpr(node):
    """Converts an AST into something that looks like sexpressions.  It's
    returning both lists and tuples to make it possible to reverse this
    without having to know what nodes expect.
    """
    if isinstance(node, list):
        return [to_sexpr(x) for x in node]
    if not isinstance(node, ast.AST):
        return ':', node
    rv = []
    rv.append(node.__class__.__name__)
    for field, value in ast.iter_fields(node):
        rv.append((field, to_sexpr(value)))
    if len(rv) == 1:
        return rv[0]
    return tuple(rv)


def from_sexpr(sexpr):
    """Reverse of :func:`to_sexpr`"""
    if isinstance(sexpr, list):
        return [from_sexpr(x) for x in sexpr]
    if not isinstance(sexpr, tuple):
        sexpr = (sexpr,)
    sexpriter = iter(sexpr)
    name = sexpriter.next()
    if name == ':':
        return sexpriter.next()
    if name.startswith('_') or not hasattr(ast, name):
        cls = lookup_node(str(name))
    rv = cls()
    for field, val in sexpriter:
        setattr(rv, field, from_sexpr(val))
    return rv
