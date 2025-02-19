#!/usr/bin/python
# Classification (U)

"""Program:  mysql_log_admin.py

    Description:  The program is an administration program for the MySQL binary
        log to include locating log positions, suspending slaves at a
        specific location, and printing logs.

    Usage:
        mysql_log_admin.py -c file -d path
            {-L [-s "date time" | -t "date time"] |
             -D [-f file | -g file | -s "date time"] [-t "date time"] |
             -R -e file [-f file | -g file]}
            [-y flavor_id] [-p path]
            [-v | -h]

    Arguments:
        -c file => Database configuration file.  Required arg.
        -d dir path => Directory path to config files.  Required arg.

        -L => Locate position in binary logs, if start and stop
            datetimes are NULL, then get current position.
            -s "date time" => Start datetime.  Format:  "YYYY-MM-DD HH:MM:SS"
            -t "date time" => Stop datetime.  Format:  "YYYY-MM-DD HH:MM:SS"

        -D => Display log(s).  Will use a combination of start and stop
            datetimes and first and last binary log file names.
            -f file => First binary log file name.
            -g file => Last binary log file name.
            -s "date time" => Start datetime.  Format:  "YYYY-MM-DD HH:MM:SS"
            -t "date time" => Stop datetime.  Format:  "YYYY-MM-DD HH:MM:SS"

        -R => Restore binary logs from a master database (-c) to a slave
            database (-e).
            -e file => Target database configuration file.
            -f file => First binary log file name.
            -g file => Last binary log file name.

        -p dir path => Directory path to mysql programs.  Only required if the
            mysql binary programs do not run properly.  (i.e. not in the $PATH
            variable.)
        -y value => A flavor id for the program lock.  To create unique lock.
        -v => Display version of this program.
        -h => Help and usage message.

        NOTE:  -v or -h overrides the other options.

    Notes:
        Database configuration file format (config/mysql_cfg.py.TEMPLATE):
            Ignore the replication entries as they are not needed.
            # Configuration file for a Database connection.
            user = "USER"
            japd = "PSWORD"
            host = "HOST_IP"
            name = "HOSTNAME"
            sid = SERVER_ID
            extra_def_file = "PYTHON_PROJEXT/config/mysql.cfg"
            serv_os = "Linux"
            port = 3306
            cfg_file = "MYSQL_DIRECTORY/mysqld.cnf"

            # If SSL connections are being used, configure one or more of these
                entries:
            ssl_client_ca = None
            ssl_client_key = None
            ssl_client_cert = None

            # Only changes these if necessary and have knowledge in MySQL
                SSL configuration setup:
            ssl_client_flag = None
            ssl_disabled = False
            ssl_verify_id = False
            ssl_verify_cert = False

            # TLS versions: Set the TLS versions allowed in the connection
            tls_versions = []

        NOTE 1:  Include the cfg_file even if running remotely as the file will
            be used in future releases.
        NOTE 2:  In MySQL 5.6 - it now gives warning if password is passed on
            the command line.  To suppress this warning, will require the use
            of the --defaults-extra-file option (i.e. extra_def_file) in the
            database configuration file.  See below for the defaults-extra-file
            format.
        NOTE 3:  Ignore the Replication user information entries.  They are
            not required for this program.

        configuration modules -> name is runtime dependent as it can be used to
            connect to different databases with different names.

        Defaults Extra File format (config/mysql.cfg.TEMPLATE):
        password="PSWORD"
        socket="DIRECTORY_PATH/mysqld.sock"

        NOTE 1:  The socket information can be obtained from the my.cnf
            file under ~/mysql directory.
        NOTE 2:  The --defaults-extra-file option will be overridden if there
            is a ~/.my.cnf or ~/.mylogin.cnf file located in the home directory
            of the user running this program.  The extras file will in effect
            be ignored.
        NOTE 3:  Socket use is only required to be set in certain conditions
            when connecting using localhost.

    Example:
        mysql_log_admin.py -c database -d config -L

"""

# Libraries and Global Variables

# Standard
import sys
import subprocess
import re
import itertools

# Local
try:
    from .lib import gen_libs
    from .lib import gen_class
    from .mysql_lib import mysql_class
    from .mysql_lib import mysql_libs
    from . import version

except (ValueError, ImportError) as err:
    import lib.gen_libs as gen_libs                     # pylint:disable=R0402
    import lib.gen_class as gen_class                   # pylint:disable=R0402
    import mysql_lib.mysql_class as mysql_class         # pylint:disable=R0402
    import mysql_lib.mysql_libs as mysql_libs           # pylint:disable=R0402
    import version

__version__ = version.__version__


def help_message():

    """Function:  help_message

    Description:  Displays the program's docstring which is the help and usage
        message when -h option is selected.

    Arguments:

    """

    print(__doc__)


def fetch_binlog(                                       # pylint:disable=R0913
        server, start_dt=None, stop_dt=None, binlog_files=None,
        opt_arg_list=None, bin_path=None):

    """Function:  fetch_binlog

    Description:  Returns a list of binary log entries based on the binary log
        file names passed and/or the start and/or stop datetimes.
        Returns the entries as a file.

    Arguments:
        (input) server -> Server instance
        (input) start_dt -> Start datetime
        (input) stop_dr -> Stop datetime
        (input) binlog_files -> List of binary log names
        (input) opt_arg_list ->  Arguments to be added to command line
        (input) bin_path -> Path to Mysql binary directory
        (output) -> File handler to list of log entries

    """

    opt_arg_list = [] if opt_arg_list is None else list(opt_arg_list)

    if bin_path is None:
        bin_path = ""

    if binlog_files is None:
        # List of binary logs.
        binlog_files = [
            row["Log_name"] for row in mysql_libs.fetch_logs(server)]

    else:
        binlog_files = list(binlog_files)

    cmd = mysql_libs.crt_cmd(server, bin_path + "mysqlbinlog")

    if opt_arg_list:
        for arg in opt_arg_list:
            cmd = gen_libs.add_cmd(cmd, arg=arg)

    if start_dt:
        cmd = gen_libs.add_cmd(cmd, arg=f"--start-datetime={start_dt}")

    if stop_dt:
        cmd = gen_libs.add_cmd(cmd, arg=f"--stop-datetime={stop_dt}")

    # Return a file handler with log entries.
    return iter(
        subprocess.Popen(cmd + binlog_files, stdout=subprocess.PIPE).stdout)


def find_dt_pos(                                # pylint:disable=R0913,R0914
        master, start_dt, stop_dt, opt_arg_list=None, bin_path=None,
        slave=None):

    """Function:  find_dt_pos

    Description:  Gets all binary logs, unless a Slave is present.  Fetches all
        lines that match the start and stop datatimes and checks these
        entries for end log positions and returns the last end log
        position found along with the binary log name that it was found in.

    Arguments:
        (input) master -> Server instance or Master, if Slave present
        (input) start_dt -> Start datetime
        (input) stop_dt -> Stop datetime
        (input) opt_arg_list ->  Arguments to be added to command line
        (input) slave -> Slave server instance
        (output) -> Position class (file, pos)

    """

    sub1 = r"#\d{6}\s+\d?\d:\d\d:\d\d\s+"
    sub2 = r"server id\s+(?P<sid>\d+)\s+"
    sub3 = r"end_log_pos\s+(?P<epos>\d+)\s+"
    sub4 = r"CRC32\s+(?P<crc>\w+)\s+"
    sub5 = r"(?P<type>\w+)"

    opt_arg_list = [] if opt_arg_list is None else list(opt_arg_list)

    if bin_path is None:
        bin_path = ""

    # List of current binary log names.
    log_files = [row["Log_name"] for row in mysql_libs.fetch_logs(master)]

    if slave:
        # Get only those binary log files up to the relay log file.
        efile = slave.relay_mst_log
        files = list(
            itertools.dropwhile(lambda file: file != efile, log_files))
        log_files = files

    # Get entries between start and stop datetimes.
    lines = fetch_binlog(
        master, start_dt, stop_dt, log_files, opt_arg_list, bin_path)
    num_files = 0
    last_log_pos = None

    for item in lines:
        if not isinstance(item, str):
            item = item.decode("utf-8")

        match = re.match(sub1 + sub2 + sub3 + sub5, item)

        # Supports checksum and match for approriate format.
        if master.crc == "CRC32":
            match = re.match(sub1 + sub2 + sub3 + sub4 + sub5, item)

        # If a line matches then see if the end_log_pos is Start (new file) or
        #   has found a Query within the datetime range requested.
        # Matched line is at the start of the log.
        if match and match.group("type") == "Start":
            # Increase file position by 1.
            num_files += 1

        # Matched line is a Query
        if match and match.group("type") == "Query":
            # Capture position of the log.
            last_log_pos = match.group("epos")

    # Return file and position as a Position class.
    return mysql_class.Position(log_files[num_files - 1], last_log_pos)


def fetch_log_pos(server, args, opt_arg_list=None):

    """Function:  fetch_log_pos

    Description:  Gets the server's file name and position that are between the
        start and stop datetimes.

    Arguments:
        (input) server -> Server instance
        (input) args -> ArgParser class instance
        (input) opt_arg_list ->  Arguments to be added to command line

    """

    opt_arg_list = [] if opt_arg_list is None else list(opt_arg_list)

    # Get Position class from file and log position.
    pos = find_dt_pos(server, args.get_val("-s"), args.get_val("-t"),
                      opt_arg_list, args.get_val("-p"))

    print(f"Filename: {pos.file}, Position: {pos.pos}")


def fetch_log_entries(server, args, opt_arg_list):

    """Function:  fetch_log_entries

    Description:  Prints out the binary log entries that are between the start
        and stop datetimes.

    Arguments:
        (input) server -> Server instance
        (input) args -> ArgParser class instance
        (input) opt_arg_list ->  Arguments to be added to command line

    """

    opt_arg_list = list(opt_arg_list)
    status, binlog_list = process_logs_list(server, args)

    if status[0]:

        lines = fetch_binlog(
            server, opt_arg_list=opt_arg_list, start_dt=args.get_val("-s"),
            stop_dt=args.get_val("-t"), binlog_files=binlog_list,
            bin_path=args.get_val("-p"))

        for item in lines:
            if not isinstance(item, str):
                item = item.decode("utf-8")

            print(item, end="")

    else:
        print(f"Error encountered: {status[1]}")


def process_logs_list(server, args):

    """Function:  process_logs_list

    Description:  Get a list of binary log file names from the source database.
        Clean up the list if the -f and/or -g options are used.

    Arguments:
        (input) server -> Server instance
        (input) args -> ArgParser class instance
        (output) status -> Tuple on process status
            status[0] - True|False - Process successful
            status[1] - Error message if process failed
        (output) binlog_list -> List of binary log file names

    """

    status = (True, None)
    binlog_list = []

    # Is -f and -g in the argument list and in the correct order.
    if (args.arg_exist("-f") and args.arg_exist("-g")) \
       and args.get_val("-g") < args.get_val("-f"):

        status = (False, f'Error:  Option -g: {args.get_val("-g")} is before'
                  f' -f {args.get_val("-f")}')

        return status, binlog_list

    binlog_list = gen_libs.dict_2_list(
        mysql_libs.fetch_logs(server), "Log_name")

    if args.arg_exist("-f") and args.get_val("-f") in binlog_list:

        # Remove any logs before log file name.
        while binlog_list[0] < args.get_val("-f"):
            binlog_list.pop(0)

    elif args.arg_exist("-f"):

        status = (
            False, f'Error:  Option -f: {args.get_val("-f")} not found in'
            f' binary log list.')

        return status, binlog_list

    if args.arg_exist("-g") and args.get_val("-g") in binlog_list:
        # Remove any logs after log file name.
        while binlog_list[-1] > args.get_val("-g"):
            binlog_list.pop(-1)

    elif args.arg_exist("-g"):

        status = (
            False, f'Error:  Option -g: {args.get_val("-g")} not found in'
            f' binary log list.')

    return status, binlog_list


def load_log(server, args, opt_arg_list):

    """Function:  load_log

    Description:  Get the binary logs from the source database, then fetch the
        revelant binary log entries and load them into the target
        database before closing all connections.

    Arguments:
        (input) server -> Server instance
        (input) args -> ArgParser class instance
        (input) opt_arg_list ->  Arguments to be added to command line

    """

    opt_arg_list = list(opt_arg_list)
    status, binlog_list = process_logs_list(server, args)

    if status[0]:
        target = mysql_libs.create_instance(
            args.get_val("-e"), args.get_val("-d"), mysql_class.Server)
        target.connect(silent=True)

        if not target.conn_msg:
            cmd = mysql_libs.crt_cmd(
                target, args.arg_set_path("-p", cmd="mysql"))

            # Fetch binary logs and restore to target database
            proc1 = fetch_binlog(
                server, args.get_val("-s"), args.get_val("-t"),
                binlog_list, opt_arg_list, args.get_val("-p"))
            proc2 = subprocess.Popen(cmd, stdin=proc1)  # pylint:disable=R1732
            proc2.wait()
            mysql_libs.disconnect(target)

        else:
            print(f"load_log:  Error encountered on slave {target.name}:"
                  f" {target.conn_msg}")

    else:
        print(f"load_log:  Error encountered in process_logs_list:"
              f" {status[1]}")


def run_program(args, func_dict, opt_arg_list):

    """Function:  run_program

    Description:  Creates class instance(s) and controls flow of the program.

    Arguments:
        (input) args -> ArgParser class instance
        (input) func_dict -> Dictionary list of functions and options
        (input) opt_arg_list ->  Arguments to be added to command line

    """

    func_dict = dict(func_dict)
    opt_arg_list = list(opt_arg_list)
    server = mysql_libs.create_instance(
        args.get_val("-c"), args.get_val("-d"), mysql_class.Server)
    server.connect(silent=True)

    if not server.conn_msg:
        server.set_srv_binlog_crc()

        # Call function(s) - intersection of command line and function dict.
        for item in set(args.get_args_keys()) & set(func_dict.keys()):
            # Call the function requested.
            func_dict[item](server, args, opt_arg_list)

        mysql_libs.disconnect(server)

    else:
        print(f"run_program:  Error encountered on master {server.name}:"
              f" {server.conn_msg}")


def main():

    """Function:  main

    Description:  Initializes program-wide used variables and processes command
        line arguments and values.

    Variables:
        dir_perms_chk -> contains options which will be directories and the
            octal permission settings
        func_dict -> dictionary list for the function calls or other options
        opt_arg_list -> contains arguments to add to command line by default
        opt_con_req_list -> contains the options that require other options
        opt_req_list -> contains the options that are required for the program
        opt_val_list -> contains options which require values
        opt_valid_val -> contains list of types of values to be validated
        opt_xor_val -> dictionary with key and values that will be xor

    Arguments:
        (input) argv -> Arguments from the command line.

    """

    dir_perms_chk = {"-d": 5, "-p": 5}
    func_dict = {"-L": fetch_log_pos, "-D": fetch_log_entries, "-R": load_log}
    opt_arg_list = ["--force-read", "--read-from-remote-server"]
    opt_con_req_list = {"-R": ["-e"]}
    opt_req_list = ["-c", "-d"]
    opt_val_list = ["-c", "-e", "-d", "-f", "-g", "-p", "-s", "-t", "-y"]
    valid_func = {"-s": gen_libs.validate_date, "-t": gen_libs.validate_date}
    opt_xor_val = {"-L": ["-D", "-R"], "-D": ["-L", "-R"], "-R": ["-D", "-L"]}

    # Process argument list from command line.
    args = gen_class.ArgParser(sys.argv, opt_val=opt_val_list)

    if args.arg_parse2()                                            \
       and not gen_libs.help_func(args, __version__, help_message)  \
       and args.arg_require(opt_req=opt_req_list)                   \
       and args.arg_xor_dict(opt_xor_val=opt_xor_val)               \
       and args.arg_dir_chk(dir_perms_chk=dir_perms_chk)            \
       and args.arg_validate(valid_func=valid_func)                 \
       and args.arg_cond_req(opt_con_req=opt_con_req_list):

        try:
            prog_lock = gen_class.ProgramLock(
                sys.argv, args.get_val("-y", def_val=""))
            run_program(args, func_dict, opt_arg_list)
            del prog_lock

        except gen_class.SingleInstanceException:
            print(f'WARNING:  lock in place for mysql_log_admin with id of:'
                  f' {args.get_val("-y", def_val="")}')


if __name__ == "__main__":
    sys.exit(main())
