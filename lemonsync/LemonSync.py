#!/usr/bin/env python

# Copyright (c) 2014 LemonStand eCommerce Inc. https://lemonstand.com/
# All rights reserved.
#
# This is free and unencumbered software released into the public domain.

# Anyone is free to copy, modify, publish, use, compile, sell, or
# distribute this software, either in source code form or as a compiled
# binary, for any purpose, commercial or non-commercial, and by any
# means.
#
# In jurisdictions that recognize copyright laws, the author or authors
# of this software dedicate any and all copyright interest in the
# software to the public domain. We make this dedication for the benefit
# of the public at large and to the detriment of our heirs and
# successors. We intend this dedication to be an overt act of
# relinquishment in perpetuity of all present and future rights to this
# software under copyright law.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#
# For more information, please refer to <http://unlicense.org/>

import sys 
import os 
import argparse
import time
import json
from sys import version_info
from Parser import Parser
from Listener import Listener
from Utils import Utils
from Connector import Connector
from watchdog.observers import Observer
from colorama import init, Fore, Back, Style

def get_configuration (args):
	configuration = Parser(args.config)

	# Make sure the watch directory has a trailing slash
	configuration.watch_dir = os.path.normpath(configuration.watch_dir) + os.sep

	# Make sure the watch directory exists before trying to run any utilities
	if not os.path.isdir(configuration.watch_dir):
		sys.exit(Fore.RED + "Watch directory does not exist!" + Style.RESET_ALL)

	if hasattr(configuration, 'file_patterns'):
		try:
			configuration.file_patterns = json.loads(configuration.file_patterns)
		except:
			sys.exit(Fore.RED + 'The configuration value for file_patterns is malformed.' + Style.RESET_ALL)
	else:
		# Set the default patterns to watch
		configuration.file_patterns = [ "*" ]

	if hasattr(configuration, 'ignore_patterns'):
		try:
			configuration.ignore_patterns = json.loads(configuration.ignore_patterns)
		except:
			sys.exit(Fore.RED + 'The configuration value for ignore_patterns is malformed.' + Style.RESET_ALL)
	else:
		# Set the default patterns to watch
		configuration.ignore_patterns = [ "*.tmp", "*.TMP", "*/.git/*" ]

	return configuration

def get_connection (configuration):
	# Start 
	print(Back.YELLOW + Fore.BLACK + 'LemonSync is initiating connection...' + Style.RESET_ALL)

	# Establish a connection to the LemonStand API, and then to s3
	c = Connector()
	identity = c.get_identity(configuration.api_host, configuration.store_host, configuration.api_access)
	connection = c.s3_connection(identity);

	return connection

def run_utils (connection, configuration, reset):
	# Used to run some basic utilities
	utils = Utils(connection, configuration)

	if reset == "local":
		utils.reset_local()
	elif reset == "remote":
		utils.reset_remote()
	else:
		# Loop over every file in the watch dir
		# Do not need to perform this action if the local files have been overwritten already
		changes = utils.file_changes()

		if changes:
			utils.clean_changes(changes)
	
	return utils

def start_watching (connection, configuration, utils):
	# Watchdog initialtion
	observer = Observer()
	observer.schedule(Listener(connection, configuration, utils), configuration.watch_dir, recursive=True)
	observer.start()

	print(Back.GREEN + Fore.BLACK + 'LemonSync is listening to changes on ' + configuration.watch_dir + Style.RESET_ALL)

	try:
		while True:
			time.sleep(1)
	except KeyboardInterrupt:
		observer.stop()

	observer.join()

	return

# Handle any command line arguments
def parse_args ():
	p = argparse.ArgumentParser(description='LemonSync v0.1.13')
	p.add_argument("-c", "--config", help="A configuration file must be present.", required=True)
	p.add_argument("-r", "--reset", help="Options for this argument are [local|remote].", required=False)
	args = p.parse_args()

	# If the reset option was passed 
	if args.reset and not args.reset in ("local", "remote"):
		p.error('Options for [-r RESET] are [local|remote].')
	
	return args

def main ():
	# the call to init() will start filtering ANSI escape sequences out of any text sent to 
	# stdout or stderr, and will replace them with equivalent Win32 calls.
	init(autoreset=True)

	args = parse_args()
	configuration = get_configuration(args)
	connection = get_connection(configuration)

	# Run any start up utilities that were passed in on the command line
	utils = run_utils(connection, configuration, args.reset)

	# This function will not return until the user manually exits the program by typing Ctrl-C
	start_watching(connection, configuration, utils)

if __name__ == '__main__': 
	main()