from . import currency


class Average:
    def __init__(self, my_stock):
        self.crypto = bool(my_stock.crypto)
        self.precision = my_stock.precision
        self.numerator = my_stock.purchased_average * my_stock.purchased_quantity
        self.denominator = my_stock.purchased_quantity
        self.additional_numerator = 0.000
        self.additional_denominator = 0.000

    def get_numerator(self):
        return self.numerator + self.additional_numerator

    def get_denominator(self):
        return self.denominator + self.additional_denominator

    def avg(self):
        numer = self.get_numerator()
        denom = self.get_denominator()
        return round(numer / denom, self.precision)

    '''Adds a new instance to the numerator and increments the denominator accordingly'''
    def add_new(self, numerator, denominator):
        self.additional_numerator += numerator
        self.additional_denominator += denominator

    # def clear(self):
    #     self.additional_numerator = 0.000
    #     self.additional_denominator = 0.000

    def __str__(self):
        """Returns the potential average in currency format with
        3 decimal precision for regular stock, 8 for cryptocurrency."""
        numer = self.get_numerator()
        denom = self.get_denominator()
        return f'${currency.price(numer / denom, self.precision)}'
