# Python project for transaction log administration in a MySQL database.
# Classification (U)

# Description:
  Administrate transaction logs in a MySQL database to include locating log positions and restoring transaction logs to a database.


###  This README file is broken down into the following sections:
  * Features
  * Prerequisites
  * Installation
  * Configuration
  * Program Help Function
  * Testing
    - Unit


# Features:
  * Locate a transaction log position using start and end datetimes.
  * Display transaction logs in readable format using start and end datetimes.
  * Restore transaction logs from a source database to a target database.

# Prerequisites:

  * List of Linux packages that need to be installed on the server.
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

Create MySQL configuration file for Source database.  Make the appropriate change to the environment.
  * Change these entries in the MySQL setup:
    - japd = "PSWORD"
    - host = "HOST_IP"
    - name = "HOST_NAME"
    - sid = SERVER_ID
    - extra_def_file = "PYTHON_PROJECT/config/mysql.cfg"
    - cfg_file = "MYSQL_DIRECTORY/mysqld.cnf"
  * Change these entries only if required:
    - serv_os = "Linux"
    - port = 3306  

```
cd config
cp mysql_cfg.py.TEMPLATE mysql_cfg.py
vim mysql_cfg.py
chmod 600 mysql_cfg.py
```

Create MySQL definition file for Source database.  Make the appropriate change to the MySQL definition setup.
  * Change these entries in the MySQL configuration file:
    - password="PASSWORD"
    - socket=DIRECTORY_PATH/mysql.sock

```
cp mysql.cfg.TEMPLATE mysql.cfg
vim mysql.cfg
chmod 600 mysql.cfg
```

Create MySQL configuration file for each Target database.  Make the appropriate change to the environment.
  * Change these entries in the MySQL setup:
    - japd = "PSWORD"
    - host = "HOST_IP"
    - name = "HOST_NAME"
    - sid = SERVER_ID
    - extra_def_file = "PYTHON_PROJECT/config/mysql.cfg"
    - cfg_file = "MYSQL_DIRECTORY/mysqld.cnf"
  * Change these entries only if required:
    - serv_os = "Linux"
    - port = 3306

```
cp mysql_cfg.py.TEMPLATE mysql_cfg_TARGET_NAME.py
vim mysql_cfg._TARGET_NAME.py
chmod 600 mysql_cfg_TARGET_NAME.py
```

Create MySQL definition file for each Target database.  Make the appropriate change to the MySQL definition setup.
  * Change these entries in the MySQL configuration file:
    - password="PASSWORD"
    - socket=DIRECTORY_PATH/mysql.sock

```
cp mysql.cfg.TEMPLATE mysql_TARGET_NAME.cfg
vim mysql_TARGET_NAME.cfg
chmod 600 mysql_TARGET_NAME.cfg
```



# Program Help Function:

  The program has a -h (Help option) that will show display an usage message.  The help message will usually consist of a description, usage, arugments to the program, example, notes about the program, and any known bugs not yet fixed.  To run the help command:
  * Replace **{Python_Project}** with the baseline path of the python program.

```
{Python_Project}/mysql-log-admin/mysql_log_admin.py -h
```


# Testing:

# Unit Testing:

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


### Testing
  * Replace **{Python_Project}** with the baseline path of the python program.

```
cd {Python_Project}/mysql-log-admin
test/unit/mysql_log_admin/unit_test_run.sh
```

### Code coverage:

```
cd {Python_Project}/mysql-log-admin
test/unit/mysql_log_admin/code_coverage.sh
```

