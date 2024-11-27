import argparse
import sys

from .conf import Config


class CLI():
    """Parses command line arguments for contacts program"""
    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument(
            '-q',
            '--query',
            default=None,
            type=str,
            help='Query contacts list by checking for matches to this string' \
                 '(in any field.'
        )
        self.subparsers = self.parser.add_subparsers(dest='subcommand')
        self.gen_show_parser()
        self.gen_export_parser()
        self.gen_modify_parser()
        self.gen_add_parser()
        self.gen_import_parser()
        self.gen_edit_parser()
        self.gen_get_field_parser()
        self.gen_delete_parser()
        try:
            self.args = self.parser.parse_args()
        except argparse.ArgumentError:
            sys.stderr.write('Invalid arguments passed')
            self.parser.print_help()
            sys.exit(1)

    def gen_show_parser(self):
        show_parser = self.subparsers.add_parser('show', help='Show help')
        show_parser.add_argument(
            '-c',
            '--color',
            action='store_true',
            default=False,
            help='Show contacts with colored output'
        )

    def gen_export_parser(self):
        export_parser = self.subparsers.add_parser(
            'export',
            help='Export help',
        )
        export_parser.add_argument(
            '-o',
            '--output_file',
            type=str,
            default=None,
            help='Optional output file path. Default is writing to stdout.'
        )

    def gen_modify_parser(self):
        modify_parser = self.subparsers.add_parser(
            'modify',
            help='Modify help',
        )
        modify_parser.add_argument(
            '-n',
            '--name',
            type=str,
            help='Modify contact name and overwrite with new value.'
        )
        modify_parser.add_argument(
            '-e',
            '--email',
            nargs='+',
            type=str,
            help='Modify contact emails and overwrite with new values.'
        )
        modify_parser.add_argument(
            '-p',
            '--phone',
            nargs='+',
            type=str,
            help='Modify contact phone numbers and overwrite with new values.'
        )
        modify_parser.add_argument(
            '-t',
            '--tags',
            nargs='+',
            type=str,
            help='Modify contact tags and overwrite with new values.'
        )

    def gen_add_parser(self):
        add_parser = self.subparsers.add_parser('add', help='Add help')
        add_parser.add_argument(
            '-n',
            '--name',
            type=str,
            help='Add contact name.'
        )
        add_parser.add_argument(
            '-e',
            '--email',
            nargs='+',
            type=str,
            help='Add contact emails.'
        )
        add_parser.add_argument(
            '-p',
            '--phone',
            nargs='+',
            type=str,
            help='Add contact phone numbers.'
        )
        add_parser.add_argument(
            '-t',
            '--tags',
            nargs='+',
            type=str,
            help='Add contact tags.'
        )

    def gen_import_parser(self):
        import_parser = self.subparsers.add_parser(
            'import',
            help='Import help'
        )
        import_parser.add_argument(
            'input_file',
            type=str,
            help='Path to JSON file'
        )

    def gen_edit_parser(self):
        edit_parser = self.subparsers.add_parser('edit', help='Edit help')
        edit_parser.add_argument(
            '--editor',
            default=Config.editor,
            help='Manually select a text editor.'
        )

    def gen_get_field_parser(self):
        get_field_parser = self.subparsers.add_parser(
            'get_field',
            help='get field help'
        )
        get_field_parser.add_argument(
            'fieldname',
            help='fieldname to get value for'
        )

    def gen_delete_parser(self):
        delete_parser = self.subparsers.add_parser(
            'delete',
            help='delete'
        )
        delete_parser.add_argument(
            '--backup',
            default=Config.deleted_data,
            help='path to backup file where deleted contacts will be exiled'
        )
