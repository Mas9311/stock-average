from tkinter import *
from sample import stock_average
from sample import file_helper


def run():
    # if parameter_passed != 'cli':
        root = Tk()
        GUI(root)
        root.resizable(False, False)
        root.mainloop()
    # else:
    #     stock_average.run()


class GUI(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.master.title("Compute New Average")
        self.pack(fill=BOTH, expand=True)
        self.root = parent
        self.root.configure(background='black', bd=0, width=500)

        self.symbol = StringVar()

        self.close_button = None
        self.main_frame = None
        self.create_widgets()

    def _close(self):
        self.root.destroy()

    def create_widgets(self):
        self.close_button = Button(self, highlightthickness=0, text='×', command=self._close,
                                   activebackground='#444444', activeforeground='#cccccc')
        self.close_button.pack(side=TOP, anchor=NE)
        self.main_frame = Main(self)


class Main(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.pack(fill=BOTH, expand=True)
        self.parent = parent

        self.symbol_frame = None
        self.symbol_label = None
        self.symbol_entry = None
        self.symbol_description = 'Enter the ticker symbol'
        self.symbol_focused = False
        self.create_symbol_frame()
        self.update_idletasks()

        self.current_average_frame = None
        self.current_average_label = None
        self.current_average_entry = None

        self.projected_average_frame = None
        self.projected_average_label = None
        self.projected_average_entry = None

    def create_symbol_frame(self):
        self.symbol_frame = Frame(self)
        self.symbol_frame.pack(fill=X, expand=True)

        self.symbol_label = Label(self.symbol_frame, text="Symbol", width=15)
        self.symbol_label.pack(side=LEFT, anchor=W)

        self.symbol_entry = Entry(self.symbol_frame, textvariable=self.parent.symbol)
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

    def create_current_average_frame(self):
        self.current_average_frame = Frame(self)
        self.current_average_frame.pack(fill=X)

        self.current_average_label = Label(self.current_average_frame, text="Current Average", width=15)
        self.current_average_label.pack(side=LEFT, anchor=W)

        self.current_average_entry = Entry(self.current_average_frame)
        self.current_average_entry.pack(side=LEFT)

    def create_projected_average_frame(self):
        self.projected_average_frame = Frame(self)
        self.projected_average_frame.pack(fill=X, expand=True)

        self.projected_average_label = Label(self.projected_average_frame, text="Projected Average", width=15)
        self.projected_average_label.pack(side=LEFT, expand=True)

        self.projected_average_entry = Entry(self.projected_average_frame, state='readonly')
        self.projected_average_entry.pack(side=LEFT)

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
                print('Symbol:', curr_symbol, self.parent.symbol.get())

            if file_helper.file_exists(curr_symbol.lower()):
                # If user previously saved a file for this symbol, load it!
                self.populate_from_file()
                return

            if not self.current_average_frame:
                self.create_current_average_frame()
        else:
            # No characters remain
            if self.current_average_frame:
                self.current_average_frame.forget()
                self.current_average_frame = None
            if self.projected_average_frame:
                self.projected_average_frame.forget()
                self.projected_average_frame = None

    def delete_symbol_spaces(self):
        space_position = self.symbol_entry.get().find(' ')
        last_char_index = len(self.symbol_entry.get()) - 1

        if space_position != -1:
            if space_position < last_char_index:
                self.symbol_entry.delete(0, END)
            elif space_position is last_char_index:
                self.symbol_entry.delete(last_char_index)

    def populate_from_file(self):
        if not self.current_average_frame:
            self.create_current_average_frame()
        if not self.projected_average_frame:
            self.create_projected_average_frame()
