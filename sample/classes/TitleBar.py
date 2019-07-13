from tkinter import *


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

        for button_type, anchor_location in self.parent.get(self.index, 'options'):
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
