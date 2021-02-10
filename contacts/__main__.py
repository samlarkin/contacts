#!/usr/bin/env python3
"""Main module for contacts package.

Executes main procedures.
"""

from cli import ContactsCLI
from contacts import ContactData


def main():
    """Follow this main procedure when application is called"""
    processor = DataProcessor()
    processor.subcommand(indices=processor.indices, args=processor.args)
    return


class DataProcessor:
    """Process data using CLI arguments to determine required methods"""

    def __init__(self):
        self.args = ContactsCLI().args
        self.data = ContactData('/home/sam/documents/contacts.json')
        self.subcommand = self.get_subcommand_func()
        self.indices = self.get_indices()
        return

    def get_indices(self):
        """Get indices of contacts which match the filter string"""
        if self.args.filter is not None:
            indices = self.data.query(self.args.filter)
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


if __name__ == '__main__':
    main()
