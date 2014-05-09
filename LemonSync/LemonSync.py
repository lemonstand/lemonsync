#!/usr/bin/env python

import sys 
import time
import os 
import argparse
from sys import version_info
from Parser import Parser
from Listener import Listener
from Utils import Utils
from Connector import Connector
from watchdog.observers import Observer

def main(): 
	# Handle any command line arguments
	p = argparse.ArgumentParser(description='LemonSync v 0.1.6')
	p.add_argument("-c", "--config", help="A configuration file must be present.", required=True)
	p.add_argument("-r", "--reset", help="Options for this argument are [local|remote].", required=False)
	args = p.parse_args()

	# If the reset option was passed 
	if args.reset and not args.reset in ("local", "remote"):
		p.error('Options for [-r RESET] are [local|remote].')

	config = Parser(args.config)

	# Make sure the watch directory exists
	if not os.path.isdir(config.watch_dir):
		sys.exit("Watch directory does not exist!")

	# Start 
	print '\033[93m' + 'LemonSync is initiating connection...'

	# Establish a connection to the LemonStand API, and then to S3
	c = Connector()
	identity = c.getIdentity(config.api_host, config.store_host, config.api_access)
	connection = c.s3Connection(identity);

	# Used to run some basic utilities
	utils = Utils(connection, config)

	if args.reset == "local":
		utils.reset_local()
	elif args.reset == "remote":
		utils.reset_remote()
	else:
		# Loop over every file in the watch dir
		# Do not need to perform this action if the local files have been overwritten already
		changes = utils.file_changes()

		if changes:
			utils.clean_changes(changes)

	# Watchdog initialtion
	observer = Observer()
	observer.schedule(Listener(connection, config), config.watch_dir, recursive=True)
	observer.start()

	print '\033[92m' + 'LemonSync is listening to changes on ' + config.watch_dir

	try:
		while True:
			time.sleep(1)
	except KeyboardInterrupt:
		observer.stop()

	observer.join()

if __name__ == '__main__': 
	main() 