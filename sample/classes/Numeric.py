from tkinter import *

from sample.classes.base_class import TextBaseClass, EntryBaseClass
from sample.format import Price


# CLI interface classes


class CliNumeric(TextBaseClass):
    def __init__(self, parent, key, message):
        super().__init__(parent, message)
        self.key = key
        self.valid_chars = [('0', '9'), '.']

    def assign_to_variable(self):
        self.parent.set(self.key, self.user_input)

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

    def __str__(self):
        return f'{self.parent.get(self.key)}'


class CliCurrency(CliNumeric):
    def __init__(self, parent, key, message):
        super().__init__(parent, key, message)
        self.intro_char = '$'

    def convert_to_number(self):
        """Modifies the user_input to """
        self.user_input = float(self.user_input)

    def __str__(self):
        return f'{Price(super().__str__())}'


# GUI interface classes


class GuiNumeric(EntryBaseClass):
    def __init__(self, parent, index):
        super().__init__(parent, index)
        self.valid_chars = [('0', '9'), '.']

        self.entry.bind('<KeyRelease>', self.numeric_entry_key_released)  # key pressed => key released

    def arg_set(self, value):
        if value:
            if value[len(str(value)) - 1] == '.':
                value = str(value) + '0'
            value = float(value)
            if value == int(value):
                value = int(value)
            super().arg_set(value)

    def correct_entry(self, char):
        self.place_intro_char()
        self.delete_extra_decimal_points()
        self.delete_for_max_length()
        self.move_cursor()

        if self.parent.is_char_printable(char):
            # Received a printable character: {alpha || numeric || punctuation}
            if self.parent.is_char_valid(char, self.valid_chars):
                # Received valid input: [09] || .
                if not self.is_empty():
                    if char != '.' and self.string_var.get() != 0.0:
                        print(f'{self.parent.get(self.index, "label")}: {self.entry.get()}')
                    self.parent.create_next_frame(self.index + 1)
            else:
                # Received invalid input: {numeric || punctuation}
                if not self._delete_spaces():
                    self._delete_character(INSERT, -1, END)

    def delete_extra_decimal_points(self):
        if self.entry.get().count('.'):
            # If there is at least 1 decimal point
            while self.entry.get().count('.') > 1:
                self.entry.delete(self.find_furthest_decimal_point())

    def delete_for_max_length(self):
        if len(self.entry.get()) > 15:
            self.entry.delete(15, END)

    def entry_text_valid(self):
        try:
            float(self.entry.get())
            return True
        except ValueError:
            self.entry.delete(0, END)
            print('Invalid character detected.')
            return False

    def find_furthest_decimal_point(self):
        char_pos = self.entry.index(INSERT) - 1
        first_pos = self.entry.get().find('.')
        second_pos = self.entry.get().find('.', first_pos + 1)
        if abs(char_pos - first_pos) > abs(char_pos - second_pos):
            return first_pos
        return second_pos

    def is_empty(self, value=None):
        """Detects if a valid number > 0.0 is currently in the Entry's textbox.
        Returns True if empty || equivalent to 0.0
        returns False if text is a valid number > 0.0"""
        if value is None:
            # if not manually overriding the value, assign value to the StringVar's current field
            value = self.string_var.get()

        if not super().is_empty():
            # there is a non-intro_char character in the Entry's textbox
            if value[len(value) - 1] == '.':
                # if the last character is a decimal point => convert to a float by ending it with '.0'
                value = str(value) + '0'

            # return True == 'Yes, it is empty.' == equal to 0.0
            return float(value) == 0.0

        # no characters in the Entry's textbox
        return True

    def move_cursor(self):
        pass

    def numeric_entry_key_released(self, event=None, char=None):
        self.correct_entry(char if char is not None else event.char)

        if not self._destroyed_for_empty_input():
            # Entry text contains user input
            self.parent.create_next_frame(self.index + 1)
        self.arg_set(self.entry.get())


class GuiCurrency(GuiNumeric):
    def __init__(self, parent, index):
        super().__init__(parent, index)
        self.intro_char = '$'

    def arg_set(self, value):
        if len(value) > 1:
            super().arg_set(value[1:])

    def entry_text_valid(self):
        try:
            float(self.entry.get()[1:])
            return True
        except ValueError:
            print('Invalid character detected.')
        except IndexError:
            print('Index error')
        self.entry.delete(0, END)
        self.entry.insert(0, self.intro_char)
        return False

    def is_empty(self, _=None):
        return super().is_empty(self.string_var.get()[1:])

    def move_cursor(self):
        if self.entry.index(INSERT) is 0:
            self.entry.icursor(1)
