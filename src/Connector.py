import sys 
import time
import os 
import json
import requests

class Connector:
	# Need an AWS key, ID, and access token to talk to S3
	def getIdentity(self, api_host, store_host, api_access):

		path = '/v2/s3/identity'
		headers = { 
			'content-type': 'application/json',
			'x-store-host': store_host, 
			'authorization': api_access
		}

		r = requests.get(api_host + path, headers=headers, allow_redirects=False)
		return r.json()