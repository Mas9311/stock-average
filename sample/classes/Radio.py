from tkinter import *
from sample import menu
from .base_class import TextBaseClass


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


class GuiRadio(Frame):
    """A Frame that contains a label and options for the user to select.
    A maximum of one and only one option (button) can be selected at any given time."""
    def __init__(self, parent, index, key):
        Frame.__init__(self, parent)
        self.pack(expand=True, fill=BOTH)
        self.parent = parent
        self.root = self.parent.root

        self.buttons = []
        self.index = index
        self.key = key
        self.label = None
        self.current_button_selected = None

        self.create_radio_widgets()

    def arg_get(self):
        return self.parent.arg_dict[self.key]

    def arg_set(self, option_text):
        self.parent.arg_dict[self.key] = option_text
        self.parent.save_to_file()

    def create_radio_widgets(self):
        """Only called when creating a new Radio instance, in the _init_ method above."""
        self.bind('<FocusIn>', self.radio_focus_in)  # cursor lies within this Frame

        self.label = Label(self, text=self.parent.get(self.index, 'label'), width=15)
        self.label.pack(side=LEFT, anchor=W)

        for option_text in self.parent.get(self.index, 'options'):
            button = Radiobutton(self, text=option_text, variable=self.current_button_selected,
                                 val=option_text, command=lambda option=option_text: self.select(option))
            button.pack(side=LEFT, anchor=W)
            self.buttons.append(button)
            button.select()
            button.deselect()

    def deselect_buttons(self):
        """Deselects all Radiobuttons currently within this Frame."""
        for button in self.buttons:
            button.deselect()
        self.parent.set(self.index, 'StringVar', StringVar())

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
        if self.current_button_selected is None:
            self.parent.focused_frame = self.index
            # Case 1: no Buttons selected => a Button selected
            print(self.parent.symbol_string.get(), 'is a', option_text)
            self.current_button_selected = option_text
            self.parent.create_next_frame(self.index + 1)
            self.buttons[self.parent.get(self.index, 'options').index(option_text)].select()
        elif self.current_button_selected != option_text:
            self.parent.focused_frame = self.index
            # Case 2: a Button selected => a different Button selected
            print(self.parent.symbol_string.get(), 'is a', option_text)
            self.current_button_selected = option_text
        else:
            # Case 3: a Button selected => no Buttons selected
            self.deselect_buttons()
            self.current_button_selected = None
            self.parent.destroy_all_frames_after(self.index)
        self.arg_set(option_text)
