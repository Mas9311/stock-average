from sample.format import Price


class PotentialAverage:
    def __init__(self, parent, curr_iter):
        self.parent = parent
        self.curr_iter = curr_iter

        self.n = None  # number of shares user currently has
        self.x = None  # number of shares user is about to purchase
        self.old_price = None  # user's current average
        self.new_price = None  # price per share || can be multiple shares if scaled

        self.numerator_old = None  # (n * old_price)
        self.numerator_new = None  # (x * new_price)
        self.numerator = None  # (n * old_price) + (x * new_price)
        self.denominator = None  # (n + x)

        self.average = None  # numerator / denominator

        self.assign_variables()

    def assign_variables(self):
        self.n = self.parent.arg_dict['quantity']
        self.old_price = self.parent.arg_dict['current_average']
        self.numerator_old = self.n * self.old_price

        self.new_price = self.parent.arg_dict['market_price']
        self.x = self.curr_iter * self.parent.arg_dict['amount_per']
        self.numerator_new = self.x * self.new_price

        self.numerator = self.numerator_old + self.numerator_new
        self.denominator = self.n + self.x

        self.average = round(self.numerator / self.denominator, 3)

    def get_coordinates(self):
        """Returns the (x, y) coordinates to plot this PotentialAverage instance on a graph"""
        return self.numerator_new, self.average

    def __str__(self):
        """Returns the potential average in string format."""
        x_coordinate, y_coordinate = self.get_coordinates()
        return (
            f'After spending {Price(x_coordinate, 2)}, '
            f'your new average would be {Price(y_coordinate, 2)}.'
        )
