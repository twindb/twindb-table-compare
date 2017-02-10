===============================
TwinDB Table Compare
===============================

.. image:: https://badges.gitter.im/twindb/twindb_table_compare.svg
   :alt: Join the chat at https://gitter.im/twindb/twindb_table_compare
   :target: https://gitter.im/twindb/twindb_table_compare?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge


.. image:: https://img.shields.io/pypi/v/twindb_table_compare.svg
        :target: https://pypi.python.org/pypi/twindb_table_compare

.. image:: https://img.shields.io/travis/twindb/twindb_table_compare.svg
        :target: https://travis-ci.org/twindb/twindb_table_compare

.. image:: https://img.shields.io/codecov/c/github/twindb/twindb_table_compare.svg
        :target: https://codecov.io/gh/twindb/twindb_table_compare
        :alt: Code test coverage

.. image:: https://readthedocs.org/projects/twindb-table-compare/badge/?version=latest
        :target: https://twindb-table-compare.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/twindb/twindb_table_compare/shield.svg
     :target: https://pyup.io/repos/github/twindb/twindb_table_compare/
     :alt: Updates

.. image:: https://img.shields.io/pypi/dd/Django.svg?maxAge=2592000
     :target: https://pypi.python.org/pypi/twindb-table-compare
     :alt: Pypi


TwinDB Table Compare reads percona.checksums from the master and slave and shows what records are difference if there are any inconsistencies.


* Free software: Apache Software License 2.0
* Documentation: https://twindb-table-compare.readthedocs.io.
* Blogpost with usage examples: https://twindb.com/pt-table-checksum-show-differences/


Usage
--------

TwinDB Table Compare should be used in the command line.

This will show differences in data between *slave* and its master.

``twindb_table_compare`` *slave*


where *slave* is a hostname of a MySQL slave.

::

    [root@master vagrant]# twindb_table_compare --user=dba --password=qwerty 192.168.35.251
    2016-09-03 22:48:01,732: INFO: twindb_table_compare.get_inconsistencies():127: Executing: SELECT chunk FROM `percona`.`checksums` WHERE (this_crc&lt;&gt;master_crc OR this_cnt&lt;&gt;master_cnt) AND db='mysql' AND tbl='proxies_priv'
    2016-09-03 22:48:01,734: INFO: twindb_table_compare.get_inconsistencies():138: Found 1 inconsistent chunk
    2016-09-03 22:48:01,734: INFO: twindb_table_compare.get_inconsistencies():141: # mysql.proxies_priv, chunk 1
    2016-09-03 22:48:01,736: INFO: twindb_table_compare.get_inconsistencies():143: # chunk index: None
    2016-09-03 22:48:01,736: INFO: twindb_table_compare.get_inconsistencies():215: Executing: SELECT * FROM `mysql`.`proxies_priv` WHERE 1
    2016-09-03 22:48:01,743: INFO: twindb_table_compare.get_inconsistencies():257: Differences between slave 192.168.35.251 and its master:
    --- /tmp/master.GZ8S7V 2016-09-03 22:48:01.737762174 +0000
    +++ /tmp/slave.9t4HhV 2016-09-03 22:48:01.738761674 +0000
    @@ -1,2 +1,2 @@
    -localhost root 1 2016-09-03 20:02:28
    -master.box root 1 2016-09-03 20:02:28
    +localhost root 1 2016-09-03 20:10:04
    +slave.box root 1 2016-09-03 20:10:04

    2016-09-03 22:48:01,746: INFO: twindb_table_compare.get_inconsistencies():127: Executing: SELECT chunk FROM `percona`.`checksums` WHERE (this_crc&lt;&gt;master_crc OR this_cnt&lt;&gt;master_cnt) AND db='mysql' AND tbl='user'
    2016-09-03 22:48:01,747: INFO: twindb_table_compare.get_inconsistencies():138: Found 1 inconsistent chunk
    2016-09-03 22:48:01,747: INFO: twindb_table_compare.get_inconsistencies():141: # mysql.user, chunk 1
    2016-09-03 22:48:01,747: INFO: twindb_table_compare.get_inconsistencies():143: # chunk index: None
    2016-09-03 22:48:01,748: INFO: twindb_table_compare.get_inconsistencies():215: Executing: SELECT * FROM `mysql`.`user` WHERE 1
    2016-09-03 22:48:01,757: INFO: twindb_table_compare.get_inconsistencies():257: Differences between slave 192.168.35.251 and its master:
    --- /tmp/master.l_zYw7 2016-09-03 22:48:01.749756174 +0000
    +++ /tmp/slave.39qG9N 2016-09-03 22:48:01.752754674 +0000
    @@ -1,9 +1,9 @@
     localhost root Y Y Y Y Y Y Y Y Y Y Y Y Y Y Y Y Y Y Y Y Y Y Y Y Y Y Y Y Y 0 0 0 0 mysql_native_password N
    -master.box root Y Y Y Y Y Y Y Y Y Y Y Y Y Y Y Y Y Y Y Y Y Y Y Y Y Y Y Y Y 0 0 0 0 mysql_native_password N
    +slave.box root Y Y Y Y Y Y Y Y Y Y Y Y Y Y Y Y Y Y Y Y Y Y Y Y Y Y Y Y Y 0 0 0 0 mysql_native_password N
     127.0.0.1 root Y Y Y Y Y Y Y Y Y Y Y Y Y Y Y Y Y Y Y Y Y Y Y Y Y Y Y Y Y 0 0 0 0 mysql_native_password N
     ::1 root Y Y Y Y Y Y Y Y Y Y Y Y Y Y Y Y Y Y Y Y Y Y Y Y Y Y Y Y Y 0 0 0 0 mysql_native_password N
     localhost N N N N N N N N N N N N N N N N N N N N N N N N N N N N N 0 0 0 0 mysql_native_password None N
    -master.box N N N N N N N N N N N N N N N N N N N N N N N N N N N N N 0 0 0 0 mysql_native_password None N
    +slave.box N N N N N N N N N N N N N N N N N N N N N N N N N N N N N 0 0 0 0 mysql_native_password None N
     % dba *AA1420F182E88B9E5F874F6FBE7459291E8F4601 Y Y Y Y Y Y Y Y Y Y Y Y Y Y Y Y Y Y Y Y Y Y Y Y Y Y Y Y Y 0 0 0 0 mysql_native_password N
     localhost dba *AA1420F182E88B9E5F874F6FBE7459291E8F4601 Y Y Y Y Y Y Y Y Y Y Y Y Y Y Y Y Y Y Y Y Y Y Y Y Y Y Y Y Y 0 0 0 0mysql_native_password N
     % repl *809534247D21AC735802078139D8A854F45C31F3 N N N N N N N N N N N N N N N N N N N Y N N N N N N N N N 0 0 0 0 mysql_native_password N

Run ``twindb_table_compare --help`` for other options.


Credits
---------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage

