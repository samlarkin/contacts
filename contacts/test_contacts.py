"""Tests for the contacts module.

Author: Sam Larkin
Date: 2021-02-12
"""

import unittest
import json
import os

from shutil import copyfile

import contacts


class TestContacts(unittest.TestCase):
    """Test contact management utilities"""

    def setUp(self):
        """Set up for testing.

        Instantiate a ContactData object. Make a copy of the example
        dataset and read test data from the copy (so the example does
        not become corrupted in the event of unexpected behaviour).
        """

        copyfile('example_contacts.json', 'test_contacts.json')
        self.json_file = 'test_contacts.json'
        self.data = contacts.ContactData(self.json_file)

    def tearDown(self):
        """Tear down after testing.

        Remove test_contacts.json file which may or may not have been
        edited by the preceding test.
        """

        os.remove('test_contacts.json')

    def test_read_json(self):
        """Test read_json method (used in ContactData constructor)."""

        with open(self.json_file, 'r') as f:
            raw = json.load(f)
            raw.sort(key=lambda k: k['name'])
            correct_result = raw
        self.assertEqual(self.data.contacts, correct_result)

    def test_repr(self):
        """Test ContactData __repr__."""

        correct_result = f'ContactData({self.json_file})'
        self.assertEqual(repr(self.data), correct_result)

    def test_overwrite(self):
        """Test overwrite method.

        The overwritten file should be in exactly the same format as
        the input read during the setUp function.
        """
        self.data.overwrite()
        with open(self.json_file, 'r') as overwritten_f:
            test_data = json.load(overwritten_f)
        with open('example_contacts.json', 'r') as correct_f:
            example_data = json.load(correct_f)
        correct_result = sorted(example_data, key=lambda k: k['name'])
        self.assertEqual(test_data, correct_result)

    def test_query(self):
        """Test query method."""
        pass

    def test_list_matches(self):
        """Test list_matches method."""
        pass

    def test_show(self):
        """Test show method."""
        pass

    def test_export(self):
        """Test export method."""
        pass

    def test_edit(self):
        """Test edit method."""
        pass

    def test_modify(self):
        """Test modify method."""
        pass

    def test_add(self):
        """Test add method."""
        pass

    def test_import_json(self):
        """Test import_json method."""
        pass

    def test_get_field(self):
        """Test get_field method."""
        pass

    def test_delete(self):
        """Test delete method."""
        pass


if __name__ == '__main__':
    unittest.main()
