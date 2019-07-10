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
    Price(0.000000016)  returns $0.00000002
    Price(0.499, 0)     returns $0
    Price(0.500, 0)     returns $1
    Price(11.09, 1)     returns $11.1
    Price(22, 2)        returns $22.00
    Price(44.1, 4)      returns $44.1000
    Price(88.1234, 8)   returns $88.12340000
    Price(123456)       returns $123,456.00
    Price(1234567)      returns $1,234,567.00"""
    def __init__(self, money, precision=2):
        self.money = money
        self.precision = precision
        self.output = '$'

        self.create_output()

    def create_output(self):
        try:
            self.money = abs(float(str(self.money)))
            self.precision = abs(int(self.precision))
        except ValueError:
            print('Invalid: the money parameter in Price is not a number')
            self.output = 'Error'
            return

        if self.precision == 0:
            self.output += str(int(round(float(self.money), self.precision)))
            self.place_commas()
            return

        if self.money and not round(float(self.money), self.precision):
            # if money != 0.00, but rounding using this precision would lead to a 0.00 dollar value:
            # recursively call Price with precision+1 until money holds some value > 0.00
            self.output = Price(self.money, self.precision + 1).output
        else:
            # truncate the least-significant decimal digits if money trails farther than precision
            self.money = str(round(float(self.money), self.precision))
            if self.money.find('e-'):
                # if the money is in scientific notation:
                # convert back to decimal (max of 14 '0's after '.')
                self.money = ("%0.15f" % float(self.money)).rstrip('0')
            
            # create the leading zeros if precision is longer than 
            # the location of the least-significant decimal digit
            zeros = '0' * (self.precision - (len(self.money) - 1 - self.money.find('.')))
            # combine the dollar sign, money, and trailing zeros
            self.output += self.money + zeros
            self.place_commas()

    def place_commas(self):
        count = 0
        for i in range(self.output.find('.') - 1, 1, -1):
            # walks through the characteristic digits (left-side of decimal point) backwards
            # and places a comma in the appropriate location 1000 => 1,000
            count += 1
            if count % 3 == 0:
                self.output = self.output[:i] + ',' + self.output[i:]

    def __str__(self):
        """Returns the money in string format by either adding zeros or truncating them."""
        return self.output
