import sys 
import time
import os 
import json
from watchdog.events import PatternMatchingEventHandler

class Listener (PatternMatchingEventHandler):
		
	def __init__ (self, connection, config, utils):

		if hasattr(config, 'file_patterns'):
			try:
				PatternMatchingEventHandler.patterns = json.loads(config.file_patterns)
			except:
				sys.exit('The configuration value for file_patterns needs to be valid JSON.')
		else:
			PatternMatchingEventHandler.patterns = [ "*.md", "*.yaml","*.ini","*.conf","*.cfg","*.png", "*.jpeg", "*.jpg", "*.gif", "*.ico", "*.pdf", "*.htm","*.html","*.scss","*.css","*.js","*.coffee","*.htm" ]

		if hasattr(config, 'ignore_dirs'):
			try:
				PatternMatchingEventHandler.ignore_patterns = json.loads(config.ignore_dirs)
			except:
				sys.exit('The configuration value for ignore_dirs needs to be valid JSON.')
		else:
			PatternMatchingEventHandler.ignore_patterns = [ "*.tmp" , "*.git/*" ]

		PatternMatchingEventHandler.ignore_directories = True
		PatternMatchingEventHandler.case_sensitive = True

		self.connection = connection
		self.config = config
		self.utils = utils

	def __getKey (self, event_path):
		# strip out the watch dir, from the modified path to get the relative folder in S3
		path = event_path.replace(self.config.watch_dir, '')
		# this will create the full s3 key
		key = os.path.join(self.connection["store"], "themes", self.connection["theme"], path)

		return key

	def remove (self, event_path):
		key = self.__getKey(event_path)

		try:
			self.connection["bucket"].delete_key(key)
			print '\033[92m' + '[' + time.strftime("%c") + '] Successfully removed ' + key + ''
		except:
			print '\033[91m' + '[' + time.strftime("%c") + '] Failed to remove ' + key + ''

	def upsert (self, event_path):
		key = self.__getKey(event_path)

		try:
			k = self.connection["bucket"].new_key(key)
			k.set_contents_from_filename(event_path)
			print '\033[92m' + '[' + time.strftime("%c") + '] Successfully uploaded ' + key + ''
		except:
			print '\033[91m' + '[' + time.strftime("%c") + '] Failed to upload ' + key + ''


	def on_modified (self, event):
		self.upsert(event.src_path)

	def on_created (self, event):
		self.upsert(event.src_path)

	def on_moved (self, event):
		self.upsert(event.dest_path)

	def on_deleted (self, event):
		self.remove(event.src_path)