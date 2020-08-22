#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""

if __name__ == '__main__':
	from django.core.management import execute_from_command_line
	from treux import load_environment
	from sys import argv

	load_environment()
	execute_from_command_line(argv)
