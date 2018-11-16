import menu
import os


def get_folder():
    """Returns the /symbols folder path"""
    return os.path.join(os.getcwd(), 'symbols')


def get_file(stock_symbol):
    """Returns the given stock's file path"""
    return os.path.join(get_folder(), stock_symbol)


def modify_file(answer, stock):
    """This function is called once you have
    selected to modify a given value of the stock"""
    lines = get_parameters(stock.symbol.lower())

    if answer is 1:
        lines[0] = stock.symbol.upper() + ' is a cryptocurrency!'
    elif answer is 2:
        lines[1] = stock.purchased_price
    elif answer is 3:
        lines[2] = stock.purchased_quantity
    elif answer is 4:
        lines[3] = stock.current_price

    with open(get_file(stock.symbol.lower()), 'w') as f:
        if stock.crypto:
            f.write(lines[0])
        f.write('\n')
        f.write(repr(lines[1]) + '\n')
        f.write(repr(lines[2]) + '\n')
        f.write(repr(lines[3]) + '\n')
        f.close()


def make_sure_dir_exists():
    """Create the symbols folder if it does not exist"""
    symbols = get_folder()
    if not os.path.exists(symbols):
        os.mkdir(symbols)
        print('Created the directory', end='\n\n')


def read_shares_from_file(stock):
    """Called when a stock is modified from NOT a crytpo -> a crypto.
    Retrieves the purchased_quantity back from the stock's file"""

    with open(get_file(stock.symbol.lower()), 'r') as f:
        lines = f.read().splitlines()
        stock.purchased_quantity = float(lines[2])
        f.close()


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
        print('Is', stock_symbol, 'a cryptocurrency?')
        menu.print_y_or_n('save it is a cryptocurrency', 'save it as a regular stock')
        crypto_answer = input().strip().lower()
        if crypto_answer:
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
        if len(lines) > 3:
            lines[3] = abs(float(lines[3]))  # current price
        return lines
