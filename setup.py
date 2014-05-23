# -*- coding: utf-8 -*-
from setuptools import setup, find_packages


install_requires = (
    'parsimonious',
    )
description = "Connexions project search query parsing library."
with open('README.rst', 'r') as fb:
    readme = fb.read()
long_description = readme


setup(
    name='cnx-query-grammar',
    version='0.2',
    author='Connexions team',
    author_email='info@cnx.org',
    url='https://github.com/connexions/cnx-query-grammar',
    license='AGPL, See also LICENSE.txt',
    description=description,
    long_description=long_description,
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
