from tkinter import *
from sample import stock_average
from sample import file_helper


def run():
    # if parameter_passed != 'cli':
        root = Tk()
        GUI(root)
        root.mainloop()
    # else:
    #     stock_average.run()


class GUI(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.master.title("Compute New Average")
        self.pack(expand=True, fill=BOTH)
        self.root = parent
        self.root.configure(background='black', bd=0, width=500)
        # self.root.resizable(False, False)

        self.symbol = StringVar()
        self.asset_type = StringVar()
        self.quantity = DoubleVar()
        self.current_average = DoubleVar()
        self.potential_average = DoubleVar()

        self.close_button = None
        self.symbol_frame = None
        self.asset_type_frame = None
        self.quantity_frame = None
        self.current_average_frame = None
        self.potential_average_frame = None

        self.create_widgets()

    def _close(self):
        self.root.destroy()

    def create_widgets(self):
        self.close_button = Button(self, highlightthickness=0, text='×', command=self._close,
                                   activebackground='#444444', activeforeground='#cccccc')
        self.close_button.pack(side=TOP, anchor=NE)
        self.symbol_frame = Symbol(self)

    def create_asset_type_frame(self):
        if self.asset_type_frame is None:
            self.asset_type_frame = AssetType(self)
        else:
            self.asset_type_frame.deselect_buttons()

    def reload_quantity_description(self):
        self.quantity_frame.reload_description()

    def create_quantity_frame(self):
        if self.quantity_frame is None:
            self.quantity_frame = Quantity(self)

    def create_current_average_frame(self):
        if self.current_average_frame is None:
            self.current_average_frame = CurrentAverage(self)

    def create_potential_average_frame(self):
        if self.potential_average_frame is None:
            self.potential_average_frame = PotentialAverage(self)

    def populate_from_file(self):
        # Read from file, then populate the frames with the data
        self.create_asset_type_frame()
        self.create_quantity_frame()
        self.create_current_average_frame()
        self.create_potential_average_frame()

    def destroy_all_frames_after_symbol(self):
        if self.asset_type_frame:
            self.asset_type_frame.destroy()
            self.asset_type_frame = None
        if self.quantity_frame:
            self.quantity_frame.destroy()
            self.quantity_frame = None
        if self.current_average_frame:
            self.current_average_frame.destroy()
            self.current_average_frame = None
        if self.potential_average_frame:
            self.potential_average_frame.destroy()
            self.potential_average_frame = None


class Symbol(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.pack(expand=True, fill=BOTH)
        self.parent = parent
        self.root = self.parent

        self.symbol_label = None
        self.symbol_entry = None
        self.symbol_description = 'Enter the ticker symbol'
        self.symbol_focused = False
        self.create_symbol_widgets()
        self.update_idletasks()

    def create_symbol_widgets(self):
        self.symbol_label = Label(self, text="Symbol", width=15)
        self.symbol_label.pack(side=LEFT, anchor=W)

        self.symbol_entry = Entry(self, textvariable=self.parent.symbol)
        self.symbol_entry.insert(0, self.symbol_description)
        self.symbol_entry.bind('<Enter>', self.symbol_entry_entered)
        self.symbol_entry.bind('<Leave>', self.symbol_entry_left)
        self.symbol_entry.bind('<FocusIn>', self.symbol_entry_focused)
        self.symbol_entry.bind('<FocusOut>', self.symbol_entry_focused)
        self.symbol_entry.bind('<KeyRelease>', self.symbol_entry_key_released)

        self.symbol_entry.bind('<Insert>', lambda e: 'break')  # disable Insert
        self.symbol_entry.bind('<Control-v>', lambda e: 'break')  # disable paste
        self.symbol_entry.bind('<Control-y>', lambda e: 'break')  # disable uncommon undo (paste in tkinter)
        self.symbol_entry.bind('<Button-3>', lambda e: 'break')  # disable right-click
        self.symbol_entry.pack(side=LEFT, expand=True, fill=X)

    def symbol_entry_entered(self, _):
        if self.symbol_entry.get() == self.symbol_description:
            self.symbol_entry.delete(0, END)

    def symbol_entry_left(self, _):
        if not self.symbol_entry.get() and not self.symbol_focused:
            self.symbol_entry.insert(0, self.symbol_description)

    def symbol_entry_focused(self, _):
        self.symbol_focused = not self.symbol_focused
        if not self.symbol_focused and not self.symbol_entry.get():
            self.symbol_entry.insert(0, self.symbol_description)

    def symbol_entry_key_released(self, event):
        if (len(repr(event.char)) is 3 or event.char == '\\') and not 'a' <= event.char.lower() <= 'z':
            # Received invalid input: punctuation or digit"""
            self.symbol_entry.delete(self.symbol_entry.index(INSERT) - 1)

        self.delete_symbol_spaces()

        cursor_pos = self.symbol_entry.index(INSERT)
        curr_symbol = self.symbol_entry.get().upper()

        if 'a' <= event.char.lower() <= 'z':
            # Received valid alpha input [a-zA-Z], so clear the entry text and re-write in ALL CAPS
            self.symbol_entry.delete(0, END)
            self.symbol_entry.insert(0, curr_symbol)
            self.symbol_entry.icursor(cursor_pos)

        if curr_symbol:
            # If at least one character remains
            if 'a' <= event.char.lower() <= 'z':
                # If the last button received was valid
                if len(self.symbol_entry.get()) > 4:
                    # If the length of the symbol is 5+, delete the last letter
                    self.symbol_entry.delete(self.symbol_entry.index(END) - 1)
                print('Symbol:', curr_symbol)

            if file_helper.file_exists(curr_symbol.lower()):
                # If user previously saved a file for this symbol, load it!
                self.parent.populate_from_file()
            else:
                self.parent.create_asset_type_frame()
        else:
            # No characters remain in the Entry textbox, so destroy all children
            self.parent.destroy_all_frames_after_symbol()

    def delete_symbol_spaces(self):
        space_position = self.symbol_entry.get().find(' ')
        last_char_index = len(self.symbol_entry.get()) - 1

        if space_position != -1:
            if space_position < last_char_index:
                self.symbol_entry.delete(0, END)
            elif space_position is last_char_index:
                self.symbol_entry.delete(last_char_index)


class AssetType(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.pack(expand=True, fill=BOTH)
        self.parent = parent

        self.asset_type_label = None
        self.stock_button = None
        self.crypto_button = None

        self.create_asset_type_widgets()

    def create_asset_type_widgets(self):
        self.asset_type_label = Label(self, text="Asset Type", width=15)
        self.asset_type_label.grid(row=0, column=0)

        self.stock_button = Radiobutton(self, text='stock', variable=self.parent.asset_type,
                                        val='stock', command=self.select)
        self.stock_button.grid(row=0, column=1)

        self.crypto_button = Radiobutton(self, text='crypto', variable=self.parent.asset_type,
                                         val='cryptocurrency', command=self.select)
        self.crypto_button.grid(row=0, column=2)

    def select(self):
        self.parent.create_quantity_frame()

    def deselect_buttons(self):
        self.stock_button.deselect()
        self.crypto_button.deselect()
        self.parent.reload_quantity_description()


class Quantity(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.pack(expand=True, fill=BOTH)
        self.parent = parent

        self.quantity_label = None
        self.quantity_entry = None
        self.quantity_description_basic = 'Enter the # of '
        self.quantity_description = None
        self.quantity_focused = False
        self.reload_description()

        self.create_quantity_widgets()

    def create_quantity_widgets(self):
        self.quantity_label = Label(self, text="Quantity", width=15)
        self.quantity_label.grid(row=0, column=0)

        self.quantity_entry = Entry(self, textvariable=self.parent.quantity)
        self.quantity_entry.insert(0, self.quantity_description)
        self.quantity_entry.bind('<Enter>', self.quantity_entry_entered)
        self.quantity_entry.bind('<Leave>', self.quantity_entry_left)
        self.quantity_entry.bind('<FocusIn>', self.quantity_entry_focused)
        self.quantity_entry.bind('<FocusOut>', self.quantity_entry_focused)
        self.quantity_entry.bind('<KeyRelease>', self.quantity_entry_key_released)
        self.quantity_entry.grid(row=0, column=1)

    def quantity_entry_entered(self, _):
        if self.quantity_entry.get().find(self.quantity_description_basic) is not -1:
            self.quantity_entry.delete(0, END)

    def quantity_entry_left(self, _):
        if not self.quantity_entry.get() and not self.quantity_focused:
            self.quantity_entry.insert(0, self.quantity_description)

    def quantity_entry_key_released(self, event):
        print(event.char)
        if self.quantity_entry.get():
            self.parent.create_current_average_frame()

    def quantity_entry_focused(self, _):
        self.quantity_focused = not self.quantity_focused
        if not self.quantity_focused and not self.quantity_entry.get():
            self.quantity_entry.insert(0, self.quantity_description)

    def reload_description(self):
        self.quantity_description = self.quantity_description_basic
        self.quantity_description += 'stocks' if self.parent.asset_type.get().lower()[0:1] == 's' else 'coins'
        if self.quantity_entry:
            if self.quantity_entry.get().find(self.quantity_description_basic) != -1:
                self.quantity_entry.delete(0, END)
                self.quantity_entry.insert(0, self.quantity_description)


class CurrentAverage(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.pack(expand=True, fill=BOTH)
        self.parent = parent

        self.current_average_label = None
        self.current_average_entry = None
        self.current_average_description = 'Enter your current Average'

        self.create_current_average_widgets()

    def create_current_average_widgets(self):
        self.current_average_label = Label(self, text="Current Average", width=15)
        self.current_average_label.grid(row=0, column=0)

        self.current_average_entry = Entry(self, textvariable=self.parent.current_average)
        self.current_average_entry.insert(0, self.current_average_description)
        self.current_average_entry.bind('<KeyRelease>', self.current_average_entry_key_released)
        self.current_average_entry.grid(row=0, column=1)

    def current_average_entry_key_released(self, event):
        print(event.char)
        if self.current_average_entry.get():
            self.parent.create_potential_average_frame()


class PotentialAverage(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.pack(expand=True, fill=BOTH)
        self.parent = parent

        self.potential_average_label = None
        self.potential_average_entry = None

        self.create_potential_average_widgets()

    def create_potential_average_widgets(self):
        self.potential_average_label = Label(self, text="Potential Average", width=15)
        self.potential_average_label.pack(side=LEFT, expand=True)

        self.potential_average_entry = Entry(self, state='readonly')
        self.potential_average_entry.pack(side=LEFT)



