import sys
import getopt
from ConfigParser import SafeConfigParser

sections = 'api', 'dir', 'store'

class Config (object):
	def __init__(self, *file):
		parser = SafeConfigParser()
		parser.optionxform = str
		found = parser.read(file)
		if not found:
			raise ValueError('No config file found!')
		for name in sections:
			self.__dict__.update(parser.items(name))


if len(sys.argv) < 2:
	print 'Usage: lemonsync --config=<configfile>'
	sys.exit(2)

try:
	opts, args = getopt.getopt(sys.argv[1:],"c:f:",["config="])
except getopt.GetoptError:
	print 'Usage: lemonsync --config=<configfile>'
	sys.exit(2)

file = None

for o, a in opts:
	if o in ("-c", "--config"):
		file = a
	else:
		assert False, "unhandled option"

config = Config(file)