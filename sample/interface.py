import abc
from tkinter import *
from sample import stock_average
from sample import file_helper


def run():
    if True:  # parameter_passed != 'cli'
        root = Tk()
        GUI(root)
        root.mainloop()
    else:
        stock_average.run()


class GUI(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.master.title("Compute New Average")
        self.pack(fill=X)
        self.root = parent
        self.root.resizable(True, False)

        self.symbol_string = StringVar()
        self.asset_type_string = StringVar()
        self.quantity_string = StringVar()
        self.current_average_string = StringVar()
        self.current_price_string = StringVar()
        self.potential_average_string = StringVar()

        self.title_bar_frame = None
        self.symbol_frame = None
        self.asset_type_frame = None
        self.quantity_frame = None
        self.current_average_frame = None
        self.current_price_frame = None
        self.potential_average_frame = None

        self._frames = self._create_frames()
        self.focused_frame = 0  # location of the cursor (once user clicks/tabs to an Entry's textbox)

        self._create_gui_widgets()

    def _create_frames(self):
        return [
            {  # Title Bar Frame
                'create': self.create_title_bar_frame,
                'frame_var': self.title_bar_frame,
                'label': 'Title Bar',
                'options': [('×', 'ne')],  # ?: ('Options', 'nw')
            },
            {  # Symbol Frame
                'create': self.create_alpha_frame,
                'description': 'Enter the ticker symbol.',
                'frame_var': self.symbol_frame,
                'index': 1,
                'label': 'Symbol',
                'StringVar': self.symbol_string,
            },
            {  # Asset Type Frame
                'create': self.create_radio_frame,
                'frame_var': self.asset_type_frame,
                'index': 2,
                'label': 'Asset Type',
                'options': ['stock', 'cryptocurrency'],
                'StringVar': self.asset_type_string,
            },
            {  # Quantity Frame
                'create': self.create_numeric_frame,
                'description': 'Enter the # of shares you own.',
                'frame_var': self.quantity_frame,
                'index': 3,
                'label': 'Quantity',
                'StringVar': self.quantity_string,
            },
            {  # Current Average Frame
                'create': self.create_currency_frame,
                'description': 'Enter your current average.',
                'frame_var': self.current_average_frame,
                'index': 4,
                'label': 'Current Average',
                'StringVar': self.current_average_string,
            },
            {  # Current Price Frame
                'create': self.create_currency_frame,
                'description': 'Enter the current market price.',
                'frame_var': self.current_price_frame,
                'index': 5,
                'label': 'Current Price',
                'StringVar': self.current_price_string,
            },
            {  # Potential Average Frame
                'create': self.create_currency_frame,
                'frame_var': self.potential_average_frame,
                'index': 6,
                'label': 'Potential Average',
                'StringVar': self.potential_average_string,
            }
        ]

    def _create_gui_widgets(self):
        for i in range(len(self._frames)):
            self._frames[i]['created'] = False
        self.create_next_frame(0)  # create TitleBar Frame
        self.create_next_frame(1)  # create Alpha "Symbol" Frame

    def _resize_frame(self):
        self.root.update_idletasks()
        w = 400 if self.root.winfo_reqwidth() < 400 else self.root.winfo_reqwidth()
        h = self.root.winfo_reqheight()
        # _, _, x, y = self.root.winfo_geometry().replace('x', '.').replace('+', '.').split('.')
        geo = f'{w}x{h}'
        self.root.geometry(geo)
        # print(geo)

    def create_next_frame(self, next_index):
        """Will create the frame if:
        1. The next_index has a value (it exists) in the GUI._frames dict
          and
        2. The next_index's Frame has not been already created"""
        if next_index < self.len_frames() and not self.get_val(next_index, 'created'):
            self._frames[next_index]['frame_var'] = self.get_val(next_index, 'create')(next_index)
            self._frames[next_index]['created'] = True
            self._resize_frame()

    def create_title_bar_frame(self, index):
        return TitleBar(self, index)

    def create_alpha_frame(self, index):
        return Alpha(self, index)

    def create_radio_frame(self, index):
        return Radio(self, index)

    def create_numeric_frame(self, index):
        return Numeric(self, index)

    def create_currency_frame(self, index):
        return Currency(self, index)

    def destroy_all_frames_after(self, keep_index):
        for curr_index in range(self.len_frames()):
            if curr_index > keep_index and self.get_val(curr_index, 'created'):
                self.get_val(curr_index, 'frame_var').destroy_frame()

    def destroy_frame(self, index):
        """Destroys the Frame (and all nested widgets recursively) at a given index of GUI._frames
        Sets all modified attributes to their original values. See GUI._create_frames()"""
        if self.get_val(index, 'created'):
            self.get_val(index, 'frame_var').destroy()  # recursively destroys the Frame and all widgets inside it
            self.set_val(index, 'frame_var', None)  # forget the reference, ∴ send to GC
            self.set_val(index, 'created', False)  # reset the 'created' attribute to False (DNE)
            self.set_val(index, 'StringVar', StringVar())  # reset the String variable the Entry text is stored in
            self._resize_frame()  # resize the frame since this Frame was destroyed

    def get_keys(self, index):
        return self._frames[index].keys()

    def get_val(self, index, key):
        """Accessor of the GUI._frames variable"""
        return self._frames[index][key]

    def set_val(self, index, key, value):
        """Modifier of the GUI._frames variable"""
        self._frames[index][key] = value

    def len_frames(self):
        return len(self._frames)

    def populate_from_file(self):
        """Read data from file, create the Frame, then populate with data"""
        # Read data from file
        for index in range(self.len_frames()):
            # Create the Frame
            self.create_next_frame(index)
            # Populate the Frame's StringVar with data
        self._resize_frame()


class TitleBar(Frame):
    """The top-most Frame that contains the '×' close button."""
    def __init__(self, parent, index):
        Frame.__init__(self, parent)
        self.pack(expand=True, fill=BOTH)
        self.parent = parent
        self.root = self.parent.root

        self.index = index
        self.buttons = []

        self.create_title_bar_widgets()

    def _close(self):
        """Clicking the '×' button closes the window and exits the program."""
        self.root.destroy()

    def create_title_bar_widgets(self):
        """Only called when creating a new TitleBar instance, in the _init_ method above."""
        self.bind('<FocusIn>', self.title_bar_focus_in)  # cursor lies within this Frame

        for button_type, anchor_location in self.parent.get_val(self.index, 'options'):
            button = Button(self, highlightthickness=0, text=button_type, command=self._close,
                            activebackground='#444444', activeforeground='#cccccc')
            button.pack(side=TOP, anchor=anchor_location)
            self.buttons.append(button)

    def destroy_frame(self):
        """Calling this will delete the TitleBar Frame.
        Never planning on calling this, but all Frame classes should have this method."""
        self.parent.destroy_frame(self.index)

    def title_bar_focus_in(self, _):
        """This Frame currently contains the cursor."""
        self.parent.focused_frame = self.index


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


class EntryBaseClass(Frame):
    def __init__(self, parent, index):
        Frame.__init__(self, parent)
        self.pack(expand=True, fill=BOTH)
        self.parent = parent
        self.root = self.parent.root

        self.index = index
        if 'description' in self.parent.get_keys(self.index):
            self.description = self.parent.get_val(self.index, 'description')
            self.disabled = False
        else:
            self.disabled = True
        self.entry = None
        self.label = None
        self.intro_char = None  # placed at the beginning of the Entry's textbox when cursor is within
        self.valid_chars = None

        self.create_widgets()

    def create_widgets(self):
        self.create_label_widget()
        self.create_entry_widget()
        self.bind_frame()

    def create_label_widget(self):
        self.label = Label(self, text=self.parent.get_val(self.index, 'label'), width=15)
        self.label.pack(side=LEFT, anchor=W)

    def create_entry_widget(self):
        self.entry = Entry(self, textvariable=self.parent.get_val(self.index, 'StringVar'))
        self.entry.pack(side=LEFT, expand=True, fill=X)
        self._insert_description()

    def destroy_frame(self):
        """Calling this will delete this Alpha Frame instance.
        Resets all GUI._frames values associated to self.index completely."""
        self.parent.destroy_frame(self.index)

    def bind_frame(self):
        self.bind('<FocusIn>', self.focus_in)  # cursor lies within this Frame
        self.bind('<FocusOut>', self.focus_out)  # cursor has left this Frame
        if not self.disabled:
            self.entry.bind('<Enter>', self.mouse_enters_entry)
            self.entry.bind('<Leave>', self.mouse_leaves_entry)
            self.entry.bind('<Insert>', lambda e: 'break')  # disable Insert
            self.entry.bind('<Control-v>', lambda e: 'break')  # disable paste
            self.entry.bind('<Control-y>', lambda e: 'break')  # disable uncommon undo (paste in tkinter)
            self.entry.bind('<Button-3>', lambda e: 'break')  # disable right-click
        else:
            self.entry.configure(state='readonly')

    def mouse_enters_entry(self, _):
        """Mouse just started hovering over this Entry's textbox.
        If the description is present, delete it to prepare for user input."""
        self._clear_description()
        self._place_intro_char()

    def mouse_leaves_entry(self, _):
        """Mouse is no longer hovering over this Entry's textbox.
        If the Entry's textbox is empty (no user input), fill it with the description."""
        if self.parent.focused_frame is not self.index:
            self._insert_description()

    def focus_in(self, _):
        """This Frame currently contains the cursor.
        If the description is present, clear the Entry's textbox."""
        self.parent.focused_frame = self.index
        self._clear_description()
        self._place_intro_char()

    def focus_out(self, _):
        """This Frame does not contain the cursor anymore.
        If the Entry's textbox is empty, fill it with the Frame's description"""
        self._insert_description()

    def _clear_description(self):
        """If the Entry's textbox contains the description: clear the Entry's textbox."""
        if not self.disabled and self.entry.get() == self.description:
            self.entry.delete(0, END)

    def _insert_description(self):
        """If the Entry's textbox has no user input: insert the description."""
        if not self.disabled and self._is_empty():
            self.entry.delete(0, END)
            self.entry.insert(0, self.description)

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
        if self._is_empty():
            # No characters remain in the symbol entry widget, ∴ destroy all further frames
            self.parent.destroy_all_frames_after(self.index)
            return True
        return False

    def _is_empty(self):
        return self.entry.get() == ('', self.intro_char)[bool(self.intro_char)]

    def _place_intro_char(self):
        if self.intro_char is not None:
            if self.entry.get() == '' and not self.entry.get().count(self.intro_char):
                self.entry.insert(0, self.intro_char)


class Alpha(EntryBaseClass):
    """The only characters that will remain in this Frame's Entry textbox are Alpha letters: {A, B, ..., Z}.
    Feel free to type a lowercase letter, because the text is replaced with CAPITAL letters.
    All other printable characters {'c', '1', '~', ' ', ...} will be deleted in-place.
    Meta keys {Shift, Tab, Left, Control, Escape, ...} will not alter the Entry's textbox."""
    def __init__(self, parent, index):
        super().__init__(parent, index)
        self.last_text_entered = None
        self.valid_chars = [('a', 'z'), ('A', 'Z')]

        self.entry.bind('<KeyRelease>', self.alpha_entry_key_released)  # key pressed => key released

    def _rewrite_in_all_caps(self):
        """If we received a valid letter [azAZ]: clear the entry text and re-write in ALL CAPS"""
        curr_symbol = self.entry.get().upper()
        cursor_pos = self.entry.index(INSERT)
        self.entry.delete(0, END)
        self.entry.insert(0, curr_symbol)
        self.entry.icursor(cursor_pos)

    def alpha_entry_key_released(self, event):
        """Called every time a key on the keyboard is released while the cursor is in the Alpha Entry's textbox.
        If the key pressed is a printable character: check if it a valid character.
         If it is a valid character [azAZ]: convert the Entry's text to ALL CAPS.
          If the length of the Entry's text is greater than 4: truncate the last character.
         Else the char is a digit or punctuation: delete it in place. (doesn't move the cursor)
        If the textbox's last character is a space, delete it.
        If the textbox contains a space anywhere else: clear all text. (the description is present)
        If no characters currently remain in the textbox: destroy all frames after this Frame.
        Else the is at least one character: check if the file exists"""
        if is_char_printable(event.char):
            # Received a printable character: {alpha || numeric || punctuation}
            if is_char_valid(event.char, self.valid_chars):
                # Received valid input: [azAZ]
                self._rewrite_in_all_caps()  # [AZ]

                if len(self.entry.get()) <= 4:
                    print('Symbol:', self.entry.get())
                else:
                    # Length is >= 5, ∴ delete the last letter
                    self._delete_character(4, to_i=END)
            else:
                # Received invalid input: {numeric || punctuation}
                if not self._delete_spaces():
                    self._delete_character(INSERT, -1)

        if not self._destroyed_for_empty_input():
            # If at least one character remains
            if file_helper.file_exists(self.entry.get().lower()):
                # If user previously saved a file for this symbol, load it!
                self.parent.populate_from_file()
            else:
                # Else the file does not exist
                if self.last_text_entered != self.entry.get():
                    # If the symbol has changed: destroy all frames below this Frame
                    self.parent.destroy_all_frames_after(self.index)
                self.parent.create_next_frame(self.index + 1)

        self.last_text_entered = self.entry.get()


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
        if is_char_printable(event.char):
            # Received a printable character: {alpha || numeric || punctuation}
            if is_char_valid(event.char, self.valid_chars):
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


def is_char_printable(char):
    """Returns True if the character is {[azAZ09] || punctuation}.
    Returns False if the character is a meta key"""
    return len(repr(char)) is 3 or char == '\\'


def is_char_valid(char, valid_chars):
    if is_char_printable(char):
        for valid in valid_chars:
            if isinstance(valid, tuple) and valid[0] <= char <= valid[1]:
                # char lies within valid range
                return True
            elif isinstance(valid, str) and char == valid:
                # char matches the valid character
                return True
            # else: continue checking

    # char did not pass any validity checks || is a meta key, ∴ char is invalid
    return False
