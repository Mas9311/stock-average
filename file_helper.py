import os


def get_folder():
    """Returns the /symbols folder path"""
    return os.path.join(os.getcwd(), 'symbols')


def get_file(stock_symbol):
    """Returns the given stock's file path"""
    return os.path.join(get_folder(), stock_symbol)


def modify_file(stock):
    """This function is called once you have
    selected to modify a given value of the stock"""
    with open(get_file(stock.symbol.lower()), 'w') as f:
        crypto_string = ' ' if not stock.crypto else stock.symbol + ' is a cryptocurrency!'
        f.write(crypto_string + '\n')
        f.write(repr(stock.purchased_price) + '\n')
        f.write(repr(stock.purchased_quantity) + '\n')
        f.write(repr(stock.current_price) + '\n')
        f.close()


def make_sure_dir_exists():
    """Create the symbols folder if it does not exist"""
    symbols = get_folder()
    if not os.path.exists(symbols):
        os.mkdir(symbols)
        print('Created the directory', end='\n\n')


def file_exists(stock_symbol):
    """Returns true if the file is already made and has valid values"""
    file_path = get_file(stock_symbol)

    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            lines = f.read().splitlines()
            if len(lines) >= 2:
                try:
                    p_price = float(lines[1])
                    p_quantity = float(lines[2])
                    if len(lines) is 3:
                        return p_price and p_quantity >= 0
                    c_price = float(lines[3])
                    return p_price and p_quantity and c_price >= 0
                except ValueError:
                    print('One of the non-crypto values in the', stock_symbol, 'file not a number.')
                    os.remove(file_path)
                    print('Starting with a clean file.')
    return False


def make_file(stock_symbol):
    """The stock file does not currently exist in the folder.
    We will now make one so you can use it again later"""
    print(stock_symbol, 'file is not in the symbols folder, so we\'ll make it now.', end='\n\n')
    file_path = get_file(stock_symbol)

    with open(file_path, 'w') as new_file:
        crypto = input('Is ' + stock_symbol + ' a cryptocurrency? \n\t\'y\' or simply press enter for no\n').strip().lower()
        if len(crypto) is not 0:
            if crypto.strip().lower()[0] == 'y':
                new_file.write(stock_symbol.upper() + ' is a cryptocurrency!')
        new_file.write('\n')

        shares = input('How many shares of ' + stock_symbol.upper() + ' do you currently own?\n').strip().lower()
        new_file.write(input('What price are you currently averaging?\n').strip().lower() + '\n')
        new_file.write(shares + '\n')
        new_file.write(input('And what is the current price?\n').strip().lower())
        new_file.close()


def get_parameters(stock_symbol):
    """Retrieves the stocks values from the input file.
    If the stock file does not exist, we will create one. """
    make_sure_dir_exists()
    while not file_exists(stock_symbol):
        make_file(stock_symbol)

    with open(get_file(stock_symbol), 'r') as stock_file:
        lines = stock_file.read().splitlines()
        stock_file.close()

        lines[0] = bool(lines[0].strip())
        lines[1] = abs(float(lines[1].strip()))  # purchased price
        lines[2] = abs(float(lines[2].strip()))  # purchased quantity
        if len(lines) >= 4:
            lines[3] = abs(float(lines[3]))  # current price
        return lines
