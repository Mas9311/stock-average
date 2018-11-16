class Stock:
    def __init__(self, input_list, symbol):
        self.crypto = input_list[0]
        self.purchased_price = input_list[1]
        self.purchased_quantity = input_list[2]
        self.current_price = input_list[3]
        self.symbol = symbol
        self.update_formatting()

    '''If the first index in the file is empty, it is not a cryptocurrency'''
    def update_formatting(self):
        self.crypto = bool(self.crypto)
        if repr(self.purchased_quantity).find('.0') is not -1 and not self.crypto:
            self.purchased_quantity = int(self.purchased_quantity)

    '''Return the price in currency format with a decimal precion of 2 or 8, depending
    on if it is a regular stock or a cryptocurrency'''
    def price(self, price):
        if self.crypto:
            return '${:.8f}'.format(round(price, 8))
        return '${:.2f}'.format(round(price, 2))

    def __str__(self):
        print_crypto = ', the cryptocurrency' if self.crypto else ''
        return (f'{self.symbol.upper()}{print_crypto}:\n'
                f'  You previously bought {self.purchased_quantity} shares\n'
                f'  with a current average of {self.price(self.purchased_price)}\n'
                f'  and the current price is  {self.price(self.current_price)}\n')
