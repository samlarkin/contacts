"""Configuration"""

from os import environ
from pathlib import Path
from json import load

contacts_path = Path(environ['XDG_CONFIG_HOME'], 'contacts')

default_config = {
    'path': contacts_path,
    'working_data': contacts_path/'contacts.json',
    'backup_data': contacts_path/'contacts.json.bak',
    'deleted_data': contacts_path/'contacts_deleted.json',
    'backup_deleted_data': contacts_path/'contacts_deleted.json.bak',
    'tmp_edit_path': contacts_path/'contacts_tmp',
    'editor': Path(environ['EDITOR'])
}

config_file = contacts_path/'config.json'

if config_file.exists():
    with open(config_file, 'r') as cf:
        config = load(cf)
else:
    config = default_config
