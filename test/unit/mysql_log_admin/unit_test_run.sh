#!/bin/bash
# Unit testing program for the program module.
# This will run all the units tests for this program.
# Will need to run this from the base directory where the module file
#   is located at.

echo ""
echo "Unit testing..."
test/unit/mysql_log_admin/fetch_binlog.py
test/unit/mysql_log_admin/fetch_log_entries.py
test/unit/mysql_log_admin/fetch_log_pos.py
test/unit/mysql_log_admin/find_dt_pos.py
test/unit/mysql_log_admin/help_message.py
test/unit/mysql_log_admin/process_logs_list.py
