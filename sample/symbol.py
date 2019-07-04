# import math
# from . import average, format, file_helper
#
#
# class Symbol:
#     def __init__(self):
#         self.symbol = file_helper.get_symbol().lower()
#         file_lines = file_helper.get_parameters(self.symbol)
#         self.crypto = bool(file_lines[0])  # If the first line in the file is not empty, it is a cryptocurrency
#         self.precision = 8 if self.crypto else 3
#         self.type_of = 'coin' if self.crypto else 'share'
#
#         self.purchased_average = format.normalize(float(file_lines[1]))
#         self.purchased_quantity = format.normalize(float(file_lines[2]))
#         self.current_price = file_lines[3]
#
#         self.average = average.Average(self)
#         self.allotted = None
#
#     def update_crypto(self, is_crypto):
#         """Updates the crypto variable and everything else including the objects within this object."""
#         self.crypto = is_crypto
#         self.precision = 8 if self.crypto else 3
#         self.type_of = 'coin' if self.crypto else 'share'
#
#         self.average.update_crypto(self)
#         if self.allotted:
#             self.allotted.update_crypto(self)
#
#     def set_allotted(self, allotted_money):
#         """For stocks, increments are set to the current price.
#         For crypto, increments do not need to be in whole coins, so square root(money)."""
#         cost_per = math.sqrt(allotted_money) if self.crypto else self.current_price
#         self.allotted = AllottedMoney(self, allotted_money, cost_per)
#
#     def get_allotted(self):
#         """Returns the allotted money that the user is willing to spend today."""
#         return self.allotted.get_allotted()
#
#     def get_iterations(self):
#         """Returns how many potential averages we will be calculating using the allotted money."""
#         return self.allotted.get_iterations()
#
#     def get_symbol(self):
#         """Returns the symbol in all caps."""
#         return self.symbol.upper()
#
#     def __str__(self):
#         """Returns the stock in string format."""
#         return (f'{self.get_symbol()}{", the cryptocurrency" if self.crypto else ""}:\n'
#                 f'\tYou previously purchased  {format.multiple(self.purchased_quantity, "", self.type_of)},\n'
#                 f'\twith a current average of {format.price(self.purchased_average, self.precision)}\n'
#                 f'\twith the current price at {format.price(self.current_price, self.precision)}\n')
#
#
# class AllottedMoney:
#     def __init__(self, my_stock, money, cost_per):
#         self.symbol = my_stock.get_symbol()
#         self.crypto = my_stock.crypto
#         self.precision = my_stock.precision
#         self.type_of = my_stock.type_of
#
#         self.allotted_money = money
#         self.iterations = int(self.allotted_money / cost_per)
#         self.cost_per = self.allotted_money / self.iterations if self.crypto else my_stock.current_price
#         self.selections = []
#
#     def update_crypto(self, my_stock):
#         """Updates the crypto variable and everything else that depends on it."""
#         self.crypto = my_stock.crypto
#         self.precision = my_stock.precision
#         self.type_of = my_stock.type_of
#         for each in self.selections:
#             each.update_crypto(self)
#
#     def set_allotted(self, money, cost_per):
#         self.allotted_money = money
#         self.cost_per = cost_per
#         self.iterations = self.allotted_money // cost_per
#
#     def get_allotted(self):
#         """Returns the allotted money that the user is willing to spend today."""
#         return self.allotted_money
#
#     def get_iterations(self):
#         """Returns how many potential averages to be calculated using the allotted money."""
#         return self.iterations
#
#     def add_outcome(self, index, potential_cost, potential_average):
#         new_outcome = average.PotentialOutcome(self, index, potential_cost, potential_average)
#         self.selections.append(new_outcome)
#
#     def __str__(self):
#         """Returns the potential averages as a string."""
#         output = '\n'
#         for current_potential in self.selections:
#             if current_potential is not self.selections[-1]:
#                 output += str(current_potential) + '\n'
#             else:
#                 output += str(self.selections[-1])
#
#         return(f'For {self.symbol.upper()}, the potential averages will be calculated in {self.iterations} '
#                f'increments of {format.price(self.cost_per, self.precision)} each iteration.\n'
#                f'{output}')
