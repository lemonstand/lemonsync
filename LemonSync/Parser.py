import sys
import getopt
from ConfigParser import SafeConfigParser

sections = 'api', 'dir', 'store'

class Parser (object):
	def __init__(self, *file):
		parser = SafeConfigParser()
		parser.optionxform = str
		found = parser.read(file)
		if not found:
			sys.exit('No config file found!')
		for name in sections:
			self.__dict__.update(parser.items(name))