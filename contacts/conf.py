"""Configuration file for customising data storage defaults."""

import os
from pathlib import Path

default_path = Path(os.environ['XDG_CONFIG_HOME'], 'contacts')


class Config:
    path = default_path
    working_data = Path(path, 'contacts.json')
    backup_data = Path(path, 'contacts.json.bak')
    deleted_data = Path(path, 'contacts_deleted.json')
    del_bak_data = Path(path, 'contacts_deleted.json.bak')
    edit_tmp = Path(path, 'edit_tmp')
    editor = Path('/usr/bin/vim')
