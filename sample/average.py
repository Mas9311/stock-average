from . import format


class Average:
    """This class keeps track of the running totals of the numerator and denominator for a faster calculation."""
    def __init__(self, my_stock):
        self.crypto = bool(my_stock.crypto)
        self.precision = my_stock.precision
        self.numerator = my_stock.purchased_average * my_stock.purchased_quantity
        self.denominator = my_stock.purchased_quantity
        self.additional_numerator = 0.00
        self.additional_denominator = 0.00

    def update_crypto(self, my_stock):
        """Updates the crypto variable and the dependent variable."""
        self.crypto = my_stock.crypto
        self.precision = my_stock.precision

    def add_new(self, add_to_numerator, add_to_denominator):
        """Adds a new instance to the numerator and increments the denominator accordingly."""
        self.additional_numerator += add_to_numerator
        self.additional_denominator += add_to_denominator

    def retrieve_average(self):
        """Returns the average is float format without rounding."""
        return (self.numerator + self.additional_numerator) / (self.denominator + self.additional_denominator)

    def avg(self):
        """Returns the potential average in rounded float format."""
        return round(self.retrieve_average(), self.precision)

    def __str__(self):
        """Returns the potential average in string format."""
        return format.price(self.retrieve_average(), self.precision)


class PotentialOutcome:
    def __init__(self, my_allotted, potential_index, potential_cost, potential_average):
        self.symbol = my_allotted.symbol
        self.crypto = my_allotted.crypto
        self.precision = my_allotted.precision
        self.type_of = my_allotted.type_of

        self.index = int(potential_index)
        self.cost = potential_cost
        self.average = float(potential_average)

    def update_crypto(self, my_allotted):
        """Updates the crypto variable and everything else that depends on it."""
        self.crypto = my_allotted.crypto
        self.precision = my_allotted.precision
        self.type_of = my_allotted.type_of

    def __str__(self):
        if not self.crypto:
            type_str = f'buying {format.multiple(self.index, "additional ", self.type_of)}'
        else:
            type_str = f'spending {format.price(self.cost, 2)}'
        return f'After {type_str}, \tyour new average would be\t{format.price(self.average, self.precision)}.'
