#!/usr/bin/env python

import sys 
import time
import os 
import getopt
from sys import version_info
from Parser import Parser
from Listener import Listener
from Utils import Utils
from Connector import Connector
from watchdog.observers import Observer

def main(): 
	# Defaults
	cfile = None
	reset = False
	usage = 'Usage: lemonsync --config=<configfile> [options]'

	# Handle any command line arguments
	if len(sys.argv) < 2:
		print usage
		sys.exit(2)

	try:
		opts, args = getopt.getopt(sys.argv[1:],"c:r:",["config=", "reset="])
	except getopt.GetoptError:
		print usage
		sys.exit(2)

	for o, attr in opts:
		if o in ("-c", "--config"):
			cfile = attr
		elif o in ("-r", "--reset"):
			reset = attr
		else:
			sys.exit(usage)


	# If the reset option was passed 
	if not reset in ("local", "remote"):
		sys.exit(usage)


	config = Parser(cfile)

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

	if reset == "local":
		utils.reset_local()
	elif reset == "remote":
		utils.reset_remote()
	else:
		# Loop over every file in the watch dir
		# Do not need to perform this action if the local files have been overwritten already
		changes = utils.file_changes()

		if changes:
			utils.clean_changes()



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