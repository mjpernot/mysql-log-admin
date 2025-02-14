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
import unittest
import mock

# Local
sys.path.append(os.getcwd())
import mysql_log_admin                          # pylint:disable=E0401,C0413
import lib.gen_libs as gen_libs             # pylint:disable=E0401,C0413,R0402
import version                                  # pylint:disable=E0401,C0413

__version__ = version.__version__


class ArgParser():

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

        self.args_array = {
            "-e": "mysql_cfg", "-d": "config", "-s": "start_time",
            "-t": "end_time", "-p": "/path"}

    def get_val(self, skey, def_val=None):

        """Method:  get_val

        Description:  Method stub holder for gen_class.ArgParser.get_val.

        Arguments:

        """

        return self.args_array.get(skey, def_val)

    def arg_set_path(self, arg_opt, cmd):

        """Method:  arg_set_path

        Description:  Method stub holder for gen_class.ArgParser.arg_set_path.

        Arguments:

        """

        path = os.path.join(
            self.args_array[arg_opt] if arg_opt in self.args_array else "",
            cmd)

        return path


class SubProcess():                                     # pylint:disable=R0903

    """Class:  SubProcess

    Description:  Class stub holder for subprocess class.

    Methods:
        __init__
        wait

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


class Server():                                         # pylint:disable=R0903

    """Class:  Server

    Description:  Class stub holder for mysql_class.Server class.

    Methods:
        __init__
        connect

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

        Description:  Connect method.

        Arguments:
            (input) silent

        """

        status = True

        if silent:
            status = True

        return status


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp
        test_connection_error
        test_connection_success
        test_list_fail
        test_no_opt_arg_lists
        test_load_log

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.server = Server()
        self.proc = SubProcess()
        self.args = ArgParser()
        self.opt_arg_list = ["--force-read", "--read-from-remote-server"]
        self.cmd_list = ["command", "options"]
        self.status = (True, None)
        self.status2 = (False, "Error Message")
        self.binlog_list = ["binlog1", "binlog2"]

    @mock.patch("mysql_log_admin.mysql_libs.create_instance")
    @mock.patch("mysql_log_admin.process_logs_list")
    def test_connection_error(self, mock_logs, mock_inst):

        """Function:  test_connection_error

        Description:  Test with connection error.

        Arguments:

        """

        self.server.conn_msg = "Connection error message"

        mock_logs.return_value = self.status, self.binlog_list
        mock_inst.return_value = self.server

        with gen_libs.no_std_out():
            self.assertFalse(mysql_log_admin.load_log(
                self.server, self.args, self.opt_arg_list))

    @mock.patch("mysql_log_admin.mysql_libs.disconnect",
                mock.Mock(return_value=True))
    @mock.patch("mysql_log_admin.subprocess.Popen")
    @mock.patch("mysql_log_admin.fetch_binlog")
    @mock.patch("mysql_log_admin.mysql_libs.crt_cmd")
    @mock.patch("mysql_log_admin.mysql_libs.create_instance")
    @mock.patch("mysql_log_admin.process_logs_list")
    def test_connection_success(                        # pylint:disable=R0913
            self, mock_logs, mock_inst, mock_cmd, mock_fetch, mock_popen):

        """Function:  test_connection_success

        Description:  Test with successful connection.

        Arguments:

        """

        mock_logs.return_value = self.status, self.binlog_list
        mock_inst.return_value = self.server
        mock_cmd.return_value = self.cmd_list
        mock_fetch.return_value = "Process"
        mock_popen.return_value = self.proc

        self.assertFalse(mysql_log_admin.load_log(
            self.server, self.args, self.opt_arg_list))

    @mock.patch("mysql_log_admin.process_logs_list")
    def test_list_fail(self, mock_logs):

        """Function:  test_list_fail

        Description:  Test with process_logs_list function fails.

        Arguments:

        """

        mock_logs.return_value = self.status2, self.binlog_list

        with gen_libs.no_std_out():
            self.assertFalse(mysql_log_admin.load_log(
                self.server, self.args, self.opt_arg_list))

    @mock.patch("mysql_log_admin.mysql_libs.disconnect",
                mock.Mock(return_value=True))
    @mock.patch("mysql_log_admin.subprocess.Popen")
    @mock.patch("mysql_log_admin.fetch_binlog")
    @mock.patch("mysql_log_admin.mysql_libs.crt_cmd")
    @mock.patch("mysql_log_admin.mysql_libs.create_instance")
    @mock.patch("mysql_log_admin.process_logs_list")
    def test_no_opt_arg_lists(                          # pylint:disable=R0913
            self, mock_logs, mock_inst, mock_cmd, mock_fetch, mock_popen):

        """Function:  test_no_opt_arg_lists

        Description:  Test with empty opt_arg_list list.

        Arguments:

        """

        mock_logs.return_value = self.status, self.binlog_list
        mock_inst.return_value = self.server
        mock_cmd.return_value = self.cmd_list
        mock_fetch.return_value = "Process"
        mock_popen.return_value = self.proc

        self.assertFalse(mysql_log_admin.load_log(
            self.server, self.args, []))

    @mock.patch("mysql_log_admin.mysql_libs.disconnect",
                mock.Mock(return_value=True))
    @mock.patch("mysql_log_admin.subprocess.Popen")
    @mock.patch("mysql_log_admin.fetch_binlog")
    @mock.patch("mysql_log_admin.mysql_libs.crt_cmd")
    @mock.patch("mysql_log_admin.mysql_libs.create_instance")
    @mock.patch("mysql_log_admin.process_logs_list")
    def test_load_log(                                  # pylint:disable=R0913
            self, mock_logs, mock_inst, mock_cmd, mock_fetch, mock_popen):

        """Function:  test_load_log

        Description:  Test with only default arguments passed.

        Arguments:

        """

        mock_logs.return_value = self.status, self.binlog_list
        mock_inst.return_value = self.server
        mock_cmd.return_value = self.cmd_list
        mock_fetch.return_value = "Process"
        mock_popen.return_value = self.proc

        self.assertFalse(mysql_log_admin.load_log(
            self.server, self.args, self.opt_arg_list))


if __name__ == "__main__":
    unittest.main()
