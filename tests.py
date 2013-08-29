# -*- coding: utf-8 -*-
import os
import unittest
from parsimonious import Grammar
from parsimonious.nodes import Node, RegexNode


here = os.path.abspath(os.path.dirname(__file__))
QUERY_PEG = os.path.join(here, 'query.peg')


class QueryPEGTestCase(unittest.TestCase):
    # Simple test to ensure the 'query.peg' file loads properly.

    @property
    def grammar(self):
        if not hasattr(self, '_grammar'):
            with open(QUERY_PEG, 'r') as fb:
                grammar = Grammar(fb.read())
            self._grammar = grammar
        return self._grammar

    def test_term_matching(self):
        gram = self.grammar

        # Simple term matching
        text = "grumble"
        node_tree = gram['term'].parse(text)
        self.assertEqual(node_tree,
                         RegexNode('term', text, 0, len(text)),
                         node_tree)
        self.assertEqual(
            gram['term'].parse(text).match.group(),
            text)

        # Quoted single term matching, should respond the same way as
        #   the simple term matching.
        text = "'grumble'"
        match_text = text[1:len(text)-1]
        node_tree = gram['quoted_term'].parse(text)
        self.assertEqual(node_tree,
                         Node('quoted_term', text, 0, len(text), children=[
                             Node('quote', text, 0, 1, children=[Node('', text, 0, 1)]),
                             # Grouping '()' node.
                             Node('', text, 1, 8, children=[
                                 # ZeroOrMore '*' node.
                                 Node('', text, 1, 8, children=[
                                     RegexNode('term', text, 1, 8),
                                     ]),
                                 ]),
                             Node('quote', text, 8, 9, children=[Node('', text, 8, 9)])
                             ]),
                         node_tree)
        self.assertEqual(node_tree.children[1].text,
            match_text)


        # Two quoted term matching, should respond as one term value.
        text = "'grumble wildly'"
        match_text = text[1:len(text)-1]
        node_tree = gram['quoted_term'].parse(text)
        self.assertEqual(node_tree,
                         Node('quoted_term', text, 0, len(text), children=[
                             Node('quote', text, 0, 1, children=[Node('', text, 0, 1)]),
                             # Grouping '()' node.
                             Node('', text, 1, 15, children=[
                                 # ZeroOrMore '*' nodes.
                                 Node('', text, 1, 8, children=[
                                     RegexNode('term', text, 1, 8),
                                     ]),
                                 Node('', text, 8, 9, children=[
                                     RegexNode('space', text, 8, 9),
                                     ]),
                                 Node('', text, 9, 15, children=[
                                     RegexNode('term', text, 9, 15),
                                     ]),
                                 ]),
                             Node('quote', text, 15, 16, children=[Node('', text, 15, 16)]),
                             ]),
                         node_tree)
        self.assertEqual(node_tree.children[1].text,
                         match_text)

    def test_field_matching(self):
        gram = self.grammar

        # Simple field matching
        field_name = 'toggle'
        value = 'knob'
        text = "{}:{}".format(field_name, value)
        node_tree = gram['field'].parse(text)
        self.assertEqual(node_tree,
                         Node('field', text, 0, 11, children=[
                             RegexNode('field_name', text, 0, 6),
                             Node('', text, 6, 7),  # The ':'.
                             Node('', text, 7, 11, children=[
                                 RegexNode('term', text, 7, 11),
                             ]),
                         ]),
                         node_tree)
        self.assertEqual(node_tree.children[0].text, field_name)
        self.assertEqual(node_tree.children[2].text, value)

        # Field with quoted terms matching
        value = 'air knob'
        text = "{}:'{}'".format(field_name, value)
        node_tree = gram['field'].parse(text)
        self.assertEqual(node_tree,
                         Node('field', text, 0, 17, children=[
                             RegexNode('field_name', text, 0, 6),
                             Node('', text, 6, 7),  # The ':'.
                             Node('', text, 7, 17, children=[
                                 Node('quoted_term', text, 7, 17, children=[
                                     Node('quote', text, 7, 8, children=[
                                         Node('', text, 7, 8)]),
                                     Node('', text, 8, 16, children=[
                                         Node('', text, 8, 11, children=[
                                             RegexNode('term', text, 8, 11)]),
                                         Node('', text, 11, 12, children=[
                                             RegexNode('space', text, 11, 12)]),
                                         Node('', text, 12, 16, children=[
                                             RegexNode('term', text, 12, 16)]),
                                         ]),
                                     Node('quote', text, 16, 17, children=[
                                         Node('', text, 16, 17)]),
                                     ]),
                                 ]),
                             ]),
                         node_tree)
        self.assertEqual(node_tree.children[2].children[0].children[1].text,
                         value)