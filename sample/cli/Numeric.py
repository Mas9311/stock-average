from .TextBaseClass import TextBaseClass


class Numeric(TextBaseClass):
    def __init__(self, message):
        super().__init__(message)
        self.valid_chars = [('0', '9'), '.']

    def input_in_valid_length(self):
        if self.user_input.count('.') > 1:
            print('Only one decimal point allowed.')
            return False
        return len(self.user_input) > 0


class Currency(Numeric):
    def __init__(self, message):
        super().__init__(message)
        self.intro_char = '$'
        self.valid_chars = [('0', '9'), '.']

