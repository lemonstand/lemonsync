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


config = Config('config.cfg')