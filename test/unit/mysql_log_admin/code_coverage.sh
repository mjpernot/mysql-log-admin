#!/bin/bash
# Unit test code coverage for program module.
# This will run the Python code coverage module against all unit test modules.
# This will show the amount of code that was tested and which lines of code
#   that was skipped during the test.

coverage erase

echo ""
echo "Running unit test modules in conjunction with coverage"
coverage run -a --source=mysql_log_admin test/unit/mysql_log_admin/fetch_binlog.py
coverage run -a --source=mysql_log_admin test/unit/mysql_log_admin/fetch_log_entries.py
coverage run -a --source=mysql_log_admin test/unit/mysql_log_admin/fetch_log_pos.py
coverage run -a --source=mysql_log_admin test/unit/mysql_log_admin/find_dt_pos.py
coverage run -a --source=mysql_log_admin test/unit/mysql_log_admin/help_message.py

echo ""
echo "Producing code coverage report"
coverage combine
coverage report -m
