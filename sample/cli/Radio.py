from sample import menu
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
        self.valid_chars = [('0', f'{len(self.valid_options) - 1}')]

    def create_message(self):
        description = f'Is {self.parent.get_symbol()} a '
        for index in range(len(self.valid_options)):
            description += self.valid_options[index]
            if index is not len(self.valid_options) - 1:
                description += ' or '
            else:
                description += '?'

        self.message = menu.create_menu_output(
            description,
            [f'for {opt}' for opt in self.valid_options]
        )

    def input_in_valid_length(self):
        if len(self.user_input) is 0:
            # user selected first option, index [0]
            self.user_input = str(0)
            return True
        if len(self.user_input) > 1:
            print('Invalid: input is too long.')
            return False
        return True

    def assign_to_variable(self):
        self.input = self.valid_options[int(self.user_input)]
