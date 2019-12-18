#!/usr/bin/python
# Classification (U)

"""Program:  find_dt_pos.py

    Description:  Unit testing of find_dt_pos in mysql_log_admin.py.

    Usage:
        test/unit/mysql_log_admin/find_dt_pos.py

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
import re

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
        self.sql_pass = "pwd"
        self.host = "hostname"
        self.port = 3306
        self.crc = "CRC32"


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp -> Initialize testing environment.
        test_match_query -> Test with group match is query.
        test_match_start -> Test with group match is start of line.
        test_crc_32_match -> Test with CRC set to CRC32 and re.match.
        test_crc_none -> Test with CRC set to None.
        test_crc_32 -> Test with CRC set to CRC32.
        test_fetch_binlog_data -> Test with list from fetch_binlog.
        test_fetch_binlog_empty -> Test with empty list from fetch_binlog.
        test_opt_arg_list -> Test with opt_arg_list argument passed.
        test_binpath -> Test with bin_path argument passed.
        test_find_dt_pos -> Test with only default arguments passed.

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.master = Server()
        self.filehandler = ["binlog1"]
        self.binlog_files = [{"Log_name": "binlog1"}, {"Log_name": "binlog2"}]
        self.opt_arg_list = ["--force-read", "--read-from-remote-server"]
        self.start_dt = "start_datetime_format"
        self.stop_dt = "end_datetime_format"
        self.fetch_log = ["data line here"]

        self.m1 = re.match(r"(?P<type>\w+)\s+(?P<epos>\w+)", "Start line")
        self.m2 = re.match(r"(?P<type>\w+)\s+(?P<epos>\w+)", "Query 123")

    @mock.patch("mysql_log_admin.mysql_class.Position",
                mock.Mock(return_value="Position"))
    @mock.patch("mysql_log_admin.re.match")
    @mock.patch("mysql_log_admin.fetch_binlog")
    @mock.patch("mysql_log_admin.mysql_libs.fetch_logs")
    def test_match_query(self, mock_fetch, mock_binlog, mock_match):

        """Function:  test_match_query

        Description:  Test with group match is query.

        Arguments:

        """

        mock_fetch.return_value = self.binlog_files
        mock_binlog.return_value = self.fetch_log
        mock_match.return_value = self.m2

        self.assertEqual(mysql_log_admin.find_dt_pos(
            self.master, self.start_dt, self.stop_dt), "Position")

    @mock.patch("mysql_log_admin.mysql_class.Position",
                mock.Mock(return_value="Position"))
    @mock.patch("mysql_log_admin.re.match")
    @mock.patch("mysql_log_admin.fetch_binlog")
    @mock.patch("mysql_log_admin.mysql_libs.fetch_logs")
    def test_match_start(self, mock_fetch, mock_binlog, mock_match):

        """Function:  test_match_start

        Description:  Test with group match is start of line.

        Arguments:

        """

        mock_fetch.return_value = self.binlog_files
        mock_binlog.return_value = self.fetch_log
        mock_match.return_value = self.m1

        self.assertEqual(mysql_log_admin.find_dt_pos(
            self.master, self.start_dt, self.stop_dt), "Position")

    @mock.patch("mysql_log_admin.mysql_class.Position",
                mock.Mock(return_value="Position"))
    @mock.patch("mysql_log_admin.re.match")
    @mock.patch("mysql_log_admin.fetch_binlog")
    @mock.patch("mysql_log_admin.mysql_libs.fetch_logs")
    def test_crc_32_match(self, mock_fetch, mock_binlog, mock_match):

        """Function:  test_crc_32_match

        Description:  Test with CRC set to CRC32 and re.match.

        Arguments:

        """

        mock_fetch.return_value = self.binlog_files
        mock_binlog.return_value = self.fetch_log
        mock_match.return_value = self.m1

        self.assertEqual(mysql_log_admin.find_dt_pos(
            self.master, self.start_dt, self.stop_dt), "Position")

    @mock.patch("mysql_log_admin.mysql_class.Position",
                mock.Mock(return_value="Position"))
    @mock.patch("mysql_log_admin.fetch_binlog")
    @mock.patch("mysql_log_admin.mysql_libs.fetch_logs")
    def test_crc_none(self, mock_fetch, mock_binlog):

        """Function:  test_crc_none

        Description:  Test with CRC set to None.

        Arguments:

        """

        mock_fetch.return_value = self.binlog_files
        mock_binlog.return_value = self.fetch_log

        self.master.crc = None

        self.assertEqual(mysql_log_admin.find_dt_pos(
            self.master, self.start_dt, self.stop_dt), "Position")

    @mock.patch("mysql_log_admin.mysql_class.Position",
                mock.Mock(return_value="Position"))
    @mock.patch("mysql_log_admin.fetch_binlog")
    @mock.patch("mysql_log_admin.mysql_libs.fetch_logs")
    def test_crc_32(self, mock_fetch, mock_binlog):

        """Function:  test_crc_32

        Description:  Test with CRC set to CRC32.

        Arguments:

        """

        mock_fetch.return_value = self.binlog_files
        mock_binlog.return_value = self.fetch_log

        self.assertEqual(mysql_log_admin.find_dt_pos(
            self.master, self.start_dt, self.stop_dt), "Position")

    @mock.patch("mysql_log_admin.mysql_class.Position",
                mock.Mock(return_value="Position"))
    @mock.patch("mysql_log_admin.fetch_binlog")
    @mock.patch("mysql_log_admin.mysql_libs.fetch_logs")
    def test_fetch_binlog_data(self, mock_fetch, mock_binlog):

        """Function:  test_fetch_binlog_data

        Description:  Test with list from fetch_binlog.

        Arguments:

        """

        mock_fetch.return_value = self.binlog_files
        mock_binlog.return_value = self.fetch_log

        self.assertEqual(mysql_log_admin.find_dt_pos(
            self.master, self.start_dt, self.stop_dt), "Position")

    @mock.patch("mysql_log_admin.mysql_class.Position",
                mock.Mock(return_value="Position"))
    @mock.patch("mysql_log_admin.fetch_binlog")
    @mock.patch("mysql_log_admin.mysql_libs.fetch_logs")
    def test_fetch_binlog_empty(self, mock_fetch, mock_binlog):

        """Function:  test_fetch_binlog_empty

        Description:  Test with empty list from fetch_binlog.

        Arguments:

        """

        mock_fetch.return_value = self.binlog_files
        mock_binlog.return_value = []

        self.assertEqual(mysql_log_admin.find_dt_pos(
            self.master, self.start_dt, self.stop_dt), "Position")

    @mock.patch("mysql_log_admin.mysql_class.Position",
                mock.Mock(return_value="Position"))
    @mock.patch("mysql_log_admin.fetch_binlog")
    @mock.patch("mysql_log_admin.mysql_libs.fetch_logs")
    def test_opt_arg_list(self, mock_fetch, mock_binlog):

        """Function:  test_opt_arg_list

        Description:  Test with opt_arg_list argument passed.

        Arguments:

        """

        mock_fetch.return_value = self.binlog_files
        mock_binlog.return_value = []

        self.assertEqual(mysql_log_admin.find_dt_pos(
            self.master, self.start_dt, self.stop_dt, bin_path="./",
            opt_arg_list=self.opt_arg_list),
                         "Position")

    @mock.patch("mysql_log_admin.mysql_class.Position",
                mock.Mock(return_value="Position"))
    @mock.patch("mysql_log_admin.fetch_binlog")
    @mock.patch("mysql_log_admin.mysql_libs.fetch_logs")
    def test_binpath(self, mock_fetch, mock_binlog):

        """Function:  test_binpath

        Description:  Test with bin_path argument passed.

        Arguments:

        """

        mock_fetch.return_value = self.binlog_files
        mock_binlog.return_value = []

        self.assertEqual(mysql_log_admin.find_dt_pos(
            self.master, self.start_dt, self.stop_dt, bin_path="./"),
                         "Position")

    @mock.patch("mysql_log_admin.mysql_class.Position",
                mock.Mock(return_value="Position"))
    @mock.patch("mysql_log_admin.fetch_binlog")
    @mock.patch("mysql_log_admin.mysql_libs.fetch_logs")
    def test_find_dt_pos(self, mock_fetch, mock_binlog):

        """Function:  test_find_dt_pos

        Description:  Test with only default arguments passed.

        Arguments:

        """

        mock_fetch.return_value = self.binlog_files
        mock_binlog.return_value = []

        self.assertEqual(mysql_log_admin.find_dt_pos(
            self.master, self.start_dt, self.stop_dt), "Position")


if __name__ == "__main__":
    unittest.main()
