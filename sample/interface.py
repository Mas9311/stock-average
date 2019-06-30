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

        self._frames = self.frames_dict()
        self.focused_frame = 0

        self.create_next_frame(0)  # create TitleBar Frame
        self.create_next_frame(1)  # create Alpha "Symbol" Frame

    def frames_dict(self):
        return {
            0: {
                'create': self.create_title_bar_frame,
                'created': False,
                'frame_var': self.title_bar_frame,
                'label': 'Title Bar',
                'options': [('×', 'ne')],  # ?: ('Options', 'nw')
            },
            1: {
                'create': self.create_alpha_frame,
                'created': False,
                'description': 'Enter the ticker symbol.',
                'frame_var': self.symbol_frame,
                'index': 1,
                'label': 'Symbol',
                'StringVar': self.symbol_string,
            },
            2: {
                'create': self.create_radio_frame,
                'created': False,
                'frame_var': self.asset_type_frame,
                'index': 2,
                'label': 'Asset Type',
                'options': ['stock', 'cryptocurrency'],
                'StringVar': self.asset_type_string,
            },
            3: {
                'create': self.create_numeric_frame,
                'created': False,
                'description': 'Enter the # of shares you own.',
                'frame_var': self.quantity_frame,
                'index': 3,
                'label': 'Quantity',
                'StringVar': self.quantity_string,
            },
            4: {
                'create': self.create_currency_frame,
                'created': False,
                'description': 'Enter your current average.',
                'disabled': False,
                'frame_var': self.current_average_frame,
                'index': 4,
                'label': 'Current Average',
                'StringVar': self.current_average_string,
            },
            5: {
                'create': self.create_currency_frame,
                'created': False,
                'description': 'Enter the current market price.',
                'disabled': False,
                'frame_var': self.current_price_frame,
                'index': 5,
                'label': 'Current Price',
                'StringVar': self.current_price_string,
            },
            6: {
                'create': self.create_currency_frame,
                'created': False,
                'description': None,
                'disabled': True,
                'frame_var': self.potential_average_frame,
                'index': 6,
                'label': 'Potential Average',
                'StringVar': self.potential_average_string,
            }
        }

    def resize_frame(self):
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
        if self._frames[next_index] and not self.get_val(next_index, 'created'):
            self.get_val(next_index, 'create')(next_index)
            self._frames[next_index]['created'] = True
            self.resize_frame()

    def create_title_bar_frame(self, index):
        self._frames[index]['frame_var'] = TitleBar(self, index)

    def create_alpha_frame(self, index):
        self._frames[index]['frame_var'] = Alpha(self, index)

    def create_radio_frame(self, index):
        self._frames[index]['frame_var'] = Radio(self, index)

    def create_numeric_frame(self, index):
        self._frames[index]['frame_var'] = Numeric(self, index)

    def create_currency_frame(self, index):
        self._frames[index]['frame_var'] = Currency(self, index)

    def destroy_frame(self, index):
        """Destroys the Frame (and all nested widgets recursively) at a given index of GUI.frames
        Sets all modified attributes to their original values. See GUI.frames_dict()"""
        if self.get_val(index, 'created'):
            self.get_val(index, 'frame_var').destroy()  # recursively destroys the Frame and all widgets inside it
            self.set_val(index, 'frame_var', None)  # forget the reference, ∴ send to GC
            self.set_val(index, 'created', False)  # reset the 'created' attribute to False (DNE)
            self.set_val(index, 'StringVar', StringVar())  # reset the String variable the Entry text is stored in
            self.resize_frame()  # resize the frame since this Frame was destroyed

    def get_val(self, index, key):
        """Accessor of the GUI._frames variable"""
        return self._frames[index][key]

    def set_val(self, index, key, value):
        """Modifier of the GUI._frames variable"""
        self._frames[index][key] = value

    def populate_from_file(self):
        """Read data from file, create the Frame, then populate with data"""
        # Read data from file
        for index in self._frames.keys():
            # Create the Frame
            self.create_next_frame(index)
            # Populate the Frame's StringVar with data
        self.resize_frame()

    def destroy_all_frames_after(self, index):
        for i in self._frames.keys():
            if i > index and self.get_val(i, 'created'):
                self.get_val(i, 'frame_var').destroy_frame()


class TitleBar(Frame):
    def __init__(self, parent, index):
        Frame.__init__(self, parent)
        self.pack(expand=True, fill=BOTH)
        self.parent = parent
        self.root = self.parent.root

        self.index = index
        self.buttons = []

        self.create_title_bar_widgets()

    def create_title_bar_widgets(self):
        for button_type, anchor_location in self.parent.get_val(self.index, 'options'):
            button = Button(self, highlightthickness=0, text=button_type, command=self._close,
                            activebackground='#444444', activeforeground='#cccccc')
            button.pack(side=TOP, anchor=anchor_location)
            self.buttons.append(button)

    def _close(self):
        self.root.destroy()

    def destroy_frame(self):
        self.parent.destroy_frame(self.index)


class Alpha(Frame):
    """The only characters that will remain in this Frame's Entry textbox are Alpha letters: {A, B, ..., Z}.
    Feel free to type a lowercase letter, because the text is replaced with CAPITAL letters.
    All other printable characters {'c', '1', '~', ' ', ...} will be deleted in-place.
    Meta keys {Shift, Tab, Left, Control, Escape, ...} will not alter the Entry's textbox."""
    def __init__(self, parent, index):
        Frame.__init__(self, parent)
        self.pack(expand=True, fill=BOTH)
        self.parent = parent
        self.root = self.parent

        self.index = index
        self.description = self.parent.get_val(self.index, 'description')
        self.alpha_label = None
        self.alpha_entry = None
        self.last_symbol_entered = None
        self.valid_chars = [('a', 'z')]

        self.create_alpha_widgets()

    def create_alpha_widgets(self):
        self.alpha_label = Label(self, text=self.parent.get_val(self.index, 'label'), width=15)
        self.alpha_label.pack(side=LEFT, anchor=W)

        self.alpha_entry = Entry(self, textvariable=self.parent.get_val(self.index, 'StringVar'))
        self.alpha_entry.insert(0, self.description)
        self.alpha_entry.bind('<Enter>', self.alpha_entry_entered)
        self.alpha_entry.bind('<Leave>', self.alpha_entry_left)
        self.alpha_entry.bind('<FocusIn>', self.alpha_entry_focus_in)  # mouse hovers over
        self.alpha_entry.bind('<FocusOut>', self.alpha_entry_focus_out)  # mouse leaves
        self.alpha_entry.bind('<KeyRelease>', self.alpha_entry_key_released)

        self.alpha_entry.bind('<Insert>', lambda e: 'break')  # disable Insert
        self.alpha_entry.bind('<Control-v>', lambda e: 'break')  # disable paste
        self.alpha_entry.bind('<Control-y>', lambda e: 'break')  # disable uncommon undo (paste in tkinter)
        self.alpha_entry.bind('<Button-3>', lambda e: 'break')  # disable right-click
        self.alpha_entry.pack(side=LEFT, expand=True, fill=X)

    def alpha_entry_entered(self, _):
        if self.alpha_entry.get() == self.description:
            self._delete_characters()

    def alpha_entry_left(self, _):
        if self.parent.focused_frame is not self.index and not self.alpha_entry.get():
            self.alpha_entry.insert(0, self.description)

    def alpha_entry_focus_in(self, _):
        self.parent.focused_frame = self.index

    def alpha_entry_focus_out(self, _):
        if not self.alpha_entry.get():
            self.alpha_entry.insert(0, self.description)

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
        if self._is_printable(event.char):
            # Received a printable character: {alpha || numeric || punctuation}
            if self._is_valid_char(event.char):
                # Received valid input: [azAZ]
                self._rewrite_in_all_caps()  # [AZ]

                if len(self.alpha_entry.get()) <= 4:
                    print('Symbol:', self.alpha_entry.get())
                else:
                    # Length is >= 5, ∴ delete the last letter
                    self._delete_characters(4, END)
            else:
                # Received invalid input: numeric || punctuation
                self._delete_characters(INSERT, -1, END)
        self._delete_symbol_spaces()

        if not self.alpha_entry.get():
            # No characters remain in the symbol entry widget, ∴ destroy all children
            self.parent.destroy_all_frames_after(self.index)
        else:
            # If at least one character remains
            if file_helper.file_exists(self.alpha_entry.get().lower()):
                # If user previously saved a file for this symbol, load it!
                self.parent.populate_from_file()
            else:
                # Else destroy all frames below symbol, but keep asset_type's Frame
                if self.last_symbol_entered != self.alpha_entry.get():
                    self.parent.destroy_all_frames_after(self.index)
                self.parent.create_next_frame(self.index + 1)

        self.last_symbol_entered = self.alpha_entry.get()

    def destroy_frame(self):
        self.parent.destroy_frame(self.index)

    def _delete_symbol_spaces(self):
        space_position = self.alpha_entry.get().find(' ')
        last_char_index = len(self.alpha_entry.get()) - 1

        if space_position != -1:
            if space_position < last_char_index:
                self._delete_characters()
            elif space_position is last_char_index:
                self._delete_characters(last_char_index)

    def _delete_characters(self, from_i=0, from_offset=0, to_i=END):
        if isinstance(from_i, str):
            from_i = self.alpha_entry.index(from_i)
        from_i += from_offset

        if isinstance(to_i, str):
            to_i = self.alpha_entry.index(to_i)

        self.alpha_entry.delete(from_i, to_i)

    def _is_printable(self, char):
        return len(repr(char)) is 3 or char == '\\'

    def _is_valid_char(self, char):
        if self._is_printable(char):
            char = char.lower()
            for valid in self.valid_chars:
                if isinstance(valid, tuple):
                    if not valid[0] <= char <= valid[1]:
                        # char does not lie within valid range
                        return False
                    # else the char lies within valid range: continue
                elif isinstance(valid, str):
                    if char != valid:
                        # char does not match the valid character
                        return False
                    # else the char matched the valid character: continue

            # char did not fail any validity checks, ∴ char is valid!
            print(f'_{char}_ is a valid character')
            return True
        else:
            # key is a meta key
            return False

    def _rewrite_in_all_caps(self):
        """If we received a valid letter [azAZ]: clear the entry text and re-write in ALL CAPS"""
        curr_symbol = self.alpha_entry.get().upper()
        cursor_pos = self.alpha_entry.index(INSERT)
        self._delete_characters()
        self.alpha_entry.insert(0, curr_symbol)
        self.alpha_entry.icursor(cursor_pos)


class Radio(Frame):
    def __init__(self, parent, index):
        Frame.__init__(self, parent)
        self.pack(expand=True, fill=BOTH)
        self.parent = parent

        self.index = index

        self.radio_label = None
        self.buttons = []
        self.last_button_selected = None

        self.create_asset_type_widgets()

    def create_asset_type_widgets(self):
        self.radio_label = Label(self, text=self.parent.get_val(self.index, 'label'), width=15)
        self.radio_label.pack(side=LEFT, anchor=W)

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
        for button in self.buttons:
            button.deselect()

    def destroy_frame(self):
        self.deselect_buttons()
        self.parent.destroy_frame(self.index)


class Numeric(Frame):
    def __init__(self, parent, index):
        Frame.__init__(self, parent)
        self.pack(expand=True, fill=BOTH)
        self.parent = parent

        self.index = index
        self.quantity_description = self.parent.get_val(self.index, 'description')

        self.quantity_label = None
        self.quantity_entry = None
        self.quantity_focused = False

        self.valid_chars = [('0', '9'), '.']

        self.create_quantity_widgets()

    def create_quantity_widgets(self):
        self.quantity_label = Label(self, text=self.parent.get_val(self.index, 'label'), width=15)
        self.quantity_label.pack(side=LEFT, anchor=W)

        self.quantity_entry = Entry(self, textvariable=self.parent.get_val(self.index, 'StringVar'))
        self.quantity_entry.insert(0, self.quantity_description)
        self.quantity_entry.bind('<Enter>', self.quantity_entry_entered)
        self.quantity_entry.bind('<Leave>', self.quantity_entry_left)
        self.bind('<FocusIn>', self.quantity_entry_focused)
        self.bind('<FocusOut>', self.quantity_entry_focused)
        self.quantity_entry.bind('<KeyRelease>', self.quantity_entry_key_released)

        self.quantity_entry.bind('<Insert>', lambda e: 'break')  # disable Insert
        self.quantity_entry.bind('<Control-v>', lambda e: 'break')  # disable paste
        self.quantity_entry.bind('<Control-y>', lambda e: 'break')  # disable uncommon undo (paste in tkinter)
        self.quantity_entry.bind('<Button-3>', lambda e: 'break')  # disable right-click
        self.quantity_entry.pack(side=LEFT, expand=True, fill=X)

    def quantity_entry_entered(self, _):
        if self.quantity_entry.get().find(self.quantity_description) is not -1:
            self.quantity_entry.delete(0, END)

    def quantity_entry_left(self, _):
        if not self.quantity_entry.get() and not self.quantity_focused:
            self.quantity_entry.insert(0, self.quantity_description)

    def quantity_entry_focused(self, _):
        self.quantity_focused = not self.quantity_focused
        if not self.quantity_focused and not self.quantity_entry.get():
            self.quantity_entry.insert(0, self.quantity_description)

    def quantity_entry_key_released(self, _):
        if self.quantity_entry.get():
            self.parent.create_next_frame(self.index + 1)

    def destroy_frame(self):
        self.parent.destroy_frame(self.index)


class Currency(Frame):
    def __init__(self, parent, index):
        Frame.__init__(self, parent)
        self.pack(expand=True, fill=BOTH)
        self.parent = parent

        self.index = index

        self.disabled = self.parent.get_val(self.index, 'disabled')
        self.money_frame_description = self.parent.get_val(self.index, 'description')
        self.money_frame_label = None
        self.money_frame_entry = None
        self.valid_chars = [('0', '9'), '.']

        self.create_money_frame_widgets()

    def create_money_frame_widgets(self):
        self.money_frame_label = Label(self, text=self.parent.get_val(self.index, 'label'), width=15)
        self.money_frame_label.pack(side=LEFT, anchor=W)

        self.money_frame_entry = Entry(self, textvariable=self.parent.get_val(self.index, 'StringVar'))
        if self.disabled:
            self.money_frame_entry.configure(state='readonly')
        else:
            self.money_frame_entry.insert(0, self.money_frame_description)
        self.money_frame_entry.bind('<Enter>', self.money_frame_entry_entered)
        self.money_frame_entry.bind('<Leave>', self.money_frame_entry_left)
        self.money_frame_entry.bind('<FocusIn>', self.money_frame_entry_focused_in)
        self.money_frame_entry.bind('<KeyRelease>', self.money_frame_entry_key_released)

        self.money_frame_entry.bind('<Insert>', lambda e: 'break')  # disable Insert
        self.money_frame_entry.bind('<Control-v>', lambda e: 'break')  # disable paste
        self.money_frame_entry.bind('<Control-y>', lambda e: 'break')  # disable uncommon undo (paste in tkinter)
        self.money_frame_entry.bind('<Button-3>', lambda e: 'break')  # disable right-click
        self.money_frame_entry.pack(side=LEFT, expand=True, fill=X)

    def money_frame_entry_entered(self, _):
        if not self.disabled:
            if self.money_frame_entry.get().find(self.money_frame_description) is not -1:
                self.money_frame_entry.delete(0, END)

    def money_frame_entry_left(self, _):
        if not self.disabled and self.parent.focused_frame is not self.index:
            if self.money_frame_entry.get() == '$':
                self.money_frame_entry.delete(0, END)
            if not self.money_frame_entry.get():
                self.money_frame_entry.insert(0, self.money_frame_description)

    def money_frame_entry_focused_in(self, _):
        if not self.disabled:
            self.parent.focused_frame = self.index
            if self.parent.focused_frame is not self.index and self.money_frame_entry.get() == '$':
                self.money_frame_entry.delete(0, 1)
                self.money_frame_entry.insert(0, self.money_frame_description)
            elif self.parent.focused_frame is self.index and self.money_frame_entry.get().find('$') is -1:
                self.money_frame_entry.insert(0, '$')

    def money_frame_entry_key_released(self, event):
        if (len(repr(event.char)) is 3 or event.char == '\\') and \
                (not '0' <= event.char <= '9') and \
                (event.char != '.'):
            # Received invalid input: non-period-punctuation or alpha"""
            self.money_frame_entry.delete(self.money_frame_entry.index(INSERT) - 1)

        first_decimal_point = self.money_frame_entry.get().find('.')
        if first_decimal_point is not -1:
            second_decimal_point = self.money_frame_entry.get()[first_decimal_point + 1:].find('.')
            if second_decimal_point is not -1 and event.char == '.':
                self.money_frame_entry.delete(self.money_frame_entry.index(INSERT) - 1)

        if self.money_frame_entry.get().find('$') is not 0:
            self.money_frame_entry.insert(0, '$')

        if self.money_frame_entry.index(INSERT) is 0:
            self.money_frame_entry.icursor(1)

        if len(self.money_frame_entry.get()) > 1 and '0' <= event.char <= '9':
            self.parent.create_next_frame(self.index + 1)

    def destroy_frame(self):
        self.parent.destroy_frame(self.index)
