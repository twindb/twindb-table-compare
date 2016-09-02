===============================
TwinDB Table Compare
===============================


.. image:: https://img.shields.io/pypi/v/twindb_table_compare.svg
        :target: https://pypi.python.org/pypi/twindb_table_compare

.. image:: https://img.shields.io/travis/twindb/twindb_table_compare.svg
        :target: https://travis-ci.org/twindb/twindb_table_compare

.. image:: https://readthedocs.org/projects/twindb-table-compare/badge/?version=latest
        :target: https://twindb-table-compare.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/twindb/twindb_table_compare/shield.svg
     :target: https://pyup.io/repos/github/twindb/twindb_table_compare/
     :alt: Updates


TwinDB Table Compare reads percona.checksums from the master and slave and shows what records are difference if there are any inconsistencies.


* Free software: Apache Software License 2.0
* Documentation: https://twindb-table-compare.readthedocs.io.


Usage
--------

TwinDB Table Compare should be used in the command line.

This will show differences in data between *slave* and its master.

``twindb_table_compare`` *slave*


where *slave* is a hostname of a MySQL slave.

Run ``twindb_table_compare --help`` for other options.


Credits
---------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage

