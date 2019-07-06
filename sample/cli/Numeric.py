from .TextBaseClass import TextBaseClass


class Numeric(TextBaseClass):
    def __init__(self, parent, message):
        super().__init__(parent, message)
        self.valid_chars = [('0', '9'), '.']

    def input_in_valid_length(self):
        if self.user_input.count(','):
            # If the user input a comma (1,000,000), delete the commas.
            self.user_input = self.user_input.replace(',', '')

        if self.user_input.count('.') > 1:
            print('Invalid: Only one decimal point allowed.', end='')
            return False
        elif len(self.user_input) is 0:
            print('Invalid: input cannot be empty.', end='')
            return False
        return True

    def input_is_valid(self):
        if not super().input_is_valid():
            # one or more characters entered is/are invalid.
            print()
            return False
        # every character entered is valid.
        self.convert_to_number()
        return True

    def convert_to_number(self):
        # convert string to a number {3.0 or 3.14}
        self.user_input = float(self.user_input)

        if self.user_input == int(self.user_input):
            # 3.0 => 3
            self.user_input = int(self.user_input)

        # convert the number back to a string
        self.user_input = str(self.user_input)


class Currency(Numeric):
    def __init__(self, parent, message):
        super().__init__(parent, message)
        self.intro_char = '$'

    def convert_to_number(self):
        """Modifies the user_input to """
        self.user_input = str(float(self.user_input))
        for i in range(len(self.user_input) - 1 - self.user_input.find('.')):
            self.user_input += '0'
