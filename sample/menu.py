from sample import format, modify_stock


def y_or_n(first, second):
    """Prints how to receive input from the user."""
    return input(f'\tEnter any key to {first}\n'
                 f'\t  or\n'
                 f'\tPress [enter] to {second}.\n').strip().lower()


def modify_menu(my_stock):
    """Prints the initial menu to determine if the user wants to modify any of the values printed."""
    print(my_stock)
    print(f'Would you like to update any of the values listed for {my_stock.get_symbol()}?')
    return y_or_n(f'modify a value',
                  f'skip this step')


def update_menu(my_stock):
    """The user has selected to modify a value. Which value to modify?"""
    print(f'Select the number you wish to modify from the list below:\n'
          f'\t1: Cryptocurrency:     {"Yes" if my_stock.crypto else "No"}\n'
          f'\t2: Purchased average:  {format.price(my_stock.purchased_average, my_stock.precision)}\n'
          f'\t3: Purchased quantity: {my_stock.purchased_quantity}\n'
          f'\t4: Current price:      {format.price(my_stock.current_price, my_stock.precision)}')
    return input(f'Which option number do you want to want to modify?\n').strip()


def update(my_stock):
    """Macro-function that determines which other functions to call based on the user input provided."""
    while True:
        while True:
            if not modify_menu(my_stock):
                return
            try:
                selection = int(update_menu(my_stock)[0])
                if 1 <= selection <= 4:
                    # The only way to continue is with a valid number between 1 and 4
                    break
                print(f'Invalid: \'{selection}\' must be an option between 1 and 4.')
            except ValueError:
                print(f'Invalid: the selection is not a valid number.')
            except IndexError:
                print(f'Invalid: selection cannot be left blank.')
        modify_stock.switcher(convert_selection_update(selection), my_stock)


def convert_selection_update(answer):
    """Converts the integer to a string as to not confuse the programmers."""
    if answer is 1:
        return f'crypto'
    elif answer is 2:
        return f'purchased average'
    elif answer is 3:
        return f'purchased quantity'
    elif answer is 4:
        return f'current price'


def ending_menu(symbol):
    """Prints the final menu to determine what the user wants to do now."""
    print(f'\n\nDo you wish to continue or exit?')
    if not y_or_n(f'continue finding averages',
                  f'exit the program'):
        return f'quit'
    print(f'\n\n\n')
    print(f'Do you want to choose another symbol or continue with {symbol}?')
    if not y_or_n(f'choose a different symbol',
                  f'continue with {symbol}'):
        return f'same'
    print(f'\n\n\n\n\n\n\n\n\n\n\n\n')
    return f'different'
