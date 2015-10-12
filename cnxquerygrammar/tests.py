# -*- coding: utf-8 -*-
import doctest
import os
import unittest
from parsimonious import Grammar
from parsimonious.nodes import Node, RegexNode


doctest.testfile('../README.rst')

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
        text = '"grumble"'
        match_text = text[1:len(text)-1]
        node_tree = gram['quoted_term'].parse(text)
        self.assertEqual(node_tree,
                         Node('quoted_term', text, 0, len(text), children=[
                             Node('quote', text, 0, 1),
                             # Grouping '()' node.
                             Node('', text, 1, 8, children=[
                                 # ZeroOrMore '*' node.
                                 Node('', text, 1, 8, children=[
                                     RegexNode('term', text, 1, 8),
                                     ]),
                                 ]),
                             Node('quote', text, 8, 9),
                             ]),
                         node_tree)
        self.assertEqual(node_tree.children[1].text,
                         match_text)

        # Two quoted term matching, should respond as one term value.
        text = '"grumble wildly"'
        match_text = text[1:len(text)-1]
        node_tree = gram['quoted_term'].parse(text)
        self.assertEqual(node_tree,
                         Node('quoted_term', text, 0, len(text), children=[
                             Node('quote', text, 0, 1),
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
                             Node('quote', text, 15, 16),
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
        text = '{}:"{}"'.format(field_name, value)
        node_tree = gram['field'].parse(text)
        self.assertEqual(node_tree,
                         Node('field', text, 0, 17, children=[
                             RegexNode('field_name', text, 0, 6),
                             Node('', text, 6, 7),  # The ':'.
                             Node('', text, 7, 17, children=[
                                 Node('quoted_term', text, 7, 17, children=[
                                     Node('quote', text, 7, 8),
                                     Node('', text, 8, 16, children=[
                                         Node('', text, 8, 11, children=[
                                             RegexNode('term', text, 8, 11)]),
                                         Node('', text, 11, 12, children=[
                                             RegexNode('space', text, 11, 12)
                                             ]),
                                         Node('', text, 12, 16, children=[
                                             RegexNode('term', text, 12, 16)]),
                                         ]),
                                     Node('quote', text, 16, 17),
                                     ]),
                                 ]),
                             ]),
                         node_tree)
        self.assertEqual(node_tree.children[2].children[0].children[1].text,
                         value)

    def test_query_matching(self):
        gram = self.grammar

        # Combined expressions matching
        field_value = 'book'
        text_values = ['organic', ' ', 'chemistry', ' ',
                       'type:{}'.format(field_value)]
        text = ''.join(text_values)
        node_tree = gram['query'].parse(text)
        expected_node_tree = \
            Node('query', text, 0, 27, children=[
                Node('', text, 0, 7, children=[
                    Node('expression', text, 0, 7, children=[
                        Node('', text, 0, 7, children=[
                            RegexNode('term', text, 0, 7),
                            ])
                        ]),
                    ]),
                Node('', text, 7, 8, children=[
                    RegexNode('space', text, 7, 8),
                    ]),
                Node('', text, 8, 17, children=[
                    Node('expression', text, 8, 17, children=[
                         Node('', text, 8, 17, children=[
                             RegexNode('term', text, 8, 17),
                             ])
                         ]),
                    ]),
                Node('', text, 17, 18, children=[
                    RegexNode('space', text, 17, 18),
                    ]),
                Node('', text, 18, 27, children=[
                    Node('expression', text, 18, 27, children=[
                        Node('field', text, 18, 27, children=[
                            RegexNode('field_name', text, 18, 22),
                            Node('', text, 22, 23),
                            Node('', text, 23, 27, children=[
                                RegexNode('term', text, 23, 27),
                                ]),
                            ]),
                        ]),
                    ]),
                ])
        self.assertEqual(node_tree,
                         expected_node_tree,
                         node_tree)
        self.assertEqual(node_tree.children[0].children[0].text,
                         text_values[0])  # 'organic'
        self.assertEqual(node_tree.children[2].children[0].text,
                         text_values[2])  # 'chemistry'
        self.assertEqual(
            node_tree.children[4].children[0].children[0].children[2].text,
            field_value)

        # Combined expressions with quoted terms matching
        field_value = 'book'
        text_values = ['"organic chemistry"', ' ',
                       'type:{}'.format(field_value)]
        text = ''.join(text_values)
        node_tree = gram['query'].parse(text)
        expected_node_tree = \
            Node('query', text, 0, 29, children=[
                Node('', text, 0, 19, children=[
                    Node('expression', text, 0, 19, children=[
                        Node('', text, 0, 19, children=[
                            Node('quoted_term', text, 0, 19, children=[
                                Node('quote', text, 0, 1),
                                Node('', text, 1, 18, children=[
                                    Node('', text, 1, 8, children=[
                                        RegexNode('term', text, 1, 8),
                                        ]),
                                    Node('', text, 8, 9, children=[
                                        RegexNode('space', text, 8, 9),
                                        ]),
                                    Node('', text, 9, 18, children=[
                                        RegexNode('term', text, 9, 18),
                                        ]),
                                    ]),
                                Node('quote', text, 18, 19),
                                ]),
                            ]),
                        ]),
                    ]),
                Node('', text, 19, 20, children=[
                    RegexNode('space', text, 19, 20),
                    ]),
                Node('', text, 20, 29, children=[
                    Node('expression', text, 20, 29, children=[
                        Node('field', text, 20, 29, children=[
                            RegexNode('field_name', text, 20, 24),
                            Node('', text, 24, 25),
                            Node('', text, 25, 29, children=[
                                RegexNode('term', text, 25, 29),
                                ]),
                            ]),
                        ]),
                    ]),
                ])
        self.assertEqual(node_tree,
                         expected_node_tree,
                         node_tree)
        # Match 'organic chemistry'
        self.assertEqual(
            node_tree.children[0].children[0].children[0].children[0]
            .children[1].text,
            text_values[0][1:len(text_values[0])-1])
        # Match 'book'
        self.assertEqual(
            node_tree.children[2].children[0].children[0].children[2].text,
            field_value)

    def test_utf8_term(self):
        gram = self.grammar

        text = u'你好'
        node_tree = gram['term'].parse(text)
        self.assertEqual(node_tree,
                         RegexNode('term', text, 0, len(text)))
        self.assertEqual(node_tree.match.group(), text)

    def test_punctuations(self):
        gram = self.grammar

        text = '"hello, name!"'
        node_tree = gram['quoted_term'].parse(text)

        expected_tree = Node('quoted_term', text, 0, len(text), children=[
            # "
            Node('quote', text, 0, 1),
            Node('', text, 1, 13, children=[
                # hello,
                Node('', text, 1, 7, children=[
                    RegexNode('term', text, 1, 7),
                    ]),
                # (space)
                Node('', text, 7, 8, children=[
                    RegexNode('space', text, 7, 8),
                    ]),
                # name!
                Node('', text, 8, 13, children=[
                    RegexNode('term', text, 8, 13),
                    ]),
                ]),
            # "
            Node('quote', text, 13, 14),
            ])
        self.assertEqual(node_tree, expected_tree, node_tree)
