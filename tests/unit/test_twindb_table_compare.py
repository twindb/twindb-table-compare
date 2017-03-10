#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_twindb_table_compare
----------------------------------

Tests for `twindb_table_compare` module.
"""
import binascii

import mock
import pytest

from click.testing import CliRunner

from twindb_table_compare import cli, __version__
from twindb_table_compare.compare import is_printable, diff, print_vertical, \
    get_fileds


def test_command_line_interface():
    runner = CliRunner()
    help_result = runner.invoke(cli.main, ['--help'])
    assert help_result.exit_code == 0


@mock.patch('twindb_table_compare.cli.get_inconsistencies')
def test_version(mock_get_inconsistencies):
    runner = CliRunner()
    mock_get_inconsistencies.side_effect = Exception
    help_result = runner.invoke(cli.main, ['--version'])
    assert help_result.output.strip('\n') == __version__
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
        """@@ -1,3 +1,3 @@
+3937\t2016-05-13 14:32:53
 3882\t2016-04-20 14:57:31
 3882\t2016-04-20 14:57:31
-3937\t2016-05-13 14:32:53
"""
    ),
    (
        [
            "*************************** 1. row ***************************\n",
            "                  Host: localhost\n",
            "                  User: root\n",
            "              Password: \n",
            "           Select_priv: Y\n",
            "           Insert_priv: Y\n",
            "           Update_priv: Y\n",
            "           Delete_priv: Y\n",
            "           Create_priv: Y\n",
            "             Drop_priv: Y\n",
            "           Reload_priv: Y\n",
            "         Shutdown_priv: Y\n",
            "          Process_priv: Y\n",
            "             File_priv: Y\n",
            "            Grant_priv: Y\n",
            "       References_priv: Y\n",
            "            Index_priv: Y\n",
            "            Alter_priv: Y\n",
            "          Show_db_priv: Y\n",
            "            Super_priv: Y\n",
            " Create_tmp_table_priv: Y\n",
            "      Lock_tables_priv: Y\n",
            "          Execute_priv: Y\n",
            "       Repl_slave_priv: Y\n",
            "      Repl_client_priv: Y\n",
            "      Create_view_priv: Y\n",
            "        Show_view_priv: Y\n",
            "   Create_routine_priv: Y\n",
            "    Alter_routine_priv: Y\n",
            "      Create_user_priv: Y\n",
            "            Event_priv: Y\n",
            "          Trigger_priv: Y\n",
            "Create_tablespace_priv: Y\n",
            "              ssl_type: \n",
            "       HEX(ssl_cipher): \n",
            "      HEX(x509_issuer): \n",
            "     HEX(x509_subject): \n",
            "         max_questions: 0\n",
            "           max_updates: 0\n",
            "       max_connections: 0\n",
            "  max_user_connections: 0\n",
            "                plugin: mysql_native_password\n",
            " authentication_string: \n",
            "      password_expired: N\n",
            "*************************** 2. row ***************************\n",
            "                  Host: master.box\n",
            "                  User: root\n",
            "              Password: \n",
            "           Select_priv: Y\n",
            "           Insert_priv: Y\n",
            "           Update_priv: Y\n",
            "           Delete_priv: Y\n",
            "           Create_priv: Y\n",
            "             Drop_priv: Y\n",
            "           Reload_priv: Y\n",
            "         Shutdown_priv: Y\n",
            "          Process_priv: Y\n",
            "             File_priv: Y\n",
            "            Grant_priv: Y\n",
            "       References_priv: Y\n",
            "            Index_priv: Y\n",
            "            Alter_priv: Y\n",
            "          Show_db_priv: Y\n",
            "            Super_priv: Y\n",
            " Create_tmp_table_priv: Y\n",
            "      Lock_tables_priv: Y\n",
            "          Execute_priv: Y\n",
            "       Repl_slave_priv: Y\n",
            "      Repl_client_priv: Y\n",
            "      Create_view_priv: Y\n",
            "        Show_view_priv: Y\n",
            "   Create_routine_priv: Y\n",
            "    Alter_routine_priv: Y\n",
            "      Create_user_priv: Y\n",
            "            Event_priv: Y\n",
            "          Trigger_priv: Y\n",
            "Create_tablespace_priv: Y\n",
            "              ssl_type: \n",
            "       HEX(ssl_cipher): \n",
            "      HEX(x509_issuer): \n",
            "     HEX(x509_subject): \n",
            "         max_questions: 0\n",
            "           max_updates: 0\n",
            "       max_connections: 0\n",
            "  max_user_connections: 0\n",
            "                plugin: mysql_native_password\n",
            " authentication_string: \n",
            "      password_expired: N\n",
            "*************************** 3. row ***************************\n",
            "                  Host: 127.0.0.1\n",
            "                  User: root\n",
            "              Password: \n",
            "           Select_priv: Y\n",
            "           Insert_priv: Y\n",
            "           Update_priv: Y\n",
            "           Delete_priv: Y\n",
            "           Create_priv: Y\n",
            "             Drop_priv: Y\n",
            "           Reload_priv: Y\n",
            "         Shutdown_priv: Y\n",
            "          Process_priv: Y\n",
            "             File_priv: Y\n",
            "            Grant_priv: Y\n",
            "       References_priv: Y\n",
            "            Index_priv: Y\n",
            "            Alter_priv: Y\n",
            "          Show_db_priv: Y\n",
            "            Super_priv: Y\n",
            " Create_tmp_table_priv: Y\n",
            "      Lock_tables_priv: Y\n",
            "          Execute_priv: Y\n",
            "       Repl_slave_priv: Y\n",
            "      Repl_client_priv: Y\n",
            "      Create_view_priv: Y\n",
            "        Show_view_priv: Y\n",
            "   Create_routine_priv: Y\n",
            "    Alter_routine_priv: Y\n",
            "      Create_user_priv: Y\n",
            "            Event_priv: Y\n",
            "          Trigger_priv: Y\n",
            "Create_tablespace_priv: Y\n",
            "              ssl_type: \n",
            "       HEX(ssl_cipher): \n",
            "      HEX(x509_issuer): \n",
            "     HEX(x509_subject): \n",
            "         max_questions: 0\n",
            "           max_updates: 0\n",
            "       max_connections: 0\n",
            "  max_user_connections: 0\n",
            "                plugin: mysql_native_password\n",
            " authentication_string: \n",
            "      password_expired: N\n",
            "*************************** 4. row ***************************\n",
            "                  Host: ::1\n",
            "                  User: root\n",
            "              Password: \n",
            "           Select_priv: Y\n",
            "           Insert_priv: Y\n",
            "           Update_priv: Y\n",
            "           Delete_priv: Y\n",
            "           Create_priv: Y\n",
            "             Drop_priv: Y\n",
            "           Reload_priv: Y\n",
            "         Shutdown_priv: Y\n",
            "          Process_priv: Y\n",
            "             File_priv: Y\n",
            "            Grant_priv: Y\n",
            "       References_priv: Y\n",
            "            Index_priv: Y\n",
            "            Alter_priv: Y\n",
            "          Show_db_priv: Y\n",
            "            Super_priv: Y\n",
            " Create_tmp_table_priv: Y\n",
            "      Lock_tables_priv: Y\n",
            "          Execute_priv: Y\n",
            "       Repl_slave_priv: Y\n",
            "      Repl_client_priv: Y\n",
            "      Create_view_priv: Y\n",
            "        Show_view_priv: Y\n",
            "   Create_routine_priv: Y\n",
            "    Alter_routine_priv: Y\n",
            "      Create_user_priv: Y\n",
            "            Event_priv: Y\n",
            "          Trigger_priv: Y\n",
            "Create_tablespace_priv: Y\n",
            "              ssl_type: \n",
            "       HEX(ssl_cipher): \n",
            "      HEX(x509_issuer): \n",
            "     HEX(x509_subject): \n",
            "         max_questions: 0\n",
            "           max_updates: 0\n",
            "       max_connections: 0\n",
            "  max_user_connections: 0\n",
            "                plugin: mysql_native_password\n",
            " authentication_string: \n",
            "      password_expired: N\n",
            "*************************** 5. row ***************************\n",
            "                  Host: localhost\n",
            "                  User: \n",
            "              Password: \n",
            "           Select_priv: N\n",
            "           Insert_priv: N\n",
            "           Update_priv: N\n",
            "           Delete_priv: N\n",
            "           Create_priv: N\n",
            "             Drop_priv: N\n",
            "           Reload_priv: N\n",
            "         Shutdown_priv: N\n",
            "          Process_priv: N\n",
            "             File_priv: N\n",
            "            Grant_priv: N\n",
            "       References_priv: N\n",
            "            Index_priv: N\n",
            "            Alter_priv: N\n",
            "          Show_db_priv: N\n",
            "            Super_priv: N\n",
            " Create_tmp_table_priv: N\n",
            "      Lock_tables_priv: N\n",
            "          Execute_priv: N\n",
            "       Repl_slave_priv: N\n",
            "      Repl_client_priv: N\n",
            "      Create_view_priv: N\n",
            "        Show_view_priv: N\n",
            "   Create_routine_priv: N\n",
            "    Alter_routine_priv: N\n",
            "      Create_user_priv: N\n",
            "            Event_priv: N\n",
            "          Trigger_priv: N\n",
            "Create_tablespace_priv: N\n",
            "              ssl_type: \n",
            "       HEX(ssl_cipher): \n",
            "      HEX(x509_issuer): \n",
            "     HEX(x509_subject): \n",
            "         max_questions: 0\n",
            "           max_updates: 0\n",
            "       max_connections: 0\n",
            "  max_user_connections: 0\n",
            "                plugin: mysql_native_password\n",
            " authentication_string: NULL\n",
            "      password_expired: N\n",
            "*************************** 6. row ***************************\n",
            "                  Host: master.box\n",
            "                  User: \n",
            "              Password: \n",
            "           Select_priv: N\n",
            "           Insert_priv: N\n",
            "           Update_priv: N\n",
            "           Delete_priv: N\n",
            "           Create_priv: N\n",
            "             Drop_priv: N\n",
            "           Reload_priv: N\n",
            "         Shutdown_priv: N\n",
            "          Process_priv: N\n",
            "             File_priv: N\n",
            "            Grant_priv: N\n",
            "       References_priv: N\n",
            "            Index_priv: N\n",
            "            Alter_priv: N\n",
            "          Show_db_priv: N\n",
            "            Super_priv: N\n",
            " Create_tmp_table_priv: N\n",
            "      Lock_tables_priv: N\n",
            "          Execute_priv: N\n",
            "       Repl_slave_priv: N\n",
            "      Repl_client_priv: N\n",
            "      Create_view_priv: N\n",
            "        Show_view_priv: N\n",
            "   Create_routine_priv: N\n",
            "    Alter_routine_priv: N\n",
            "      Create_user_priv: N\n",
            "            Event_priv: N\n",
            "          Trigger_priv: N\n",
            "Create_tablespace_priv: N\n",
            "              ssl_type: \n",
            "       HEX(ssl_cipher): \n",
            "      HEX(x509_issuer): \n",
            "     HEX(x509_subject): \n",
            "         max_questions: 0\n",
            "           max_updates: 0\n",
            "       max_connections: 0\n",
            "  max_user_connections: 0\n",
            "                plugin: mysql_native_password\n",
            " authentication_string: NULL\n",
            "      password_expired: N\n",
        ],
        [
            "*************************** 1. row ***************************\n",
            "                  Host: localhost\n",
            "                  User: root\n",
            "              Password: \n",
            "           Select_priv: Y\n",
            "           Insert_priv: Y\n",
            "           Update_priv: Y\n",
            "           Delete_priv: Y\n",
            "           Create_priv: Y\n",
            "             Drop_priv: Y\n",
            "           Reload_priv: Y\n",
            "         Shutdown_priv: Y\n",
            "          Process_priv: Y\n",
            "             File_priv: Y\n",
            "            Grant_priv: Y\n",
            "       References_priv: Y\n",
            "            Index_priv: Y\n",
            "            Alter_priv: Y\n",
            "          Show_db_priv: Y\n",
            "            Super_priv: Y\n",
            " Create_tmp_table_priv: Y\n",
            "      Lock_tables_priv: Y\n",
            "          Execute_priv: Y\n",
            "       Repl_slave_priv: Y\n",
            "      Repl_client_priv: Y\n",
            "      Create_view_priv: Y\n",
            "        Show_view_priv: Y\n",
            "   Create_routine_priv: Y\n",
            "    Alter_routine_priv: Y\n",
            "      Create_user_priv: Y\n",
            "            Event_priv: Y\n",
            "          Trigger_priv: Y\n",
            "Create_tablespace_priv: Y\n",
            "              ssl_type: \n",
            "       HEX(ssl_cipher): \n",
            "      HEX(x509_issuer): \n",
            "     HEX(x509_subject): \n",
            "         max_questions: 0\n",
            "           max_updates: 0\n",
            "       max_connections: 0\n",
            "  max_user_connections: 0\n",
            "                plugin: mysql_native_password\n",
            " authentication_string: \n",
            "      password_expired: N\n",
            "*************************** 2. row ***************************\n",
            "                  Host: slave.box\n",
            "                  User: root\n",
            "              Password: \n",
            "           Select_priv: Y\n",
            "           Insert_priv: Y\n",
            "           Update_priv: Y\n",
            "           Delete_priv: Y\n",
            "           Create_priv: Y\n",
            "             Drop_priv: Y\n",
            "           Reload_priv: Y\n",
            "         Shutdown_priv: Y\n",
            "          Process_priv: Y\n",
            "             File_priv: Y\n",
            "            Grant_priv: Y\n",
            "       References_priv: Y\n",
            "            Index_priv: Y\n",
            "            Alter_priv: Y\n",
            "          Show_db_priv: Y\n",
            "            Super_priv: Y\n",
            " Create_tmp_table_priv: Y\n",
            "      Lock_tables_priv: Y\n",
            "          Execute_priv: Y\n",
            "       Repl_slave_priv: Y\n",
            "      Repl_client_priv: Y\n",
            "      Create_view_priv: Y\n",
            "        Show_view_priv: Y\n",
            "   Create_routine_priv: Y\n",
            "    Alter_routine_priv: Y\n",
            "      Create_user_priv: Y\n",
            "            Event_priv: Y\n",
            "          Trigger_priv: Y\n",
            "Create_tablespace_priv: Y\n",
            "              ssl_type: \n",
            "       HEX(ssl_cipher): \n",
            "      HEX(x509_issuer): \n",
            "     HEX(x509_subject): \n",
            "         max_questions: 0\n",
            "           max_updates: 0\n",
            "       max_connections: 0\n",
            "  max_user_connections: 0\n",
            "                plugin: mysql_native_password\n",
            " authentication_string: \n",
            "      password_expired: N\n",
            "*************************** 3. row ***************************\n",
            "                  Host: 127.0.0.1\n",
            "                  User: root\n",
            "              Password: \n",
            "           Select_priv: Y\n",
            "           Insert_priv: Y\n",
            "           Update_priv: Y\n",
            "           Delete_priv: Y\n",
            "           Create_priv: Y\n",
            "             Drop_priv: Y\n",
            "           Reload_priv: Y\n",
            "         Shutdown_priv: Y\n",
            "          Process_priv: Y\n",
            "             File_priv: Y\n",
            "            Grant_priv: Y\n",
            "       References_priv: Y\n",
            "            Index_priv: Y\n",
            "            Alter_priv: Y\n",
            "          Show_db_priv: Y\n",
            "            Super_priv: Y\n",
            " Create_tmp_table_priv: Y\n",
            "      Lock_tables_priv: Y\n",
            "          Execute_priv: Y\n",
            "       Repl_slave_priv: Y\n",
            "      Repl_client_priv: Y\n",
            "      Create_view_priv: Y\n",
            "        Show_view_priv: Y\n",
            "   Create_routine_priv: Y\n",
            "    Alter_routine_priv: Y\n",
            "      Create_user_priv: Y\n",
            "            Event_priv: Y\n",
            "          Trigger_priv: Y\n",
            "Create_tablespace_priv: Y\n",
            "              ssl_type: \n",
            "       HEX(ssl_cipher): \n",
            "      HEX(x509_issuer): \n",
            "     HEX(x509_subject): \n",
            "         max_questions: 0\n",
            "           max_updates: 0\n",
            "       max_connections: 0\n",
            "  max_user_connections: 0\n",
            "                plugin: mysql_native_password\n",
            " authentication_string: \n",
            "      password_expired: N\n",
            "*************************** 4. row ***************************\n",
            "                  Host: ::1\n",
            "                  User: root\n",
            "              Password: \n",
            "           Select_priv: Y\n",
            "           Insert_priv: Y\n",
            "           Update_priv: Y\n",
            "           Delete_priv: Y\n",
            "           Create_priv: Y\n",
            "             Drop_priv: Y\n",
            "           Reload_priv: Y\n",
            "         Shutdown_priv: Y\n",
            "          Process_priv: Y\n",
            "             File_priv: Y\n",
            "            Grant_priv: Y\n",
            "       References_priv: Y\n",
            "            Index_priv: Y\n",
            "            Alter_priv: Y\n",
            "          Show_db_priv: Y\n",
            "            Super_priv: Y\n",
            " Create_tmp_table_priv: Y\n",
            "      Lock_tables_priv: Y\n",
            "          Execute_priv: Y\n",
            "       Repl_slave_priv: Y\n",
            "      Repl_client_priv: Y\n",
            "      Create_view_priv: Y\n",
            "        Show_view_priv: Y\n",
            "   Create_routine_priv: Y\n",
            "    Alter_routine_priv: Y\n",
            "      Create_user_priv: Y\n",
            "            Event_priv: Y\n",
            "          Trigger_priv: Y\n",
            "Create_tablespace_priv: Y\n",
            "              ssl_type: \n",
            "       HEX(ssl_cipher): \n",
            "      HEX(x509_issuer): \n",
            "     HEX(x509_subject): \n",
            "         max_questions: 0\n",
            "           max_updates: 0\n",
            "       max_connections: 0\n",
            "  max_user_connections: 0\n",
            "                plugin: mysql_native_password\n",
            " authentication_string: \n",
            "      password_expired: N\n",
            "*************************** 5. row ***************************\n",
            "                  Host: localhost\n",
            "                  User: \n",
            "              Password: \n",
            "           Select_priv: N\n",
            "           Insert_priv: N\n",
            "           Update_priv: N\n",
            "           Delete_priv: N\n",
            "           Create_priv: N\n",
            "             Drop_priv: N\n",
            "           Reload_priv: N\n",
            "         Shutdown_priv: N\n",
            "          Process_priv: N\n",
            "             File_priv: N\n",
            "            Grant_priv: N\n",
            "       References_priv: N\n",
            "            Index_priv: N\n",
            "            Alter_priv: N\n",
            "          Show_db_priv: N\n",
            "            Super_priv: N\n",
            " Create_tmp_table_priv: N\n",
            "      Lock_tables_priv: N\n",
            "          Execute_priv: N\n",
            "       Repl_slave_priv: N\n",
            "      Repl_client_priv: N\n",
            "      Create_view_priv: N\n",
            "        Show_view_priv: N\n",
            "   Create_routine_priv: N\n",
            "    Alter_routine_priv: N\n",
            "      Create_user_priv: N\n",
            "            Event_priv: N\n",
            "          Trigger_priv: N\n",
            "Create_tablespace_priv: N\n",
            "              ssl_type: \n",
            "       HEX(ssl_cipher): \n",
            "      HEX(x509_issuer): \n",
            "     HEX(x509_subject): \n",
            "         max_questions: 0\n",
            "           max_updates: 0\n",
            "       max_connections: 0\n",
            "  max_user_connections: 0\n",
            "                plugin: mysql_native_password\n",
            " authentication_string: NULL\n",
            "      password_expired: N\n",
            "*************************** 6. row ***************************\n",
            "                  Host: slave.box\n",
            "                  User: \n",
            "              Password: \n",
            "           Select_priv: N\n",
            "           Insert_priv: N\n",
            "           Update_priv: N\n",
            "           Delete_priv: N\n",
            "           Create_priv: N\n",
            "             Drop_priv: N\n",
            "           Reload_priv: N\n",
            "         Shutdown_priv: N\n",
            "          Process_priv: N\n",
            "             File_priv: N\n",
            "            Grant_priv: N\n",
            "       References_priv: N\n",
            "            Index_priv: N\n",
            "            Alter_priv: N\n",
            "          Show_db_priv: N\n",
            "            Super_priv: N\n",
            " Create_tmp_table_priv: N\n",
            "      Lock_tables_priv: N\n",
            "          Execute_priv: N\n",
            "       Repl_slave_priv: N\n",
            "      Repl_client_priv: N\n",
            "      Create_view_priv: N\n",
            "        Show_view_priv: N\n",
            "   Create_routine_priv: N\n",
            "    Alter_routine_priv: N\n",
            "      Create_user_priv: N\n",
            "            Event_priv: N\n",
            "          Trigger_priv: N\n",
            "Create_tablespace_priv: N\n",
            "              ssl_type: \n",
            "       HEX(ssl_cipher): \n",
            "      HEX(x509_issuer): \n",
            "     HEX(x509_subject): \n",
            "         max_questions: 0\n",
            "           max_updates: 0\n",
            "       max_connections: 0\n",
            "  max_user_connections: 0\n",
            "                plugin: mysql_native_password\n",
            " authentication_string: NULL\n",
            "      password_expired: N\n",
        ],
        "@@ -43,7 +43,7 @@\n"
        "  authentication_string: \n"
        "       password_expired: N\n"
        " *************************** 2. row ***************************\n"
        "-                  Host: master.box\n"
        "+                  Host: slave.box\n"
        "                   User: root\n"
        "               Password: \n"
        "            Select_priv: Y\n"
        "@@ -219,7 +219,7 @@\n"
        "  authentication_string: NULL\n"
        "       password_expired: N\n"
        " *************************** 6. row ***************************\n"
        "-                  Host: master.box\n"
        "+                  Host: slave.box\n"
        "                   User: \n"
        "               Password: \n"
        "            Select_priv: N\n"
    )
])
def test_diff(master_lines, slave_lines, difference):

    actual_diff = diff(master_lines, slave_lines)
    assert actual_diff == difference


@mock.patch('twindb_table_compare.compare.Popen')
def test_print_vertical(mock_popen, out_master, out_slave):
    mock_proc = mock.Mock()
    mock_proc.communicate.side_effect = [out_master, out_slave]
    mock_proc.returncode = 0

    mock_popen.return_value = mock_proc
    assert print_vertical('foo1', 'foo2', 'foo3', 'foo4', 'foo5',
                          color=False) == """@@ -43,7 +43,7 @@
  authentication_string:
       password_expired: N
 **************************************************************
-                  Host: master.box
+                  Host: slave.box
                   User: root
               Password:
            Select_priv: Y
@@ -219,7 +219,7 @@
  authentication_string: NULL
       password_expired: N
 **************************************************************
-                  Host: master.box
+                  Host: slave.box
                   User:
               Password:
            Select_priv: N
"""


@pytest.mark.parametrize('fields, result', [
    (
        (
            ('Host', 'char'),
            ('User', 'char'),
            ('Proxied_host', 'char'),
            ('Proxied_user', 'char'),
            ('With_grant', 'tinyint'),
            ('Grantor', 'char'),
            ('Timestamp', 'timestamp')
        ),
        'Host, User, Proxied_host, Proxied_user, With_grant, Grantor, Timestamp'
    ),
    (
        (
            ('f1', 'char'),
            ('f2', 'blob')
        ),
        'f1, HEX(f2)'
    ),
    (
        (
            ('f1', 'char'),
            ('f2', 'BLOB')
        ),
        'f1, HEX(f2)'
    ),
    (
        (
            ('f1', 'char'),
            ('f2', 'mediumblob')
        ),
        'f1, HEX(f2)'
    ),
    (
        (
            ('f1', 'char'),
            ('f2', 'BINARY'),
            ('f2', 'VARBINARY'),
            ('f2', 'TINYBLOB'),
            ('f2', 'BLOB'),
            ('f2', 'MEDIUMBLOB'),
            ('f2', 'LONGBLOB'),
        ),
        'f1, HEX(f2), HEX(f2), HEX(f2), HEX(f2), HEX(f2), HEX(f2)'
    )
])
def test_get_fileds(fields, result):
    mock_conn = mock.Mock()
    mock_cursor = mock.Mock()
    mock_cursor.fetchall.return_value = fields
    mock_conn.cursor.return_value = mock_cursor
    assert get_fileds(mock_conn, 'foo', 'bar') == result
