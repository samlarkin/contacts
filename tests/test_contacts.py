"""Tests for the contacts module."""

import json
import os
import unittest

from unittest.mock import patch
from shutil import copyfile#, get_terminal_size
from io import StringIO
from pathlib import Path

from contacts.contacts import ContactManager

class TestContacts(unittest.TestCase):
    """Test contact management utilities"""

    def setUp(self):
        """Set up for testing.

        Instantiate a ContactManager object. Make a copy of the example
        dataset and read test data from the copy (so the example does
        not become corrupted in the event of unexpected behaviour).
        """
        self.orig_json_file = Path('tests/test_data/example_contacts.json')
        self.json_file = Path('tests/test_data/test_contacts.json')
        copyfile(
            self.orig_json_file,
            self.json_file
        )
        self.data = ContactManager(self.json_file)

    def tearDown(self):
        """Tear down after testing.

        Remove test_contacts.json file which may or may not have been
        edited by the preceding test.
        """
        os.remove(self.json_file)

    def test_read_json(self):
        """Test read_json method (used in ContactManager constructor)."""
        with open(self.json_file, 'r') as f:
            raw = json.load(f)
            raw.sort(key=lambda k: k['name'])
            correct_result = raw

        self.assertEqual(self.data.contacts, correct_result)

    def test_repr(self):
        """Test ContactManager __repr__ returns expected string."""
        correct_result = f'ContactManager({self.json_file})'
        self.assertEqual(repr(self.data), correct_result)

    def test_overwrite(self):
        """Test overwrite method.

        The overwritten file should be in exactly the same format as
        the input read during the setUp function, but it should be
        sorted alphabetically by name.
        """
        with patch('sys.stderr', new=StringIO()) as mock_stderr:
            self.data.overwrite()
            correct_stderr = f'overwriting ... {self.json_file}'
            self.assertEqual(mock_stderr.getvalue(), correct_stderr)

        with open(self.json_file, 'r') as overwritten_f:
            test_data = json.load(overwritten_f)

        with open(self.orig_json_file, 'r') as correct_f:
            example_data = json.load(correct_f)

        correct_result = sorted(example_data, key=lambda k: k['name'])
        self.assertEqual(test_data, correct_result)

    def test_query(self):
        """Test query method returns the correct set of indices.

        The query should return a set of indices corresponding to
        contacts which contain query_string.lower() in any field
        except uuid.

        The correct result has been deterined by manual inspection of
        the testing data set.
        """
        query_string = 'Rick'
        test_indices = self.data.query(query_string)
        correct_indices = {68, 13, 15, 18, 21, 56, 59}
        self.assertEqual(test_indices, correct_indices)

    def test_list_matches(self):
        """Test list_matches method."""
        test_indices = {56, 46}
        test_matches = self.data.list_matches(test_indices)
        correct_result = [
            {'name': 'Rick Sanchez',
             'email': ['rick.sanchez@plumbus.com'],
             'phone': ['07655266089'],
             'uuid': 'ca064182-6b04-11eb-844f-274375519e58',
             'tags': []},
            {'name': 'Morty Smith',
             'email': ['morty.smith@plumbus.com'],
             'phone': ['07698312584'],
             'uuid': 'ca063a5c-6b04-11eb-844f-274375519e58',
             'tags': []}
        ]
        self.assertEqual(test_matches, correct_result)

#    def test_show(self):
#        """Test show method.
#
#        Mock up stdout with StringIO object and test that the output of
#        the show method is as expected.
#        """
#        term_size = get_terminal_size()
#        with patch('sys.stdout', new=StringIO()) as mock_stdout:
#            self.data.show(range(len(self.data.contacts)))
#            test_show = mock_stdout.getvalue()
#            with open('test/expected_show_result.txt', 'r') as f:
#                correct_result = f.read()
#            cutoff = term_size.lines - 5
#            truncated_correct = ''.join(
#                    [correct_result[:cutoff],
#                     f'{len(self.data.contacts)} contacts, truncated to '
#                     f'{cutoff} lines']
#            )
#            self.assertEqual(test_show, truncated_correct)

    def test_export(self):
        """Test export method.

        Mock up stdout with a StringIO object and test that the export
        method correctly dumps the contacts data to the mocked output
        as json.
        """

        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.data.export(range(len(self.data.contacts)))
            test_export = mock_stdout.getvalue()
            correct_export = json.dumps(self.data.contacts)
            self.assertEqual(test_export, correct_export)

#    def test_edit(self):
#        """Test edit method."""
#        pass
#
#    def test_modify(self):
#        """Test modify method."""
#        pass
#
#    def test_add(self):
#        """Test add method."""
#        pass
#
#    def test_import_json(self):
#        """Test import_json method.
#
#        Method not yet implemented...
#        """
#        pass
#
#    def test_get_field(self):
#        """Test get_field method."""
#        pass
#
#    def test_delete(self):
#        """Test delete method."""
#        pass


if __name__ == '__main__':
    unittest.main()
