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

        self.frames = self.frames_dict()
        self.frame_with_focus = 0

        self.create_next_frame(0)  # create TitleBar Frame
        self.create_next_frame(1)  # create Alpha "Symbol" Frame

    def frames_dict(self):
        return {
            0: {
                'create': self.create_title_bar_frame,
                'created': False,
                'frame_var': self.title_bar_frame,
                'label': 'Title Bar',
            },
            1: {
                'create': self.create_alpha_frame,
                'created': False,
                'description': 'Enter the ticker symbol',
                'frame_var': self.symbol_frame,
                'index': 1,
                'label': 'Symbol',
                'StringVar': self.symbol_string,
            },
            2: {
                'buttons': ['stock', 'crypto'],
                'create': self.create_radio_frame,
                'created': False,
                'frame_var': self.asset_type_frame,
                'index': 2,
                'label': 'Asset Type',
                'StringVar': self.asset_type_string,
            },
            3: {
                'create': self.create_numeric_frame,
                'created': False,
                'description': 'Enter the # of shares you own',
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
                'description': 'Enter the current market price',
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
        w = self.root.winfo_reqwidth() + 100
        h = self.root.winfo_reqheight()
        # _, _, x, y = self.root.winfo_geometry().replace('x', '.').replace('+', '.').split('.')
        geo = f'{w}x{h}'
        self.root.geometry(geo)
        # print(geo)

    def create_next_frame(self, next_index):
        """Will create the frame if the next frame has not been created already.
        Optionally passed the index of the frame"""
        if self.frames[next_index]:
            if self.get_val(next_index, 'created') is False:
                self.frames[next_index]['create'](next_index)
                self.frames[next_index]['created'] = True
                self.resize_frame()

    def create_title_bar_frame(self, index):
        self.frames[index]['frame_var'] = TitleBar(self, index)

    def create_alpha_frame(self, index):
        self.frames[index]['frame_var'] = Alpha(self, index)

    def create_radio_frame(self, index):
        self.frames[index]['frame_var'] = Radio(self, index)

    def create_numeric_frame(self, index):
        self.frames[index]['frame_var'] = Numeric(self, index)

    def create_currency_frame(self, index):
        self.frames[index]['frame_var'] = Currency(self, index)

    def get_val(self, index, key):
        return self.frames[index][key]

    #     def populate_from_file(self):
    #         # Read from file, then populate the frames with the data
    #         self.create_asset_type_frame()
    #         self.create_quantity_frame()
    #         self.create_current_average_frame()
    #         self.create_potential_average_frame()
    #         self.resize_frame()

    def destroy_all_frames_after(self, index):
        for i in self.frames.keys():
            print(i, self.frames[i]['frame_var'])
            if i > index and self.frames[i]['created']:
                self.frames[i]['frame_var'].destroy_frame()


class TitleBar(Frame):
    def __init__(self, parent, index):
        Frame.__init__(self, parent)
        self.pack(expand=True, fill=BOTH)
        self.parent = parent
        self.root = self.parent.root

        self.index = index
        self.close_button = None

        self.create_title_bar_widgets()

    def create_title_bar_widgets(self):
        self.close_button = Button(self, highlightthickness=0, text='×', command=self._close,
                                   activebackground='#444444', activeforeground='#cccccc')
        self.close_button.pack(side=TOP, anchor=NE)

    def _close(self):
        self.root.destroy()

    def destroy_frame(self):
        self.parent.frames[self.index]['frame_var'].destroy()
        self.parent.frames[self.index]['frame_var'] = None
        self.parent.frames[self.index]['created'] = False
        self.parent.resize_frame()


class Alpha(Frame):
    def __init__(self, parent, index):
        Frame.__init__(self, parent)
        self.pack(expand=True, fill=BOTH)
        self.parent = parent
        self.root = self.parent

        self.index = index
        self.description = self.parent.get_val(self.index, 'description')
        self.alpha_label = None
        self.alpha_entry = None

        self.create_alpha_widgets()

    def create_alpha_widgets(self):
        self.alpha_label = Label(self, text="Symbol", width=15)
        self.alpha_label.pack(side=LEFT, anchor=W)

        self.alpha_entry = Entry(self, textvariable=self.parent.get_val(self.index, 'StringVar'))
        self.alpha_entry.insert(0, self.description)
        self.alpha_entry.bind('<Enter>', self.alpha_entry_entered)
        self.alpha_entry.bind('<Leave>', self.alpha_entry_left)
        self.alpha_entry.bind('<FocusIn>', self.alpha_entry_focus_in)
        self.alpha_entry.bind('<FocusOut>', self.alpha_entry_focus_out)
        self.alpha_entry.bind('<KeyRelease>', self.alpha_entry_key_released)

        self.alpha_entry.bind('<Insert>', lambda e: 'break')  # disable Insert
        self.alpha_entry.bind('<Control-v>', lambda e: 'break')  # disable paste
        self.alpha_entry.bind('<Control-y>', lambda e: 'break')  # disable uncommon undo (paste in tkinter)
        self.alpha_entry.bind('<Button-3>', lambda e: 'break')  # disable right-click
        self.alpha_entry.pack(side=LEFT, expand=True, fill=X)

    def alpha_entry_entered(self, _):
        if self.alpha_entry.get() == self.description:
            self.alpha_entry.delete(0, END)

    def alpha_entry_left(self, _):
        if self.parent.frame_with_focus is not self.index and not self.alpha_entry.get():
            self.alpha_entry.insert(0, self.description)

    def alpha_entry_focus_in(self, _):
        self.parent.frame_with_focus = self.index

    def alpha_entry_focus_out(self, _):
        if not self.alpha_entry.get():
            self.alpha_entry.insert(0, self.description)

    def alpha_entry_key_released(self, event):
        if (len(repr(event.char)) is 3 or event.char == '\\') and not 'a' <= event.char.lower() <= 'z':
            # Received invalid input: punctuation or digit"""
            self.alpha_entry.delete(self.alpha_entry.index(INSERT) - 1)

        self.delete_symbol_spaces()

        curr_symbol = self.alpha_entry.get().upper()

        if 'a' <= event.char.lower() <= 'z':
            # Received valid alpha input [a-zA-Z], so clear the entry text and re-write in ALL CAPS
            cursor_pos = self.alpha_entry.index(INSERT)
            self.alpha_entry.delete(0, END)
            self.alpha_entry.insert(0, curr_symbol)
            self.alpha_entry.icursor(cursor_pos)

        if curr_symbol:
            # If at least one character remains
            if 'a' <= event.char.lower() <= 'z':
                # If the last button received was valid
                if len(self.alpha_entry.get()) > 4:
                    # If the length of the symbol is 5+, delete the last letter
                    self.alpha_entry.delete(self.alpha_entry.index(END) - 1)
                print('Symbol:', curr_symbol)

            if file_helper.file_exists(curr_symbol.lower()):
                # If user previously saved a file for this symbol, load it!
                self.parent.populate_from_file()
            else:
                # Else destroy all frames below symbol, but keep asset_type's Frame
                # self.parent.destroy_all_frames_after_symbol()
                self.parent.create_next_frame(self.index + 1)
        else:
            # No characters remain in the symbol entry widget, ∴ destroy all children
            self.parent.destroy_all_frames_after(self.index)

    def delete_symbol_spaces(self):
        space_position = self.alpha_entry.get().find(' ')
        last_char_index = len(self.alpha_entry.get()) - 1

        if space_position != -1:
            if space_position < last_char_index:
                self.alpha_entry.delete(0, END)
            elif space_position is last_char_index:
                self.alpha_entry.delete(last_char_index)

    def destroy_frame(self):
        self.parent.frames[self.index]['frame_var'].destroy()
        self.parent.frames[self.index]['frame_var'] = None
        self.parent.frames[self.index]['created'] = False
        self.parent.frames[self.index]['StringVar'] = StringVar()
        self.parent.resize_frame()


class Radio(Frame):
    def __init__(self, parent, index):
        Frame.__init__(self, parent)
        self.pack(expand=True, fill=BOTH)
        self.parent = parent

        self.index = index

        self.radio_label = None
        self.buttons = []

        self.create_asset_type_widgets()

    def create_asset_type_widgets(self):
        self.radio_label = Label(self, text="Asset Type", width=15)
        self.radio_label.pack(side=LEFT, anchor=W)

        for button_type in self.parent.frames[self.index]['buttons']:
            button = Radiobutton(self, text=button_type, variable=self.parent.get_val(self.index, 'StringVar'),
                                 val=button_type, command=self.select)
            button.pack(side=LEFT, anchor=W)
            self.buttons.append(button)

    def select(self):
        self.parent.create_next_frame(self.index + 1)

    def deselect_buttons(self):
        for i in range(len(self.buttons)):
            self.buttons[i].deselect()

    def destroy_frame(self):
        for button in self.buttons:
            button.deselect()
        self.parent.frames[self.index]['frame_var'].destroy()
        self.parent.frames[self.index]['frame_var'] = None
        self.parent.frames[self.index]['created'] = False
        self.parent.frames[self.index]['StringVar'] = StringVar()
        self.parent.resize_frame()


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

        self.create_quantity_widgets()

    def create_quantity_widgets(self):
        self.quantity_label = Label(self, text="Quantity", width=15)
        self.quantity_label.pack(side=LEFT, anchor=W)

        self.quantity_entry = Entry(self, textvariable=self.parent.get_val(self.index, 'StringVar'))
        self.quantity_entry.insert(0, self.quantity_description)
        self.quantity_entry.bind('<Enter>', self.quantity_entry_entered)
        self.quantity_entry.bind('<Leave>', self.quantity_entry_left)
        self.quantity_entry.bind('<FocusIn>', self.quantity_entry_focused)
        self.quantity_entry.bind('<FocusOut>', self.quantity_entry_focused)
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
        self.parent.frames[self.index]['frame_var'].destroy()
        self.parent.frames[self.index]['frame_var'] = None
        self.parent.frames[self.index]['created'] = False
        self.parent.frames[self.index]['StringVar'] = StringVar()
        self.parent.resize_frame()


class Currency(Frame):
    def __init__(self, parent, index):
        Frame.__init__(self, parent)
        self.pack(expand=True, fill=BOTH)
        self.parent = parent

        self.index = index

        self.disabled = self.parent.get_val(self.index, 'disabled')
        self.money_frame_description = self.parent.get_val(self.index, 'description')
        self.money_frame_focused = False

        self.money_frame_label = None
        self.money_frame_entry = None

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
        self.money_frame_entry.bind('<FocusIn>', self.money_frame_entry_focused)
        self.money_frame_entry.bind('<FocusOut>', self.money_frame_entry_focused)
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
        if not self.disabled:
            if not self.money_frame_focused:
                if self.money_frame_entry.get() == '$':
                    self.money_frame_entry.delete(0, END)
                if not self.money_frame_entry.get():
                    self.money_frame_entry.insert(0, self.money_frame_description)

    def money_frame_entry_focused(self, _):
        if not self.disabled:
            self.money_frame_focused = not self.money_frame_focused
            if not self.money_frame_focused and self.money_frame_entry.get() == '$':
                self.money_frame_entry.delete(0, 1)
                self.money_frame_entry.insert(0, self.money_frame_description)
            elif self.money_frame_focused and self.money_frame_entry.get().find('$') is -1:
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
        self.parent.frames[self.index]['frame_var'].destroy()
        self.parent.frames[self.index]['frame_var'] = None
        self.parent.frames[self.index]['created'] = False
        self.parent.frames[self.index]['StringVar'] = StringVar()
        self.parent.resize_frame()
