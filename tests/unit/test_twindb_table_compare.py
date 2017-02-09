#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_twindb_table_compare
----------------------------------

Tests for `twindb_table_compare` module.
"""
import binascii
import pytest

from click.testing import CliRunner

from twindb_table_compare import cli
from twindb_table_compare.twindb_table_compare import is_printable, diff


def test_command_line_interface():
    runner = CliRunner()
    result = runner.invoke(cli.main)
    assert result.exit_code == 0
    help_result = runner.invoke(cli.main, ['--help'])
    assert help_result.exit_code == 0


@pytest.mark.parametrize('input_str,result', [
    (
        'foo',
        True
    ),
    (
        binascii.a2b_hex('AA'),
        False
    )
])
def test_is_printable(input_str, result):
    assert is_printable(input_str) == result


@pytest.mark.parametrize('master_lines, slave_lines, difference', [
    (
        [
            'localhost\troot\t1\t2016-12-02 04:46:12\n',
            'master.box\troot\t1\t2016-12-02 04:46:12\n'
        ],
        [
            'localhost\troot\t1\t2016-12-02 05:43:47\n',
            'slave.box\troot\t1\t2016-12-02 05:43:47\n'
        ],
        """@@ -1,2 +1,2 @@
-localhost\troot\t1\t2016-12-02 04:46:12
-master.box\troot\t1\t2016-12-02 04:46:12
+localhost\troot\t1\t2016-12-02 05:43:47
+slave.box\troot\t1\t2016-12-02 05:43:47
"""
    ),
    (
        [
            '3882\t2016-04-20 14:57:31\n',
            '3882\t2016-04-20 14:57:31\n',
            '3937\t2016-05-13 14:32:53\n'
        ],
        [
            '3937\t2016-05-13 14:32:53\n',
            '3882\t2016-04-20 14:57:31\n',
            '3882\t2016-04-20 14:57:31\n'
        ],
        ""
    )
])
def test_diff(master_lines, slave_lines, difference):
    assert diff(master_lines, slave_lines) == difference
