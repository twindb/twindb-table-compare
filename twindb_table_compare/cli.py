# -*- coding: utf-8 -*-
import os

import click
import pwd


@click.command()
@click.option('--user', default=pwd.getpwuid(os.getuid()).pw_name,
              help='User name to connect to MySQL')
@click.option('--password', default='',
              help='Password to connect to MySQL')
@click.option('--db', default='percona',
              help='Database where checksums table is stored')
@click.option('--tbl', default='checksums',
              help='Table with checksums')
@click.argument('slave', default='localhost', required=False)
def main(user, password, slave):
    """twindb_table_compare reads percona.checksums from the master and slave
    and shows records that differ if there are any inconsistencies."""

    print('User: %s' % user)
    print('Password: %s' % password)
    print('Slave: %s' % slave)


if __name__ == "__main__":
    main()
