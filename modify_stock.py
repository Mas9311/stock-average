import file_helper as helper
import menu


def switcher(answer, stock):
    """Calls the corresponding function based upon
    which value the the user wishes to modify.
    It then updates the formatting of the stock
    and writes the new changes to the given stock's file"""

    if answer is 1:
        modify_crypto(stock)
    elif answer is 2:
        modify_shares(stock)
    elif answer is 3:
        modify_average(stock)
    elif answer is 4:
        modify_current(stock)

    stock.update_formatting()
    helper.modify_file(answer, stock)


def modify_crypto(stock):
    print('You have chosen to modify the crypto attribute', end='\n\n')
    print('Is', stock.symbol, 'a cryptocurrency?')
    menu.print_y_or_n('indicate that it a cryptocurrency', 'indicate that it is a regular stock')
    answer = input().strip().lower()
    stock.crypto = bool(answer)

    # Re-read stock.purchased_quantity from file
    if stock.crypto is True:
        helper.read_shares_from_file(stock)

    additional = '' if stock.crypto else ' NOT'
    print('You have indicated that', stock.symbol, 'is' + additional, 'a cryptocurrency', end='\n\n')


def modify_shares(stock):
    print('You have selected to modify the current number of shares attribute')
    print('How many shares of', stock.symbol, 'do you currently have?')
    validate_input(stock, 'purchased_quantity')


def modify_average(stock):
    print('You have selected to modify your current average attribute')
    print('What is your current average of', stock.symbol, '?')
    validate_input(stock, 'purchased_price')


def modify_current(stock):
    print('You have selected to modify the current average attribute')
    print('What is the current price of', stock.symbol, '?')
    validate_input(stock, 'current_price')


def validate_input(stock, attribute):
    """User has been asked the question, so retrieve their input.
    If it's not blank (after remove whitespace), and a number, and
    greater than zero, then update the stock's corresponding attribute"""

    answer = input().strip().lower()
    if answer:
        try:
            answer = float(answer)
            if answer < 0:
                print('ERROR:', answer, 'must be a positive number (or 0)')
            else:
                update_stock(answer, stock, attribute)
        except ValueError:
            print('ERROR:', answer, 'is not a valid input')
    else:
        print('ERROR: your input must not be left blank on this one')


def update_stock(answer, stock, attribute):
    """Once the user gives a valid input to modify the stock, this is the
    function that actually modifies the given stock's corresponding value"""

    if attribute is 'purchased_quantity':
        stock.purchased_quantity = answer
    elif attribute is 'purchased_price':
        stock.purchased_price = answer
    elif attribute is 'current_price':
        stock.current_price = answer
