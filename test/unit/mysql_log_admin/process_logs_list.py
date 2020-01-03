#!/usr/bin/python
# Classification (U)

"""Program:  process_logs_list.py

    Description:  Unit testing of process_logs_list in mysql_log_admin.py.

    Usage:
        test/unit/mysql_log_admin/process_logs_list.py

    Arguments:

"""

# Libraries and Global Variables

# Standard
import sys
import os

if sys.version_info < (2, 7):
    import unittest2 as unittest
else:
    import unittest

# Third-party
import mock

# Local
sys.path.append(os.getcwd())
import mysql_log_admin
import lib.gen_libs as gen_libs
import version

__version__ = version.__version__


class Server(object):

    """Class:  Server

    Description:  Class stub holder for mysql_class.Server class.

    Methods:
        __init__ -> Class initialization.

    """

    def __init__(self):

        """Method:  __init__

        Description:  Class initialization.

        Arguments:

        """

        self.extra_def_file = None
        self.sql_user = "mysql"
        self.host = "hostname"
        self.port = 3306


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp -> Initialize testing environment.
        test_last_missing -> Test with last argument missing in binlog list.
        test_last_only -> Test with last argument only.
        test_first_missing -> Test with first argument missing in binlog list.
        test_first_only -> Test with first argument only.
        test_last_first -> Test with last before first passed.
        test_first_last -> Test with first and last arguments passed.
        test_process_logs_list -> Test with only default arguments passed.

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.server = Server()
        self.args_array = {"-f": "binlog-08", "-g": "binlog-10"}
        self.args_array2 = {"-f": "binlog-09", "-g": "binlog-08"}
        self.args_array3 = {"-f": "binlog-08"}
        self.args_array4 = {"-g": "binlog-10"}
        self.args_array5 = {"-f": "binlog-01"}
        self.args_array6 = {"-g": "binlog-12"}
        self.fetch_logs = [{"Log_name": "binlog-07"},
                           {"Log_name": "binlog-08"},
                           {"Log_name": "binlog-09"},
                           {"Log_name": "binlog-10"},
                           {"Log_name": "binlog-11"}]
        self.loglist = ["binlog-07", "binlog-08", "binlog-09", "binlog-10",
                        "binlog-11"]
        self.loglist2 = ["binlog-08", "binlog-09", "binlog-10"]
        self.loglist3 = ["binlog-08", "binlog-09", "binlog-10", "binlog-11"]
        self.loglist4 = ["binlog-07", "binlog-08", "binlog-09", "binlog-10"]

    @mock.patch("mysql_log_admin.sys.exit", mock.Mock(return_value=True))
    @mock.patch("mysql_log_admin.cmds_gen.disconnect",
                mock.Mock(return_value=True))
    @mock.patch("mysql_log_admin.mysql_libs.fetch_logs")
    def test_last_missing(self, mock_fetch):

        """Function:  test_last_missing

        Description:  Test with last argument missing in binlog list.

        Arguments:

        """

        mock_fetch.return_value = self.fetch_logs

        self.assertEqual(mysql_log_admin.process_logs_list(self.server,
                                                           self.args_array6),
                         self.loglist)

    @mock.patch("mysql_log_admin.mysql_libs.fetch_logs")
    def test_last_only(self, mock_fetch):

        """Function:  test_last_only

        Description:  Test with last argument only.

        Arguments:

        """

        mock_fetch.return_value = self.fetch_logs

        self.assertEqual(mysql_log_admin.process_logs_list(self.server,
                                                           self.args_array4),
                         self.loglist4)

    @mock.patch("mysql_log_admin.sys.exit", mock.Mock(return_value=True))
    @mock.patch("mysql_log_admin.cmds_gen.disconnect",
                mock.Mock(return_value=True))
    @mock.patch("mysql_log_admin.mysql_libs.fetch_logs")
    def test_first_missing(self, mock_fetch):

        """Function:  test_first_missing

        Description:  Test with first argument missing in binlog list.

        Arguments:

        """

        mock_fetch.return_value = self.fetch_logs

        self.assertEqual(mysql_log_admin.process_logs_list(self.server,
                                                           self.args_array5),
                         self.loglist)

    @mock.patch("mysql_log_admin.mysql_libs.fetch_logs")
    def test_first_only(self, mock_fetch):

        """Function:  test_first_only

        Description:  Test with first argument only.

        Arguments:

        """

        mock_fetch.return_value = self.fetch_logs

        self.assertEqual(mysql_log_admin.process_logs_list(self.server,
                                                           self.args_array3),
                         self.loglist3)

    @unittest.skip("Awaiting removal of sys.exit from function")
    # @mock.patch("mysql_log_admin.sys.exit", mock.Mock(return_value=True))
    def test_last_first(self):

        """Function:  test_last_first

        Description:  Test with last before first passed.

        Arguments:

        """

        self.assertEqual(mysql_log_admin.process_logs_list(self.server,
                                                           self.args_array2),
                         self.loglist)

    @mock.patch("mysql_log_admin.mysql_libs.fetch_logs")
    def test_first_last(self, mock_fetch):

        """Function:  test_first_last

        Description:  Test with first and last arguments passed.

        Arguments:

        """

        mock_fetch.return_value = self.fetch_logs

        self.assertEqual(mysql_log_admin.process_logs_list(self.server,
                                                           self.args_array),
                         self.loglist2)

    @mock.patch("mysql_log_admin.mysql_libs.fetch_logs")
    def test_process_logs_list(self, mock_fetch):

        """Function:  test_process_logs_list

        Description:  Test with only default arguments passed.

        Arguments:

        """

        mock_fetch.return_value = self.fetch_logs

        self.assertEqual(mysql_log_admin.process_logs_list(self.server, {}),
                         self.loglist)


if __name__ == "__main__":
    unittest.main()
