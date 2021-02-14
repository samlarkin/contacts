"""Configuration file for customising data storage defaults."""

import os

default_data_dir = os.path.join(os.environ['HOME'], '.contacts')


class Config:
    data_dir = default_data_dir
    working_data = os.path.join(data_dir, 'contacts.json')
    backup_data = os.path.join(data_dir, 'contacts.json.bak')
    deleted_data = os.path.join(data_dir, 'contacts_deleted.json')
    del_bak_data = os.path.join(data_dir, 'contacts_deleted.json.bak')
    edit_tmp = os.path.join(data_dir, 'edit_tmp')
    editor = '/usr/bin/vim'
