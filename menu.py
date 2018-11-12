import modify_stock as modify


def print_modify_menu1(stock):
    """Prints the initial menu asking the user if they
    want to modify the given stock's values"""
    print(stock)
    print('Would you like to update any of the values listed for', stock.symbol + '?')
    print_y_or_n('modify a value', 'skip this step')


def print_y_or_n(first, second):
    """Prints how to receive input from the user"""
    print('  Enter the any key to', first, 'or')
    print('  Press [enter] to', second)


def print_update_menu(stock):
    """The user has selected to modify a value.
    Which value do they wish to modify?"""
    print('Enter the number you wish to modify from the list below:')
    print('  1: Is it a cryptocurrency?', 'Yes' if stock.crypto else 'No')
    print('  2: Total number of shares:', stock.purchased_quantity)
    print('  3: Current stock average :', stock.price(stock.purchased_price))
    print('  4: Stock price(currently):', stock.price(stock.current_price))


def update_file(stock):
    """The macro-function that determines which other functions
    to call based upon the user input provided"""

    while True:
        print_modify_menu1(stock)
        answer1_s = input().strip().lower()
        if not answer1_s:
            return

        print_update_menu(stock)
        answer2_s = input('Which option number do you want to want to modify?\n').strip().lower()
        if not answer2_s:
            print('ERROR: must enter the option number')
            continue
        try:
            answer2_i = int(answer2_s[0])
        except ValueError:
            print('ERROR:', answer2_s, 'must enter a number')
            continue
        if not 1 <= answer2_i <= 4:
            print('ERROR:', answer2_s, 'must be a number between 1 and 4')
            continue
        modify.switcher(answer2_i, stock)
