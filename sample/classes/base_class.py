from tkinter import *


class TextBaseClass:
    def __init__(self, parent, message):
        self.parent = parent  # CLI instance
        self.message = message
        self.user_input = None  # unverified input
        self.input = None  # stored once verified as valid
        self.valid_chars = None
        self.intro_char = ''

    def reset_and_ask_question(self):
        self.input = None
        self.retrieve_input()

    def retrieve_input(self):
        if not self.input:
            while True:
                self.ask_message()
                if self.input_is_valid():
                    self.assign_to_variable()
                    return

    def ask_message(self):
        self.user_input = input(f'{self.message}.\n> {self.intro_char}').strip().lower()

    def assign_to_variable(self):
        self.input = self.user_input

    def input_is_valid(self):
        if not self.input_in_valid_length():
            print()
            return False

        for input_index in range(len(self.user_input)):
            input_char = self.user_input[input_index]
            is_valid = True

            for valid in self.valid_chars:
                if isinstance(valid, tuple):
                    if valid[0] <= input_char <= valid[1]:
                        # this character is valid
                        is_valid = True
                        break
                    else:
                        is_valid = False

                if isinstance(valid, str):
                    if input_char == valid:
                        # this character is valid
                        is_valid = True
                        break
                    else:
                        is_valid = False

            if not is_valid:
                print('Invalid:', repr(input_char), 'is an invalid character.\n')
                return False

                # else: continue checking

        # user_input passed all invalid checks ∴ char is valid
        print()
        return True

    def input_in_valid_length(self):
        if len(self.user_input) is 0:
            print('Invalid: input is not long enough.')
            return False
        return True


class FrameBaseClass(Frame):
    def __init__(self, parent, index):
        Frame.__init__(self, master=parent)
        self.pack(expand=True, fill=BOTH)
        self.parent = parent
        self.root = self.parent.root

        self.index = index
        self.key = self.parent.get(index, 'key')
        self.label = None
        self.string_var = StringVar()

    def arg_get(self):
        if self.key in self.parent.arg_dict.keys():
            return self.parent.arg_dict[self.key]
        return None

    def arg_set(self, value):
        if self.arg_get() != value:
            self.parent.arg_dict[self.key] = value
            self.parent.save_to_file()
            if 2 <= self.index <= 6:
                self.parent.calculate_potential_averages()

    def create_label_widget(self):
        self.label = Label(self, text=self.parent.get(self.index, 'label'), width=15)
        self.label.pack(side=LEFT, anchor=W)

    def create_widgets(self):
        self.create_label_widget()

    def destroy_frame(self):
        """Calling this will delete this Alpha Frame instance.
        Resets all GUI._frames values associated to self.index completely."""
        self.parent.destroy_frame(self.index)

    def set_string(self, value):
        self.string_var.set(str(value))


class EntryBaseClass(FrameBaseClass):
    def __init__(self, parent, index):
        super().__init__(parent, index)
        self.description = self.parent.get(self.index, 'description')
        self.entry = None
        self.intro_char = ''  # placed at the beginning of the Entry's textbox when cursor is within
        self.valid_chars = None

        self.create_widgets()

    def _clear_description(self):
        """If the Entry's textbox contains the description: clear the Entry's textbox."""
        if self.entry.get() == self.description:
            self.entry.delete(0, END)

    def _delete_spaces(self):
        """Detects and delete spaces characters in the Entry's textbox.
        Returns True if it successfully deleted any space characters.
         - If only one space present: delete the last char typed.
         - If {multiple spaces present || space was not last typed char}: delete all characters
        Returns False if there are no spaces (thus, nothing was deleted)."""
        if self.entry.get().count(' '):
            # If there is at least 1 space character
            cursor_pos = self.entry.index(INSERT) - 1
            if self.entry.get().count(' ') is 1:
                # If there is only 1 space character
                if self.entry.get().find(' ') is cursor_pos:
                    # If it was the last letter typed: delete the last letter typed.
                    self._delete_character(cursor_pos)
                    return True
            # else {there are multiple spaces || was not the last letter typed}: delete all letters
            self.entry.delete(0, END)
            return True
        # else the are no spaces present: does not delete anything
        return False

    def _delete_character(self, from_i=0, from_offset=0, to_i=None):
        if isinstance(from_i, str):
            from_i = self.entry.index(from_i)
        if from_offset:
            from_i += from_offset

        if to_i is None:
            to_i = from_i + 1

        if isinstance(to_i, str):
            to_i = self.entry.index(to_i)

        self.entry.delete(from_i, to_i)

    def _destroyed_for_empty_input(self):
        if self.is_empty():
            # No characters remain in the symbol entry widget, ∴ destroy all further gui
            self.parent.destroy_all_frames_after(self.index)
            return True
        return False

    def _insert_description(self):
        """If the Entry's textbox has no user input: insert the description."""
        if self.is_empty():
            self.entry.delete(0, END)
            self.entry.insert(0, self.description)

    def bind_frame(self):
        self.bind('<FocusIn>', self.focus_in)  # cursor lies within this Frame
        self.bind('<FocusOut>', self.focus_out)  # cursor has left this Frame

        self.entry.bind('<Enter>', self.mouse_enters_entry)
        self.entry.bind('<Leave>', self.mouse_leaves_entry)
        self.entry.bind('<Insert>', lambda e: 'break')  # disable Insert
        self.entry.bind('<Control-v>', lambda e: 'break')  # disable paste
        self.entry.bind('<Control-c>', lambda e: 'break')  # disable paste
        self.entry.bind('<Control-y>', lambda e: 'break')  # disable uncommon undo (paste in tkinter)
        self.entry.bind('<Button-3>', lambda e: 'break')  # disable right-click

    def create_entry_widget(self):
        self.entry = Entry(self, textvariable=self.string_var)
        self.entry.pack(side=LEFT, expand=True, fill=X)
        self._insert_description()

    def create_widgets(self):
        super().create_widgets()
        self.create_entry_widget()
        self.bind_frame()

    def focus_in(self, _):
        """This Frame currently contains the cursor.
        If the description is present, clear the Entry's textbox."""
        self.parent.focused_frame = self.index
        self._clear_description()
        self.place_intro_char()

    def focus_out(self, _):
        """This Frame does not contain the cursor anymore.
        If the Entry's textbox is empty, fill it with the Frame's description"""
        self._insert_description()

    def is_empty(self):
        if self.entry.get() and self.entry.get() != self.description:
            return self.entry.get() == ('', self.intro_char)[bool(self.intro_char)]
        return True

    def mouse_enters_entry(self, _):
        """Mouse just started hovering over this Entry's textbox.
        If the description is present, delete it to prepare for user input."""
        self._clear_description()
        self.place_intro_char()

    def mouse_leaves_entry(self, _):
        """Mouse is no longer hovering over this Entry's textbox.
        If the Entry's textbox is empty (no user input), fill it with the description."""
        if self.parent.focused_frame is not self.index:
            self._insert_description()

    def place_intro_char(self):
        if self.intro_char:
            if not self.entry.get().count(self.intro_char):
                self.entry.insert(0, self.intro_char)

    def set_string(self, value):
        self.string_var.set(f'{self.intro_char}{value}')
