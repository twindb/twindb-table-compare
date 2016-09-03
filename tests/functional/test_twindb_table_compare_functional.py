#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_twindb_table_compare
----------------------------------

Tests for `twindb_table_compare` module.
"""
import binascii
import MySQLdb
import pytest

from click.testing import CliRunner

from twindb_table_compare import cli
from twindb_table_compare.twindb_table_compare import is_printable, \
    get_chunk_index, get_index_fields, get_boundary, get_master


@pytest.fixture
def mysql_cred():
    return {
        'user': 'dba',
        'password': 'qwerty'
    }


@pytest.fixture
def master_connection(mysql_cred):
    return MySQLdb.connect(host='192.168.35.250',
                           user=mysql_cred['user'],
                           passwd=mysql_cred['password'])


@pytest.fixture
def slave_connection(mysql_cred):
    return MySQLdb.connect(host='192.168.35.251',
                           user=mysql_cred['user'],
                           passwd=mysql_cred['password'])


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


def test_get_chunk_index(master_connection):
    assert get_chunk_index(master_connection, 'test', 't1', 1) == 'PRIMARY'
    assert not get_chunk_index(master_connection, 'mysql', 'user', 1)


def test_get_index_fields(master_connection):
    assert get_index_fields(master_connection,
                            'test', 't1', 'PRIMARY') == ['id']


def test_get_boundary(master_connection):
    boundary = get_boundary(master_connection, 'test', 't1', 1)
    assert int(boundary[0]) == 1
    assert int(boundary[1]) <= 393197


def test_get_master(slave_connection):
    assert get_master(slave_connection) == '192.168.35.250'
