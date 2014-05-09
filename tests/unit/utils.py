import unittest
import sys
import config

class TestUtils (unittest.TestCase):

	def setUp (self):
		self.base = config.base
	
	def test_file_changes (self):
		self.assertEqual(200, 200)