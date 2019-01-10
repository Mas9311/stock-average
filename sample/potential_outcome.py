from . import format


class NewOutcome:
    def __init__(self, my_allotted, potential_index, potential_cost, potential_average):
        self.symbol = my_allotted.symbol
        self.crypto = my_allotted.crypto
        self.precision = my_allotted.precision
        self.type_of = my_allotted.type_of

        self.index = int(potential_index)
        self.cost = potential_cost
        self.average = float(potential_average)

    def update_crypto(self, my_allotted):
        self.crypto = my_allotted.crypto
        self.precision = my_allotted.precision
        self.type_of = my_allotted.type_of

    def __str__(self):
        if not self.crypto:
            type_str = f'buying {format.multiple(self.index, "additional ", self.type_of)}'
        else:
            type_str = f'spending {format.price(self.cost, 2)}'
        return f'After {type_str}, your new average would be {format.price(self.average, self.precision)}.\n'
