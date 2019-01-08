from sample import file_helper, menu, stock


def run():
    """Main driver that calls everything necessary. The recipe, if you will."""
    my_stock = stock.Stock()
    file_helper.get_current_price(my_stock)
    menu.update(my_stock)

    allotted_money = retrieve_money()
    my_stock.set_allotted(allotted_money)

    calculate_allotted(my_stock)
    print(f'{my_stock.allotted}{my_stock}')


def retrieve_money():
    """Retrieves the user's allotted money to determine how much they are willing to spend today."""
    while True:
        user_input = input(f'How much additional money are you willing to spend?\n').strip()
        try:
            money = float(user_input)
            if money > 0:
                # The input is a valid, non-zero, positive number
                return money
            else:
                print(f'Invalid: {user_input} must be a non-zero, positive number.\n')
        except ValueError:
            if user_input:
                print(f'Invalid: {user_input} must be a non-zero, positive number.\n')
            else:
                print(f'Invalid: allotted money cannot be left blank.\n')


def calculate_allotted(my_stock):
    """The user may not want to spend all of the money they designated,
    so this will calculate the potential averages incrementally"""
    while True:
        iterations = int(my_stock.allotted.iterations)
        if iterations <= 0:
            print(f'Invalid: {my_stock.allotted.allotted_money} is not enough money to buy a share.')
            print(f'Please designate a number over {my_stock.allotted.cost_per}.')
            my_stock.set_allotted(retrieve_money())
        else:
            break
    for curr_iter in range(1, int(iterations) + 1):
            add_potential(my_stock, curr_iter)


def add_potential(my_stock, curr_iter):
    add_to_denom = 1 if not my_stock.crypto else (my_stock.allotted.cost_per / my_stock.current_price)
    my_stock.average.add_new(my_stock.allotted.cost_per, add_to_denom)
    my_stock.allotted.add_outcome(curr_iter, my_stock.allotted.cost_per * curr_iter, my_stock.average.avg())


# def add_new_stock(new_shares_bought):
#     """Adds the new share to the numerator, and increment the denominator."""
#     spent_money = round(new_shares_bought * my_stock.current_price, my_stock.precision)
#
#     # Add this share to the numerator and increment the denominator
#     my_average.add_stock(my_stock.current_price)
#
#     print_new_average(new_shares_bought, spent_money)
#
#
# def add_new_crypto(shares_to_add, curr_iter):
#     """Adds the new ratio to the numerator, and the number of shares to the denominator"""
#     # Calculate "How much money have we theoretically spent so far?"
#     spent_money = round((shares_to_add * curr_iter) * my_stock.current_price, 8)
#
#     # Add ratio to numerator, and add the number of shares to denominator
#     my_average.add_crypto(shares_to_add, my_stock.current_price)
#
#     print_new_average(shares_to_add * curr_iter, spent_money)
