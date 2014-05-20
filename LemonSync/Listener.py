import sys 
import time
import os 
import json
import requests
import time
from Connector import Connector
from watchdog.events import PatternMatchingEventHandler
from colorama import Fore, Back, Style

class Listener (PatternMatchingEventHandler):
		
	def __init__ (self, connection, config, utils):
		PatternMatchingEventHandler.patterns = config.file_patterns
		PatternMatchingEventHandler.ignore_patterns = config.ignore_patterns
		PatternMatchingEventHandler.ignore_directories = True
		PatternMatchingEventHandler.case_sensitive = True

		self.connection = connection
		self.config = config
		self.utils = utils
		self.retries = 1

	def __checkConnection (self):
		# Get a new connection object to lemonstand API
		c = Connector()
		identity = c.get_identity(self.config.api_host, self.config.store_host, self.config.api_access)
		connection = c.s3_connection(identity);
		self.connection = connection

		return

	def __getPath (self, filepath):
		# strip out the watch dir, from the modified path to get the relative folder in S3
		path = filepath.replace(self.config.watch_dir, '')
		return path

	def __getKey (self, event_path):
		path = self.__getPath(event_path)
		# this will create the full s3 key
		key = "/".join([self.connection["store"], "themes", self.connection["theme"], path])

		return key

	def __register (self, event_path):
		key = self.__getPath(event_path)
		data = { 'key': key }
		try:
			# Update the resource with LemonStand
			res = requests.put(
				self.config.api_host + '/v2/resource', 
				headers = { 
					'content-type': 'application/json',
					'x-store-host': self.config.store_host, 
					'authorization': self.config.api_access
				},
				data=json.dumps(data), 
				allow_redirects=False
			)			

			if res.status_code != 200:
				raise Exception()
		except:
			print Fore.RED + '[' + time.strftime("%c") + '] Failed to register file with LemonStand!' + Style.RESET_ALL

	def remove (self, event_path):
		key = self.__getKey(event_path)

		try:
			self.connection["bucket"].delete_key(key)
			print Fore.GREEN + '[' + time.strftime("%c") + '] Successfully removed ' + key + Style.RESET_ALL
		except:
			if (self.retries > 0):
				self.retries-=1
				self.__checkConnection()
				self.remove(event_path)
			else:
				print Fore.RED + '[' + time.strftime("%c") + '] Failed to remove ' + key + Style.RESET_ALL

		# Register the file with LS
		self.__register(event_path)

	def upsert (self, event_path):
		key = self.__getKey(event_path)
		expires = int(time.time())
		headers = {
			'Cache-Control': "max-age=" + str(expires) + ", public",
			'Expires': expires
		}

		try:
			k = self.connection["bucket"].new_key(key)
			k.set_contents_from_filename(event_path, headers=headers)
			print Fore.GREEN + '[' + time.strftime("%c") + '] Successfully uploaded ' + key + Style.RESET_ALL
		except:
			if (self.retries > 0):
				self.retries-=1
				self.__checkConnection()
				self.upsert(event_path)
			else:
				print Fore.RED + '[' + time.strftime("%c") + '] Failed to upload ' + key + Style.RESET_ALL

		# Register the file with LS
		self.__register(event_path)

	def on_modified (self, event):
		self.upsert(event.src_path)

	def on_created (self, event):
		self.upsert(event.src_path)

	def on_moved (self, event):
		self.upsert(event.dest_path)

	def on_deleted (self, event):
		self.remove(event.src_path)