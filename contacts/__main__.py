#!/usr/bin/env python3
"""Main module for contacts package"""

from .cli import CLI
from .contacts import ContactManager
from .conf import Config


class ContactProcessor:
    """Process contact data using CLI arguments to determine required
    operations.
    """

    def __init__(self):
        self.args = CLI().args
        self.data = ContactManager(Config.working_data)
        self.subcommand = self.get_subcommand_func()
        self.indices = self.get_indices()

    def get_indices(self):
        """Get indices of contacts which match the query string"""
        if self.args.query is not None:
            indices = self.data.query(self.args.query)
        else:
            indices = range(len(self.data.contacts))
        return indices

    def get_subcommand_func(self):
        """Get callable from string representing subcommand method"""
        if self.args.subcommand is not None:
            subcommand = getattr(self.data, self.args.subcommand)
        else:
            subcommand = getattr(self.data, 'show')
        return subcommand


def main():
    """Follow this main procedure when application is called"""
    processor = ContactProcessor()
    processor.subcommand(indices=processor.indices, args=processor.args)


if __name__ == '__main__':
    main()
