#!/usr/bin/env python

import sys 
import time
import os 
import getopt
import hashlib

from Listener import Listener
from Utils import Utils
from ConfigParser import SafeConfigParser
from watchdog.observers import Observer
from Config import config

def main(): 

	# Start 
	print '\033[93m' + 'LemonSync is initiating connection...'
	observer = Observer()
	utils = Utils()

	observer.schedule(Listener(), config.watch_dir, recursive=True)

	# Loop over every file in the watch dir
	utils.file_changes()

	observer.start()

	try:
		while True:
			time.sleep(1)
	except KeyboardInterrupt:
		observer.stop()

	observer.join()

if __name__ == '__main__': 
	main() 