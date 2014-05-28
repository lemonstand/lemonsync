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
import time
import os 
import json
import requests
import time
from Connector import Connector
from watchdog.events import PatternMatchingEventHandler
from colorama import Fore, Back, Style

class Listener (PatternMatchingEventHandler):
	# The number of times to retry a connection to LemonStand API
	RETRIES = 2

	def __init__ (self, connection, config, utils):
		PatternMatchingEventHandler.patterns = config.file_patterns
		PatternMatchingEventHandler.ignore_patterns = config.ignore_patterns
		PatternMatchingEventHandler.ignore_directories = True
		PatternMatchingEventHandler.case_sensitive = True

		self.connection = connection
		self.config = config
		self.utils = utils
		self.reset = self.RETRIES

	def __checkConnection (self):
		# Get a new connection object to lemonstand API
		c = Connector()
		identity = c.get_identity(self.config.api_host, self.config.store_host, self.config.api_access)
		connection = c.s3_connection(identity);
		self.connection = connection

		return

	def __reset_retries (self):
		self.reset = self.RETRIES

	def __register (self, event_path):
		path = event_path.replace(self.config.watch_dir, '')
		data = { 'key': path }

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
			print(Fore.RED + '[' + time.strftime("%c") + '] Failed to register file with LemonStand!' + Style.RESET_ALL)

	def remove (self, event_path):
		path = event_path.replace(self.config.watch_dir, '')
		key = "/".join([self.connection["store"], "themes", self.connection["theme"], path])

		try:
			self.connection["bucket"].delete_key(key)
			print(Fore.GREEN + '[' + time.strftime("%c") + '] Successfully removed ' + path + Style.RESET_ALL)
		except:
			if (self.reset > 0):
				self.reset-=1
				self.__checkConnection()
				self.remove(event_path)
			else:
				print(Fore.RED + '[' + time.strftime("%c") + '] Failed to remove ' + path + Style.RESET_ALL)

		self.__reset_retries()
		# Register the file with LS
		self.__register(event_path)

	def upsert (self, event_path):
		path = event_path.replace(self.config.watch_dir, '')
		key = "/".join([self.connection["store"], "themes", self.connection["theme"], path])
		expires = int(time.time())
		headers = {
			'Cache-Control': "max-age=" + str(expires) + ", public",
			'Expires': expires
		}

		try:
			k = self.connection["bucket"].new_key(key)
			k.set_contents_from_filename(event_path, headers=headers)
			print(Fore.GREEN + '[' + time.strftime("%c") + '] Successfully uploaded ' + path + Style.RESET_ALL)
		except:
			if (self.reset > 0):
				self.reset-=1
				self.__checkConnection()
				self.upsert(event_path)
			else:
				print(Fore.RED + '[' + time.strftime("%c") + '] Failed to upload ' + path + Style.RESET_ALL)

		self.__reset_retries()
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