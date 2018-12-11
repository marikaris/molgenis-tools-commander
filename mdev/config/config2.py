from configobj import ConfigObj

from mdev.config.home import get_properties_file

default_config = ConfigObj()
default_config.filename = str(get_properties_file())

default_config['git_root'] = ''
default_config.comments['git_root'] = ['The absolute path to the MOLGENIS git folder (e.g. /git/molgenis/)']

default_config['git_paths'] = 'test, test2'

user_config = ConfigObj(str(get_properties_file()))

default_config.merge(user_config)
default_config.write()
