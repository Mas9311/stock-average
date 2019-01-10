from . import format, potential_outcome as potential


class ActionTaken:
    def __init__(self, my_stock, money, cost_per):
        self.symbol = my_stock.get_symbol()
        self.crypto = my_stock.crypto
        self.precision = my_stock.precision
        self.type_of = my_stock.type_of

        self.allotted_money = money
        self.iterations = int(self.allotted_money / cost_per)
        self.cost_per = self.allotted_money / self.iterations if self.crypto else my_stock.current_price
        self.selections = []

    def update_crypto(self, my_stock):
        self.crypto = my_stock.crypto
        self.precision = my_stock.precision
        self.type_of = my_stock.type_of
        for each in self.selections:
            each.update_crypto(self)

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
        new_outcome = potential.NewOutcome(self, index, potential_cost, potential_average)
        self.selections.append(new_outcome)

    # def clear_list(self):
    #     self.selections.clear()

    def __str__(self):
        """Returns the potential averages as a string."""
        output = f''
        for curr in self.selections:
            output += str(curr)
        return(f'For {self.symbol.upper()}, the potential averages will be calculated in {self.iterations} '
               f'increments of {format.price(self.cost_per, self.precision)} each iteration.\n\n'
               f'{output}')
