class Average:
    def __init__(self, numerator, denominator):
        self.numerator = numerator
        self.denominator = denominator

    '''Adds a new instance to the numerator and increments the denominator'''
    def add_stock(self, price):
        self.numerator += price
        self.denominator += 1

    def add_crypto(self, shares_of_crypto, current_price):
        self.numerator += shares_of_crypto * current_price
        self.denominator += shares_of_crypto

    '''Return the average with 3 decimal places for regular stock precision, 8 for cryptocurrencies'''
    def avg(self, stock):
        precision = 3
        if stock.crypto:
            precision = 8
        return round(self.numerator / self.denominator, precision)

    '''Print out the current average in USD'''
    def show_avg(self):
        print('$', self.avg())
