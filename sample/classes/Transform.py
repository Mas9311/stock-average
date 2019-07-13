from tkinter import *
from sample.classes.Radio import GuiRadio


class Transform(GuiRadio):
    """This class will Transform the display of the frame based on which button is selected.
    If 'T-Chart' is selected, print the Potential Averages as a list of (x, y) coordinates.
    If 'Graph' is selected, display a graph of the (x, y) coordinates."""
    def __init__(self, parent, index):
        super().__init__(parent, index)
        self.display = StringVar()

        self.create_widgets()

    def create_widgets(self):
        """GuiRadio already create_widgets(), so no need to re-create.
        Selects the first button (intentionally) by default."""
        self.buttons[0].select()
