try:
	import configparser
except ImportError:
	import ConfigParser as configparser
import os

def create_config(path):
	"""
	Створює файл конфігурації
	"""
	config = configparser.ConfigParser()
	config.add_section("Settings")
	config.set("Settings", "USERNAME", "[NO_USERNAME]")
	config.set("Settings", "TOWN", "[NO_TOWN]")
	
	with open(path, "w") as config_file:
		config.write(config_file)
 
 
def get_config(path):
	"""
	Повертає всі значення конфігурації
	"""
	if not os.path.exists(path):
		create_config(path)
	
	config = configparser.ConfigParser()
	config.read(path)
	return config
 
def get_setting(path, section, setting):
	"""
	Отримати значення конфігурації
	"""
	config = get_config(path)
	value = config.get(section, setting)
	return value

def set_setting(path, section, setting, value):
	"""
	Вставляє значення конфігурації
	"""
	config = get_config(path)
	config.set(section, setting, value)
	with open(path, "w") as config_file:
		config.write(config_file)


def delete_setting(path, section, setting):
	"""
	Видаляє значення конфігурації
	"""
	config = get_config(path)
	config.remove_option(section, setting)
	with open(path, "w") as config_file:
		config.write(config_file)