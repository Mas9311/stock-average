from tkinter import *
from sample.frames.EntryBaseClass import EntryBaseClass


class Numeric(EntryBaseClass):
    def __init__(self, parent, index):
        super().__init__(parent, index)
        self.valid_chars = [('0', '9'), '.']

        self.entry.bind('<KeyRelease>', self.numeric_entry_key_released)  # key pressed => key released

    def delete_extra_decimal_points(self):
        if self.entry.get().count('.'):
            # If there is at least 1 decimal point
            while self.entry.get().count('.') > 1:
                self.entry.delete(self.find_furthest_decimal_point())

    def find_furthest_decimal_point(self):
        char_pos = self.entry.index(INSERT) - 1
        first_pos = self.entry.get().find('.')
        second_pos = self.entry.get().find('.', first_pos + 1)
        if abs(char_pos - first_pos) > abs(char_pos - second_pos):
            return first_pos
        return second_pos

    def move_cursor(self):
        pass

    def numeric_entry_key_released(self, event):
        if self.parent.is_char_printable(event.char):
            # Received a printable character: {alpha || numeric || punctuation}
            if self.parent.is_char_valid(event.char, self.valid_chars):
                # Received valid input: [09] || .
                if self.entry.get():
                    self.parent.create_next_frame(self.index + 1)
            else:
                # Received invalid input: {numeric || punctuation}
                if not self._delete_spaces():
                    self._delete_character(INSERT, -1, END)

        self.delete_extra_decimal_points()
        self.move_cursor()

        if not self._destroyed_for_empty_input():
            # Entry text contains user input
            self.parent.create_next_frame(self.index + 1)
            if not self._is_empty():
                if self.entry_text_valid():
                    # Entry text contains _valid_ user input
                    # save to file
                    pass

    def entry_text_valid(self):
        try:
            float(self.entry.get())
            return True
        except ValueError:
            self.entry.delete(0, END)
            print('Invalid character detected. Please stop smashing.')
            return False


class Currency(Numeric):
    def __init__(self, parent, index):
        super().__init__(parent, index)
        self.intro_char = '$'

    def entry_text_valid(self):
        if not self.disabled:
            try:
                float(self.entry.get()[1:])
                return True
            except ValueError:
                self.entry.delete(0, END)
                self.entry.insert(0, self.intro_char)
                print('Invalid character detected. Please don\'t mash the keys')
                return False

    def move_cursor(self):
        if self.entry.index(INSERT) is 0:
            self.entry.icursor(1)

