# -*- coding: utf-8 -*-
"""
Command line routines
"""
from __future__ import print_function
import pwd
import os

import MySQLdb
import click

from twindb_table_compare.compare import get_inconsistencies, \
    get_inconsistent_tables

from . import __version__, setup_logging, LOG


@click.command()
@click.option('--user', default=pwd.getpwuid(os.getuid()).pw_name,
              help='User name to connect to MySQL')
@click.option('--password', default='',
              help='Password to connect to MySQL')
@click.option('--db', default='percona',
              help='Database where checksums table is stored')
@click.option('--tbl', default='checksums',
              help='Table with checksums')
@click.option('--vertical', default=False, is_flag=True,
              help='Print result vertically. '
                   'Otherwise will print one record in one line')
@click.option('--version', is_flag=True,
              help='Print version and exit', default=False)
@click.option('--debug', is_flag=True,
              help='Print debug messages', default=False)
@click.option('--color/--no-color', is_flag=True,
              help='Print colored log messages', default=True)
@click.argument('slave',
                default='localhost',
                required=False)  # pylint: disable=too-many-arguments
def main(user, password, db, tbl, slave,
         vertical, debug, version, color):
    """twindb_table_compare reads percona.checksums from the master and slave
    and shows records that differ if there are any inconsistencies."""
    if version:
        print(__version__)
        exit(0)

    setup_logging(LOG, debug=debug, color=color)
    try:
        for database, table in get_inconsistent_tables(slave,
                                                       user,
                                                       password,
                                                       ch_db=db,
                                                       ch_tbl=tbl):
            get_inconsistencies(database, table, slave, user, password,
                                ch_db=db, ch_tbl=tbl,
                                vertical=vertical, color=color)
    except MySQLdb.Error as err:  # pylint: disable=no-member
        LOG.error(err)
        exit(1)
