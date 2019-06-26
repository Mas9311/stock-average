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
        self.pack(fill=BOTH, expand=True)
        self.root = parent
        self.root.configure(background='black', bd=0, width=500)

        self.symbol = StringVar()

        self.close = None
        self.main_frame = None
        self.create_widgets()

    def _close(self):
        self.root.destroy()

    def create_widgets(self):
        self.close = Button(self, highlightthickness=0, text='×', command=self._close,
                            activebackground='#444444', activeforeground='#cccccc')
        self.close.pack(side=TOP, anchor=NE)
        self.main_frame = Main(self)


class Main(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.pack(fill=BOTH, expand=True)
        self.root = parent

        self.symbol_frame = None
        self.symbol_label = None
        self.symbol_entry = None
        self.symbol_description = 'NYSE symbol'
        self.symbol_focused = False
        self.create_symbol_frame()

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

        self.symbol_entry = Entry(self.symbol_frame, textvariable=self.root.symbol)
        self.symbol_entry.insert(0, self.symbol_description)
        self.symbol_entry.bind('<Enter>', self.symbol_entry_entered)
        self.symbol_entry.bind('<FocusIn>', self.symbol_entry_focused)
        self.symbol_entry.bind('<FocusOut>', self.symbol_entry_focused)
        self.symbol_entry.bind('<Leave>', self.symbol_entry_left)
        self.symbol_entry.bind('<KeyRelease>', self.symbol_entry_changed)
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

        self.projected_average_entry = Entry(self.projected_average_frame)
        self.projected_average_entry.pack(side=LEFT)

    def symbol_entry_entered(self, _):
        if self.root.symbol.get() == self.symbol_description:
            self.symbol_entry.delete(0, END)

    def symbol_entry_left(self, _):
        if not self.root.symbol.get() and not self.symbol_focused:
            self.symbol_entry.insert(0, self.symbol_description)

    def symbol_entry_focused(self, _):
        self.symbol_focused = not self.symbol_focused
        if not self.symbol_focused and not self.root.symbol.get():
            self.symbol_entry.insert(0, self.symbol_description)

    def symbol_entry_changed(self, _):
        # if event.keysym not in ['BackSpace', 'Delete']:
        #     if self.root.symbol.get()[:-1] == self.symbol_description:
        #         self.symbol_entry.delete(0, END)

            curr_symbol = self.root.symbol.get()

            if curr_symbol:
                if file_helper.file_exists(self.root.symbol.get()):
                    if not self.current_average_frame and not self.projected_average_frame:
                        self.create_current_average_frame()
                        self.create_projected_average_frame()
                else:
                    pass
