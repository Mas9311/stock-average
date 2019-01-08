from . import currency


class NewOutcome:
    def __init__(self, crypto, potential_index, potential_cost, potential_average):
        self.crypto = None
        self.precision = 0
        self.type_of = ''
        self.update_crypto(bool(crypto))

        self.index = int(potential_index)
        self.cost = potential_cost
        self.average = float(potential_average)

    def update_crypto(self, is_crypto):
        self.crypto = is_crypto
        self.precision = 8 if self.crypto else 3
        self.type_of = 'coin' if self.crypto else 'share'

    def __str__(self):
        if not self.crypto:
            iter_str = currency.multiple(self.index, "additional ", self.type_of)
        else:
            iter_str = f'{currency.price(self.cost, self.precision)} worth of coins'
        return(f'After buying {iter_str}, your new average would be {currency.price(self.average, self.precision)}\n'
               f'\tafter spending {currency.price(self.cost, 2)} today.\n\n')
