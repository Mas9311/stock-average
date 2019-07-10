from .TextBaseClass import TextBaseClass


class CliAlpha(TextBaseClass):
    def __init__(self, parent, key, message):
        super().__init__(parent, message)
        self.key = key
        self.valid_chars = [('a', 'z'), ('A', 'Z')]

    def assign_to_variable(self):
        self.parent.set(self.key, self.user_input)

    def __str__(self):
        return f'{self.parent.get(self.key).upper()}'

