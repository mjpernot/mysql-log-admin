#!/usr/bin/python
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


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp -> Initialize testing environment.
        test_fetch_binlog -> Test with only default argument passed.

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.server = Server()
        self.filehandler = "FileHandler"
        self.binlog_files = [{"Log_name": "binlog1"}, {"Log_name": "binlog2"}]

    @mock.patch("mysql_log_admin.mysql_libs.fetch_logs")
    @mock.patch("mysql_log_admin.subprocess.Popen")
    def test_fetch_binlog(self, mock_sub, mock_fetch):

        """Function:  test_fetch_binlog

        Description:  Test with only default argument passed.

        Arguments:

        """

        mock_sub.return_value = "FileHandler"
        mock_fetch.return_value = self.binlog_files

        self.assertEqual(mysql_log_admin.fetch_binlog(
            self.server, binlog_files=self.binlog_files, bin_path="./"),
                         self.filehandler)


if __name__ == "__main__":
    unittest.main()
