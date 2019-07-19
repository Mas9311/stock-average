from tkinter import *
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from sample.classes.Radio import GuiRadio
from sample.format import Price

matplotlib.use("TkAgg")


class Transform(GuiRadio):
    """This class will Transform the display of the frame based on which button is selected.
    If 'T-Chart' is selected, print the Potential Averages as a list of (x, y) coordinates.
    If 'Graph' is selected, display a graph of the (x, y) coordinates."""
    def __init__(self, parent, index):
        super().__init__(parent, index)
        self.verbose = False
        self.scale_frame = None
        self.display_frame = None

        self.create_widgets()

    def bind_radio_frame(self):
        pass

    def create_widgets(self):
        """GuiRadio already create_widgets(), so no need to re-create.
        Selects the first button (intentionally) by default."""
        self.buttons[0].select()
        self.update()

    def create_scale(self):
        self.destroy_scale()
        self.scale_frame = ScaleFrame(self)

    def create_display_frame(self):
        self.destroy_display_frame()
        if self.string_var.get() == self.parent.get(self.index, 'options')[0]:
            self.display_frame = TChart(self)
        elif self.string_var.get() == self.parent.get(self.index, 'options')[1]:
            self.display_frame = Graph(self)

    def destroy_frame(self):
        self.destroy_scale()
        self.destroy_display_frame()
        super().destroy_frame()

    def destroy_scale(self):
        if self.scale_frame:
            self.scale_frame.destroy()
            self.scale_frame = None
            self.parent.resize_frame()

    def destroy_display_frame(self):
        if self.display_frame:
            self.display_frame.destroy()
            self.display_frame = None
            self.parent.resize_frame()

    def select(self, value):
        self.string_var.set(value)
        if not self.string_var.get():
            self.destroy_display_frame()
            self.deselect_buttons()
            self.parent.resize_frame()
        super().select(value)

    def update(self):
        self.create_scale()
        self.create_display_frame()


class ScaleFrame(Frame):
    def __init__(self, parent):
        self.gui = parent.parent
        Frame.__init__(self, master=self.gui)
        self.parent = parent
        self.pack(expand=True, fill=BOTH)

        self.label = None
        self.amount_per = StringVar(name='amount_per')
        self.amount_entry = None
        self.type_of_label = None
        self.cost_per = StringVar(name='cost_per')
        self.cost_entry = None

        self.create_widgets()

    def create_widgets(self):
        self.create_label()
        self.create_amount_entry()
        self.create_type_of_label()
        self.create_cost_entry()
        self.update()

    def create_label(self):
        self.label = Label(self, text='Increments of')
        self.label.grid(row=0, column=0)

    def create_amount_entry(self):
        self.amount_entry = Entry(self, textvariable=self.amount_per, borderwidth=0, width=3, state='readonly')
        self.amount_entry.grid(row=0, column=1)

    def create_type_of_label(self):
        self.type_of_label = Label(self, text='', borderwidth=0)
        self.type_of_label.grid(row=0, column=2)

    def create_cost_entry(self):
        self.cost_entry = Entry(self, textvariable=self.cost_per, borderwidth=0, width=6, state='readonly')
        self.cost_entry.grid(row=0, column=3)

    def update(self):
        self.update_amount_per()
        self.update_type_of()
        self.update_cost_per()

    def update_amount_per(self):
        key = 'amount_per'
        if key in self.gui.arg_dict.keys() and self.gui.arg_dict[key]:
            self.amount_entry.configure(state=NORMAL)
            self.amount_per.set(round(self.gui.arg_dict[key], 4))
            self.amount_entry.configure(state='readonly', width=len(self.amount_per.get()))

    def update_cost_per(self):
        key = 'cost_per'
        if key in self.gui.arg_dict.keys() and self.gui.arg_dict[key]:
            self.cost_entry.configure(state=NORMAL)
            self.cost_per.set(Price(self.gui.arg_dict[key]))
            self.cost_entry.configure(state='readonly', width=len(self.cost_per.get()))

    def update_type_of(self):
        type_of_text = 'share' if self.gui.arg_dict['asset_type'] == 'stock' else 'coin'
        if self.amount_per.get():
            type_of_text += '' if float(self.amount_per.get()) == 1.0 else 's'
        type_of_text += ' at'
        self.type_of_label.configure(text=type_of_text)


class TChart(Frame):
    def __init__(self, parent):
        self.gui = parent.parent
        Frame.__init__(self, master=self.gui)
        self.pack(side=LEFT)

        self.pa_key = 'potential_average'
        self.create_entries()

    def create_entries(self):
        if self.ready_to_populate():
            self.create_headers()
            self.populate_entries()

    def ready_to_populate(self):
        return self.pa_key in self.gui.arg_dict.keys() and self.gui.arg_dict[self.pa_key]

    def create_headers(self):
        keys = ['Additional Cost', 'Potential Average']
        for i, text in zip(range(len(keys)), keys):
            entry = Entry(self)
            entry.grid(row=0, column=i)
            entry.insert(0, text)
            entry.configure(state='readonly')

    def populate_entries(self):
        if self.pa_key in self.gui.arg_dict.keys() and self.gui.arg_dict[self.pa_key]:
            height = len(self.gui.arg_dict['potential_average'])  # length of PotentialAverages

            for i in range(0, height):
                potential_average = self.gui.arg_dict['potential_average'][i]
                for col, data in enumerate(potential_average.get_coordinates()):
                    entry = Entry(self)
                    entry.grid(row=i + 1, column=col)
                    entry.insert(0, Price(data))
            self.gui.resize_frame()
        else:
            print('not populated, because not calculated')


class Graph(Frame):
    def __init__(self, parent):
        self.gui = parent.parent
        Frame.__init__(self, master=self.gui)
        self.pack(side=LEFT)

        self.canvas = None
        self.figure = None
        self.subplot = None
        self.x_axis = None
        self.y_axis = None

        self.y_max = None
        self.y_min = None
        self.x_max = None
        self.x_min = None
        self.y_offset = None
        self.x_offset = None

        self.create_entries()

    def create_entries(self):
        if not self.gui.arg_dict['potential_average']:
            return

        self.create_subplot()
        self.set_axes()
        self.set_axes_offset()
        self.set_subplot_axes()

        self.set_y_axis_ticks()
        self.set_x_axis_ticks()

        self.plot_graph()

    def create_subplot(self):
        self.figure = Figure(figsize=(4, 3), dpi=100)
        self.subplot = self.figure.add_subplot(111)

    def set_axes(self):
        self.y_axis = []
        self.x_axis = []

        for pa in self.gui.arg_dict['potential_average']:
            x, y = pa.get_coordinates()
            self.x_axis.append(round(x, 2))
            self.y_axis.append(round(y, 2))

        self.y_min = min(self.y_axis)
        self.y_max = max(self.y_axis)
        self.x_min = min(self.x_axis)
        self.x_max = max(self.x_axis)

    def set_axes_offset(self):
        self.y_offset = abs(self.y_axis[1] - self.y_axis[0]) / 10
        self.x_offset = abs(self.x_axis[1] - self.x_axis[0]) / 5

    def set_subplot_axes(self):
        self.subplot.set_ylabel('Potential Average')
        self.subplot.set_xlabel('Additional Cost')
        self.subplot.set_ylim((self.y_min - self.y_offset, self.y_max + self.y_offset))
        self.subplot.set_xlim((self.x_min - self.x_offset, self.x_max + self.x_offset))

    def set_y_axis_ticks(self):
        if self.y_max - self.y_min <= .20:
            # if the scale is less than 20 cents, manually set the y_axis ticks in pennies.
            y_difference = (self.y_max - self.y_min) // 0.01
            y_ticks = [round(self.y_min + (0.01 * l), 2) for l in range(-1, int(y_difference + 2))]
            self.subplot.set_yticks(y_ticks)
            self.subplot.set_yticklabels(y_ticks, fontsize=7)
        # else: allow matplotlib to generate and place the y_axis ticks.

    def set_x_axis_ticks(self):
        self.subplot.set_xticks(self.x_axis)

        if self.x_axis[-1] < 100:
            # if the x_axis labels will not overlap => keep labels horizontal
            self.subplot.set_xticklabels(self.x_axis, fontsize=7)
        else:
            # else: the x_axis labels would overlap => rotate the labels
            self.subplot.set_xticklabels(self.x_axis, fontsize=7, rotation=23, ha='right')

    def plot_graph(self):
        self.subplot.grid(True)
        x_axis = [-self.x_axis[1]] + self.x_axis
        y_axis = [self.gui.arg_dict['potential_average'][0].get_coordinates()[1]] + self.y_axis
        self.subplot.plot(x_axis, y_axis)

        self.canvas = FigureCanvasTkAgg(figure=self.figure, master=self)
        self.canvas.draw()
        self.figure.tight_layout()
        self.canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=True)
        self.gui.resize_frame()
        # TODO: cursor is extracted from its current Frame and placed within Figure...
