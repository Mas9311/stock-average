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
            print('Only one decimal point allowed.')
            return False
        return len(self.user_input) > 0


class Currency(Numeric):
    def __init__(self, parent, message):
        super().__init__(parent, message)
        self.intro_char = '$'
        self.valid_chars = [('0', '9'), '.']

