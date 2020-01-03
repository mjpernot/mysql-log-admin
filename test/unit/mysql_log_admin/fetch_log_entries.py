#!/usr/bin/python
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
        test_no_binlogs -> Test with no binary logs detected.
        test_fetch_log_entries -> Test with only default arguments passed.

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.server = Server()
        self.opt_arg_list = ["--force-read", "--read-from-remote-server"]
        self.args_array = {"-s": True, "-t": True, "-p": "/dir/patch"}
        self.loglist = ["binlog1", "binlog2"]

    @mock.patch("mysql_log_admin.fetch_binlog")
    def test_no_binlogs(self, mock_fetch):

        """Function:  test_no_binlogs

        Description:  Test with no binary logs detected.

        Arguments:

        """

        mock_fetch.return_value = []

        self.assertFalse(mysql_log_admin.fetch_log_entries(
            self.server, self.args_array, self.opt_arg_list))

    @mock.patch("mysql_log_admin.fetch_binlog")
    def test_fetch_log_entries(self, mock_fetch):

        """Function:  test_fetch_log_entries

        Description:  Test with only default arguments passed.

        Arguments:

        """

        mock_fetch.return_value = self.loglist

        with gen_libs.no_std_out():
            self.assertFalse(mysql_log_admin.fetch_log_entries(
                self.server, self.args_array, self.opt_arg_list))


if __name__ == "__main__":
    unittest.main()
