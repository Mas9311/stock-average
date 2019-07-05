from sample import format, menu, modify_stock
import os
import sys


def get_folder():
    """Returns the symbols/ folder path."""
    # return os.path.join('~/', 'Software', 'MyPrograms', 'stock-average', 'symbols')
    return os.path.join(os.getcwd(), 'symbols')


def get_file(stock_symbol):
    """Returns the given stock's file path."""
    return os.path.join(get_folder(), stock_symbol)


def modify_file(my_stock, selection):
    """This function is called once the user has selected to modify a given value of the stock."""
    lines = retrieve_file_data(my_stock.get_symbol().lower())
    if selection == f'crypto':
        lines[0] = f'{my_stock.get_symbol()} is a cryptocurrency!' if my_stock.crypto else f''
    elif selection == f'purchased average':
        lines[1] = my_stock.purchased_average
    elif selection == f'purchased quantity':
        lines[2] = my_stock.purchased_quantity
    elif selection == f'current price':
        lines[3] = my_stock.current_price

    with open(get_file(my_stock.symbol.lower()), 'w') as f:
        f.write(f'{lines[0]}\n')
        f.write(f'{repr(lines[1])}\n')
        f.write(f'{repr(lines[2])}\n')
        f.write(f'{repr(lines[3])}\n')
        f.close()
    print(format.Feedback(False, f'{my_stock.get_symbol()} has been updated.'))


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
    (asset_type, current_average, quantity, current_price) = retrieve_file_data(cli.get_symbol())
    if asset_type.lower().count(cli.asset_type.valid_options[0]):
        cli.asset_type.input = cli.asset_type.valid_options[0]
    else:
        cli.asset_type.input = cli.asset_type.valid_options[1]
    cli.current_average.input = str(current_average)
    cli.quantity.input = str(quantity)
    cli.current_price.input = str(current_price)


def make_file(stock_symbol):
    """The stock file does not currently exist in the folder.
    We will now make one so you can use it again later."""
    print(f'The {stock_symbol} file is not in the symbols folder, so we will make it now.\n\n')
    file_path = get_file(stock_symbol)
    stock_symbol = stock_symbol.upper()
    with open(file_path, 'w') as new_file:
        crypto_answer = menu.y_or_n(f'Is {stock_symbol} a cryptocurrency?',
                                    f'save it is a cryptocurrency',
                                    f'save it as a regular stock')
        if crypto_answer:
            new_file.write(f'{stock_symbol} is a cryptocurrency!')
        new_file.write('\n')
        type_of = f'share' if not crypto_answer else f'coin'
        shares = input(f'How many {type_of}s of {stock_symbol} have you purchased?\n').strip()
        new_file.write(input(f'What is your current average of {stock_symbol}?\n').strip().lower() + '\n')
        new_file.write(f'{shares}\n')
        new_file.write(input(f'What is the current price of {stock_symbol}?\n').strip().lower() + '\n')
        new_file.close()


def get_symbol():
    if len(sys.argv) >= 2:
        symbol = sys.argv[1].strip().lower()
        try:
            float(symbol)  # This should fail, meaning correct arguments given
            print(format.Feedback(True, f'First arg should be the symbol, not the current price.'))
        except ValueError:
            return symbol
    else:
        return input(f'What is the symbol of the stock or cryptocurrency?\n').strip().lower()


def get_current_price(my_stock):
    if len(sys.argv) >= 3:
        value = sys.argv[2]  # current price
        modify_stock.validate_input(my_stock, f'current_price', value)
        my_stock.update_quantity_format()
        modify_file(my_stock, f'current price')


def retrieve_file_data(symbol):
    """Retrieves the stocks values from the input file.
    If the stock file does not exist, this will create one."""
    make_sure_dir_exists()
    symbol = symbol.lower()

    with open(get_file(symbol), 'r') as stock_file:
        lines = stock_file.read().splitlines()
        stock_file.close()

        return [lines[0].strip(),               # is this a crypto?
                abs(float(lines[1].strip())),   # purchased average
                abs(float(lines[2].strip())),   # purchased quantity
                abs(float(lines[3].strip()))]   # current price
