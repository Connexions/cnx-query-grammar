import os
import argparse
import json
from parsimonious import Grammar
from parsimonious.nodes import NodeVisitor


here = os.path.abspath(os.path.dirname(__file__))
QUERY_PEG = os.path.join(here, 'query.peg')

with open(QUERY_PEG, 'r') as fb:
    grammar = Grammar(fb.read())


class DictFormater(NodeVisitor):
    """Translates a node tree to a dictionary"""

    def visit_query(self, node, visited_children):
        return [x[0] for x in visited_children if x]

    def visit_expression(self, node, visited_children):
        if node.children[0].expr_name == 'field':
            return visited_children[0]
        else:
            # extra node layer in everything else.
            return visited_children[0][0]

    def visit_field(self, node, visited_children):
        """Fields end up as a key value pair"""
        return (visited_children[0], visited_children[2][0][1],)

    def visit_field_name(self, node, visited_children):
        return node.text

    def visit_quoted_term(self, node, visited_children):
        """Quoted terms are text that shouldn't be separated"""
        termtexts = []
        for child in visited_children:
            if child:  # Non-empty child is a list of all terms
                for term in child:
                    termtexts.append(term[0][1])
        return ('text', ' '.join(termtexts))

    def visit_term(self, node, visited_children):
        """terms are standalone text values."""
        return ('text', node.text,)

    def generic_visit(self, node, visited_children):
        return [x for x in visited_children if x]


def main(argv=None):
    """Main command-line utility for acquiring a query's parsed form."""
    arg_parser = argparse.ArgumentParser("parse query to json")
    arg_parser.add_argument('query', nargs='+',
                            help="the query...")

    args = arg_parser.parse_args(argv)
    query = ' '.join(args.query)

    node_tree = grammar.parse(query)
    print(node_tree)

    parsed_query = DictFormater().visit(node_tree)
    print(json.dumps(parsed_query))

    return 0


if __name__ == '__main__':
    main()
