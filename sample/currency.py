def price(money, precision):
    """Return the price in currency format with a decimal precision of 2 or 8
    depending on if it is a regular stock or a cryptocurrency"""
    output = repr(round(money, precision))
    add = len(output) - 1 - output.find('.')
    print(f'Additional 0s: {precision - add}')
    for x in range(precision - add):
        output += '0'
    return f'${output}'


def multiple(number, additional, type_of):
    """Returns the string to correctly display the optional 's'. For example:
        '3 additional coins'  '1 share'  '3 additional shares'  """
    type_of += '' if number is 1 else 's'
    return f'{number} {additional}{type_of}'
