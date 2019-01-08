from sample import file_helper, menu


def switcher(selection, my_stock):
    """Calls the corresponding function based upon
    which value the the user wishes to modify.
    It then updates the formatting of the stock
    and writes the new changes to the given stock's file"""
    print(f'You have selected to modify the {selection} attribute.\n')
    if selection == 'crypto':
        modify_crypto(my_stock, selection)
        return
    elif selection == 'purchased average':
        value = input(f'What is your {selection} of {my_stock.get_symbol()}?\n').strip().lower()
    elif selection == 'purchased quantity':
        value = input(f'How many {my_stock.type_of}s of {my_stock.get_symbol()} '
                      f'do you currently have?\n').strip().lower()
        my_stock.update_quantity_format()
    elif selection == 'current price':
        value = input(f'What is the current price of {my_stock.get_symbol()}?\n').strip().lower()
    else:
        print('Nothing was modified in the object...')
        return
    validate_input(my_stock, selection, value)
    file_helper.modify_file(my_stock, selection)


def modify_crypto(my_stock, selection):
    print(f'Is {my_stock.get_symbol()} a cryptocurrency?')
    my_stock.update_crypto(bool(menu.y_or_n('indicate that it a cryptocurrency',
                                            'indicate that it is a regular stock')))
    file_helper.reread_quantity(my_stock)
    additional = '' if my_stock.crypto else ' not'
    print(f'You have just indicated that {my_stock.get_symbol()} is{additional} a cryptocurrency.\n')
    my_stock.update_quantity_format()
    file_helper.modify_file(my_stock, selection)


def validate_input(my_stock, selection, value):
    """User has been asked the question, so retrieve their input.
    If it's not blank (after remove whitespace), and a number, and
    greater than zero, then update the stock's corresponding attribute.."""
    if value:
        try:
            value = float(value)
            if value < 0:
                print(f'Invalid: \'{value}\' must a valid, positive number.')
            else:
                valid_update(my_stock, selection, value)
        except ValueError:
            print(f'Invalid: \'{value}\' is not a valid, positive number.')
    else:
        print(f'Invalid: input cannot not be left blank.')


def valid_update(my_stock, selection, value):
    """Once the user gives a valid input to modify the stock, this is the
    function that actually modifies the given stock's corresponding value"""
    if selection == 'purchased average':
        my_stock.purchased_average = value
    elif selection == 'purchased quantity':
        my_stock.purchased_quantity = value
    elif selection == 'current price':
        my_stock.current_price = value
    else:
        print(f'The {my_stock.symbol} object was not modified...')
        return
    print(f'The {my_stock.symbol} object was updated to reflect the new {selection} of {value}.')
