# -*- coding: utf-8 -*-
import logging
import os
import string
import tempfile
import MySQLdb
import binascii
import subprocess
import clogging

log = logging.getLogger(__name__)


def setup_logging(logger, debug=False):

    fmt_str = "%(asctime)s: %(levelname)s:" \
              " %(module)s.%(funcName)s():%(lineno)d: %(message)s"

    # console_handler = logging.StreamHandler()
    console_handler = clogging.ColorizingStreamHandler()
    console_handler.setFormatter(logging.Formatter(fmt_str))
    logger.handlers = []
    logger.addHandler(console_handler)
    if debug:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

setup_logging(log)


def is_printable(str_value):
    """
    Checks if str_value is printable string
    :param str_value:
    :return: True if str_value is printable. False otherwise
    """
    return set(str_value).issubset(string.printable)


def get_chunk_index(connection, db, tbl, chunk,
                    ch_db='percona', ch_tbl='checksums'):
    """
    Get index that was used to cut the chunk

    :param connection: MySQLDb connection
    :param db: database of the chunk
    :param tbl: table of the chunk
    :param chunk: chunk id
    :return: index name or None if no index was used
    """
    cur = connection.cursor()
    query = "SELECT chunk_index FROM `%s`.`%s` " \
            "WHERE db='%s' AND tbl='%s' AND chunk = %s"

    log.info('Executing %s' % query % (ch_db, ch_tbl, db, tbl, chunk))
    cur.execute(query % (ch_db, ch_tbl, db, tbl, chunk))
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
    query = "SELECT COLUMN_NAME FROM information_schema.STATISTICS " \
            "WHERE TABLE_SCHEMA='%s' " \
            "AND TABLE_NAME='%s' " \
            "AND INDEX_NAME='%s' " \
            "ORDER BY SEQ_IN_INDEX"
    log.info('Executing %s' % query % (db, tbl, index))
    cur.execute(query % (db, tbl, index))
    cols = []
    for row in cur.fetchall():
        cols.append(row[0])
    return cols


def get_boundary(connection, db, tbl, chunk,
                 ch_db='percona', ch_tbl='checksums'):
    """
    Get lower and upper boundary values of a chunk

    :param connection: MySQLDb connection
    :param db: database of the chunk
    :param tbl: table of the chunk
    :param chunk: chunk id
    :return: tuple with values lower_boundary and upper_boundary of
             percona.checksums
    """
    cur = connection.cursor()
    query = "SELECT lower_boundary, upper_boundary FROM `%s`.`%s` " \
            "WHERE db='%s' AND tbl='%s' AND chunk = %s"
    log.info('Executing %s' % query % (ch_db, ch_tbl, db, tbl, chunk))
    cur.execute(query % (ch_db, ch_tbl, db, tbl, chunk))
    return cur.fetchone()


def get_master(connection):
    """
    Get master host

    :param connection: MySQL connection
    :return: Master hostname
    """
    cur = connection.cursor(MySQLdb.cursors.DictCursor)
    query = "SHOW SLAVE STATUS"
    log.info('Executing %s' % query)
    cur.execute(query)
    return cur.fetchone()['Master_Host']


def get_inconsistencies(db, tbl, slave, user, passwd,
                        ch_db='percona', ch_tbl='checksums'):
    try:
        conn_slave = MySQLdb.connect(host=slave, user=user, passwd=passwd)
        master = get_master(conn_slave)
        conn_master = MySQLdb.connect(host=master, user=user, passwd=passwd)

        # Get chunks that are different on the slave and its master
        query = ("SELECT chunk "
                 "FROM `%s`.`%s` "
                 "WHERE (this_crc<>master_crc OR this_cnt<>master_cnt) "
                 "AND db='%s' AND tbl='%s'")
        log.info("Executing: %s" % (query % (ch_db, ch_tbl, db, tbl)))
        cur_master = conn_master.cursor()
        cur_slave = conn_slave.cursor()

        cur_slave.execute(query % (ch_db, ch_tbl, db, tbl))
        chunks = cur_slave.fetchall()

        if len(chunks) == 1:
            chunks_str = "chunk"
        else:
            chunks_str = "chunks"
        log.info("Found %d inconsistent %s" % (len(chunks), chunks_str))
        # generate WHERE clause to fetch records of the chunk
        for chunk, in chunks:
            log.info("# %s.%s, chunk %d" % (db, tbl, chunk))
            chunk_index = get_chunk_index(conn_slave, db, tbl, chunk,
                                          ch_db=ch_db, ch_tbl=ch_tbl)
            log.info("# chunk index: %s" % chunk_index)
            where = "WHERE"
            if chunk_index:
                index_fields = get_index_fields(conn_slave,
                                                db,
                                                tbl,
                                                chunk_index)
                index_field_last = index_fields[len(index_fields) - 1]
                lower_boundary, upper_boundary = get_boundary(conn_slave,
                                                              db, tbl, chunk,
                                                              ch_db=ch_db,
                                                              ch_tbl=ch_tbl)
                lower_boundaries = lower_boundary.split(",")
                upper_boundaries = upper_boundary.split(",")
                # generate lower boundary clause
                clause_fields = []
                v_num = 0
                where += " (0 "
                op = ">"
                for index_field in index_fields:
                    clause_fields.append(index_field)
                    where += " OR ( 1"
                    for clause_field in clause_fields:
                        if clause_field == \
                                clause_fields[len(clause_fields) - 1]:
                            if clause_field == index_field_last:
                                op = ">="
                            else:
                                op = ">"
                        v = lower_boundaries[v_num]
                        v_num += 1
                        if is_printable(v):
                            where += (" AND `%s` %s '%s'"
                                      % (clause_field, op, v))
                        else:
                            v = ("UNHEX('%s')"
                                 % binascii.hexlify(str(v)))
                            where += (" AND `%s` %s %s"
                                      % (clause_field, op, v))
                        op = "="
                    where += " )"
                where += " )"

                # generate upper boundary clause
                clause_fields = []
                v_num = 0
                where += " AND ( 0"
                op = "<"
                for index_field in index_fields:
                    clause_fields.append(index_field)
                    where += " OR ( 1"
                    for clause_field in clause_fields:
                        if clause_field == \
                                clause_fields[len(clause_fields) - 1]:
                            if clause_field == index_field_last:
                                op = "<="
                            else:
                                op = "<"
                        v = upper_boundaries[v_num]
                        v_num += 1
                        if is_printable(v):
                            where += (" AND `%s` %s '%s'"
                                      % (clause_field, op, v))
                        else:
                            v = ("UNHEX('%s')"
                                 % binascii.hexlify(str(v)))
                            where += (" AND `%s` %s %s"
                                      % (clause_field, op, v))
                        op = "="
                    where += " )"
                where += " )"
            else:
                where += " 1"
            query = "SELECT * FROM `%s`.`%s` %s"
            log.info("Executing: %s" % query % (db, tbl, where))

            master_f, master_filename = tempfile.mkstemp(prefix="master.")
            slave_f, slave_filename = tempfile.mkstemp(prefix="slave.")
            # Now fetch records from the master and slave
            # and write them to temporary files
            # If a field contains unprintable characters print the field in HEX
            cur_master.execute(query % (db, tbl, where))
            result = cur_master.fetchall()

            for row in result:
                for field in row:
                    # print(field)
                    if is_printable(str(field)):
                        os.write(master_f, str(field))
                    else:
                        # pprint HEX-ed string
                        os.write(master_f, binascii.hexlify(str(field)))
                    os.write(master_f, "\t")
                os.write(master_f, "\n")
            os.close(master_f)

            log.info("Executing: %s" % query % (db, tbl, where))
            cur_slave.execute(query % (db, tbl, where))
            result = cur_slave.fetchall()
            for row in result:
                for field in row:
                    if is_printable(str(field)):
                        os.write(slave_f, str(field))
                    else:
                        # pprint HEX-ed string
                        os.write(slave_f, binascii.hexlify(str(field)))
                    os.write(slave_f, "\t")
                os.write(slave_f, "\n")
            os.close(slave_f)

            # Feed diff with the records from the master and slave
            # to show the difference to a user
            cmd = ["diff", "-u", master_filename, slave_filename]
            proc = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE)
            cout, cerr = proc.communicate()
            log.info("Differences between slave %s and its master:\n"
                     % slave + cout)
            if cerr:
                log.error(cerr)
            os.remove(master_filename)
            os.remove(slave_filename)
    except MySQLdb.Error as err:
        log.error(err)


def get_inconsistent_tables(host, user, password,
                            ch_db='percona',
                            ch_tbl='checksums'):
    try:
        conn = MySQLdb.connect(host=host, user=user, passwd=password)
        cur = conn.cursor()
        cur.execute("SELECT db, tbl FROM `%s`.`%s` "
                    "WHERE this_crc <> master_crc OR this_cnt <> master_cnt"
                    % (ch_db, ch_tbl))
        return cur.fetchall()
    except MySQLdb.Error as err:
        log.error(err)
        return []
