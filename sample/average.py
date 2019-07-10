from sample.format import Price


class PotentialAverage:
    def __init__(self, parent, curr_iter, cost_per):
        self.parent = parent

        self.curr_iter = curr_iter
        self.cost_per = cost_per
        self.additional_cost = self.get_additional_cost()
        if self.parent.get('asset_type') != 'stock':
            # convert curr_iter to a fraction relative to its coin
            self.curr_iter = (self.cost_per * self.curr_iter) / self.parent.get('market_price')

        self.numerator = self.parent.get('quantity') * self.parent.get('current_average')  # (n * oldPrice)
        self.additional_numerator = self.curr_iter * self.parent.get('market_price')  # (x *currentPrice)
        self.denominator = self.parent.get('quantity')  # n
        self.additional_denominator = self.curr_iter

    def get_additional_cost(self):
        return round(self.curr_iter * self.cost_per, 2)

    def average(self):
        """Returns the average is float format without rounding."""
        num = self.numerator + self.additional_numerator
        den = self.denominator + self.additional_denominator
        return round(num / den, 3)

    def get_coordinates(self):
        """Returns the (x, y) coordinates to plot this PotentialAverage instance on a graph"""
        return self.get_additional_cost(), self.average()

    def __str__(self):
        """Returns the potential average in string format."""
        return (
            f'After spending {Price(self.additional_cost, 2)}, '
            f'your new average would be {Price(self.average(), 2)}.'
        )
