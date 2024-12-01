import sys
import os
import json
import subprocess
from json.decoder import JSONDecodeError
from shutil import get_terminal_size
from uuid import uuid1

from tabulate import tabulate

from .conf import config

# Color and formatting definitions for pretty printing
colors = {
    'no_color': '\033[0m',
    'name': '\033[95m',
    'email': '\033[96m',
    'phone': '\033[92m'
}


def new_uuid():
    return str(uuid1())


def read_json(path):
    """Read existing contact list from json file.

    Return existing contacts as a list of dicts (assuming json file is in
    the correct format.
    """
    with open(path, 'r') as f:
        return json.load(f)


class ContactManager:
    """Stores and manipulates contact information"""

    def __init__(self, json_path):
        self.json_path = json_path
        self.contacts = read_json(self.json_path)
        self.sort()

    def __repr__(self):
        """Return simple string to represent ContactData instance"""
        return f'ContactManager({self.json_path})'

    def sort(self, by='name'):
        """Sort contacts in contact list by a given field"""
        self.contacts.sort(key=lambda contact: contact[by])

    def overwrite(self):
        """Write self.contacts to json file"""
        self.sort()
        sys.stderr.write(f'overwriting ... {self.json_path}')
        with open(self.json_path, 'w+') as f:
            json.dump(self.contacts, f)

    def query(self, query):
        """Query contact information.

        Return a set of indices corresponding to matching contacts. If no
        query string is supplied, return the indices of the full dataset (as a
        generator).
        """
        if query is None:
            return range(len(self.contacts))

        matching_indices = set()
        for index, contact in enumerate(self.contacts):
            values = [val for val in contact.values() if val is not None]
            for value in values:
                # Concatenate lists of phone numbers, emails, tags
                if isinstance(value, list):
                    value = ', '.join(value)

                if query.lower() in value.lower():
                    matching_indices.add(index)
        return list(matching_indices)

    def list_matches(self, indices):
        """Return a list of contacts at given indices"""
        return [self.contacts[i] for i in indices]

    def show(self, indices=None, args=None):
        """Write pretty matches to stdout"""
        term_size = get_terminal_size()
        matches = self.list_matches(indices)
        pretty_matches = []
        for index, match in enumerate(matches):
            pretty_dict = {"#": indices[index]}
            for k, v in match.items():
                if k in ('tags', 'uuid'):  # Don't show tags or uuid
                    continue
                if v is None:
                    v = '...'
                elif isinstance(v, list):
                    v = f'{v[0]}, ... '
                try:
                    color = colors[k]
                    v = f'{color}{v}{colors["no_color"]}'
                except IndexError:
                    pretty_v = v
                pretty_dict.update({k: v})
            pretty_matches.append(pretty_dict)

        nlines = None
        if len(pretty_matches) >= term_size.lines:
            nlines = term_size.lines - 5
            pretty_matches = pretty_matches[:nlines]

        sys.stdout.write(tabulate(pretty_matches, headers='keys'))
        sys.stdout.write('\n\n')
        sys.stdout.write(f'{len(indices)} contacts')
        if nlines is not None:
            sys.stdout.write(f', truncated to {nlines} lines\n')

    def export(self, indices=None, args=None):
        """Export matching contacts as json"""
        output = self.list_matches(indices)
        try:
            with open(args.output_file, 'w+') as output_file:
                output_file.write(json.dumps(output))
        except (TypeError, AttributeError) as error:
            sys.stdout.write(json.dumps(output))

    def edit(self, indices=None, args=None):
        """Manually edit contacts with text editor"""
        assert len(indices) == 1, 'You must edit exactly one contact at a time'
        index = indices.pop()
        with open(config['tmp_edit_path'], 'w+') as tmpfile:
            json.dump(self.contacts[index], tmpfile)
        process = subprocess.run([config['editor'], config['tmp_edit_path']])
        assert process.returncode == 0, 'Editor process exited with an error'
        with open(config['tmp_edit_path'], 'r') as tmpfile:
            edited_contact = json.load(tmpfile)
        self.contacts[index] = edited_contact
        self.overwrite()
        os.remove(config['tmp_edit_path'])

    def modify(self, indices=None, args=None):
        """Modify filtered contacts directly from the command line"""
        matches = self.list_matches(indices)
        for index, match in zip(indices, matches):
            modified_contact = {'uuid': match['uuid']}
            for arg in ['name', 'email', 'phone', 'tags']:
                if getattr(args, arg) is not None:
                    modified_contact.update({arg: getattr(args, arg)})
                else:
                    modified_contact.update({arg: match[arg]})
            msg = f'Modifying contact ... \n' \
                  f'{self.contacts[index]}\n' \
                  f'to ... \n' \
                  f'{modified_contact}\n'
            sys.stderr.write(msg)
            self.contacts[index] = modified_contact
        self.overwrite()

    def add(self, indices=None, args=None):
        """Add a contact"""
        new_contact = {'uuid': new_uuid()}
        for arg in ['name', 'email', 'phone', 'tags']:
            attr = getattr(args, arg)
            new_contact.update({arg: attr})
        sys.stderr.write(f'adding contact info ... \n{new_contact}\n')
        self.contacts.append(new_contact)
        self.overwrite()

    def import_json(self, args=None):
        """Write a function to import contacts"""
        pass

    def get_field(self, indices=None, args=None):
        """Write uuids of filtered contacts to stdout"""

        if args.fieldname is not None:
            matches = self.list_matches(indices)
            for match in matches:
                try:
                    value = match[args.fieldname]
                    if isinstance(value, list):
                        value = ' '.join(value)
                    sys.stdout.write(''.join([str(value), '\n']))
                except KeyError(
                    f'There is no fieldname {args.fieldname}...\n'
                    f'Try one of [name, uuid, email, phone, tags]'
                ):
                    sys.exit(1)

    def delete(self, indices=None, args=None):
        """Delete filtered contacts from main data file and store in a
        deleted contacts file
        """
        matches = self.list_matches(indices)
        sys.stderr.write('The following contacts are staged for deletion:\n')
        self.show(indices=indices)
        verify = input('Are you sure you want to delete these contacts? (y/n): ')
        if verify.lower() != 'y':
            sys.stderr.write('Exiting without deletion')
        sys.stderr.write(f'exiling contacts to ... {args.backup}\n')
        with open(args.backup, 'r+') as f:
            try:
                deleted = json.load(f)
            except JSONDecodeError:
                deleted = []
        with open(args.backup, 'w+') as f:
            json.dump(deleted + matches, f)
        for index in indices:
            self.contacts.pop(index)
        self.overwrite()
