# Python project for transaction log administration in a MySQL database.
# Classification (U)

# Description:
  This program is used to administrate transaction logs in a MySQL database to include locating log positions and restoring transaction logs to a database.


###  This README file is broken down into the following sections:
  * Features
  * Prerequisites
  * Installation
  * Configuration
  * Program Description
  * Program Help Function
  * Help Message
  * Testing
    - Unit
    - Integration
    - Blackbox


# Features:
  * Locate a transaction log position using start and end datetimes.
  * Display transaction logs in readable format using start and end datetimes.
  * Restore transaction logs from a source database to a target database.

# Prerequisites:

  * List of Linux packages that need to be installed on the server.
    - python-libs
    - python-devel
    - git
    - python-pip

  * Local class/library dependencies within the program structure.
    - lib/cmds_gen
    - lib/arg_parser
    - lib/gen_libs
    - mysql_lib/mysql_libs
    - mysql_lib/mysql_class


# Installation:

Install this project using git.
  * Replace **{Python_Project}** with the baseline path of the python program.

```
umask 022
cd {Python_Project}
clone git@sc.appdev.proj.coe.ic.gov:JAC-DSXD/mysql-log-admin.git
```

Install/upgrade system modules.

```
cd mysql-log-admin
sudo bash
umask 022
pip install -r requirements.txt --upgrade --trusted-host pypi.appdev.proj.coe.ic.gov
exit
```

Install supporting classes and libraries.

```
pip install -r requirements-python-lib.txt --target lib --trusted-host pypi.appdev.proj.coe.ic.gov
pip install -r requirements-mysql-lib.txt --target mysql_lib --trusted-host pypi.appdev.proj.coe.ic.gov
pip install -r requirements-python-lib.txt --target mysql_lib/lib --trusted-host pypi.appdev.proj.coe.ic.gov
```

# Configuration:

Create MySQL configuration file.

```
cd config
cp mysql_cfg.py.TEMPLATE mysql_cfg.py
```

Make the appropriate change to the environment.
  * Change these entries in the MySQL setup:
    - passwd = "ROOT_PASSWORD"
    - host = "SERVER_IP"
    - name = "HOST_NAME"
    - sid = SERVER_ID
    - extra_def_file = "{Python_Project}/config/mysql.cfg"

```
vim mysql_cfg.py
chmod 600 mysql_cfg.py
```

Create MySQL definition file.

```
cp mysql.cfg.TEMPLATE mysql.cfg
```

Make the appropriate change to the MySQL definition setup.
  * Change these entries in the MySQL configuration file:
    - password="ROOT_PASSWORD"
    - socket={BASE_DIR}/mysql/tmp/mysql.sock

```
vim mysql.cfg
chmod 600 mysql.cfg
```


# Program Descriptions:
### Program: mysql_log_admin.py
##### Description: Administration program for the MySQL binary log system.


# Program Help Function:

  The program has a -h (Help option) that will show display an usage message.  The help message will usually consist of a description, usage, arugments to the program, example, notes about the program, and any known bugs not yet fixed.  To run the help command:
  * Replace **{Python_Project}** with the baseline path of the python program.

```
{Python_Project}/mysql-log-admin/mysql_log_admin.py -h
```


# Help Message:
  Below is the help message for the program the program.  Run the program with the -h option get the latest help message for the program.

    Program:  mysql_log_admin.py

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
        Database configuration file format (mysql_{host}.py):
            # Configuration file for {Database Name/Server}
            user = "root"
            passwd = "ROOT_PASSWORD"
            host = "IP_ADDRESS"
            serv_os = "Linux" or "Solaris"
            name = "HOSTNAME"
            port = PORT_NUMBER (default of mysql is 3306)
            cfg_file = "DIRECTORY_PATH/my.cfg"
            sid = "SERVER_ID"
            extra_def_file = "DIRECTORY_PATH/myextra.cfg"

            NOTE 1:  Include the cfg_file even if running remotely as the
                file will be used in future releases.

            NOTE 2:  In MySQL 5.6 - it now gives warning if password is
                passed on the command line.  To suppress this warning, will
                require the use of the --defaults-extra-file option
                (i.e. extra_def_file) in the database configuration file.
                See below for the defaults-extra-file format.

            configuration modules -> name is runtime dependent as it can be
                used to connect to different databases with different names.

            Defaults Extra File format (filename.cfg):
            [client]
            password="ROOT_PASSWORD"
            socket="DIRECTORY_PATH/mysql.sock"

            NOTE:  The socket information can be obtained from the my.cnf
                file under ~/mysql directory.

    Example:
        mysql_log_admin.py -c database -d config -L


# Testing:


# Unit Testing:

### Description: Testing consists of unit testing for the functions in the mysql_log_admin.py program.

### Installation:

Install this project using git.
  * Replace **{Python_Project}** with the baseline path of the python program.
  * Replace **{Branch_Name}** with the name of the Git branch being tested.  See Git Merge Request.

```
umask 022
cd {Python_Project}
git clone --branch {Branch_Name} git@sc.appdev.proj.coe.ic.gov:JAC-DSXD/mysql-log-admin.git
```

Install/upgrade system modules.

```
cd mysql-log-admin
sudo bash
umask 022
pip install -r requirements.txt --upgrade --trusted-host pypi.appdev.proj.coe.ic.gov
exit
```

Install supporting classes and libraries.

```
pip install -r requirements-python-lib.txt --target lib --trusted-host pypi.appdev.proj.coe.ic.gov
pip install -r requirements-mysql-lib.txt --target mysql_lib --trusted-host pypi.appdev.proj.coe.ic.gov
pip install -r requirements-python-lib.txt --target mysql_lib/lib --trusted-host pypi.appdev.proj.coe.ic.gov
```


# Unit test runs for mysql_log_admin.py:
  * Replace **{Python_Project}** with the baseline path of the python program.

```
cd {Python_Project}/mysql-log-admin
```

### Unit:  help_message
```
test/unit/mysql_log_admin/help_message.py
```

### Unit:  
```
test/unit/mysql_log_admin/
```

### Unit:  
```
test/unit/mysql_log_admin/
```

### Unit:  run_program
```
test/unit/mysql_log_admin/run_program.py
```

### Unit:  main
```
test/unit/mysql_log_admin/main.py
```

### All unit testing
```
test/unit/mysql_log_admin/unit_test_run.sh
```

### Code coverage program
```
test/unit/mysql_log_admin/code_coverage.sh
```


# Integration Testing:

### Description: Testing consists of integration testing of functions in the mysql_log_admin.py program.

### Installation:

Install this project using git.
  * Replace **{Python_Project}** with the baseline path of the python program.
  * Replace **{Branch_Name}** with the name of the Git branch being tested.  See Git Merge Request.

```
umask 022
cd {Python_Project}
git clone --branch {Branch_Name} git@sc.appdev.proj.coe.ic.gov:JAC-DSXD/mysql-log-admin.git
```

Install/upgrade system modules.

```
cd mysql-log-admin
sudo bash
umask 022
pip install -r requirements.txt --upgrade --trusted-host pypi.appdev.proj.coe.ic.gov
exit
```

Install supporting classes and libraries.

```
pip install -r requirements-python-lib.txt --target lib --trusted-host pypi.appdev.proj.coe.ic.gov
pip install -r requirements-mysql-lib.txt --target mysql_lib --trusted-host pypi.appdev.proj.coe.ic.gov
pip install -r requirements-python-lib.txt --target mysql_lib/lib --trusted-host pypi.appdev.proj.coe.ic.gov
```

### Configuration:

Create MySQL configuration file.

```
cd test/integration/mysql_log_admin/config
cp ../../../../config/mysql_cfg.py.TEMPLATE mysql_cfg.py
```

Make the appropriate change to the environment.
  * Change these entries in the MySQL setup:
    - passwd = "ROOT_PASSWORD"
    - host = "SERVER_IP"
    - name = "HOST_NAME"
    - sid = SERVER_ID
    - extra_def_file = "{Python_Project}/config/mysql.cfg"

```
vim mysql_cfg.py
chmod 600 mysql_cfg.py
```

Create MySQL definition file.
```
cp ../../../../config/mysql.cfg.TEMPLATE mysql.cfg
```

Make the appropriate change to the MySQL definition setup.
  * Change these entries in the MySQL configuration file:
    - password="ROOT_PASSWORD"
    - socket={BASE_DIR}/mysql/tmp/mysql.sock

```
vim mysql.cfg
chmod 600 mysql.cfg
```


# Integration test runs for mysql_log_admin.py:
  * Replace **{Python_Project}** with the baseline path of the python program.

```
cd {Python_Project}/mysql-log-admin
```

### Integration:  
```
test/integration/mysql_log_admin/
```

### All integration testing
```
test/integration/mysql_log_admin/integration_test_run.sh
```

### Code coverage program
```
test/integration/mysql_log_admin/code_coverage.sh
```


# Blackbox Testing:

### Description: Testing consists of blackbox testing of the mysql_log_admin.py program.

### Installation:

Install this project using git.
  * Replace **{Python_Project}** with the baseline path of the python program.
  * Replace **{Branch_Name}** with the name of the Git branch being tested.  See Git Merge Request.

```
umask 022
cd {Python_Project}
git clone --branch {Branch_Name} git@sc.appdev.proj.coe.ic.gov:JAC-DSXD/mysql-log-admin.git
```

Install/upgrade system modules.

```
cd mysql-log-admin
sudo bash
umask 022
pip install -r requirements.txt --upgrade --trusted-host pypi.appdev.proj.coe.ic.gov
exit
```

Install supporting classes and libraries.

```
pip install -r requirements-python-lib.txt --target lib --trusted-host pypi.appdev.proj.coe.ic.gov
pip install -r requirements-mysql-lib.txt --target mysql_lib --trusted-host pypi.appdev.proj.coe.ic.gov
pip install -r requirements-python-lib.txt --target mysql_lib/lib --trusted-host pypi.appdev.proj.coe.ic.gov
```

### Configuration:

Create MySQL configuration file.

```
cd test/blackbox/mysql_log_admin/config
cp ../../../../config/mysql_cfg.py.TEMPLATE mysql_cfg.py
```

Make the appropriate change to the environment.
  * Change these entries in the MySQL setup:
    - passwd = "ROOT_PASSWORD"
    - host = "SERVER_IP"
    - name = "HOST_NAME"
    - sid = SERVER_ID
    - extra_def_file = "{Python_Project}/config/mysql.cfg

```
vim mysql_cfg.py
chmod 600 mysql_cfg.py
```

Create MySQL definition file.

```
cp ../../../../config/mysql.cfg.TEMPLATE mysql.cfg
```

Make the appropriate change to the MySQL definition setup.
  * Change these entries in the MySQL configuration file:
    - password="ROOT_PASSWORD"
    - socket={BASE_DIR}/mysql/tmp/mysql.sock

```
vim mysql.cfg
chmod 600 mysql.cfg
```


# Blackbox test run for mysql_log_admin.py:
  * Replace **{Python_Project}** with the baseline path of the python program.

```
cd {Python_Project}/mysql-log-admin
```


### Blackbox:  
```
test/blackbox/mysql_log_admin/blackbox_test.sh
```

