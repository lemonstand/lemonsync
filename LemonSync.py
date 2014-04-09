#!/usr/bin/env python

import sys 
import time
import os 

from watchdog.observers import Observer
from src import Listener
from src.Config import config

def main(): 
	observer = Observer()
	observer.schedule(Listener(), config.watch, recursive=True)
	observer.start()

	try:
		while True:
			time.sleep(1)
	except KeyboardInterrupt:
		observer.stop()

	observer.join()

if __name__ == '__main__': 
	main() 