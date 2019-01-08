import math
from . import additional, average, currency, file_helper


class Stock:
    def __init__(self):
        self.symbol = file_helper.get_symbol().lower()
        # If the first line in the file is not empty, it is a cryptocurrency
        file_lines = file_helper.get_parameters(self.symbol)
        self.crypto = bool(file_lines[0])
        self.precision = 8 if self.crypto else 3
        self.type_of = 'coin' if self.crypto else 'share'

        self.purchased_average = 0.00
        self.purchased_quantity = 0
        self.set_purchased(file_lines[1], file_lines[2])
        self.current_price = file_lines[3]

        self.average = average.Average(self)
        # allotted money is not set yet, so this is intentionally 'blank' initially
        self.allotted = additional.ActionTaken(self)
        self.update_crypto(self.crypto)

    def set_purchased(self, price_str, quantity_str):
        """Helper method that sets the purchased_{average, quantity} correctly."""
        self.purchased_average = Stock.retrieve_purchased('average', price_str)
        self.purchased_quantity = Stock.retrieve_purchased('quantity', quantity_str)

    def update_quantity_format(self):
        """Will safely convert the float to an int if they are equivalent.
            12.0 -> 12"""
        # if repr(self.purchased_quantity).find('.0') is not -1:
        if self.purchased_quantity == math.floor(self.purchased_quantity):
            self.purchased_quantity = int(self.purchased_quantity)

    @staticmethod
    def retrieve_purchased(purchased_type, value_str):
        """If the string cannot be converted to a float, retrieve user input"""
        value = value_str
        while True:
            try:
                value = float(value_str)
                break
            except ValueError:
                print(f'The purchased {purchased_type} of \'{value}\' cannot be converted properly')
                value = input(f'Please input a valid purchased {purchased_type}: ')
        return value

    def update_crypto(self, is_crypto):
        """Update the class variables that depend on the self.crypto variable's value"""
        self.crypto = is_crypto
        self.type_of = 'coin' if self.crypto else 'share'
        self.precision = 8 if self.crypto else 3
        self.allotted.update_crypto(self.crypto)

    def set_allotted(self, allotted_money):
        """For stocks, increments are set to the current price.
        For crypto, increments do not need to be in whole coins, so square root(money)."""
        cost_per = math.sqrt(allotted_money) if self.crypto else self.current_price
        self.allotted.set_allotted(allotted_money, cost_per)

    def get_allotted(self):
        """Returns the allotted money that the user is willing to spend today."""
        return self.allotted.get_allotted()

    def get_iterations(self):
        """Returns how many potential averages we will be calculating using the allotted money."""
        return self.allotted.get_iterations()

    def get_symbol(self):
        """Returns the symbol in all caps."""
        return self.symbol.upper()

    def __str__(self):
        """Returns the stock in string format."""
        print_crypto = ', the cryptocurrency' if self.crypto else ''
        return (f'\n{self.get_symbol()}{print_crypto}:\n'
                f'\tYou previously purchased {currency.multiple(self.purchased_quantity, "", self.type_of)},\n'
                f'\twith a current average of {currency.price(self.purchased_average, self.precision)}\n'
                f'\twith the current price at {currency.price(self.current_price, self.precision)}\n')
