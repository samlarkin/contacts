import sys
import os
import json
from json.decoder import JSONDecodeError

from tabulate import tabulate

from colors import Colors
from uuids import new_uuid


class ContactData:
    """Data holder for contact information"""

    def __init__(self, json_path):
        """Construct ContactData instance"""
        self.json_path = json_path
        self.contacts = self.read_json()

    def __repr__(self):
        """Return simple string to represent ContactData instance"""
        return f'ContactData({self.json_path})'

    def read_json(self):
        """Read existing contact list from json file.

        Return existing contacts as a list of dicts.
        """
        with open(self.json_path, 'r') as f:
            contacts = json.load(f)
        contacts.sort(key=lambda k: k['name'])
        return contacts

    def overwrite(self):
        """Write self.contacts to json file"""
        self.contacts.sort(key=lambda k: k['name'])
        with open(self.json_path, 'w+') as f:
            json.dump(self.contacts, f)
        sys.stderr.write(f'overwriting ... {self.json_path}')
        return

    def query(self, query):
        """Query contact information.

        Return a set of indices corresponding to matching contacts.
        """
        matching_indices = set()
        for index, contact in enumerate(self.contacts):
            for value in contact.values():
                if isinstance(value, str):
                    if query.lower() in value.lower():
                        matching_indices.add(index)
                elif isinstance(value, list):
                    for subvalue in value:
                        if query.lower() in subvalue.lower():
                            matching_indices.add(index)
                            break
                elif value is None:
                    continue
                else:
                    raise TypeError('Invalid contact entry')
        return matching_indices

    def list_matches(self, indices):
        matches = [self.contacts[i] for i in indices]
        return matches

    def show(self, indices=None, args=None):
        """Write pretty matches to stdout"""
        matches = self.list_matches(indices)
        pretty_matches = []
        for match in matches:
            pretty_dict = {}
            for k, v in match.items():
                if k == 'tags' or k == 'uuid':  # Don't show tags or uuid
                    continue
                elif k == 'name':
                    color = Colors.NAME
                    pretty_v = f'{color}{v}{Colors.ENDC}'
                elif k == 'email':
                    color = Colors.EMAIL
                elif k == 'phone':
                    color = Colors.PHONE
                if v is None:
                    pretty_v = f'{color}...{Colors.ENDC}'
                if isinstance(v, list):
                    ellipsis = ''
                    if len(v) > 1:
                        ellipsis = ' + ... '
                    pretty_v = f'{color}{v[0]}{ellipsis}{Colors.ENDC}'
                v = pretty_v
                pretty_dict.update({k: v})
            pretty_matches.append(pretty_dict)
        sys.stdout.write(tabulate(pretty_matches, headers='keys'))
        sys.stdout.write('\n')
        sys.stdout.close()
        return

    def export(self, indices=None, args=None):
        """Export matching contacts as json"""
        output = []
        for match in self.list_matches(indices):
            output.append(match)
        sys.stdout.write(json.dumps(output))
        return

    def edit(self, indices=None, args=None):
        """Manually edit contacts with vim"""
        contact_tmp = '/home/sam/tmp/contact_tmp'
        if len(indices) != 1:
            raise ValueError('You must edit exactly one contact at a time')
        index = indices.pop()
        with open(contact_tmp, 'w+') as tmpfile:
            json.dump(self.contacts[index], tmpfile)
        os.system(f'vim {contact_tmp}')
        with open(contact_tmp, 'r') as tmpfile:
            edited_contact = json.load(tmpfile)
        self.contacts[index] = edited_contact
        self.overwrite()
        os.remove(contact_tmp)
        return

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
            sys.stderr.write(f'Modifying contact ... \n'
                             f'{self.contacts[index]}\n'
                             f'to ... \n'
                             f'{modified_contact}')
            sys.stderr.write('\n')
            self.contacts[index] = modified_contact
        sys.stderr.close()
        self.overwrite()
        return

    def add(self, indices=None, args=None):
        """Add a contact"""
        new_contact = {'uuid': new_uuid()}
        for arg in ['name', 'email', 'phone', 'tags']:
            if getattr(args, arg) is not None:
                new_contact.update({arg: getattr(args, arg)})
            else:
                new_contact.update({arg: None})
        sys.stderr.write(f'adding contact info ... {new_contact}')
        self.contacts.append(new_contact)
        self.overwrite()
        return

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
        return

    def delete(self, indices=None, args=None):
        """Delete filtered contacts from main data file and store in a
        deleted contacts file
        """

        matches = self.list_matches(indices)
        verify = input('Are you sure? (y/n)\n')
        if verify.lower() == 'y' or verify.lower() == 'yes':
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
        else:
            sys.stderr.write('Exiting without deletion')
        return
