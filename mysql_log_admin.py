#!/usr/bin/python
# Classification (U)

"""Program:  mysql_log_admin.py

    Description:  The program is an administration program for the MySQL binary
        log to include locating log positions, suspending slaves at a
        specific location, and printing logs.

    Usage:
        mysql_log_admin.py -c file -d path {-L | -D | -R {-e file}
            [-f file | -g file]} [-p path | -s datetime | -t datetime]
            [-v | -h]

    Arguments:
        -c file => Database configuration file.  Required arg.
        -d dir path => Directory path to config files.  Required arg.
        -L => Locate position in binary logs, if start and stop
            datetimes are NULL, then get current position.
        -D => Display log(s).  Will use a combination of start and stop
            datetimes along with log names.
        -R => Restore binary logs from a source database (-c to a
            target database (-e).  Requires args: -c and -e.
        -e file => Target database configuration file.
        -s "date time" => Start datetime.  Format:  YYYY-MM-DD HH:MM:SS
        -t "date time" => Stop datetime.  Format:  YYYY-MM-DD HH:MM:SS
        -f file => First binary log file name.
        -g file => Last binary log file name.
        -p dir path => Directory path to mysql programs.  Only required if the
            mysql binary programs do not run properly.  (i.e. not in the $PATH
            variable.)
        -v => Display version of this program.
        -h => Help and usage message.

        NOTE:  -v or -h overrides the other options.

    Notes:
        Database configuration file format (mysql_cfg.py):
            # Configuration file for {Database Name/Server}
            user = "root"
            passwd = "ROOT_PASSWORD"
            host = "IP_ADDRESS"
            serv_os = "Linux" or "Solaris"
            name = "HOSTNAME"
            port = PORT_NUMBER (default of mysql is 3306)
            cfg_file = "DIRECTORY_PATH/mysql.cfg"
            sid = "SERVER_ID"
            extra_def_file = "DIRECTORY_PATH/myextra.cfg"

        NOTE 1:  Include the cfg_file even if running remotely as the file will
            be used in future releases.

        NOTE 2:  In MySQL 5.6 - it now gives warning if password is passed on
            the command line.  To suppress this warning, will require the use
            of the --defaults-extra-file option (i.e. extra_def_file) in the
            database configuration file.  See below for the defaults-extra-file
            format.

        configuration modules -> name is runtime dependent as it can be used to
            connect to different databases with different names.

        Defaults Extra File format (mysql.cfg):
        password="ROOT_PASSWORD"
        socket="DIRECTORY_PATH/mysql.sock"

        NOTE:  The socket information can be obtained from the my.cnf file
            under ~/mysql directory.

    Example:
        mysql_log_admin.py -c database -d config -L

"""

# Libraries and Global Variables

# Standard
# For Python 2.6/2.7: Redirection of stdout in a print command.
from __future__ import print_function
import sys
import os
import subprocess
import re
import itertools

# Local
import lib.arg_parser as arg_parser
import lib.gen_libs as gen_libs
import lib.cmds_gen as cmds_gen
import mysql_lib.mysql_libs as mysql_libs
import mysql_lib.mysql_class as mysql_class
import version

__version__ = version.__version__


def help_message():

    """Function:  help_message

    Description:  Displays the program's docstring which is the help and usage
        message when -h option is selected.

    Arguments:

    """

    print(__doc__)


def fetch_binlog(server, start_dt=None, stop_dt=None, binlog_files=None,
                 opt_arg_list=None, bin_path=None, **kwargs):

    """Function:  fetch_binlog

    Description:  Returns a list of binary log entries based on the binary log
        file names passed and/or the start and/or stop datetimes.
        Returns the entries as a file.

    Arguments:
        (input) server -> Server instance.
        (input) start_dt -> Start datetime.
        (input) stop_dr -> Stop datetime.
        (input) binlog_files -> List of binary log names.
        (input) opt_arg_list ->  Arguments to be added to command line.
        (input) bin_path -> Path to Mysql binary directory.
        (output) -> File handler to list of log entries.

    """

    if binlog_files is None:
        # List of current binary logs.
        binlog_files = [row["Log_name"]
                        for row in mysql_libs.fetch_logs(server)]

    cmd = mysql_libs.crt_cmd(server, bin_path + "mysqlbinlog")

    if opt_arg_list:

        for arg in opt_arg_list:
            cmd = cmds_gen.add_cmd(cmd, arg=arg)

    if start_dt:
        cmd = cmds_gen.add_cmd(cmd, arg="--start-datetime=%s" % (start_dt))

    if stop_dt:
        cmd = cmds_gen.add_cmd(cmd, arg="--stop-datetime=%s" % (stop_dt))

    # Return a file handler with log entries.
    return iter(subprocess.Popen(cmd + binlog_files,
                                 stdout=subprocess.PIPE).stdout)


def find_dt_pos(master, start_dt, stop_dt, opt_arg_list=None, bin_path=None,
                slave=None, **kwargs):

    """Function:  find_dt_pos

    Description:  Gets all binary logs, unless a Slave is present.  Fetches all
        lines that match the start and stop datatimes and checks these
        entries for end log positions and returns the last end log
        position found along with the binary log name that it was found in.

    Arguments:
        (input) master -> Server instance or Master, if Slave present.
        (input) start_dt -> Start datetime.
        (input) stop_dt -> Stop datetime.
        (input) opt_arg_list ->  Arguments to be added to command line.
        (input) slave -> Slave server instance.
        (output) -> Position class (file, pos).

    """

    # List of current binary log names.
    log_files = [row["Log_name"] for row in mysql_libs.fetch_logs(master)]

    if slave:
        # Get only those binary log files up to the relay log file.
        efile = slave.relay_mst_log
        files = list(itertools.dropwhile(lambda file: file != efile,
                                         log_files))
        log_files = files

    # Get entries between start and stop datetimes.
    lines = fetch_binlog(master, start_dt, stop_dt, log_files, opt_arg_list,
                         bin_path)

    num_files = 0
    last_log_pos = None

    for x in lines:

        # Supports checksum and match for approriate format.
        if master.crc == "CRC32":
            m = re.match(r"#\d{6}\s+\d?\d:\d\d:\d\d\s+"
                         r"server id\s+(?P<sid>\d+)\s+"
                         r"end_log_pos\s+(?P<epos>\d+)\s+"
                         r"CRC32\s+(?P<crc>\w+)\s+"
                         r"(?P<type>\w+)", x)

        else:
            m = re.match(r"#\d{6}\s+\d?\d:\d\d:\d\d\s+"
                         r"server id\s+(?P<sid>\d+)\s+"
                         r"end_log_pos\s+(?P<epos>\d+)\s+"
                         r"(?P<type>\w+)", x)

        # If a line matches then see if the end_log_pos is Start (new file) or
        #   has found a Query within the datetime range requested.
        if m:
            # If matched line is at the start of the log.
            if m.group("type") == "Start":
                # Increase file position by 1.
                num_files += 1

            # If matched line is a Query
            if m.group("type") == "Query":
                # Capture position of the log.
                last_log_pos = m.group("epos")

    # Return file and position as a Position class.
    return mysql_class.Position(log_files[num_files - 1], last_log_pos)


def fetch_log_pos(server, args_array, opt_arg_list=None, **kwargs):

    """Function:  fetch_log_pos

    Description:  Gets the server's file name and position that are between the
        start and stop datetimes.

    Arguments:
        (input) server -> Server instance.
        (input) args_array -> Array of command line options and values.
        (input) opt_arg_list ->  Arguments to be added to command line.

    """

    # Get Position class from file and log position.
    pos = find_dt_pos(server, args_array.get("-s"), args_array.get("-t"),
                      opt_arg_list, arg_parser.arg_set_path(args_array, "-p"))

    print("Filename: {0}, Position: {1}".format(pos.file, pos.pos))


def fetch_log_entries(server, args_array, opt_arg_list, **kwargs):

    """Function:  fetch_log_entries

    Description:  Prints out the binary log entries that are between the start
        and stop datetimes.

    Arguments:
        (input) server -> Server instance.
        (input) args_array -> Array of command line options and values.
        (input) opt_arg_list ->  Arguments to be added to command line.

    """

    args_array = dict(args_array)
    opt_arg_list = list(opt_arg_list)
    lines = fetch_binlog(server, args_array.get("-s"), args_array.get("-t"),
                         opt_arg_list=opt_arg_list,
                         bin_path=arg_parser.arg_set_path(args_array, "-p"))

    for x in lines:
        print(x, end="")


def process_logs_list(server, args_array, **kwargs):

    """Function:  process_logs_list

    Description:  Get a list of binary log file names from the source database.
        Clean up the list if the -f and/or -g options are used.

    Arguments:
        (input) server -> Server instance.
        (input) args_array -> Array of command line options and values.
        (output) binlog_list -> List of binary log file names.

    """

    args_array = dict(args_array)

    # Is -f and -g in the argument list and in the correct order.
    if ("-f" in args_array and "-g" in args_array) \
       and args_array["-g"] < args_array["-f"]:

        sys.exit("Error:  Option -g: '%s' is before -f '%s'." %
                 (args_array["-g"], args_array["-f"]))

    binlog_list = gen_libs.dict_2_list(mysql_libs.fetch_logs(server),
                                       "Log_name")

    if "-f" in args_array and args_array["-f"] in binlog_list:
        # Remove any logs before log file name.
        while binlog_list[0] < args_array["-f"]:
            binlog_list.pop(0)

    elif "-f" in args_array:
        cmds_gen.disconnect(server)
        sys.exit("Error:  Option -f: '%s' not found in binary log list." %
                 (args_array["-f"]))

    if "-g" in args_array and args_array["-g"] in binlog_list:
        # Remove any logs after log file name.
        while binlog_list[-1] > args_array["-g"]:
            binlog_list.pop(-1)

    elif "-g" in args_array:
        cmds_gen.disconnect(server)
        sys.exit("Error:  Option -g: '%s' not found in binary log list." %
                 (args_array["-g"]))

    return binlog_list


def load_log(server, args_array, opt_arg_list, **kwargs):

    """Function:  load_log

    Description:  Get the binary logs from the source database, then fetch the
        revelant binary log entries and load them into the target
        database before closing all connections.

    Arguments:
        (input) server -> Server instance.
        (input) args_array -> Array of command line options and values.
        (input) opt_arg_list ->  Arguments to be added to command line.

    """

    args_array = dict(args_array)
    opt_arg_list = list(opt_arg_list)
    binlog_list = process_logs_list(server, args_array)
    target = mysql_libs.create_instance(args_array["-e"], args_array["-d"],
                                        mysql_class.Server)
    cmd = mysql_libs.crt_cmd(
        target, arg_parser.arg_set_path(args_array, "-p") + "mysql")

    # Fetch binary logs (server) and restore to destination database (target)
    #   Wait until the load process has completed, before continuing.
    P1 = fetch_binlog(server, args_array.get("-s"), args_array.get("-t"),
                      binlog_list, opt_arg_list,
                      arg_parser.arg_set_path(args_array, "-p"))
    P2 = subprocess.Popen(cmd, stdin=P1)
    P2.wait()

    cmds_gen.disconnect(server, target)


def run_program(args_array, func_dict, opt_arg_list, **kwargs):

    """Function:  run_program

    Description:  Creates class instance(s) and controls flow of the program.

    Arguments:
        (input) args_array -> Array of command line options and values.
        (input) func_dict -> Dictionary list of functions and options.
        (input) opt_arg_list ->  Arguments to be added to command line.

    """

    args_array = dict(args_array)
    func_dict = dict(func_dict)
    opt_arg_list = list(opt_arg_list)
    server = mysql_libs.create_instance(args_array["-c"], args_array["-d"],
                                        mysql_class.Server)
    server.connect()
    server.set_srv_binlog_crc()

    # Call function(s) - intersection of command line and function dict.
    for x in set(args_array.keys()) & set(func_dict.keys()):
        # Call the function requested.
        func_dict[x](server, args_array, opt_arg_list)

    cmds_gen.disconnect(server)


def main():

    """Function:  main

    Description:  Initializes program-wide used variables and processes command
        line arguments and values.

    Variables:
        dir_chk_list -> contains options which will be directories.
        func_dict -> dictionary list for the function calls or other options.
        opt_arg_list -> contains arguments to add to command line by default.
        opt_con_req_list -> contains the options that require other options.
        opt_req_list -> contains the options that are required for the program.
        opt_val_list -> contains options which require values.
        opt_valid_val -> contains list of types of values to be validated.
        opt_xor_dict -> contains options which are XOR with its values.

    Arguments:
        (input) argv -> Arguments from the command line.

    """

    dir_chk_list = ["-d", "-p"]
    func_dict = {"-L": fetch_log_pos, "-D": fetch_log_entries, "-R": load_log}
    opt_arg_list = ["--force-read", "--read-from-remote-server"]
    opt_con_req_list = {"-R": ["-e"]}
    opt_req_list = ["-c", "-d"]
    opt_val_list = ["-c", "-e", "-d", "-f", "-g", "-p", "-s", "-t"]
    opt_valid_val = {"-s": gen_libs.validate_date,
                     "-t": gen_libs.validate_date}
    opt_xor_dict = {"-L": ["-D", "-R"], "-D": ["-L", "-R"], "-R": ["-D", "-L"]}

    # Process argument list from command line.
    args_array = arg_parser.arg_parse2(sys.argv, opt_val_list)

    if not gen_libs.help_func(args_array, __version__, help_message) \
       and not arg_parser.arg_require(args_array, opt_req_list) \
       and arg_parser.arg_xor_dict(args_array, opt_xor_dict) \
       and not arg_parser.arg_dir_chk_crt(args_array, dir_chk_list) \
       and arg_parser.arg_validate(args_array, opt_valid_val) \
       and arg_parser.arg_cond_req(args_array, opt_con_req_list):
        run_program(args_array, func_dict, opt_arg_list)


if __name__ == "__main__":
    sys.exit(main())
