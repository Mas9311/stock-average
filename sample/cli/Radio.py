from .TextBaseClass import TextBaseClass


class Radio(TextBaseClass):
    def __init__(self, valid_options):
        self.valid_options = valid_options
        self.message = None
        self.create_message()
        super().__init__(self.message)
        self.valid_options = valid_options
        self.valid_chars = [('1', f'{len(self.valid_options)}')]

    def create_message(self):
        self.message = ''
        for option_index in range(len(self.valid_options)):
            self.message += f'Enter [{option_index + 1}] for {self.valid_options[option_index]}'
            if option_index is not len(self.valid_options) - 1:
                self.message += '\n\tor\n'

    def input_in_valid_length(self):
        if len(self.user_input) is not 1:
            print('Invalid: input is too long.')
            return False
        return True
