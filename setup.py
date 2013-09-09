# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

install_requires = (
    'parsimonious',
    )
description = ''

setup(
    name='cnx-query-grammar',
    version='0.1',
    author='Connexions team',
    author_email='info@cnx.org',
    url='https://github.com/connexions/cnx-query-grammar',
    license='LGPL, See also LICENSE.txt',
    description=description,
    packages=find_packages(),
    install_requires=install_requires,
    package_data={
        '': ['query.peg'],
        },
    entry_points="""\
    [console_scripts]
    query_parser = cnxquerygrammar.query_parser:main
    """,
    test_suite='cnxquerygrammar.tests'
    )
