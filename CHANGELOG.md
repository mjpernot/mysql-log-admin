# Changelog
All notable changes to this project will be documented in this file.

The format is based on "Keep a Changelog".  This project adheres to Semantic Versioning.


## [2.2.0] - 2021-08-20
- Updated to work in MySQL 8.0 and 5.7 environments.
- Updated to work in a SSL environment.
- Updated to use the mysql_libs v5.2.2 library.
- Updated to use gen_libs v2.8.4 library.

### Changed
- fetch_binlog:  Changed cmds_gen.add_cmd to gen_libs.add_cmd.
- config/mysql_cfg.py.TEMPLATE:  Add SSL configuration entries.
- config/mysql.cfg.TEMPLATE:  Point to correct socket file.
- run_program, load_log:  Replaced cmds_gen.disconnect with mysql_libs.disconnect.
- Removed unnecessary \*\*kwargs in function argument list.
- Documentation updates.

### Removed
- cmds_gen module.


## [2.1.1] - 2020-11-10
- Updated to use the mysql_libs v5.0.3 library.

### Fixed
- load_log:  Added connect command and removed cmds_gen.disconnect for "server".
- config/mysql.cfg.TEMPLATE:  Point to correct socket file.
- find_dt_pos:  Fixed handling re line from SonarQube scan finding.
- load_log, fetch_binlog:  Fixed handling subprocess line from SonarQube scan finding.
- main: Fixed handling command line arguments from SonarQube scan finding.
- fetch_binlog:  Changed bin_path argument default to empty string.

### Changed
- load_log, run_program:  Added check on status of server connection message.
- fetch_log_entries:  Add ability to fetch binary logs based on file names.
- load_log:  Captured and processed "status" from process_logs_list function.
- process_logs_list:  Removed sys.exit() and replaced with status and returned status to calling function.
- find_dt_pos:  Refactored the re.match regular expression string.
- load_log, fetch_log_entries, find_dt_pos, run_program:  Changed variables to standard naming convention.
- config/mysql_cfg.py.TEMPLATE:  Changed entry name.
- Documentation updates.

### Removed
- Removed os library module.


## [2.1.0] - 2019-12-16
### Fixed
- find_dt_pos, fetch_log_pos, fetch_log_entries, process_logs_list, load_log, run_program, fetch_binlog:  Fixed problem with mutable default arguments issue.

### Changed
- main:  Added program lock functionality to program.
- main:  Added new option -y to the program.
- main:  Refactored 'if' statements.
- find_dt_pos, fetch_log_pos, fetch_log_entries, process_logs_list, load_log, run_program, fetch_binlog: Changed variable name to standard convention.
- Documentation updates.


## [2.0.1] - 2018-12-03
### Changed
- Added \*\*kwargs to those function parameter lists without the keyword argument capability.
- fetch_binlog:  Changed check on binlog_files to be user readable.


## [2.0.0] - 2018-05-22
Breaking Change

### Change
- Changed "mysql_libs" calls to new naming schema.
- Changed "cmds_gen" calls to new naming schema.
- Changed "gen_libs" calls to new naming schema.
- Changed "arg_parser" calls to new naming schema.
- Changed function names from uppercase to lowercase.
- Setup single-source version control.


## [1.8.0] - 2018-05-03
### Changed
- Changed "server" to "mysql_class" module reference.
- Changed "commands" to "mysql_libs" module reference.

### Added
- Added single-source version control.


## [1.7.0] - 2017-08-21
### Changed
- Help_Message:  Replace docstring with printing the programs \_\_doc\_\_.
- Change single quotes to double quotes.
- Convert program to use local libraries from ./lib directory.

### Fixed
- main:  Correct misrepresented variable: valid_func to opt_valid_val.


## [1.6.0] - 2016-10-20
### Changed
- MySQL 5.6 binary logs have checksums included in their log entries.  This changes the format of the log header when looking for log positions.  Require two different matching searches depending on whether Checksum is supported or not.
- Find_DT_Pos:  Added check to see if the Servers binary log supports checksum and run appropriate search method.
- Run_Program:  Update the servers checksum attribute.
- Fetch_Binlog:  Replaced prog_gen.Add_Cmd with cmds_gen.Add_Cmd.


## [1.5.0] - 2016-09-27
### Changed
- MySQL 5.6 now gives warning if password is passed on the command line.  To suppress this warning, will require the use of the --defaults-extra-file option.  This will require the use of updated commands library and server class files.  See in documentation above for exact version required for MySQL 5.6.


## [1.4.0] - 2016-09-23
- Documentation updates.


## [1.3.0] - 2016-09-15
### Changed
- Load_Log:  Changed -C to -e.  To bring the argument options inline with the other programs.  Changed commands.Disconnect() to cmds_gen.Disconnect().  Replaced my_prog.Crt_Cmd with commands.Crt_Cmd.
- main:  Changed -C to -e.  To bring the argument options inline with the other programs.  Replaced Arg_Parse with Arg_Parse2.
- Run_Program, Process_Logs_List:  Changed commands.Disconnect() to cmds_gen.Disconnect().
- Fetch_Binlog:  Replaced my_prog.Append_Cmd with prog_gen.Add_Cmd.  Replaced my_prog.Crt_Cmd with commands.Crt_Cmd.


## [1.2.0] - 2016-01-11
### Added
- Process_Logs_List function.
- Load_Log function.
- Added new function (-R option) to restore binary log files from a source database to a target database.

### Changed
- main:  Added new variables and a number of new options.  Also added new function call and replaced a function call with a new function.


## [1.1.0] - 2016-01-07
### Changed
- Fetch_Log_Pos, Fetch_Log_Entries:  Added \*\*kwargs to argument list to allow for future use of additional arguments to the function.
- Fetch_Binlog:  Removed extranous print command from function, left over from original testing phase.
- main:  Added new variable to hold function calls to the validity functions.
- main:  Added function call to Arg_Validate to check the validity of the data in some of the arguments.


## [1.0.0] - 2015-12-29
- Initial creation.

