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
from twindb_table_compare.twindb_table_compare import is_printable


def test_command_line_interface():
    runner = CliRunner()
    result = runner.invoke(cli.main)
    assert result.exit_code == 0
    # assert 'twindb_table_compare.cli.main' in result.output
    help_result = runner.invoke(cli.main, ['--help'])
    assert help_result.exit_code == 0
    # assert '--help  Show this message and exit.' in help_result.output


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
