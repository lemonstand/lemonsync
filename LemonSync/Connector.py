import sys 
import time
import os 
import json
import requests
import boto.s3 
import boto.s3.connection 
from boto.s3.key import Key

class Connector:

	def __init__ (self):
		self.connection = {}
		self.identity = None

	# Handke the connection to the LemonStand API
	def getIdentity (self, api_host, store_host, api_access):

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
			sys.exit("Could not make connection to LemonStand. Please make sure your configuration values are set correctly.")

		response = r.json()

		if 'errors' in response:
			sys.exit('Error! Access token or store host is not valid.')

		return response

	# Handles the connection to s3
	def s3Connection (self, identity):
		connection = {}

		try:
			connection["conn"] = boto.s3.connection.S3Connection(aws_access_key_id=identity['key'], aws_secret_access_key=identity['secret'], security_token=identity['token']) 
			connection["bucket"] = connection["conn"].get_bucket(identity['bucket'], validate = False)
			connection["store"] = identity['store']
			connection["theme"] = identity['theme']
		except:
			print "Could not make connection to s3. Please make sure your configuration values are set correctly."

		return connection