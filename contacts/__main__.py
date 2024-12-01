"""Main module for contacts package"""
import sys
from .cli import CLI
from .contacts import ContactManager
from .conf import config


def main():
    """Main procedure"""
    cli = CLI()
    args = cli.args
    contact_manager = ContactManager(config['working_data'])
    indices = contact_manager.query(args.query_str)

    if args.subcommand is None:
        cli.parser.print_help()
        sys.exit()

    subcommand_callable = getattr(contact_manager, args.subcommand)
    subcommand_callable(indices=indices, args=args)


if __name__ == '__main__':
   main() 
