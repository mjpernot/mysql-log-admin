#!/usr/bin/python
# Classification (U)

"""Program:  load_log.py

    Description:  Unit testing of load_log in mysql_log_admin.py.

    Usage:
        test/unit/mysql_log_admin/load_log.py

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


class SubProcess(object):

    """Class:  SubProcess

    Description:  Class stub holder for subprocess class.

    Methods:
        __init__ -> Class initialization.
        wait -> Stub holder for subprocess subprocess.wait method.

    """

    def __init__(self):

        """Method:  __init__

        Description:  Class initialization.

        Arguments:

        """

        self.stdout = ["binlog1"]

    def wait(self):

        """Method:  wait

        Description:  Wait method.

        Arguments:

        """

        return True


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
        test_no_opt_arg_lists -> Test with empty opt_arg_list list.
        test_load_log -> Test with only default arguments passed.

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.server = Server()
        self.opt_arg_list = ["--force-read", "--read-from-remote-server"]
        self.args_array = {"-e": True, "-d": True, "-p": "/dir/patch",
                           "-s": True, "-t": True}

    @mock.patch("mysql_log_admin.cmds_gen.disconnect",
                mock.Mock(return_value=True))
    @mock.patch("mysql_log_admin.subprocess.Popen",
                mock.Mock(return_value=SubProcess()))
    @mock.patch("mysql_log_admin.fetch_binlog",
                mock.Mock(return_value="Process"))
    @mock.patch("mysql_log_admin.mysql_libs.crt_cmd",
                mock.Mock(return_value=["command", "options"]))
    @mock.patch("mysql_log_admin.mysql_libs.create_instance",
                mock.Mock(return_value=Server()))
    @mock.patch("mysql_log_admin.process_logs_list",
                mock.Mock(return_value=["binlog1", "binlog2"]))
    def test_no_opt_arg_lists(self):

        """Function:  test_no_opt_arg_lists

        Description:  Test with empty opt_arg_list list.

        Arguments:

        """

        self.assertFalse(mysql_log_admin.load_log(
            self.server, self.args_array, []))

    @mock.patch("mysql_log_admin.cmds_gen.disconnect",
                mock.Mock(return_value=True))
    @mock.patch("mysql_log_admin.subprocess.Popen",
                mock.Mock(return_value=SubProcess()))
    @mock.patch("mysql_log_admin.fetch_binlog",
                mock.Mock(return_value="Process"))
    @mock.patch("mysql_log_admin.mysql_libs.crt_cmd",
                mock.Mock(return_value=["command", "options"]))
    @mock.patch("mysql_log_admin.mysql_libs.create_instance",
                mock.Mock(return_value=Server()))
    @mock.patch("mysql_log_admin.process_logs_list",
                mock.Mock(return_value=["binlog1", "binlog2"]))
    def test_load_log(self):

        """Function:  test_load_log

        Description:  Test with only default arguments passed.

        Arguments:

        """

        self.assertFalse(mysql_log_admin.load_log(
            self.server, self.args_array, self.opt_arg_list))


if __name__ == "__main__":
    unittest.main()
