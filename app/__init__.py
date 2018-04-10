from configparser import ConfigParser
import collections

class AppConfig(object):
    def __init__(self, config_path):
        self.config_path = config_path

    def get_config_dict(self):
        config = ConfigParser()
        config.read(self.config_path)
        sections_dict = {}
        defaults = config.defaults()
        temp_dict = {}
        for key in defaults.items():
            temp_dict[key] = defaults[key]
        sections_dict['default'] = temp_dict
        sections = config.sections()
        for section in sections:
            options = config.options(section)
            temp_dict = {}
            for option in options:
                temp_dict[option] = config.get(section,option)

            sections_dict[section] = temp_dict
        return sections_dict

config_object = AppConfig('config.ini')
config = config_object.get_config_dict()


from .banlist import *
