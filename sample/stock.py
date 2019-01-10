import math
from . import additional, average, format, file_helper


class Stock:
    def __init__(self):
        self.symbol = file_helper.get_symbol().lower()
        file_lines = file_helper.get_parameters(self.symbol)
        self.crypto = bool(file_lines[0])  # If the first line in the file is not empty, it is a cryptocurrency
        self.precision = 8 if self.crypto else 3
        self.type_of = 'coin' if self.crypto else 'share'

        self.purchased_average = 0.00
        self.purchased_quantity = 0
        self.set_purchased(file_lines[1], file_lines[2])
        self.current_price = file_lines[3]

        self.average = average.Average(self)
        self.allotted = None

    def set_purchased(self, price_str, quantity_str):
        """Helper method that sets the purchased_{average, quantity} correctly."""
        self.purchased_average = Stock.retrieve_purchased('average', price_str)
        self.purchased_quantity = Stock.retrieve_purchased('quantity', quantity_str)

    @staticmethod
    def retrieve_purchased(purchased_type, value_str):
        """Returns the normalized If the string cannot be converted to a float, retrieve a valid input."""
        output = value_str
        while True:
            try:
                return format.normalize(float(output))
            except ValueError:
                print(f'Invalid: The purchased {purchased_type} of \'{output}\' cannot be converted properly.')
                output = input(f'Please input a valid purchased {purchased_type}: ').strip()

    def update_crypto(self, is_crypto):
        """Updates the crypto variable and everything else including the objects within this object."""
        self.crypto = is_crypto
        self.precision = 8 if self.crypto else 3
        self.type_of = 'coin' if self.crypto else 'share'

        self.average.update_crypto(self)
        if self.allotted:
            self.allotted.update_crypto(self)

    def set_allotted(self, allotted_money):
        """For stocks, increments are set to the current price.
        For crypto, increments do not need to be in whole coins, so square root(money)."""
        cost_per = math.sqrt(allotted_money) if self.crypto else self.current_price
        self.allotted = additional.ActionTaken(self, allotted_money, cost_per)

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
                f'\tYou previously purchased {format.multiple(self.purchased_quantity, "", self.type_of)},\n'
                f'\twith a current average of {format.price(self.purchased_average, self.precision)}\n'
                f'\twith the current price at {format.price(self.current_price, self.precision)}\n')
