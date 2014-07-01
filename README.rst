cnx-query-grammar
=================

The Connections project query grammar parsing library.

Install
-------

Use setup.py to install cnx-query-grammar::

    $ python setup.py install

This creates a script called ``query_parser``.

Usage
-----

::

    >>> from cnxquerygrammar.query_parser import grammar, DictFormater

    >>> node_tree = grammar.parse('Some text')
    >>> DictFormater().visit(node_tree)
    [('text', 'Some'), ('text', 'text')]

    >>> node_tree = grammar.parse('"A phrase"')
    >>> DictFormater().visit(node_tree)
    [('text', 'A phrase')]

    >>> node_tree = grammar.parse('author:"John Smith" type:book')
    >>> DictFormater().visit(node_tree)
    [('author', 'John Smith'), ('type', 'book')]

    >>> node_tree = grammar.parse('author:"John Smith" type:book title:" A Title   With Spaces"')
    >>> DictFormater().visit(node_tree)
    [('author', 'John Smith'), ('type', 'book'), ('title', 'A Title With Spaces')]

Test
----

To run the tests:

::

    $ python -m unittest discover

License
-------

This software is subject to the provisions of the GNU Affero General
Public License Version 3.0 (AGPL). See license.txt for details.
Copyright (c) 2013 Rice University
