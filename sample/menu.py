from sample import currency, modify_stock


def y_or_n(first, second):
    """Prints how to receive input from the user."""
    print(f'\tEnter any key to {first}\n'
          f'\t  or\n'
          f'\tPress [enter] to {second}.')
    return input().strip().lower()


def modify_menu(my_stock):
    """Prints the initial menu asking the user if they
    want to modify any of the values printed."""
    print(my_stock)
    print(f'Would you like to update any of the values listed for {my_stock.get_symbol()}?')
    return y_or_n('modify a value',
                  'skip this step')


def update_menu(my_stock):
    """The user has selected to modify a value.
    Which value do they wish to modify?"""
    print(f'Select the number you wish to modify from the list below:\n'
          f'\t1: Cryptocurrency:     {"Yes" if my_stock.crypto else "No"}\n'
          f'\t2: Purchased average:  {currency.price(my_stock.purchased_average, my_stock.precision)}\n'
          f'\t3: Purchased quantity: {my_stock.purchased_quantity}\n'
          f'\t4: Current price:      {currency.price(my_stock.current_price, my_stock.precision)}')
    return input(f'Which option number do you want to want to modify?\n').strip()[0]


def update(my_stock):
    """Macro-function that determines which other functions
    to call based upon the user input provided"""
    while True:
        answer1_str = modify_menu(my_stock)
        if not answer1_str:
            return

        answer2_str = update_menu(my_stock)
        if not answer2_str:
            print(f'Invalid: must enter an option number.')
            continue
        try:
            answer2 = int(answer2_str)
        except ValueError:
            print(f'Invalid: {answer2_str} is not a valid number.')
            continue
        if not 1 <= answer2 <= 4:
            print(f'Invalid: {answer2_str} must be an option between 1 and 4.')
            continue
        selection = convert(answer2)
        modify_stock.switcher(selection, my_stock)


def convert(answer):
    if answer is 1:
        return 'crypto'
    elif answer is 2:
        return 'purchased average'
    elif answer is 3:
        return 'purchased quantity'
    elif answer is 4:
        return 'current price'
