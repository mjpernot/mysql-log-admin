#!/usr/bin/python
# Classification (U)

"""Program:  run_program.py

    Description:  Unit testing of run_program in mysql_log_admin.py.

    Usage:
        test/unit/mysql_log_admin/run_program.py

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


def fetch_log_pos(server, args_array, opt_arg_list):

    """Method:  fetch_log_pos

    Description:  Stub holder for mysql_log_admin.fetch_log_pos function.

    Arguments:

    """

    status = True

    if server and args_array and opt_arg_list:
        status = True

    return status


class Server(object):

    """Class:  Server

    Description:  Class stub holder for mysql_class.Server class.

    Methods:
        __init__
        connect
        set_srv_binlog_crc

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
        self.name = "Server_Name"
        self.conn = "Connection Handler"
        self.conn_msg = None

    def connect(self, silent):

        """Method:  connect

        Description:  Method stub holder for mysql_class.Server.connect.

        Arguments:
            (input) silent

        """

        status = True

        if silent:
            status = True

        return status

    def set_srv_binlog_crc(self):

        """Method:  set_srv_binlog_crc

        Description:  Stub holder for mysql_class.Server.set_srv_binlog_crc.

        Arguments:

        """

        return True


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp
        test_connect_failure
        test_connect_successful
        test_run_program

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.opt_arg_list = ["--force-read", "--read-from-remote-server"]
        self.args_array = {"-c": True, "-d": True, "-L": True}
        self.func_dict = {"-L": fetch_log_pos}
        self.server = Server()

    @mock.patch("mysql_log_admin.mysql_libs.disconnect",
                mock.Mock(return_value=True))
    @mock.patch("mysql_log_admin.mysql_libs.create_instance")
    def test_connect_failure(self, mock_server):

        """Function:  test_connect_failure

        Description:  Test with failed connection.

        Arguments:

        """

        self.server.conn_msg = "Error connection message"

        mock_server.return_value = self.server

        with gen_libs.no_std_out():
            self.assertFalse(mysql_log_admin.run_program(
                self.args_array, self.func_dict, self.opt_arg_list))

    @mock.patch("mysql_log_admin.mysql_libs.disconnect",
                mock.Mock(return_value=True))
    @mock.patch("mysql_log_admin.mysql_libs.create_instance")
    def test_connect_successful(self, mock_server):

        """Function:  test_connect_successful

        Description:  Test with successful connection.

        Arguments:

        """

        mock_server.return_value = self.server

        self.assertFalse(mysql_log_admin.run_program(
            self.args_array, self.func_dict, self.opt_arg_list))

    @mock.patch("mysql_log_admin.mysql_libs.disconnect",
                mock.Mock(return_value=True))
    @mock.patch("mysql_log_admin.mysql_libs.create_instance")
    def test_run_program(self, mock_server):

        """Function:  test_run_program

        Description:  Test with only default arguments passed.

        Arguments:

        """

        mock_server.return_value = self.server

        self.assertFalse(mysql_log_admin.run_program(
            self.args_array, self.func_dict, self.opt_arg_list))


if __name__ == "__main__":
    unittest.main()
