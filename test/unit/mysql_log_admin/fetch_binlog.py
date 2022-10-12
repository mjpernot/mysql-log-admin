# Classification (U)

"""Program:  fetch_binlog.py

    Description:  Unit testing of fetch_binlog in mysql_log_admin.py.

    Usage:
        test/unit/mysql_log_admin/fetch_binlog.py

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
import version

__version__ = version.__version__


class Popen(object):

    """Class:  Popen

    Description:  Class stub holder for subprocess.Popen class.

    Methods:
        __init__

    """

    def __init__(self):

        """Method:  __init__

        Description:  Class initialization.

        Arguments:

        """

        self.stdout = ["binlog1"]


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
        self.sql_pass = "japd"
        self.host = "hostname"
        self.port = 3306


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp
        test_stop_dt
        test_start_dt
        test_opt_arg_list
        test_binlog_files
        test_binpath
        test_fetch_binlog

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.server = Server()
        self.filehandler = ["binlog1"]
        self.binlog_files = [{"Log_name": "binlog1"}, {"Log_name": "binlog2"}]
        self.opt_arg_list = ["--force-read", "--read-from-remote-server"]
        self.start_dt = "start_datetime_format"
        self.stop_dt = "end_datetime_format"

    @mock.patch("mysql_log_admin.mysql_libs.fetch_logs")
    @mock.patch("mysql_log_admin.subprocess.Popen")
    def test_stop_dt(self, mock_sub, mock_fetch):

        """Function:  test_stop_dt

        Description:  Test with stop_dt argument passed.

        Arguments:

        """

        mock_sub.return_value = Popen()
        mock_fetch.return_value = self.binlog_files

        dataout = mysql_log_admin.fetch_binlog(
            self.server, bin_path="./", stop_dt=self.stop_dt)

        self.assertEqual([x for x in dataout], self.filehandler)

    @mock.patch("mysql_log_admin.mysql_libs.fetch_logs")
    @mock.patch("mysql_log_admin.subprocess.Popen")
    def test_start_dt(self, mock_sub, mock_fetch):

        """Function:  test_start_dt

        Description:  Test with start_dt argument passed.

        Arguments:

        """

        mock_sub.return_value = Popen()
        mock_fetch.return_value = self.binlog_files

        dataout = mysql_log_admin.fetch_binlog(
            self.server, bin_path="./", start_dt=self.start_dt)

        self.assertEqual([x for x in dataout], self.filehandler)

    @mock.patch("mysql_log_admin.mysql_libs.fetch_logs")
    @mock.patch("mysql_log_admin.subprocess.Popen")
    def test_opt_arg_list(self, mock_sub, mock_fetch):

        """Function:  test_opt_arg_list

        Description:  Test with opt_arg_list argument passed.

        Arguments:

        """

        mock_sub.return_value = Popen()
        mock_fetch.return_value = self.binlog_files

        dataout = mysql_log_admin.fetch_binlog(
            self.server, bin_path="./", opt_arg_list=self.opt_arg_list)

        self.assertEqual([x for x in dataout], self.filehandler)

    @mock.patch("mysql_log_admin.subprocess.Popen")
    def test_binlog_files(self, mock_sub):

        """Function:  test_binlog_files

        Description:  Test with binlog_files argument passed.

        Arguments:

        """

        mock_sub.return_value = Popen()

        dataout = mysql_log_admin.fetch_binlog(
            self.server, bin_path="./", binlog_files=self.binlog_files)

        self.assertEqual([x for x in dataout], self.filehandler)

    @mock.patch("mysql_log_admin.mysql_libs.fetch_logs")
    @mock.patch("mysql_log_admin.subprocess.Popen")
    def test_binpath(self, mock_sub, mock_fetch):

        """Function:  test_binpath

        Description:  Test with bin_path argument passed.

        Arguments:

        """

        mock_sub.return_value = Popen()
        mock_fetch.return_value = self.binlog_files

        dataout = mysql_log_admin.fetch_binlog(self.server, bin_path="./")

        self.assertEqual([x for x in dataout], self.filehandler)

    @mock.patch("mysql_log_admin.mysql_libs.fetch_logs")
    @mock.patch("mysql_log_admin.subprocess.Popen")
    def test_fetch_binlog(self, mock_sub, mock_fetch):

        """Function:  test_fetch_binlog

        Description:  Test with only default arguments passed.

        Arguments:

        """

        mock_sub.return_value = Popen()
        mock_fetch.return_value = self.binlog_files

        dataout = mysql_log_admin.fetch_binlog(self.server)

        self.assertEqual([x for x in dataout], self.filehandler)


if __name__ == "__main__":
    unittest.main()
