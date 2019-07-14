import sys

from sample import file_helper, format


def create_menu_output(description, options):
    """The generic formula for creating the header message + [Enter] to x + [1] to y + ... """
    menu_output = f'{description}\n [Enter] {options[0]}.\n'
    for index in range(1, len(options)):
        menu_output += f' [{index}] {options[index]}.\n'
    return menu_output


def ask_options(description, options):
    """Prints how to receive input from the user."""
    last_index = len(options) - 1
    menu_output = create_menu_output(description, options)
    while True:
        # while input is not valid: keep asking
        output = input(f'{menu_output}> ').strip()
        if not output or output == str(0):
            # user selected the first option: nothing [Enter]ed || '0'
            print()
            return 0
        elif len(options) is 2:
            # only two options: return the numerical index regardless of what the user typed
            print()
            return last_index
        try:
            output = int(output)
            if 1 <= output <= last_index:
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
        f'Do you wish to modify any of the values listed for {cli.get("symbol")}?',
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
            f'{mod}Asset type:         \'{cli.asset_type}\'',
            f'{mod}Quantity:           {cli.quantity}',
            f'{mod}Current average:    {cli.current_average}',
            f'{mod}Market price:       {cli.market_price}'
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
                    # user selected to quit CLI modification
                    return
                if 1 <= selection <= 4:
                    # The only way to continue is with a valid number between 1 and 4
                    break
                print(format.Feedback(True, f'\'{selection}\' must be an option between 1 and 4.'))
            except ValueError:
                print(format.Feedback(True, f'The selection is not a valid number.'))
            except IndexError:
                print(format.Feedback(True, f'The selection cannot be left blank.'))

        # user has input a number between [1, 4]
        update_selected_option(selection, cli)
        # continue while loop: ask user (again) if they wish to modify any CLI variables


def update_selected_option(selection, cli):
    """Clears the variable's input and re-asks the question
    based upon which value the the user wishes to modify.
    It then updates the formatting of the stock
    and writes the new changes to the given stock's file"""
    if selection is 1:
        cli.asset_type.reset_and_ask_question()
    elif selection is 2:
        cli.quantity.reset_and_ask_question()
    elif selection is 3:
        cli.current_average.reset_and_ask_question()
    elif selection is 4:
        cli.current_price.reset_and_ask_question()
    file_helper.export_to_file(cli.arg_dict)


def ending_menu(symbol):
    """Prints the final menu to determine what the user wants to do now."""
    if ask_options(
            'Do you wish to quit or continue?',
            [

                'to continue finding averages',
                'to quit the program'
            ]
    ):
        # user selected to quit the program
        sys.exit()
    if ask_options(
            f'Do you wish to continue with {symbol} or choose another symbol?',
            [
                f'continue with {symbol}',
                'choose a different symbol'
            ]
    ):
        # user selected to choose a different symbol
        print('\n' * 20)  # print 21 newlines for visual detachment
        return 'different'

    # else: continue finding averages for the same symbol
    return 'same'
