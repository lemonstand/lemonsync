import sys 
import time
import os 
import boto.s3 
import boto.s3.connection 
import hashlib

from boto.s3.key import Key
from watchdog.events import FileSystemEventHandler
from boto.s3.key import Key
from Config import config
from Connector import Connector

class Utils ():
	
	def __init__(self):
		# Get the s3 credentials for a federated user from the LemonStand2 API
		credentials = Connector()
		identity = credentials.getIdentity(config.api_host, config.store_host, config.api_access)

		self.conn = boto.s3.connection.S3Connection(aws_access_key_id=identity['key'], aws_secret_access_key=identity['secret'], security_token=identity['token']) 
		self.bucket = self.conn.get_bucket(identity['bucket'], validate = False)
		self.store = identity['store']
		self.theme = identity['theme']
		self.watch = config.watch_dir

	def file_changes (self):
		path = os.path.join(self.store, "themes", self.theme)
		rs_keys = self.bucket.list(prefix=path)
		for key_val in rs_keys:

			loc_path = key_val.name.replace(path+'/', '')

			# ignore git files
			if loc_path.startswith(".git"):
				continue

			md5hash = hashlib.md5(open(self.watch+loc_path).read()).hexdigest()

			# The etag is quotes, so they need to be removed to compare
			if (md5hash == key_val.etag[1:-1]):
				print 'match'