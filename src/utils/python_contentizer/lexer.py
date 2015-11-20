#!/usr/bin/env python

import ast


class Lexer(ast.NodeVisitor):
    """Parse a node from a AST and return a tuple of the content.

    The returned tuple is of the form:

        (line_number, node_type, name)

    node_type can be either "Import" or "Call".

    """

    def visit_Import(self, node):
        """Called for "import library" statements."""
        items = []
        for item in node.names:
            items.append((node.lineno, "Import", item.name))
        self.generic_visit(node)
        return items

    def visit_ImportFrom(self, node):
        """Called for "from library import object" statements."""
        self.generic_visit(node)
        return [(node.lineno, "Import", node.module)]

    def visit_Call(self, node):
        """Called for function and method calls."""
        id = None
        # Some nodes have their name in the function object
        try:
            id = node.func.id
        except AttributeError:
            pass
        # Others (those called as methods, or with a library name leading) have
        # the name in the attr block
        try:
            id = node.func.value.id + '.' + node.func.attr
        except AttributeError:
            pass

        self.generic_visit(node)

        if id:
            return [(node.lineno, "Call", id)]


if __name__ == "__main__":
    with open("lexer.py") as f:
        tree = ast.parse(f.read())

    for node in ast.walk(tree):
        ret = Lexer().visit(node)
        if ret:
            print ret
