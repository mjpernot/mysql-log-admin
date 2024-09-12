# Classification (U)

"""Program:  fetch_log_entries.py

    Description:  Unit testing of fetch_log_entries in mysql_log_admin.py.

    Usage:
        test/unit/mysql_log_admin/fetch_log_entries.py

    Arguments:

"""

# Libraries and Global Variables

# Standard
import sys
import os
import unittest
import mock

# Local
sys.path.append(os.getcwd())
import mysql_log_admin
import lib.gen_libs as gen_libs
import version

__version__ = version.__version__


class ArgParser(object):

    """Class:  ArgParser

    Description:  Class stub holder for gen_class.ArgParser class.

    Methods:
        __init__
        get_val
        arg_set_path

    """

    def __init__(self):

        """Method:  __init__

        Description:  Class initialization.

        Arguments:

        """

        self.args_array = {"-s": True, "-t": True, "-p": "/dir/patch"}

    def get_val(self, skey, def_val=None):

        """Method:  get_val

        Description:  Method stub holder for gen_class.ArgParser.get_val.

        Arguments:

        """

        return self.args_array.get(skey, def_val)

    def arg_set_path(self, arg_opt):

        """Method:  arg_set_path

        Description:  Method stub holder for gen_class.ArgParser.arg_set_path.

        Arguments:

        """

        path = os.path.join(
            self.args_array[arg_opt] if arg_opt in self.args_array else "")

        return path


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


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp
        test_log_failure
        test_log_success
        test_no_binlogs
        test_fetch_log_entries

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.server = Server()
        self.args = ArgParser()
        self.opt_arg_list = ["--force-read", "--read-from-remote-server"]
        self.loglist = ["line1", "line2"]
        self.binlog_list = ["binarylog1", "binarylog2"]
        self.status = (True, None)
        self.status2 = (False, "Error Message")

    @mock.patch("mysql_log_admin.process_logs_list")
    @mock.patch("mysql_log_admin.fetch_binlog")
    def test_log_failure(self, mock_fetch, mock_logs):

        """Function:  test_log_failure

        Description:  Test with process_logs_list successful.

        Arguments:

        """

        mock_fetch.return_value = self.loglist
        mock_logs.return_value = self.status2, []

        with gen_libs.no_std_out():
            self.assertFalse(mysql_log_admin.fetch_log_entries(
                self.server, self.args, self.opt_arg_list))

    @mock.patch("mysql_log_admin.process_logs_list")
    @mock.patch("mysql_log_admin.fetch_binlog")
    def test_log_success(self, mock_fetch, mock_logs):

        """Function:  test_log_success

        Description:  Test with process_logs_list successful.

        Arguments:

        """

        mock_fetch.return_value = self.loglist
        mock_logs.return_value = self.status, self.binlog_list

        self.assertFalse(mysql_log_admin.fetch_log_entries(
            self.server, self.args, self.opt_arg_list))

    @mock.patch("mysql_log_admin.process_logs_list")
    @mock.patch("mysql_log_admin.fetch_binlog")
    def test_no_binlogs(self, mock_fetch, mock_logs):

        """Function:  test_no_binlogs

        Description:  Test with no binary logs detected.

        Arguments:

        """

        mock_fetch.return_value = []
        mock_logs.return_value = self.status, self.binlog_list

        self.assertFalse(mysql_log_admin.fetch_log_entries(
            self.server, self.args, self.opt_arg_list))

    @mock.patch("mysql_log_admin.process_logs_list")
    @mock.patch("mysql_log_admin.fetch_binlog")
    def test_fetch_log_entries(self, mock_fetch, mock_logs):

        """Function:  test_fetch_log_entries

        Description:  Test with only default arguments passed.

        Arguments:

        """

        mock_fetch.return_value = self.loglist
        mock_logs.return_value = self.status, self.binlog_list

        self.assertFalse(mysql_log_admin.fetch_log_entries(
            self.server, self.args, self.opt_arg_list))


if __name__ == "__main__":
    unittest.main()
