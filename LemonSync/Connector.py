import sys 
import time
import os 
import json
import requests
import boto.s3 
import boto.s3.connection 
from boto.s3.key import Key
from colorama import Fore, Back, Style

class Connector:

	def __init__ (self):
		self.connection = {}
		self.identity = None

	# Handke the connection to the LemonStand API
	def get_identity (self, api_host, store_host, api_access):

		# This is the API endpoint that will give us access to our s3 bucket in AWS
		path = '/v2/identity/s3'

		# We need to give the API the store-host and the access token,
		# which are both read in from the configuration file
		headers = { 
			'content-type': 'application/json',
			'x-store-host': store_host, 
			'authorization': api_access
		}

		try:
			# The connection will fail if the configuation values are not set correctly.
			r = requests.get(api_host + path, headers=headers, allow_redirects=False)
		except:
			sys.exit(Fore.RED + "Could not make connection to LemonStand. Please make sure your configuration values are set correctly." + Style.RESET_ALL)

		if r.status_code != 200:
			sys.exit(Fore.RED + 'Access token or store host is not valid!' + Style.RESET_ALL)

		response = r.json()

		return response

	# Handles the connection to s3
	def s3_connection (self, identity):
		connection = {}

		try:
			connection["conn"] = boto.s3.connection.S3Connection(aws_access_key_id=identity['key'], aws_secret_access_key=identity['secret'], security_token=identity['token']) 
			connection["bucket"] = connection["conn"].get_bucket(identity['bucket'], validate = False)
			connection["store"] = identity['store']
			connection["theme"] = identity['theme']
			connection["bucket_name"] = identity['bucket']
		except:
			sys.exit(Fore.RED + 'Could not make connection to s3! Please make sure your configuration values are set correctly.' + Style.RESET_ALL)

		return connection