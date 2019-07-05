from .TextBaseClass import TextBaseClass


class Radio(TextBaseClass):
    def __init__(self, parent, valid_options):
        self.parent = parent
        self.valid_options = valid_options
        self.message = None
        self.create_message()
        message = self.message
        super().__init__(parent, message)
        self.message = message
        self.valid_options = valid_options
        self.valid_chars = [('1', f'{len(self.valid_options)}')]

    def create_message(self):
        self.message = f'Is {self.parent.get_symbol()} a '
        for option_index in range(len(self.valid_options)):
            self.message += f'{self.valid_options[option_index]}'
            if option_index is not len(self.valid_options) - 1:
                self.message += ' or '
            else:
                self.message += '?\n'

        for option_index in range(len(self.valid_options)):
            self.message += f' [{option_index + 1}] for {self.valid_options[option_index]}'
            if option_index is not len(self.valid_options) - 1:
                self.message += '.\n'

    def input_in_valid_length(self):
        if len(self.user_input) is not 1:
            print('Invalid: input is too long.')
            return False
        return True

    def assign_to_variable(self):
        self.input = self.valid_options[int(self.user_input)]
