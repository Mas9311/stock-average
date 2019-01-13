class Feedback:
    """Creates a border wall around the message so the user can notice messages easier.
    If the is_invalid """
    def __init__(self, is_invalid, information):
        self.is_invalid = is_invalid
        self.information = information
        self.indent = '  ' if self.is_invalid else ''
        self.width = 2 + 14 + 2
        self.vert_border_char = '*' if self.is_invalid else '║'

    def create_border_line(self, is_top):
        first_char = '*'
        last_char = '*'
        horizontal_border_char = '*'
        output = ''
        if not self.is_invalid:
            horizontal_border_char = '═'
            if is_top:
                first_char = '╔'
                last_char = '╗'
            else:
                first_char = '╚'
                last_char = '╝'
        for _ in range(self.width - 2):
            output += horizontal_border_char
        return f'{first_char}{output}{last_char}'

    def spacing(self, information_line):
        ending_spaces = ''
        num_spaces = self.width - 4 - len(information_line)
        for _ in range(num_spaces):
            ending_spaces += ' '
        return f'{self.vert_border_char} {information_line}{ending_spaces} {self.vert_border_char}'

    def __str__(self):
        information_str = f''
        padding = 6 if self.indent else 4
        if type(self.information) is list:
            self.width = max(2 + 14 + 2, max([len(each_line) for each_line in self.information]) + padding)
            for i in range(len(self.information)):
                information_str += f'{self.spacing(self.indent + self.information[i])}'
                information_str += f'\n' if i is not len(self.information)-1 else ''
        else:
            self.width = max(self.width, len(self.information) + padding)
            information_str = f'{self.spacing(self.indent + self.information)}'

        invalid_str = self.spacing('Invalid entry:') + '\n' if self.is_invalid else ''
        top_border_line = self.create_border_line(True)
        bot_border_line = self.create_border_line(False)
        output = (f'{invalid_str}'
                  f'{information_str}')

        return (f'\n\n{top_border_line}\n'
                f'{output}\n'
                f'{bot_border_line}\n\n')


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
