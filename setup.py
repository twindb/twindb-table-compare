#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pip.req import parse_requirements
from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()


requirements = [str(ir.req) for ir in
                parse_requirements('requirements.txt', session=False)]

test_requirements = [str(ir.req) for ir in
                     parse_requirements('requirements_dev.txt', session=False)]

setup(
    name='twindb_table_compare',
    version='1.1.3',
    description="TwinDB Table Compare reads percona.checksums from the master "
                "and slave and shows what records are difference "
                "if there are any inconsistencies.",
    long_description=readme + '\n\n' + history,
    author="Aleksandr Kuzminsky",
    author_email='aleks@twindb.com',
    url='https://github.com/twindb/twindb_table_compare',
    packages=[
        'twindb_table_compare',
    ],
    package_dir={'twindb_table_compare':
                 'twindb_table_compare'},
    entry_points={
        'console_scripts': [
            'twindb_table_compare=twindb_table_compare.cli:main'
        ]
    },
    include_package_data=True,
    install_requires=requirements,
    license="Apache Software License 2.0",
    zip_safe=False,
    keywords='twindb_table_compare',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
