#!/bin/bash
# Unit testing program for the program module.
# This will run all the units tests for this program.
# Will need to run this from the base directory where the module file
#   is located at.

echo ""
echo "Unit testing..."
/usr/bin/python3 ./test/unit/mysql_log_admin/fetch_binlog.py
/usr/bin/python3 ./test/unit/mysql_log_admin/fetch_log_entries.py
/usr/bin/python3 ./test/unit/mysql_log_admin/fetch_log_pos.py
/usr/bin/python3 ./test/unit/mysql_log_admin/find_dt_pos.py
/usr/bin/python3 ./test/unit/mysql_log_admin/help_message.py
/usr/bin/python3 ./test/unit/mysql_log_admin/load_log.py
/usr/bin/python3 ./test/unit/mysql_log_admin/main.py
/usr/bin/python3 ./test/unit/mysql_log_admin/process_logs_list.py
/usr/bin/python3 ./test/unit/mysql_log_admin/run_program.py
