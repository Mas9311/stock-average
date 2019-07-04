from tkinter import *


class Radio(Frame):
    """A Frame that contains a label and options for the user to select.
    A maximum of one and only one option (button) can be selected at any given time."""
    def __init__(self, parent, index):
        Frame.__init__(self, parent)
        self.pack(expand=True, fill=BOTH)
        self.parent = parent
        self.root = self.parent.root

        self.buttons = []
        self.index = index
        self.label = None
        self.last_button_selected = None

        self.create_radio_widgets()

    def create_radio_widgets(self):
        """Only called when creating a new Radio instance, in the _init_ method above."""
        self.bind('<FocusIn>', self.radio_focus_in)  # cursor lies within this Frame

        self.label = Label(self, text=self.parent.get_val(self.index, 'label'), width=15)
        self.label.pack(side=LEFT, anchor=W)

        for option_text in self.parent.get_val(self.index, 'options'):
            button = Radiobutton(self, text=option_text, variable=self.parent.get_val(self.index, 'StringVar'),
                                 val=option_text, command=lambda option=option_text: self.select(option))
            button.pack(side=LEFT, anchor=W)
            self.buttons.append(button)

    def select(self, option_text):
        if self.last_button_selected is None:
            # Case 1: no Buttons selected => a Button selected
            print(self.parent.symbol_string.get(), 'is a', option_text)
            self.last_button_selected = option_text
            self.parent.create_next_frame(self.index + 1)
        elif self.last_button_selected != option_text:
            # Case 2: a Button selected => a different Button selected
            print(self.parent.symbol_string.get(), 'is a', option_text)
            self.last_button_selected = option_text
        else:
            # Case 3: a Button selected => no Buttons selected
            self.deselect_buttons()
            self.last_button_selected = None
            self.parent.destroy_all_frames_after(self.index)

    def deselect_buttons(self):
        """Deselects all Radiobuttons currently within this Frame."""
        for button in self.buttons:
            button.deselect()
        self.parent.set_val(self.index, 'StringVar', StringVar())

    def destroy_frame(self):
        """Calling this will delete this Radio Frame instance and deselects all Rabiobuttons in this Frame.
        Resets all GUI._frames values associated to self.index completely."""
        self.deselect_buttons()
        self.parent.destroy_frame(self.index)

    def radio_focus_in(self, _):
        """This Frame currently contains the cursor."""
        self.parent.focused_frame = self.index

