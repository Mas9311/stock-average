from sample import menu
from .TextBaseClass import TextBaseClass


class Radio(TextBaseClass):
    def __init__(self, parent, key, valid_options):
        self.parent = parent
        self.key = key
        self.valid_options = valid_options
        self.message = None
        self.create_message()
        message = self.message
        super().__init__(parent, message)
        self.message = message
        self.valid_options = valid_options
        self.valid_chars = [('0', f'{len(self.valid_options) - 1}')]

    def ask_message(self):
        self.user_input = input(f'{self.message}> ').strip()

    def create_message(self):
        description = f'Is {self.parent.get("symbol")} a '
        for index in range(len(self.valid_options)):
            description += self.valid_options[index]
            if index is not len(self.valid_options) - 1:
                description += ' or '

        self.message = menu.create_menu_output(
            f'{description}?',
            [f'for {opt}' for opt in self.valid_options]
        )

    def input_in_valid_length(self):
        if not len(self.user_input):
            # user selected first option by [Enter]ing '': index=0
            self.user_input = str(0)
            return True
        if len(self.user_input) > 1:
            print('Invalid: input is too long.')
            return False
        return True

    def assign_to_variable(self):
        self.parent.set(self.key, self.valid_options[int(self.user_input)])

    def __str__(self):
        return str(self.parent.get(self.key))
