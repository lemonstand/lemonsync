import unittest
import sys
import os
import argparse
import shutil
sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))
from lemonsync.LemonSync import *

class TestUpload (unittest.TestCase):
	directory = '/tmp/LemonSync/test'

	def setUp (self):
		# Create a local directory for testing
		if not os.path.exists(self.directory):
			os.makedirs(self.directory)

	def tearDown (self):
		shutil.rmtree(self.directory)

	def test_upload_dir (self):
		assert True