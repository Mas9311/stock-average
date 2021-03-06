from tkinter import *

from sample import menu
from sample.classes.base_class import TextBaseClass, FrameBaseClass


class CliRadio(TextBaseClass):
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


class GuiRadio(FrameBaseClass):
    """A Frame that contains a label and options for the user to select.
    A maximum of one and only one option (button) can be selected at any given time."""
    def __init__(self, parent, index):
        super().__init__(parent, index)

        self.buttons = []
        self.current_button_selected = None
        self.verbose = True

        self.bind_radio_frame()
        self.create_radio_widgets()

    def bind_radio_frame(self):
        self.bind('<FocusIn>', self.radio_focus_in)  # cursor lies within this Frame

    def create_radio_widgets(self):
        """Only called when creating a new Radio instance, in the _init_ method above."""

        self.label = Label(self, text=self.parent.get(self.index, 'label'), width=15)
        self.label.pack(side=LEFT, anchor=W)

        for option_text in self.parent.get(self.index, 'options'):
            button = Radiobutton(self, text=option_text, variable=self.string_var,
                                 val=option_text, command=lambda option=option_text: self.select(option))
            button.pack(side=LEFT, anchor=W)
            self.buttons.append(button)

    def deselect_buttons(self):
        """Deselects all Radiobuttons currently within this Frame."""
        for button in self.buttons:
            button.deselect()
        self.string_var = StringVar()

    def destroy_frame(self):
        """Calling this will delete this Radio Frame instance and deselects all Radio Buttons.
        Resets all GUI._frames values associated to self.index completely."""
        self.deselect_buttons()
        self.parent.destroy_frame(self.index)

    def is_empty(self):
        if self.key in self.parent.arg_dict.keys():
            return not bool(self.parent.arg_dict[self.key])
        return True

    def radio_focus_in(self, _):
        """This Frame currently contains the cursor."""
        self.parent.focused_frame = self.index

    def select(self, option_text):
        if self.current_button_selected is None or self.current_button_selected != option_text:
            # Case 1: no Buttons selected => a Button selected
            # Case 2: a Button selected => a different Button selected
            self.parent.focused_frame = self.index
            if self.verbose:
                print(self.parent.arg_dict['symbol'].upper(), 'is a', option_text)
            self.current_button_selected = option_text
            self.parent.create_next_frame(self.index + 1)
        else:
            # Case 3: a Button selected => no Buttons selected
            self.deselect_buttons()
            self.current_button_selected = None
            self.parent.destroy_all_frames_after(self.index)
        self.arg_set(option_text)

    def set_string(self, value):
        if self.string_var.get() != value:
            super().set_string(value)
            self.verbose = not self.verbose
            self.select(value)
            self.verbose = not self.verbose

    def set_type_of(self):
        self.parent.arg_dict['type_of'] = 'share' if self.parent.arg_dict['asset_type'] == 'stock' else 'coin'
