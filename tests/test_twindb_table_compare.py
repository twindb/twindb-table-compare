#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_twindb_table_compare
----------------------------------

Tests for `twindb_table_compare` module.
"""

import pytest

from contextlib import contextmanager
from click.testing import CliRunner

from twindb_table_compare import twindb_table_compare
from twindb_table_compare import cli


class TestTwindb_table_compare(object):

    @classmethod
    def setup_class(cls):
        pass

    def test_something(self):
        pass
    def test_command_line_interface(self):
        runner = CliRunner()
        result = runner.invoke(cli.main)
        assert result.exit_code == 0
        assert 'twindb_table_compare.cli.main' in result.output
        help_result = runner.invoke(cli.main, ['--help'])
        assert help_result.exit_code == 0
        assert '--help  Show this message and exit.' in help_result.output

    @classmethod
    def teardown_class(cls):
        pass

