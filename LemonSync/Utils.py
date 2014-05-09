import sys 
import time
import os 
import boto.s3 
import boto.s3.connection 
import hashlib
import shutil

from sys import version_info
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
			if loc_path.startswith(".git"):
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
		for f in files:
			# ignore git files
			if f.startswith(".git"):
				continue
			path = os.path.join(self.config.watch_dir, f)
			key = os.path.join(self.connection["store"], "themes", self.connection["theme"], f)

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

	# 
	def reset_remote (self):
		print 1

	def reset_local (self):

		print '\033[91m' + 'Are you sure you want to permanlty overwrite ' + self.config.watch_dir + ' with the remote theme folder?' + '\033[91m'
		print '\033[91m' + 'Type [Y] to overwrite your local files or [q] to quit. Any other key will result in no action being taken.' + '\033[91m'

		if version_info[0] > 2:
			response = input(": ")
		else:
			response = raw_input(": ")

		if not response == "Y":
			sys.exit(1)

		for the_file in os.listdir(self.config.watch_dir):
			file_path = os.path.join(self.config.watch_dir, the_file)

			# Do not delete any git files
			if the_file.startswith(".git"):
				continue

			try:
				if os.path.isfile(file_path):
					os.unlink(file_path)
				elif os.path.isdir(file_path):
					shutil.rmtree(file_path)
			except Exception, e:
				print e

		path = os.path.join(self.connection["store"], "themes", self.connection["theme"])
		rs_keys = self.connection["bucket"].list(prefix=path)

		new_files = []

		for key_val in rs_keys:
			loc_path = key_val.name.replace(path+'/', '')
			new_files.append(loc_path)

		self.sync(new_files)

		return

	def clean_changes (self, changes):
 		for files in changes:
			print '--- ' + files
			print '\033[91m' + 'Version mismatch!' + '\033[91m'
			print '\033[91m' + 'Type [1] to overwrite your local files or [q] to quit. Any other key will result in your local files remaining the same.' + '\033[91m'

			if version_info[0] > 2:
				response = input(": ")
			else:
				response = raw_input(": ")

			if response == "1":
				# Sync the changed remote files with the local files
				self.sync(changes)
			elif response == "q":
				sys.exit(0)

		return
