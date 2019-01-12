def feedback(is_invalid, information):
    default_length = 2 + 14 + 2

    if type(information) is list:
        num_asterisks = max(default_length, max([len(each_line) for each_line in information]) + 6)
        information_str = f''  # if information isa <list>, blank it out
        for i in range(len(information)):
            information_str += f'{spacing("  " + information[i], num_asterisks)}'
            information_str += f'\n' if i is not len(information) - 1 else ''
    else:
        num_asterisks = max(default_length, len(information) + 6)
        information_str = spacing('  ' + information, num_asterisks)

    invalid_str = spacing(f'Invalid entry:', num_asterisks) + '\n' if is_invalid else f''
    asterisks_line = f''
    output = (f'{invalid_str}'
              f'{information_str}')
    for i in range(num_asterisks):
        asterisks_line += f'*'

    return (f'\n\n{asterisks_line}\n'
            f'{output}\n'
            f'{asterisks_line}\n\n')


def spacing(information, line_len):
    spaces = f''
    num_spaces = line_len - 4 - len(information)
    for _ in range(num_spaces):
        spaces += f' '
    return f'* {information}{spaces} *'


# print(feedback(True, ['Today I learned that not one actually cares', 'Two']))
# print(feedback(False, ['Today I learned that not one actually cares', 'Two']))
# print(feedback(True, 'Today I learned that not one actually cares'))
# print(feedback(False, 'Today I learned that not one actually cares'))
# print(feedback(True, ['One', 'Two']))
# print(feedback(False, ['One', 'Two']))
# print(feedback(True, 'One'))
# print(feedback(False, 'One'))


def price(money, precision):
    """Something."""
    return f'${best(money, precision)}'


def normalize(number):
    """Returns the number by safely converting to an integer or keeping it as a float.
    Example outputs:
        normalize(1.0)      returns 1
        normalize(22.12)    returns 22.12 """
    return int(number) if number == int(number) else number


def best(number, precision):
    """Returns the money in string format by either adding zeros or truncating them.
    Example outputs:
        price(1.123, 0)     returns 1
        price(2, 2)         returns 2
        price(333.1, 3)     returns 222.100
        price(888.1234, 8)  returns 888.12340000 """
    normalized = normalize(number)
    if normalized is not number:
        return normalized

    if precision == 0:  # or number is 0:
        return int(number)
    output = repr(round(number, precision))
    decimal_location = output.find(f'.')
    if decimal_location is -1:
        return output

    difference = (len(output) - 1) - decimal_location
    number_of_zeros = precision - difference
    for x in range(number_of_zeros):
        output += f'0'
    return output


def multiple(count, additional, type_of):
    """Returns the string to correctly display the optional 's'.
    Example outputs:
        multiple(3, 'additional', 'coin')   returns '3 additional coins'
        multiple(1, '', 'share')            returns '1 share'
        multiple(3, 'additional', share')   returns '3 additional shares' """
    type_of += f's' if count != 1 else f''
    return f'{count} {additional}{type_of}'
