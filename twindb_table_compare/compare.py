"""
Functions to find and print differences
"""
from __future__ import print_function
import binascii
from difflib import unified_diff
import os
import string
from subprocess import Popen, PIPE
import sys
import tempfile

from pymysql import connect
from pymysql.cursors import DictCursor

from . import LOG


def is_printable(str_value):
    """
    Checks if str_value is printable string.

    :param str_value:
    :return: True if str_value is printable. False otherwise
    """
    return set(str_value).issubset(string.printable)


def get_chunk_index(*args, **kwargs):
    """
    Get index that was used to cut the chunk.

    :param args: Positional arguments.
    :type args: tuple(Connection, str, str, int)
    :param kwargs: Keyword arguments.
    :type kwargs: dict
    :return: index name or None if no index was used

    .. rubric:: Positional arguments

    - **connection**: MySQL connection.
    - **database**: database of the chunk.
    - **tbl**: table of the chunk.
    - **chunk**: chunk id.

    .. rubric:: Keyword arguments.

    - **ch_db**: Database where checksums are stored. Default percona.
    - **ch_tbl**: Table where checksums are stored. Default checksums.
    """
    connection = args[0]
    database = args[1]
    tbl = args[2]
    chunk = args[3]
    ch_db = kwargs["ch_db"]
    ch_tbl = kwargs["ch_tbl"]

    cur = connection.cursor()
    query = (
        "SELECT chunk_index FROM `%s`.`%s` WHERE db='%s' AND tbl='%s' AND chunk = %s"
    )

    LOG.info("Executing %s", query % (ch_db, ch_tbl, database, tbl, chunk))
    cur.execute(query % (ch_db, ch_tbl, database, tbl, chunk))
    return cur.fetchone()[0]


def get_index_fields(connection, db, tbl, index):
    """
    Get fields of the given index

    :param connection: MySQLDb connection
    :param db: database
    :param tbl: table
    :param index: index name
    :return: list of field names
    """
    cur = connection.cursor()
    query = (
        "SELECT COLUMN_NAME FROM information_schema.STATISTICS "
        "WHERE TABLE_SCHEMA='%s' "
        "AND TABLE_NAME='%s' "
        "AND INDEX_NAME='%s' "
        "ORDER BY SEQ_IN_INDEX"
    )
    LOG.info("Executing %s", query % (db, tbl, index))
    cur.execute(query % (db, tbl, index))
    cols = []
    for row in cur.fetchall():
        cols.append(row[0])
    return cols


def get_boundary(*args, **kwargs):
    """
    Get lower and upper boundary values of a chunk.

    :param args: Positional arguments.
    :type args: tuple(Connection, str, str, int)
    :param kwargs: Keyword arguments.
    :type kwargs: dict
    :return: tuple with values lower_boundary and upper_boundary of
             percona.checksums

    .. rubric:: Positional arguments

    - **connection**: MySQL connection.
    - **database**: database of the chunk.
    - **tbl**: table of the chunk.
    - **chunk**: chunk id.

    .. rubric:: Keyword arguments.

    - **ch_db**: Database where checksums are stored. Default percona.
    - **ch_tbl**: Table where checksums are stored. Default checksums.
    """
    connection = args[0]
    database = args[1]
    tbl = args[2]
    chunk = args[3]
    ch_db = kwargs["ch_db"]
    ch_tbl = kwargs["ch_tbl"]

    cur = connection.cursor()
    query = (
        "SELECT lower_boundary, upper_boundary FROM `%s`.`%s` "
        "WHERE db='%s' AND tbl='%s' AND chunk = %s"
    )
    LOG.info("Executing %s", query % (ch_db, ch_tbl, database, tbl, chunk))
    cur.execute(query % (ch_db, ch_tbl, database, tbl, chunk))
    return cur.fetchone()


def get_master(connection):
    """
    Get master host

    :param connection: MySQL connection
    :return: Master hostname
    """
    cur = connection.cursor(DictCursor)
    query = "SHOW SLAVE STATUS"
    LOG.info("Executing %s", query)
    cur.execute(query)
    return cur.fetchone()["Master_Host"]


# Colorize diff
# https://goo.gl/GqSyoj
def _green(line):
    if sys.stdout.isatty():
        return "\033[92m" + line + "\033[0m"

    return line


def _red(line):
    if sys.stdout.isatty():
        return "\033[91m" + line + "\033[0m"

    return line


def diff(master_lines, slave_lines, color=True):
    """
    Find differences between two set of lines.

    :param master_lines: First set of lines
    :type master_lines: list
    :param slave_lines: Second set of lines
    :type slave_lines: list
    :param color: If True return colored diff
    :type color: bool
    :return: Difference between two set of lines
    :rtype: str
    """
    result = ""
    for line in unified_diff(master_lines, slave_lines):
        if not line.startswith("---") and not line.startswith("+++"):
            if not line.endswith("\n"):
                # print(result)
                line += "\n"

            if line.startswith("+"):

                if color:
                    result += _green(line)
                else:
                    result += line

            elif line.startswith("-"):

                if color:
                    result += _red(line)
                else:
                    result += line
            else:
                result += line

    return result


def get_fields(conn, db, tbl):
    """
    Construct fields list string for a SELECT.
    If a field is a binary type (BLOB, VARBINARY) then HEX() it.

    :param conn: MySQL connection.
    :type conn: Connection
    :param db: Database name.
    :type db: str
    :param tbl: Table name.
    :type tbl: str
    :return: A comma separated list of fields.
    :rtype: str
    """
    query = (
        "SELECT COLUMN_NAME, DATA_TYPE "
        "FROM information_schema.COLUMNS "
        "WHERE TABLE_SCHEMA='{db}' AND TABLE_NAME='{tbl}' "
        "ORDER BY ORDINAL_POSITION".format(db=db, tbl=tbl)
    )
    cursor = conn.cursor()
    cursor.execute(query)

    fields = []
    for row in cursor.fetchall():
        col_name = row[0]
        col_type = row[1].lower()
        if col_type in [
                "tinyblob",
                "mediumblob",
                "blob",
                "longblob",
                "binary",
                "varbinary",
        ]:
            col_name = "HEX(%s)" % col_name

        fields.append(col_name)

    return ", ".join(fields)


def primary_exists(conn, db, tbl):
    """
    Check if PRIMARY index exists in table db.tbl

    :param conn: MySQLdb connection.
    :type conn: Connection
    :param db: Database name.
    :type db: str
    :param tbl: Table name.
    :type tbl: str
    :return: True if index PRIMARY exists in table db.tbl
    :rtype: bool
    """
    query = (
        "SELECT COUNT(*)"
        "FROM INFORMATION_SCHEMA.STATISTICS "
        "WHERE TABLE_SCHEMA = %s "
        "AND TABLE_NAME = %s"
        "AND INDEX_NAME = 'PRIMARY'"
    )
    cursor = conn.cursor()
    cursor.execute(query, (db, tbl))

    n_fields = cursor.fetchone()[0]

    LOG.debug("Number of fields in PRIMARY index %d", n_fields)

    return bool(n_fields > 0)


def get_boundary_clause(oper=">", index_fields=None, boundaries=None):
    """
    Generate a clause for the WHERE statement based on field names and values

    :param oper: Can be either ``<`` for the lower boundary or ``>``
    for the upper boundary
    :param index_fields: list of fields in the index
    :type index_fields: list
    :param boundaries: list of values for a boundary.
    :type boundaries: list
    :return: a clause that defines a boundary (upper or lower) of a chunk.
    """
    # generate boundary clause
    index_field_last = index_fields[len(index_fields) - 1]
    LOG.debug("index last field: %s", index_field_last)

    clause_fields = []
    v_num = 0
    where = "( 0"
    oper_current = oper
    for index_field in index_fields:
        clause_fields.append(index_field)
        where += " OR ( 1"
        for clause_field in clause_fields:
            if clause_field == clause_fields[len(clause_fields) - 1]:
                if clause_field == index_field_last:
                    oper_current = oper + "="
                else:
                    oper_current = oper
            value = boundaries[v_num]
            v_num += 1
            if is_printable(value):
                where += " AND `%s` %s '%s'" % (clause_field, oper_current, value)
            else:
                value = "UNHEX('%s')" % binascii.hexlify(str(value))
                where += " AND `%s` %s %s" % (clause_field, oper_current, value)
            oper = "="
        where += " )"
    where += " )"
    return where


def get_where(lower_boundary, upper_boundary, index_fields):
    """
    Generate WHERE clause based on strings ``lower_boundary``,
    ``upper_boundary`` from percona.checksums table and fields in the index

    :param lower_boundary: values of lower boundary
    :type lower_boundary: str
    :param upper_boundary: values of upper boundary
    :type upper_boundary: str
    :param index_fields: list of fields in the index that was used
    to access a chunk
    :return: a WHERE clause to read a chunk
    :rtype: str
    """

    try:
        lower_boundaries = lower_boundary.split(",")

        lower_clause = get_boundary_clause(
            oper=">", index_fields=index_fields, boundaries=lower_boundaries
        )
    except AttributeError:
        lower_clause = "1"

    try:
        upper_boundaries = upper_boundary.split(",")
        upper_clause = get_boundary_clause(
            oper="<", index_fields=index_fields, boundaries=upper_boundaries
        )

    except AttributeError:
        upper_clause = "1"

    result = "WHERE {lower} AND {upper}".format(lower=lower_clause, upper=upper_clause)
    return result


# pylint: disable=too-many-arguments,too-many-locals,too-many-branches,too-many-statements
def build_chunk_query(db, tbl, chunk, conn, ch_db="percona", ch_tbl="checksums"):
    """For a given database, table and chunk number construct
    a SELECT query that would return records in this chunk.
    """

    LOG.info("# %s.%s, chunk %d", db, tbl, chunk)
    chunk_index = get_chunk_index(conn, db, tbl, chunk, ch_db=ch_db, ch_tbl=ch_tbl)
    LOG.info("# chunk index: %s", chunk_index)

    if chunk_index:
        index_fields = get_index_fields(conn, db, tbl, chunk_index)

        lower_boundary, upper_boundary = get_boundary(
            conn, db, tbl, chunk, ch_db=ch_db, ch_tbl=ch_tbl
        )

        where = get_where(lower_boundary, upper_boundary, index_fields)
    else:
        where = "WHERE 1"

    fields = get_fields(conn, db, tbl)
    if primary_exists(conn, db, tbl):
        index_hint = "USE INDEX (PRIMARY)"
    else:
        index_hint = ""

    query = "SELECT %s FROM `%s`.`%s` %s %s" % (fields, db, tbl, index_hint, where)

    return query


def print_horizontal(cur_master, cur_slave, query, color=True):
    """
    Find and return differences in horizontal format i.e. one line
    - one record

    :param cur_master: MySQLdb cursor on master
    :type cur_master: Cursor
    :param cur_slave: MySQLdb cursor on slave
    :type cur_slave: Cursor
    :param query: Query to find records in a chunk we compare
    :type query: str
    :param color: If True - produce colorful output
    :return: Differences in a chunk between master and slave
    :rtype: str
    """

    LOG.info("Executing: %s", query)

    master_f, master_filename = tempfile.mkstemp(prefix="master.")
    slave_f, slave_filename = tempfile.mkstemp(prefix="slave.")
    # Now fetch records from the master and slave
    # and write them to temporary files
    # If a field contains unprintable characters print the field in HEX
    cur_master.execute(query)
    result = cur_master.fetchall()

    for row in result:
        for field in row:
            # print(field)
            if is_printable(str(field)):
                os.write(master_f, str(field).encode())
            else:
                # pprint HEX-ed string
                os.write(master_f, binascii.hexlify(str(field).encode()))
            os.write(master_f, "\t".encode())
        os.write(master_f, "\n".encode())
    os.close(master_f)

    LOG.info("Executing: %s", query)
    cur_slave.execute(query)
    result = cur_slave.fetchall()
    for row in result:
        for field in row:
            if is_printable(str(field)):
                os.write(slave_f, str(field).encode())
            else:
                # pprint HEX-ed string
                os.write(slave_f, binascii.hexlify(str(field).encode()))
            os.write(slave_f, "\t".encode())
        os.write(slave_f, "\n".encode())
    os.close(slave_f)

    diffs = diff(
        open(master_filename).readlines(), open(slave_filename).readlines(), color=color
    )
    os.remove(master_filename)
    os.remove(slave_filename)
    return diffs


def print_vertical(master, slave, user, passwd, query, color=True):
    r"""
    Find and return differences in vertical format.
    The vertical format is when you end MySQL query with '\G'

    :param master: Hostname of the master.
    :type master: str
    :param slave: Hostname of the slave.
    :type slave: str
    :param query: Query to find records in a chunk we compare
    :type query: str
    :param color: If True - produce colorful output
    :return: Differences in a chunk between master and slave
    :rtype: str
    """
    LOG.info("Executing: %s", query)

    proc = Popen(
        ["mysql", "-h", master, "-u", user, "-p%s" % passwd, "-e", r"%s\G" % query],
        stdout=PIPE,
        stderr=PIPE,
    )
    master_cout, master_cerr = proc.communicate()
    master_lines = []
    for line in master_cout.split("\n"):
        if line.startswith("***************************"):
            master_lines.append(
                "*******************************" "*******************************"
            )
        else:
            master_lines.append(line)

    if proc.returncode:
        LOG.error("Failed to query master.")
        LOG.error(master_cerr)
        sys.exit(1)

    LOG.info("Executing: %s", query)
    proc = Popen(
        ["mysql", "-h", slave, "-u", user, "-p%s" % passwd, "-e", r"%s\G" % query],
        stdout=PIPE,
        stderr=PIPE,
    )
    slave_cout, slave_cerr = proc.communicate()

    slave_lines = []
    for line in slave_cout.split("\n"):
        if line.startswith("***************************"):
            slave_lines.append(
                "*******************************" "*******************************"
            )
        else:
            slave_lines.append(line)

    if proc.returncode:
        LOG.error("Failed to query slave.")
        LOG.error(slave_cerr)
        sys.exit(1)

    return diff(master_lines, slave_lines, color=color)


def get_inconsistencies(
        db,
        tbl,
        slave,
        user,
        passwd,
        ch_db="percona",
        ch_tbl="checksums",
        vertical=False,
        color=True,
):
    r"""
    Print differences between slave and its master.

    :param db: Database name of the inconsistent table.
    :param tbl: Table name of the inconsistent table.
    :param slave: Hostname of the slave.
    :param user: User to connect to MySQL.
    :param passwd: Password to connect to MySQL.
    :param ch_db: Database where checksums are stored.
    :param ch_tbl: Table name where checksums are stored.
    :param vertical: If True - print result vertically (\G in MySQL)
    :param color: If True - print colorful output
    """
    conn_slave = connect(host=slave, user=user, passwd=passwd)
    master = get_master(conn_slave)
    conn_master = connect(host=master, user=user, passwd=passwd)

    # Get chunks that are different on the slave and its master
    query = (
        "SELECT chunk "
        "FROM `%s`.`%s` "
        "WHERE (this_crc<>master_crc OR this_cnt<>master_cnt) "
        "AND db='%s' AND tbl='%s'"
    )
    LOG.info("Executing: %s", query % (ch_db, ch_tbl, db, tbl))
    cur_master = conn_master.cursor()
    cur_slave = conn_slave.cursor()

    cur_slave.execute(query % (ch_db, ch_tbl, db, tbl))
    chunks = cur_slave.fetchall()

    if len(chunks) == 1:
        chunks_str = "chunk"
    else:
        chunks_str = "chunks"
    LOG.info("Found %d inconsistent %s", len(chunks), chunks_str)
    # generate WHERE clause to fetch records of the chunk
    for (chunk,) in chunks:

        query = build_chunk_query(
            db, tbl, chunk, conn_slave, ch_db=ch_db, ch_tbl=ch_tbl
        )

        if vertical:
            diffs = print_vertical(master, slave, user, passwd, query, color=color)
        else:
            diffs = print_horizontal(cur_master, cur_slave, query, color=color)
            LOG.info("Differences between slave %s and its master:", slave)

        print(diffs)


def get_inconsistent_tables(host, user, password, ch_db="percona", ch_tbl="checksums"):
    """
    On a given MySQL server find tables that are inconsistent with the master.

    :param host: Hostname with potentially inconsistent tables.
    :param user: MySQL user.
    :param password: MySQL password.
    :param ch_db: Database where checksums are stored.
    :param ch_tbl: Table name where checksums are stored.
    :return: List of tuples with inconsistent tables.
    Each tuple is database name, table name
    :rtype: list
    """
    conn = connect(host=host, user=user, passwd=password)
    cur = conn.cursor()
    cur.execute(
        "SELECT db, tbl FROM `%s`.`%s` "
        "WHERE this_crc <> master_crc OR this_cnt <> master_cnt" % (ch_db, ch_tbl)
    )
    return cur.fetchall()
