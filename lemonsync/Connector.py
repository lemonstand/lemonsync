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
			r = requests.get(api_host + path, headers=headers, allow_redirects=False, verify=False)
		except:
			sys.exit(Fore.RED + "Could not make connection to LemonStand!" + Style.RESET_ALL)

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
			sys.exit(Fore.RED + 'Could not make connection to s3!' + Style.RESET_ALL)

		return connection