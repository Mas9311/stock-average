from tkinter import *
from sample.classes.Radio import GuiRadio
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from sample.format import Price

matplotlib.use("TkAgg")


class Transform(GuiRadio):
    """This class will Transform the display of the frame based on which button is selected.
    If 'T-Chart' is selected, print the Potential Averages as a list of (x, y) coordinates.
    If 'Graph' is selected, display a graph of the (x, y) coordinates."""
    def __init__(self, parent, index):
        super().__init__(parent, index)
        self.verbose = False
        self.inner_frame = None

    def create_widgets(self):
        """GuiRadio already create_widgets(), so no need to re-create.
        Selects the first button (intentionally) by default."""
        self.buttons[0].select()
        self.create_inner_frame()

    def create_inner_frame(self):
        self.destroy_inner_frame()
        if self.string_var.get() == self.parent.get(self.index, 'options')[0]:
            self.inner_frame = TChart(self)
        elif self.string_var.get() == self.parent.get(self.index, 'options')[1]:
            self.inner_frame = Graph(self)

    def destroy_frame(self):
        self.destroy_inner_frame()
        super().destroy_frame()

    def destroy_inner_frame(self):
        if self.inner_frame:
            self.inner_frame.destroy()
            self.inner_frame = None

    def select(self, value):
        self.string_var.set(value)
        super().select(value)
        if not self.string_var.get():
            self.destroy_inner_frame()
            self.deselect_buttons()
            self.parent.resize_frame()
        else:
            # self.buttons[self.parent.get(self.index, 'options').index(value)].select()
            self.parent.calculate_potential_averages()
            self.create_inner_frame()


class TChart(Frame):
    def __init__(self, parent):
        self.gui = parent.parent
        Frame.__init__(self, master=self.gui)
        self.pack(side=BOTTOM)

        self.create_entries()

    def create_entries(self):
        height = len(self.gui.arg_dict['potential_average'])  # length of PotentialAverages
        a = Entry(self)
        a.grid(row=0, column=0)
        a.insert(0, 'Additional Cost')
        a.configure(state='readonly')

        a = Entry(self)
        a.grid(row=0, column=1)
        a.insert(0, 'Potential Average')
        a.configure(state='readonly')

        for i in range(height):
            x, y = self.gui.arg_dict['potential_average'][i].get_coordinates()
            b = Entry(self)
            b.grid(row=i + 1, column=0)
            b.insert(0, Price(x))
            c = Entry(self)
            c.grid(row=i + 1, column=1)
            c.insert(0, Price(y))
        self.gui.resize_frame()


class Graph(Frame):
    def __init__(self, parent):
        self.gui = parent.parent
        Frame.__init__(self, master=self.gui)
        self.pack(side=BOTTOM)
        self.canvas = None

        self.create_entries()

    def create_entries(self):
        f = Figure(figsize=(4, 2))
        a = f.add_subplot(111)
        x_axis = []
        y_axis = []
        for pa in self.gui.arg_dict['potential_average']:
            x, y = pa.get_coordinates()
            x_axis.append(x)
            y_axis.append(y)
        a.plot(x_axis, y_axis)

        self.canvas = FigureCanvasTkAgg(f, self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=BOTTOM, fill=BOTH, expand=True)

        self.gui.resize_frame()

