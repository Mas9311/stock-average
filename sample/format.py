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


class Price:
    """Converts the money input into a price format with precision.
    Examples include:
    Price(0.499, 0)     returns $0
    Price(0.500, 0)     returns $1
    Price(11.09, 1)     returns $11.1
    Price(22, 2)        returns $22.00
    Price(44.1, 4)      returns $44.1000
    Price(88.1234, 8)   returns $88.12340000"""
    def __init__(self, money, precision=2):
        self.money = money
        self.precision = precision
        self.output = '$'

        self.create_output()

    def create_output(self):
        try:
            self.money = abs(float(self.money))
            self.precision = abs(int(self.precision))
        except ValueError:
            print('Invalid: the money parameter in Price is not a number')
            return

        if self.precision == 0:
            self.output += str(int(round(float(self.money), self.precision)))
            return

        # truncate any decimals if the money is longer than the precision
        self.money = str(round(float(self.money), self.precision))
        zeros = '0' * (self.precision - (len(self.money) - 1 - self.money.find('.')))
        self.output += self.money + zeros

    def __str__(self):
        """Returns the money in string format by either adding zeros or truncating them."""
        return self.output
