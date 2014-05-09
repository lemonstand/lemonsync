import sys 
import time
import os 
import boto.s3 
import boto.s3.connection 
import hashlib

from boto.s3.key import Key
from watchdog.events import FileSystemEventHandler
from boto.s3.key import Key

class Utils ():

	def __init__ (self, connection, config):
		self.connection = connection
		self.config = config

	def file_changes (self):
		modified_files = []
		path = os.path.join(self.connection["store"], "themes", self.connection["theme"])
		rs_keys = self.connection["bucket"].list(prefix=path)

		# Go though each file in s3 and compare it with the local file system
		for key_val in rs_keys:

			loc_path = key_val.name.replace(path+'/', '')

			# ignore git files
			if loc_path.startswith(".git/"):
				continue

			if not os.path.isfile(self.config.watch_dir + loc_path):
				modified_files.append(loc_path)
			else:
				md5hash = hashlib.md5(open(self.config.watch_dir + loc_path).read()).hexdigest()
				# The etag is quotes, so they need to be removed to compare
				if not (md5hash == key_val.etag[1:-1]):
					modified_files.append(loc_path)

		return modified_files

	#  Download changed files from LemonStand and save them locally
	def sync (self, files):
		for modified in files:
			# this will create the full s3 key
			path = os.path.join(self.config.watch_dir, modified)
			key = os.path.join(self.connection["store"], "themes", self.connection["theme"], modified)

			# Split the path into the directoy and the filename
			file_dir, file_name = os.path.split(path)

			# Check to see if the file path exists, and create the needed 
			# directories if it does not
			if not os.path.exists(file_dir):
				os.makedirs(file_dir, 0755)

			if not os.path.isdir(path):
				# This will create the file if it does not exist
				f = open(path, 'w+')
				k = self.connection["bucket"].new_key(key)
				k.get_contents_to_file(f)
			# except:
			# 	sys.exit('Error! Could not create the needed directories.')

			print '\033[92m' + '[' + time.strftime("%c") + '] Successfully downloaded ' + key + ''

		return
