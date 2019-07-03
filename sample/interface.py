from tkinter import *
from sample import stock_average
from sample.frames.Alpha import Alpha
from sample.frames.Numeric import Numeric, Currency
from sample.frames.TitleBar import TitleBar
from sample.frames.Radio import Radio


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
                'create': self._create_title_bar_frame,
                'frame_var': self.title_bar_frame,
                'label': 'Title Bar',
                'options': [('×', 'ne')],  # ?: ('Options', 'nw')
            },
            {  # Symbol Frame
                'create': self._create_alpha_frame,
                'description': 'Enter the ticker symbol.',
                'frame_var': self.symbol_frame,
                'index': 1,
                'label': 'Symbol',
                'StringVar': self.symbol_string,
            },
            {  # Asset Type Frame
                'create': self._create_radio_frame,
                'frame_var': self.asset_type_frame,
                'index': 2,
                'label': 'Asset Type',
                'options': ['stock', 'cryptocurrency'],
                'StringVar': self.asset_type_string,
            },
            {  # Quantity Frame
                'create': self._create_numeric_frame,
                'description': 'Enter the # of shares you own.',
                'frame_var': self.quantity_frame,
                'index': 3,
                'label': 'Quantity',
                'StringVar': self.quantity_string,
            },
            {  # Current Average Frame
                'create': self._create_currency_frame,
                'description': 'Enter your current average.',
                'frame_var': self.current_average_frame,
                'index': 4,
                'label': 'Current Average',
                'StringVar': self.current_average_string,
            },
            {  # Current Price Frame
                'create': self._create_currency_frame,
                'description': 'Enter the current market price.',
                'frame_var': self.current_price_frame,
                'index': 5,
                'label': 'Current Price',
                'StringVar': self.current_price_string,
            },
            {  # Potential Average Frame
                'create': self._create_currency_frame,
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

    def _create_title_bar_frame(self, index):
        return TitleBar(self, index)

    def _create_alpha_frame(self, index):
        return Alpha(self, index)

    def _create_radio_frame(self, index):
        return Radio(self, index)

    def _create_numeric_frame(self, index):
        return Numeric(self, index)

    def _create_currency_frame(self, index):
        return Currency(self, index)

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

    @staticmethod
    def is_char_printable(char):
        """Returns True if the character is {[azAZ09] || punctuation}.
        Returns False if the character is a meta key"""
        return len(repr(char)) is 3 or char == '\\'

    def is_char_valid(self, char, valid_chars):
        if self.is_char_printable(char):
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
