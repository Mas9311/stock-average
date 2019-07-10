import os
import time
from sample.format import Feedback, Price
from sample.parameters import asset_type_choices


def get_folder():
    """Returns the /.../symbols/ folder path."""
    # return os.path.join('~/', 'Software', 'MyPrograms', 'stock-average', 'symbols')
    return os.path.join(os.getcwd(), 'symbols')


def get_file_path(symbol):
    """Returns the given symbol's file path."""
    return os.path.join(get_folder(), symbol.lower())


def dir_exists():
    """Returns True if the configuration folder exists."""
    return os.path.exists(get_folder())


def make_sure_dir_exists():
    """Creates the symbols folder if it does not exist."""
    if not dir_exists():
        os.mkdir(get_folder())
        print(Feedback(False, 'Created the symbols folder.'))


def file_exists(symbol):
    """Returns true if the file exists."""
    return os.path.exists(get_file_path(symbol))


def file_keys():
    return ['asset_type', 'quantity', 'current_average', 'market_price']


def export_to_file(arg_dict):
    with open(get_file_path(arg_dict['symbol']), 'w') as symbol_file:
        for key in file_keys():
            symbol_file.write(f'{key},{arg_dict[key]}\n')
        symbol_file.close()


def import_from_file(symbol, arg_dict={}):
    """Read the configurations from the file given and place them into a dictionary format.
    Values are turned from strings into their respective data types."""
    make_sure_dir_exists()

    file_dict = {}
    symbol = symbol.lower()

    if file_exists(symbol):
        with open(get_file_path(symbol), 'r') as symbol_file:
            file_data = symbol_file.read().splitlines()
            for line in file_data:
                try:
                    key, value = line.split(',')
                except ValueError:
                    print('\nCannot read values from file, so it will be deleted.\nFile reads:')
                    for x_file_line in file_data:
                        print('', x_file_line)
                    os.remove(get_file_path(symbol))
                    print()
                    time.sleep(0.25)
                    return arg_dict, False
                file_dict[key] = convert_value(key, value, symbol)
            symbol_file.close()
        print(symbol, 'file loaded successfully.')

    if not file_dict:
        file_dict['symbol'] = symbol
        for key in file_keys():
            if key == 'asset_type':
                file_dict[key] = asset_type_choices()[0]
            else:
                file_dict[key] = None
    
    if arg_dict:
        file_dict = merge_arg_dict_with_file_dict(arg_dict, file_dict)
    
    return file_dict, True


def merge_arg_dict_with_file_dict(arg_dict, file_dict):
    for key in file_keys():
        if key == 'market_price':
            if arg_dict['market_price'] and file_dict[key] != arg_dict['market_price']:
                print(
                    f' updated {arg_dict["symbol"]}\'s current market Price:',
                    Price(file_dict['market_price']), '=>', Price(arg_dict['market_price'])
                )
                continue
        arg_dict[key] = file_dict[key]
    
    return arg_dict


def convert_value(key, value, symbol):
    if key == 'interface':
        return value.lower() == 'True'.lower()
    if key == 'symbol':
        return symbol
    elif key == 'asset_type':
        choices = asset_type_choices()
        return choices[value.lower() == choices[1]]
    # while True:
    try:
        value = float(value)
        return (float(value), int(value))[float(value) == int(value)]
        # value = float(value)
        # if value == int(value):
        #     return int(value)
        # return value
    except ValueError:
        # TODO: ask for new input of the key's value.
        # response = input('Enter the', key)
        #  user has manually modified the file, leading to this Error
        return None
