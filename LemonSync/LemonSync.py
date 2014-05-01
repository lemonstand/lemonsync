#!/usr/bin/env python

import sys 
import time
import os 
import getopt

from Listener import Listener
from ConfigParser import SafeConfigParser
from watchdog.observers import Observer
from Config import config

def main(): 

	# Start 
	print '\033[93m' + 'LemonSync is initiating connection...'
	observer = Observer()
	observer.schedule(Listener(), config.watch_dir, recursive=True)
	observer.start()

	try:
		while True:
			time.sleep(1)
	except KeyboardInterrupt:
		observer.stop()

	observer.join()

if __name__ == '__main__': 
	main() 