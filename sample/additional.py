from . import currency, potential_outcome as potential


class ActionTaken:
    def __init__(self, my_stock, money=1.00, cost_per=1.00):
        self.symbol = my_stock.symbol
        self.crypto = my_stock.crypto
        self.precision = my_stock.precision
        self.allotted_money = money
        self.cost_per = cost_per
        self.iterations = self.allotted_money // cost_per
        self.selections = []

    def update_crypto(self, is_crypto):
        self.crypto = is_crypto
        for each in self.selections:
            each.update_crypto(self.crypto)

    def set_allotted(self, money, cost_per):
        self.allotted_money = money
        self.cost_per = cost_per
        self.iterations = self.allotted_money // cost_per

    def get_allotted(self):
        """Returns the allotted money that the user is willing to spend today."""
        return self.allotted_money

    def get_iterations(self):
        """Returns how many potential averages to be calculated using the allotted money."""
        return self.iterations

    def add_outcome(self, index, potential_cost, potential_average):
        new_outcome = potential.NewOutcome(self.crypto, index, potential_cost, potential_average)
        self.selections.append(new_outcome)

    def clear_list(self):
        self.selections.clear()

    def __str__(self):
        """Returns the potential averages as a string"""
        output = ''
        for curr in self.selections:
            output += str(curr)
        return(f'For {self.symbol.upper()}, the potentials be calculated in {self.iterations} '
               f'increments of {currency.price(self.cost_per, self.precision)} each iteration.\n'
               f'{output}')
