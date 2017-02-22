# -*- coding: utf-8 -*-
import os

import click
import pwd
import twindb_table_compare
from . import __version__


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
@click.option('--version', is_flag=True, help='Print version and exit', default=False)
@click.argument('slave', default='localhost', required=False)
def main(user, password, db, tbl, slave, vertical, version):
    """twindb_table_compare reads percona.checksums from the master and slave
    and shows records that differ if there are any inconsistencies."""
    if version:
        print(__version__)
        exit(0)

    for d, t in twindb_table_compare.get_inconsistent_tables(slave,
                                                             user,
                                                             password,
                                                             ch_db=db,
                                                             ch_tbl=tbl):
        twindb_table_compare.get_inconsistencies(d, t, slave, user,
                                                 password,
                                                 ch_db=db, ch_tbl=tbl,
                                                 vertical=vertical)


if __name__ == "__main__":
    main()
