import ConfigParser

class property_fetcher:

    def __init__(self, property_file):
        self.property_file = property_file

    def get_property(self, section, value):
        config = ConfigParser.RawConfigParser()
        config.read(self.property_file)
        return config.get(section, value)