# Classification (U)

"""Program:  fetch_log_pos.py

    Description:  Unit testing of fetch_log_pos in mysql_log_admin.py.

    Usage:
        test/unit/mysql_log_admin/fetch_log_pos.py

    Arguments:

"""

# Libraries and Global Variables

# Standard
import sys
import os
import unittest
import collections
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
        test_opt_arg_list
        test_fetch_log_pos

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.server = Server()
        self.args = ArgParser()
        self.opt_arg_list = ["--force-read", "--read-from-remote-server"]
        position = collections.namedtuple("Position", "file pos")
        self.pos = position("Filename", "123")

    @mock.patch("mysql_log_admin.find_dt_pos")
    def test_opt_arg_list(self, mock_pos):

        """Function:  test_opt_arg_list

        Description:  Test with opt_arg_list arguments passed.

        Arguments:

        """

        mock_pos.return_value = self.pos

        with gen_libs.no_std_out():
            self.assertFalse(mysql_log_admin.fetch_log_pos(
                self.server, self.args, opt_arg_list=self.opt_arg_list))

    @mock.patch("mysql_log_admin.find_dt_pos")
    def test_fetch_log_pos(self, mock_pos):

        """Function:  test_fetch_log_pos

        Description:  Test with only default arguments passed.

        Arguments:

        """

        mock_pos.return_value = self.pos

        with gen_libs.no_std_out():
            self.assertFalse(
                mysql_log_admin.fetch_log_pos(self.server, self.args))


if __name__ == "__main__":
    unittest.main()
