def price(money, precision):
    """Something."""
    return f'${best(money, precision)}'


def normalize(number):
    """Returns the number by safely converting to an integer or keeping it as a float.
    Example outputs:
        normalize(1.0)      returns 1
        normalize(22.12)    returns 22.12 """
    return int(number) if number == int(number) else number


def multiple(count, additional, type_of):
    """Returns the string to correctly display the optional 's'.
    Example outputs:
        multiple(3.0, 'additional', 'coin') returns '3.0 additional coins'
        multiple(1, '', 'share')            returns '1 share'
        multiple(3, 'additional', share')   returns '3 additional shares' """
    type_of += f's' if count != 1 else f''
    return f'{count} {additional}{type_of}'


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


# print(f'In the format.py file:')
# print(price(99.999, 3))
# print(price(99.9999, 3))
# print(f'\n\n')
