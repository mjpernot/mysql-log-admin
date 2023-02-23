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
import unittest
import re
import mock

# Local
sys.path.append(os.getcwd())
import mysql_log_admin
import lib.gen_libs as gen_libs
import version

__version__ = version.__version__


class Slave(object):

    """Class:  Slave

    Description:  Class stub holder for mysql_class.Slave class.

    Methods:
        __init__

    """

    def __init__(self):

        """Method:  __init__

        Description:  Class initialization.

        Arguments:

        """

        self.relay_mst_log = "binlog2"
        self.sql_user = "mysql"
        self.host = "hostname"
        self.port = 3306
        self.crc = "CRC32"


class Server(object):

    """Class:  Server

    Description:  Class stub holder for mysql_class.Server class.

    Methods:
        __init__

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
        self.crc = "CRC32"


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp
        test_slave
        test_match_query
        test_match_start
        test_crc_32_match
        test_crc_none
        test_crc_32
        test_fetch_binlog_data
        test_fetch_binlog_empty
        test_opt_arg_list
        test_binpath
        test_find_dt_pos

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        rem = gen_libs.get_inst(re)
        self.master = Server()
        self.slave = Slave()
        self.filehandler = ["binlog1"]
        self.binlog_files = [{"Log_name": "binlog1"}, {"Log_name": "binlog2"}]
        self.binlog_files2 = [{"Log_name": "binlog1"}, {"Log_name": "binlog2"},
                              {"Log_name": "binlog3"}]
        self.opt_arg_list = ["--force-read", "--read-from-remote-server"]
        self.start_dt = "start_datetime_format"
        self.stop_dt = "end_datetime_format"
        self.fetch_log = ["data line here"]

        self.match1 = rem.match(r"(?P<type>\w+)\s+(?P<epos>\w+)", "Start line")
        self.match2 = rem.match(r"(?P<type>\w+)\s+(?P<epos>\w+)", "Query 123")

    @mock.patch("mysql_log_admin.mysql_class.Position",
                mock.Mock(return_value="Position"))
    @mock.patch("mysql_log_admin.re.match")
    @mock.patch("mysql_log_admin.fetch_binlog")
    @mock.patch("mysql_log_admin.mysql_libs.fetch_logs")
    def test_slave(self, mock_fetch, mock_binlog, mock_match):

        """Function:  test_slave

        Description:  Test with slave database.

        Arguments:

        """

        mock_fetch.return_value = self.binlog_files2
        mock_binlog.return_value = self.fetch_log
        mock_match.return_value = self.match2

        self.assertEqual(
            mysql_log_admin.find_dt_pos(
                self.master, self.start_dt, self.stop_dt, slave=self.slave),
            "Position")

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
        mock_match.return_value = self.match2

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
        mock_match.return_value = self.match1

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
        mock_match.return_value = self.match1

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

        self.assertEqual(
            mysql_log_admin.find_dt_pos(
                self.master, self.start_dt, self.stop_dt, bin_path="./",
                opt_arg_list=self.opt_arg_list), "Position")

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

        self.assertEqual(
            mysql_log_admin.find_dt_pos(
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
