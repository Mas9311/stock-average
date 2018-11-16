#!/usr/bin/python3

import average
import math
import menu
import stock
import file_helper as helper


#############################
# Usage:                    #
#  python3 stock_average.py #
#############################


def add_new_stock(new_shares_bought):
    """Adds the new share to the numerator, and increment the denominator"""

    # Calculate 'How much money have we theoretically spent so far?'
    spent_money = round(new_shares_bought * stock.current_price, 2)

    # Add this share to the numerator and increment the denominator
    average.add_stock(stock.current_price)

    print_new_average(new_shares_bought, spent_money)


def add_new_crypto(shares_to_add, iter_round):
    """Adds the new ratio to the numerator, and the number of shares to the denominator"""

    # Calculate "How much money have we theoretically spent so far?"
    spent_money = round((shares_to_add * iter_round) * stock.current_price, 8)

    # Add ratio to numerator, and add the number of shares to denominator
    average.add_crypto(shares_to_add, stock.current_price)

    print_new_average(shares_to_add * iter_round, spent_money)


def iterate_through_shares(money):
    """The user may not want to spend all of the money they indicated,
    so this incrementally adds it to the given stock's average,
    and will print out the new average for every iteration"""

    if not stock.crypto:
        # "How many shares you can buy today with that money?"
        shares = 0
        try:
            shares = math.floor(money / stock.current_price)
        except TypeError:  # User clicked off screen during additional money question
            get_money()
            return

        if shares is not 0:
            for new_shares_bought in range(1, (shares + 1)):
                add_new_stock(new_shares_bought)
        else:
            print('Unfortunately, that\'s not enough to buy a share.')
            print('Try again, but increase the money this time', end='\n\n')
            update_then_money()
            return
    else:
        # "How many iterations are we going to print to console?"
        try:
            iterations = int(math.sqrt(money))
        except TypeError:  # User clicked off screen during additional money question
            get_money()
            return

        # "How many shares can you buy in each iteration printed (in decimal)?"
        price_per_iter = money / iterations
        print('For', stock.symbol, 'we will print your average in {} increments'.format(stock.price(price_per_iter)))

        # "How many shares is that (in decimal)?"
        share_per_iter = price_per_iter / stock.current_price
        for iter_round in range(1, iterations + 1):
            add_new_crypto(share_per_iter, iter_round)


def print_new_average(new_shares_bought, spent_money):
    """Print your new average"""
    print('{}'.format(stock.price(average.avg(stock))), end='')
    print(' is your new average after buying {} additional shares'.format(round(new_shares_bought, 8)))
    print('\t\twhich would cost an additional total of {}'.format(stock.price(spent_money)), end='\n\n')


def get_money():
    """Retrieves dollar amount from user to gauge how much they are willing to spend"""
    money_s = input('How much additional money are you willing to spend?\n').strip().lower()

    try:
        money_d = float(money_s)
        if money_d < 0:
            print('You cannot add negative money, but we\'ll continue with positive')
            money_d = abs(money_d)
        return money_d
    except ValueError:
        if money_s:
            print('ERROR:', money_s, 'must be valid number')
        else:
            print('ERROR: money entry cannot be empty')
        get_money()
        return


def calculate_money():
    money = get_money()
    iterate_through_shares(money)

    # After printing all the possible options of additional stocks, print original average
    print('{} is your current average of'.format(stock.price(stock.purchased_price)), symbol.upper())


def update_then_money():
    # Would you like to update anything in this file?
    menu.update_file(stock)

    # How much additional money are you willing to spend?
    calculate_money()


if __name__ == '__main__':
    symbol = input('What is the symbol of the stock?\n').strip().lower()
    lines = helper.get_parameters(symbol)

    # Creates the class instance for the Stock
    stock = stock.Stock(lines, symbol.upper())

    # Creates the class instance for the Average
    average = average.Average(stock.purchased_price * stock.purchased_quantity, stock.purchased_quantity)

    # "Do you want to update the stock?" --> "How much money are you willing to spend?"
    update_then_money()
