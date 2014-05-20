import sys 
import time
import os 
import boto.s3 
import boto.s3.connection 
import hashlib
import shutil
import requests
import json

from sys import version_info
from boto.s3.key import Key
from watchdog.events import FileSystemEventHandler
from boto.s3.key import Key
from colorama import Fore, Back, Style
from pathtools.patterns import match_path

class Utils ():

	def __init__ (self, connection, config):
		self.connection = connection
		self.config = config

	def file_changes (self):
		modified_files = []
		# Windows compatible
		path = "/".join([self.connection["store"], "themes", self.connection["theme"]])
		rs_keys = self.connection["bucket"].list(prefix=path)

		# Go though each file in s3 and compare it with the local file system
		for key_val in rs_keys:
			loc_path = key_val.name.replace(path+'/', '')
			filepath = self.config.watch_dir + loc_path

			# Only remove files that are on the watch list
			if not match_path(filepath,
				included_patterns=self.config.file_patterns,
				excluded_patterns=self.config.ignore_patterns,
				case_sensitive=True):
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
			path = os.path.join(self.config.watch_dir, f)

			if not match_path(path,
				included_patterns=self.config.file_patterns,
				excluded_patterns=self.config.ignore_patterns,
				case_sensitive=True):
				continue

			key = "/".join([self.connection["store"], "themes", self.connection["theme"], f])

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

			print Fore.GREEN + '[' + time.strftime("%c") + '] Successfully downloaded ' + key + Style.RESET_ALL

		return

	# This will overwrite any contents in the remote theme with the contents of the watch_dir
	def reset_remote (self):
		print Back.RED + Fore.WHITE + 'Are you sure you want to permanlty overwrite your remote theme with the contents of ' + self.config.watch_dir + ' ?' + Style.RESET_ALL
		print Fore.RED + 'Type [Y] to overwrite your remote theme or [q] to quit. Any other key will result in no action being taken.' + Style.RESET_ALL

		if version_info[0] > 2:
			response = input(": ")
		else:
			response = raw_input(": ")

		if not response == "Y":
			sys.exit(0)

		self.remove_remote_files()

		# Get the filenames we about to push to s3
		uploads = []
		keynames = []

		for (source, dirname, filenames) in os.walk(self.config.watch_dir):
			for name in filenames:
				uploads.append(os.path.join(source, name))

		# Upload the new files
		for filename in uploads:
			keypath = filename.replace(self.config.watch_dir, '')
			keyname = "/".join([self.connection["store"], "themes", self.connection["theme"], keypath])

			# Only remove files that are on the watch list
			if not match_path(filename,
				included_patterns=self.config.file_patterns,
				excluded_patterns=self.config.ignore_patterns,
				case_sensitive=True):
				continue

			expires = int(time.time())
			headers = {
				'Cache-Control': "max-age=" + str(expires) + ", public",
				'Expires': expires
			}

			try:
				k = self.connection["bucket"].new_key(keyname)
				k.set_contents_from_filename(filename, headers=headers)
				keynames.append(keypath)
				print Fore.GREEN + '[' + time.strftime("%c") + '] Successfully uploaded ' + keyname + Style.RESET_ALL
			except:
				print Fore.RED + '[' + time.strftime("%c") + '] Failed to upload ' + keyname + Style.RESET_ALL

		# Notify LS2 that the files have changed
		try:
			data = { 'keys': keynames }
			# Update the resource with LemonStand
			res = requests.post(
				self.config.api_host + '/v2/theme/reset', 
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
			print Fore.RED + '[' + time.strftime("%c") + '] Failed to register local files with LemonStand!' + Style.RESET_ALL
		return

	def reset_local (self):

		print Back.RED + Fore.WHITE + 'Are you sure you want to permanlty overwrite ' + self.config.watch_dir + ' with the remote theme folder?' + Style.RESET_ALL
		print Fore.RED + 'Type [Y] to overwrite your local files or [q] to quit. Any other key will result in no action being taken.' + Style.RESET_ALL

		if version_info[0] > 2:
			response = input(": ")
		else:
			response = raw_input(": ")

		if not response == "Y":
			sys.exit(0)

		# Prepare the directory
		self.remove_local_files(self.config.watch_dir)

		path = os.path.join(self.connection["store"], "themes", self.connection["theme"])

		# retreive the list of keys from the bucket
		rs_keys = self.connection["bucket"].list(prefix=path)

		new_files = []

		for key_val in rs_keys:
			loc_path = key_val.name.replace(path+'/', '')
			new_files.append(loc_path)

		self.sync(new_files)

		return

	# Removes any application files from a directory.
	# This is used when resetting a folder with the upstream theme
	def remove_local_files (self, directory):
		for the_file in os.listdir(directory):
			file_path = os.path.join(directory, the_file)

			# Only remove files that are on the watch list
			if not match_path(file_path,
				included_patterns=self.config.file_patterns,
				excluded_patterns=self.config.ignore_patterns,
				case_sensitive=True):
				continue

			# Just in case the user did not .git to their list of ignore
			if the_file.startswith(".git"):
				continue

			try:
				if os.path.isfile(file_path):
					os.unlink(file_path)
				elif os.path.isdir(file_path):
					shutil.rmtree(file_path)
			except Exception, e:
				print e + Style.RESET_ALL
		return

	def remove_remote_files (self):
		# delete the contents of the remote bucket
		path = "/".join([self.connection["store"], "themes", self.connection["theme"]])
		keys = self.connection["bucket"].list(prefix=path)

		# rest the remote theme
		for key in keys:
			key.delete()

		return

	def clean_changes (self, changes):
 		for files in changes:
			print Fore.CYAN + ' --- ' + files + Style.RESET_ALL
			
		print Back.RED + Fore.WHITE + 'Version mismatch! Do you want to pull in changed files from your remote store?' + Style.RESET_ALL
		print Fore.RED + 'Type [Y] to overwrite your local files or [q] to quit. Any other key will result in your local files remaining the same.' + Style.RESET_ALL

		if version_info[0] > 2:
			response = input(": ")
		else:
			response = raw_input(": ")

		if response == "Y":
			# Sync the changed remote files with the local files
			self.sync(changes)
		elif response == "q":
			sys.exit(0)

		return