# -*- coding: utf-8 -*-
import os

import click
import pwd
import twindb_table_compare


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
@click.argument('slave', default='localhost', required=False)
def main(user, password, db, tbl, slave, vertical):
    """twindb_table_compare reads percona.checksums from the master and slave
    and shows records that differ if there are any inconsistencies."""

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
