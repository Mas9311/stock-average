from sample import format, file_helper, menu, stock


def run():
    """This method is the main driver of the program that calls everything else."""
    while True:  # user wants to switch to a 'different' symbol from the user
        my_stock = stock.Stock()
        print('', end='\n')
        file_helper.get_current_price(my_stock)
        while True:  # user wants to continue using the 'same' symbol
            menu.update(my_stock)
            original_avg = format.price(my_stock.average.avg(), my_stock.precision)
            allotted_money = retrieve_money()
            my_stock.set_allotted(allotted_money)
            calculate_allotted(my_stock)

            print(my_stock.allotted)
            print(f'{format.Feedback(False, f"Compared to your current average of {original_avg}")}')

            ending_input = menu.ending_menu(my_stock.get_symbol())
            if ending_input is 'quit':
                return  # user 'quit' the program
            if ending_input is 'same':
                pass
            elif ending_input is 'different':
                break


def retrieve_money():
    """Retrieves the user's allotted money they are willing to spend at the current price specified."""
    while True:
        user_input = input(f'How much money are you willing to spend today?\n').strip()
        print('', end='\n')
        try:
            money = float(user_input)
            if money < 1:
                pass
            else:
                return money  # The only way to return is with a valid positive number >= !$
        except ValueError:
            pass
        print(format.Feedback(True, [f'An input of \'{user_input}\' cannot be accepted.',
                                     f'The allotted money must be a valid positive number >= {format.price(1, 2)}.']))


def calculate_allotted(my_stock):
    """The user may not want to spend all of the money they designated,
    so this will calculate the potential averages incrementally"""
    while True:
        iterations = int(my_stock.allotted.iterations)
        if iterations <= 0:
            if my_stock.crypto:
                greater_than = format.price(1, 2)
            else:
                greater_than = format.price(my_stock.allotted.cost_per, my_stock.precision)
            print(format.Feedback(True, [f'{my_stock.allotted.allotted_money} is not enough to calculate a potential.',
                                         f'Please input a number >= {greater_than}.']))
            my_stock.set_allotted(retrieve_money())
        else:
            break
    for curr_iter in range(1, int(iterations) + 1):
            add_potential(my_stock, curr_iter)


def add_potential(my_stock, curr_iter):
    """This method adds a NewOutcome to the Average.selections list, and update the average accordingly.
    Stocks add 1 to the denominator, while Cryptocurrencies add a fraction to the denominator."""
    denominator = 1 if not my_stock.crypto else (my_stock.allotted.cost_per / my_stock.current_price)
    my_stock.average.add_new(my_stock.allotted.cost_per, denominator)
    my_stock.allotted.add_outcome(curr_iter, my_stock.allotted.cost_per * curr_iter, my_stock.average.avg())
