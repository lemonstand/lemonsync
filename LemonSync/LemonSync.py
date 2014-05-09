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
	#creates boolean value for test that Python major version > 2
	py3 = version_info[0] > 2 

	# Defaults
	file = None

	# Handle any command line arguments
	if len(sys.argv) < 2:
		print 'Usage: lemonsync --config=<configfile>'
		sys.exit(2)

	try:
		opts, args = getopt.getopt(sys.argv[1:],"c:f:",["config="])
	except getopt.GetoptError:
		print 'Usage: lemonsync --config=<configfile>'
		sys.exit(2)

	for o, a in opts:
		if o in ("-c", "--config"):
			file = a
		else:
			assert False, "unhandled option"

	config = Parser(file)

	# Start 
	print '\033[93m' + 'LemonSync is initiating connection...'

	# Establish a connection to the LemonStand API, and then to S3
	c = Connector()
	identity = c.getIdentity(config.api_host, config.store_host, config.api_access)
	connection = c.s3Connection(identity);

	# Used to run some basic utilities
	utils = Utils(connection, config)

	# Loop over every file in the watch dir
	changes = utils.file_changes()

	if changes:
 		for files in changes:
			print '--- ' + files
		print '\033[91m' + 'Version mismatch!' + '\033[91m'
		print '\033[91m' + 'Type [1] + [Enter] to overwrite your local files. Any other key will result in no action being taken.' + '\033[91m'

	if py3:
		response = input(": ")
	else:
		response = raw_input(": ")

	if response == "1":
		print '000'
		# Sync the changed remote files with the local files
		utils.sync(changes)


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