from sample import format, menu
import os
# import sys


def get_folder():
    """Returns the symbols/ folder path."""
    # return os.path.join('~/', 'Software', 'MyPrograms', 'stock-average', 'symbols')
    return os.path.join(os.getcwd(), 'symbols')


def get_file(symbol):
    """Returns the given symbol's file path."""
    return os.path.join(get_folder(), symbol.lower())


def modify_file(cli):
    """This function is called once the user has selected to modify a given value of the stock."""
    print(cli.symbol, cli.get_symbol())
    write_data_to_file(
        cli.get_symbol(),
        [
            f'{cli.get_symbol()} is a {cli.asset_type}',
            f'{cli.get_quantity()}',
            f'{cli.get_current_average()}',
            f'{cli.get_current_price()}'
        ]
    )
    print(format.Feedback(False, f'{cli.get_symbol()} has been updated.'))


def write_data_to_file(symbol, data):
    with open(get_file(symbol), 'w') as symbol_file:
        symbol_file.write(f'{data[0]}\n')
        symbol_file.write(f'{data[1]}\n')
        symbol_file.write(f'{data[2]}\n')
        symbol_file.write(f'{data[3]}\n')
        symbol_file.close()


def make_sure_dir_exists():
    """Creates the symbols folder if it does not exist."""
    symbols = get_folder()
    if not os.path.exists(symbols):
        os.mkdir(symbols)
        print(format.Feedback(False, f'Created the symbols folder.'))


def reread_quantity(my_stock):
    """Called when a file is modified from 'is not a crypto' -> 'is a crypto'.
    Retrieves the purchased_quantity from the file for decimal precision purposes."""
    with open(get_file(my_stock.symbol), 'r') as f:
        lines = f.read().splitlines()
        f.close()
        my_stock.purchased_quantity = format.best(float(lines[2]), my_stock.precision)


def file_exists(symbol):
    """Returns true if the file is already made and has valid values."""
    symbol = symbol.lower()
    file_path = get_file(symbol)
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            lines = f.read().splitlines()
            if len(lines) >= 3:
                try:
                    p_price = float(lines[1])
                    p_quantity = float(lines[2])
                    if len(lines) is 3:
                        return p_price >= 0 and p_quantity >= 0
                    c_price = float(lines[3])
                    return p_price >= 0 and p_quantity >= 0 and c_price >= 0
                except ValueError:
                    print(format.Feedback(True, [f'One lines in the {symbol} '
                                                 f'file is not a number.',
                                                 f'The file, {symbol} has been removed.',
                                                 f'We will recreate the {symbol} file now.']))
                    os.remove(file_path)
    return False


def assign_file_data_to_variables(cli):
    (asset_type, quantity, current_average, current_price) = retrieve_file_data(cli.get_symbol())
    if asset_type.lower().count('stock'):
        cli.asset_type.input = cli.asset_type.valid_options[0]
    else:
        cli.asset_type.input = cli.asset_type.valid_options[1]
    cli.quantity.input = quantity
    cli.current_average.input = current_average
    cli.current_price.input = current_price


def create_new_file(cli):
    """The stock file does not currently exist in the folder.
    We will now make one so you can use it again later."""
    write_data_to_file(
        cli.get_symbol(),
        [
            f'{cli.get_symbol()} is a {cli.get_asset_type()}',
            cli.get_quantity(),
            cli.get_current_average(),
            cli.get_current_price()
        ]
    )


# def get_symbol():
#     if len(sys.argv) >= 2:
#         symbol = sys.argv[1].strip().lower()
#         try:
#             float(symbol)  # This should fail, meaning correct arguments given
#             print(format.Feedback(True, f'First arg should be the symbol, not the current price.'))
#         except ValueError:
#             return symbol
#     else:
#         return input(f'What is the symbol of the stock or cryptocurrency?\n').strip().lower()
#
#
# def get_current_price(my_stock):
#     if len(sys.argv) >= 3:
#         value = sys.argv[2]  # current price
#         modify_stock.validate_input(my_stock, f'current_price', value)
#         my_stock.update_quantity_format()
#         modify_file(my_stock, f'current price')


def retrieve_file_data(symbol):
    """Retrieves the stocks values from the input file.
    If the stock file does not exist, this will create one."""
    make_sure_dir_exists()
    symbol = symbol.lower()

    with open(get_file(symbol), 'r') as stock_file:
        lines = stock_file.read().splitlines()
        stock_file.close()

        return [lines[0].strip(),               # asset type: stock or cryptocurrency
                abs(float(lines[1].strip())),   # quantity
                abs(float(lines[2].strip())),   # current average
                abs(float(lines[3].strip()))]   # current price
