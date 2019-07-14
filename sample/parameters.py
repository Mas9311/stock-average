import argparse
import platform
import time


def default_configurations():
    return {
        'interface': True,      # True=GUI interface, False=CLI interface
        'symbol': None,         # No default symbol
        'market_price': None    # No default market_price
    }


def asset_type_choices():
    return ['stock', 'cryptocurrency']


def retrieve_parameters():
    """Retrieves the parameters from the console if provided.
    Returns the parameters in dict format.
    If an unknown argument is passed, print the --help screen.
    If no arguments are passed, then print the intro Welcome screen."""

    version_description = (
        '        ☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐           \n'
        '        ☐              ☐  stock-average v2.0.0  ☐              ☐           \n'
        '        ☐              ☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐              ☐           \n'
        '        ☐                                                      ☐           \n'
        '        ☐   Check if there are any new releases for this at:   ☐           \n'
        '        ☐   https://github.com/Mas9311/stock-average/releases  ☐           \n'
        '        ☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐           '
    )

    default = default_configurations()

    cmd_description = (
        '            ╔═══════════════════════════════════════════════════╗         ┃   \n'
        '            ║   Find your potential average of a stock/crypto   ║         ┃   \n'
        '            ╚═══════════════════════════════════════════════════╝         ┃   \n'
        '                                                                          ┃   \n'
        '  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛   '
    )

    parser = argparse.ArgumentParser(
        usage=py_cmd('[options]') + '                                        ┃',
        description=cmd_description,
        add_help=False,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    interface = parser.add_mutually_exclusive_group(required=False)
    interface.add_argument(
        '-g', '--gui',
        action='store_true',
        default=default['interface'],
        dest='interface',
        help='GUI interface: default=%(default)s.  No additional argument needed.'
    )

    interface.add_argument(
        '-c', '--cli',
        action='store_false',
        default=not default['interface'],
        dest='interface',
        help='CLI interface: default=%(default)s. No additional argument needed.'
    )

    parser.add_argument(
        '-s', '--symbol',
        type=str,
        metavar='',
        dest='symbol',
        help='SYMBOL name of the stock or cryptocurrency.'
    )

    parser.add_argument(
        '-p', '--price',
        type=float,
        default=default['market_price'],
        metavar='',
        dest='market_price',
        help='Current market PRICE of the symbol.'
    )

    parser.add_argument(
        '-v', '--version',
        action='version',
        version=version_description,
        help='VERSION prints to console, and exits.'
    )

    parser.add_argument(
        '-h', '--help',
        action='help',
        default=argparse.SUPPRESS,
        help='HELP message is displayed (this is the message), and exits'
    )

    known_args, unknown_args = parser.parse_known_args()

    if unknown_args:  # user added unknown arguments
        print(f'Unknown arguments detected: {str(unknown_args)}\n > calling --help screen\n')
        parser.print_help()  # prints help message
        time.sleep(0.25)  # pause execution just long enough for help to display
        parser.parse_args()  # prints error message and halts the execution

    # converts the execution's arguments from a Namespace type => dictionary type
    arg_dict = {
        'interface': known_args.interface,
        'symbol': known_args.symbol,
        'market_price': known_args.market_price,
    }

    return arg_dict


def py_cmd(additional=''):
    cmd = ('python3', 'python.exe')[platform.system() == 'Windows'] + ' run.py'
    if additional:
        additional.strip()
        num_spaces = 0 if platform.system() == 'Windows' else 3
        spaces = ' ' * num_spaces
        cmd += ' ' + additional + spaces
    return cmd
