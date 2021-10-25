class Config(object):
	DEVELOPMENT=False
	DEBUG=False
	TESTING=False

class Development(Config):
	DEVELOPMENT=True
	DEBUG=True
	TESTING=True

class Production(Config):
	pass