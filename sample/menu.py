from sample import format, modify_stock


def create_menu_output(description, options):
    menu_output = f'{description}\n [Enter] {options[0]}.\n'
    for index in range(1, len(options)):
        menu_output += f' [{index}] {options[index]}.\n'
    return menu_output


def ask_options(description, options):
    """Prints how to receive input from the user."""
    # if isinstance(options, str):
    #     options = [options]
    last_index = len(options) - 1
    menu_output = create_menu_output(description, options)
    while True:
        # while input is not valid: keep asking
        output = input(f'{menu_output}> ').strip()
        if not output:
            # user selected the first option: nothing [Enter]ed
            print()
            return 0
        elif len(options) is 2:
            # only two options: return the numerical index regardless of what the user typed
            print()
            return last_index
        try:
            output = int(output)
            if output is 0:
                return 0
            elif 1 <= output <= last_index:
                print()
                return output
            else:
                print('Invalid:', output, f'is not in valid range [1, {last_index}].\n')
        except ValueError:
            print('Invalid:', repr(output), 'is not a valid option.\n')


def modify_menu(cli):
    """Prints the initial menu to determine if the user wants to modify any of the values printed."""
    print(cli)
    output = ask_options(
        f'Do you wish to modify any of the values listed for {cli.get_symbol()}?',
        [
            'to skip this step',
            'to modify a value'
        ]
    )
    return output


def update_menu(cli):
    """The user has selected to modify a value. Which value to modify?"""
    mod = 'to modify the '
    output = ask_options(
        'Enter the option that you wish to modify from the list below:',
        [
            'to return',
            f'{mod}Asset type:         {cli.asset_type.input}',
            f'{mod}Quantity:           {cli.quantity.input}',
            f'{mod}Current average:    ${cli.current_average.input}',
            f'{mod}Current price:      ${cli.current_price.input}'
        ]
    )
    return output


def update(cli):
    """Macro-function that determines which other functions to call based on the user input provided."""
    while True:
        while True:
            if not modify_menu(cli):
                # user does not want to modify any of the CLI variables
                return
            try:
                selection = update_menu(cli)
                selection = int(selection)
                if selection is 0:
                    # user selected to quit file modification
                    return
                if 1 <= selection <= 4:
                    # The only way to continue is with a valid number between 1 and 4
                    print()
                    break
                print(format.Feedback(True, f'\'{selection}\' must be an option between 1 and 4.'))
            except ValueError:
                print(format.Feedback(True, f'The selection is not a valid number.'))
            except IndexError:
                print(format.Feedback(True, f'The selection cannot be left blank.'))

        # user has input a number between [1, 4]
        modify_stock.switcher(convert_selection_update(selection), cli)
        # continue: ask user again if they want to modify any variables


def convert_selection_update(selection):
    """Converts the integer to a string as to not confuse those that review the code."""
    if selection is 1:
        return f'asset type'
    elif selection is 2:
        return f'quantity'
    elif selection is 3:
        return f'current average'
    elif selection is 4:
        return f'current price'


def ending_menu(symbol):
    """Prints the final menu to determine what the user wants to do now."""
    if ask_options(f'Do you wish to continue or exit?',
                   ['to exit the program', 'to continue finding averages']) is None:
        return f'quit'
    if not ask_options(f'Do you want to choose another symbol or continue with {symbol}?',
                       [f'continue with {symbol}', 'choose a different symbol']):
        return f'same'
    print(f'\n\n\n\n\n\n\n\n\n\n\n\n')
    return f'different'
