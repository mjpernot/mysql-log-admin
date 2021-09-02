#!/usr/bin/python
# Classification (U)

"""Program:  main.py

    Description:  Unit testing of main in mysql_log_admin.py.

    Usage:
        test/unit/mysql_log_admin/main.py

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


class ProgramLock(object):

    """Class:  ProgramLock

    Description:  Class stub holder for gen_class.ProgramLock class.

    Methods:
        __init__

    """

    def __init__(self, cmdline, flavor):

        """Method:  __init__

        Description:  Class initialization.

        Arguments:
            (input) cmdline
            (input) flavor

        """

        self.cmdline = cmdline
        self.flavor = flavor


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp
        test_help_true
        test_help_false
        test_arg_req_true
        test_arg_req_false
        test_arg_req_true
        test_arg_req_false
        test_arg_xor_false
        test_arg_xor_true
        test_arg_dir_true
        test_arg_dir_false
        test_arg_validate_false
        test_arg_validate_true
        test_arg_cond_req_false
        test_arg_cond_req_true
        test_run_program
        test_programlock_id
        test_programlock_false
        test_programlock_true

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.args_array = {"-c": "CfgFile", "-d": "CfgDir"}
        self.args_array2 = {"-c": "CfgFile", "-d": "CfgDir", "-y": "Flavor"}
        self.proglock = ProgramLock(["cmdline"], "FlavorID")

    @mock.patch("mysql_log_admin.gen_libs.help_func")
    @mock.patch("mysql_log_admin.arg_parser.arg_parse2")
    def test_help_true(self, mock_arg, mock_help):

        """Function:  test_help_true

        Description:  Test help if returns true.

        Arguments:

        """

        mock_arg.return_value = self.args_array
        mock_help.return_value = True

        self.assertFalse(mysql_log_admin.main())

    @mock.patch("mysql_log_admin.gen_libs.help_func")
    @mock.patch("mysql_log_admin.arg_parser")
    def test_help_false(self, mock_arg, mock_help):

        """Function:  test_help_false

        Description:  Test help if returns false.

        Arguments:

        """

        mock_arg.arg_parse2.return_value = self.args_array
        mock_help.return_value = False
        mock_arg.arg_require.return_value = True

        self.assertFalse(mysql_log_admin.main())

    @mock.patch("mysql_log_admin.gen_libs.help_func")
    @mock.patch("mysql_log_admin.arg_parser")
    def test_arg_req_true(self, mock_arg, mock_help):

        """Function:  test_arg_req_true

        Description:  Test arg_require if returns true.

        Arguments:

        """

        mock_arg.arg_parse2.return_value = self.args_array
        mock_help.return_value = False
        mock_arg.arg_require.return_value = True

        self.assertFalse(mysql_log_admin.main())

    @mock.patch("mysql_log_admin.gen_libs.help_func")
    @mock.patch("mysql_log_admin.arg_parser")
    def test_arg_req_false(self, mock_arg, mock_help):

        """Function:  test_arg_req_false

        Description:  Test arg_require if returns false.

        Arguments:

        """

        mock_arg.arg_parse2.return_value = self.args_array
        mock_help.return_value = False
        mock_arg.arg_require.return_value = False
        mock_arg.arg_xor_dict.return_value = False

        self.assertFalse(mysql_log_admin.main())

    @mock.patch("mysql_log_admin.gen_libs.help_func")
    @mock.patch("mysql_log_admin.arg_parser")
    def test_arg_xor_false(self, mock_arg, mock_help):

        """Function:  test_arg_xor_false

        Description:  Test arg_xor_dict if returns false.

        Arguments:

        """

        mock_arg.arg_parse2.return_value = self.args_array
        mock_help.return_value = False
        mock_arg.arg_require.return_value = False
        mock_arg.arg_xor_dict.return_value = False

        self.assertFalse(mysql_log_admin.main())

    @mock.patch("mysql_log_admin.gen_libs.help_func")
    @mock.patch("mysql_log_admin.arg_parser")
    def test_arg_xor_true(self, mock_arg, mock_help):

        """Function:  test_arg_xor_true

        Description:  Test arg_xor_dict if returns true.

        Arguments:

        """

        mock_arg.arg_parse2.return_value = self.args_array
        mock_help.return_value = False
        mock_arg.arg_require.return_value = False
        mock_arg.arg_xor_dict.return_value = True
        mock_arg.arg_dir_chk_crt.return_value = True

        self.assertFalse(mysql_log_admin.main())

    @mock.patch("mysql_log_admin.gen_libs.help_func")
    @mock.patch("mysql_log_admin.arg_parser")
    def test_arg_dir_true(self, mock_arg, mock_help):

        """Function:  test_arg_dir_true

        Description:  Test arg_dir_chk_crt if returns true.

        Arguments:

        """

        mock_arg.arg_parse2.return_value = self.args_array
        mock_help.return_value = False
        mock_arg.arg_require.return_value = False
        mock_arg.arg_valid_val.return_value = True
        mock_arg.arg_xor_dict.return_value = True
        mock_arg.arg_dir_chk_crt.return_value = True

        self.assertFalse(mysql_log_admin.main())

    @mock.patch("mysql_log_admin.gen_libs.help_func")
    @mock.patch("mysql_log_admin.arg_parser")
    def test_arg_dir_false(self, mock_arg, mock_help):

        """Function:  test_arg_dir_false

        Description:  Test arg_dir_chk_crt if returns false.

        Arguments:

        """

        mock_arg.arg_parse2.return_value = self.args_array
        mock_help.return_value = False
        mock_arg.arg_require.return_value = False
        mock_arg.arg_valid_val.return_value = True
        mock_arg.arg_xor_dict.return_value = True
        mock_arg.arg_dir_chk_crt.return_value = False
        mock_arg.arg_validate.return_value = False

        self.assertFalse(mysql_log_admin.main())

    @mock.patch("mysql_log_admin.gen_libs.help_func")
    @mock.patch("mysql_log_admin.arg_parser")
    def test_arg_validate_false(self, mock_arg, mock_help):

        """Function:  test_arg_validate_false

        Description:  Test arg_validate if returns false.

        Arguments:

        """

        mock_arg.arg_parse2.return_value = self.args_array
        mock_help.return_value = False
        mock_arg.arg_require.return_value = False
        mock_arg.arg_valid_val.return_value = True
        mock_arg.arg_xor_dict.return_value = True
        mock_arg.arg_dir_chk_crt.return_value = False
        mock_arg.arg_validate.return_value = False

        self.assertFalse(mysql_log_admin.main())

    @mock.patch("mysql_log_admin.gen_libs.help_func")
    @mock.patch("mysql_log_admin.arg_parser")
    def test_arg_validate_true(self, mock_arg, mock_help):

        """Function:  test_arg_validate_true

        Description:  Test arg_validate if returns true.

        Arguments:

        """

        mock_arg.arg_parse2.return_value = self.args_array
        mock_help.return_value = False
        mock_arg.arg_require.return_value = False
        mock_arg.arg_valid_val.return_value = True
        mock_arg.arg_xor_dict.return_value = True
        mock_arg.arg_dir_chk_crt.return_value = False
        mock_arg.arg_validate.return_value = True
        mock_arg.arg_cond_req.return_value = False

        self.assertFalse(mysql_log_admin.main())

    @mock.patch("mysql_log_admin.gen_libs.help_func")
    @mock.patch("mysql_log_admin.arg_parser")
    def test_arg_cond_req_false(self, mock_arg, mock_help):

        """Function:  test_cond_req_false

        Description:  Test arg_cond_req if returns false.

        Arguments:

        """

        mock_arg.arg_parse2.return_value = self.args_array
        mock_help.return_value = False
        mock_arg.arg_require.return_value = False
        mock_arg.arg_valid_val.return_value = True
        mock_arg.arg_xor_dict.return_value = True
        mock_arg.arg_dir_chk_crt.return_value = False
        mock_arg.arg_validate.return_value = True
        mock_arg.arg_cond_req.return_value = False

        self.assertFalse(mysql_log_admin.main())

    @mock.patch("mysql_log_admin.gen_class.ProgramLock")
    @mock.patch("mysql_log_admin.run_program")
    @mock.patch("mysql_log_admin.gen_libs.help_func")
    @mock.patch("mysql_log_admin.arg_parser")
    def test_arg_cond_req_true(self, mock_arg, mock_help, mock_run, mock_lock):

        """Function:  test_arg_cond_req_true

        Description:  Test arg_cond_req if returns true.

        Arguments:

        """

        mock_arg.arg_parse2.return_value = self.args_array
        mock_help.return_value = False
        mock_arg.arg_require.return_value = False
        mock_arg.arg_valid_val.return_value = True
        mock_arg.arg_xor_dict.return_value = True
        mock_arg.arg_dir_chk_crt.return_value = False
        mock_arg.arg_validate.return_value = True
        mock_arg.arg_cond_req.return_value = True
        mock_run.return_value = True
        mock_lock.return_value = self.proglock

        self.assertFalse(mysql_log_admin.main())

    @mock.patch("mysql_log_admin.gen_class.ProgramLock")
    @mock.patch("mysql_log_admin.run_program")
    @mock.patch("mysql_log_admin.gen_libs.help_func")
    @mock.patch("mysql_log_admin.arg_parser")
    def test_run_program(self, mock_arg, mock_help, mock_run, mock_lock):

        """Function:  test_run_program

        Description:  Test run_program function.

        Arguments:

        """

        mock_arg.arg_parse2.return_value = self.args_array
        mock_help.return_value = False
        mock_arg.arg_require.return_value = False
        mock_arg.arg_valid_val.return_value = True
        mock_arg.arg_xor_dict.return_value = True
        mock_arg.arg_dir_chk_crt.return_value = False
        mock_arg.arg_validate.return_value = True
        mock_arg.arg_cond_req.return_value = True
        mock_run.return_value = True
        mock_lock.return_value = self.proglock

        self.assertFalse(mysql_log_admin.main())

    @mock.patch("mysql_log_admin.gen_class.ProgramLock")
    @mock.patch("mysql_log_admin.run_program")
    @mock.patch("mysql_log_admin.gen_libs.help_func")
    @mock.patch("mysql_log_admin.arg_parser")
    def test_programlock_id(self, mock_arg, mock_help, mock_run, mock_lock):

        """Function:  test_programlock_id

        Description:  Test ProgramLock fails with flavor id.

        Arguments:

        """

        mock_arg.arg_parse2.return_value = self.args_array2
        mock_help.return_value = False
        mock_arg.arg_require.return_value = False
        mock_arg.arg_valid_val.return_value = True
        mock_arg.arg_xor_dict.return_value = True
        mock_arg.arg_dir_chk_crt.return_value = False
        mock_arg.arg_validate.return_value = True
        mock_arg.arg_cond_req.return_value = True
        mock_run.return_value = True
        mock_lock.return_value = self.proglock

        self.assertFalse(mysql_log_admin.main())

    @mock.patch("mysql_log_admin.gen_class.ProgramLock")
    @mock.patch("mysql_log_admin.gen_libs.help_func")
    @mock.patch("mysql_log_admin.arg_parser")
    def test_programlock_false(self, mock_arg, mock_help, mock_lock):

        """Function:  test_programlock_false

        Description:  Test with ProgramLock returns False.

        Arguments:

        """

        mock_arg.arg_parse2.return_value = self.args_array
        mock_help.return_value = False
        mock_arg.arg_require.return_value = False
        mock_arg.arg_valid_val.return_value = True
        mock_arg.arg_xor_dict.return_value = True
        mock_arg.arg_dir_chk_crt.return_value = False
        mock_arg.arg_validate.return_value = True
        mock_arg.arg_cond_req.return_value = True
        mock_lock.side_effect = \
            mysql_log_admin.gen_class.SingleInstanceException

        with gen_libs.no_std_out():
            self.assertFalse(mysql_log_admin.main())

    @mock.patch("mysql_log_admin.gen_class.ProgramLock")
    @mock.patch("mysql_log_admin.run_program")
    @mock.patch("mysql_log_admin.gen_libs.help_func")
    @mock.patch("mysql_log_admin.arg_parser")
    def test_programlock_true(self, mock_arg, mock_help, mock_run, mock_lock):

        """Function:  test_programlock_true

        Description:  Test with ProgramLock returns True.

        Arguments:

        """

        mock_arg.arg_parse2.return_value = self.args_array
        mock_help.return_value = False
        mock_arg.arg_require.return_value = False
        mock_arg.arg_valid_val.return_value = True
        mock_arg.arg_xor_dict.return_value = True
        mock_arg.arg_dir_chk_crt.return_value = False
        mock_arg.arg_validate.return_value = True
        mock_arg.arg_cond_req.return_value = True
        mock_run.return_value = True
        mock_lock.return_value = self.proglock

        self.assertFalse(mysql_log_admin.main())


if __name__ == "__main__":
    unittest.main()
