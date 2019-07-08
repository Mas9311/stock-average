from tkinter import *
from math import sqrt
from sample import file_helper, menu
from sample.average import PotentialAverage

from sample.cli.Alpha import Alpha as cli_Alpha
from sample.cli.Radio import Radio as cli_Radio
from sample.cli.Numeric import Numeric as cli_Numeric, Currency as cli_Currency

from sample.gui.TitleBar import TitleBar
from sample.gui.Alpha import Alpha as gui_Alpha
from sample.gui.Radio import Radio as gui_Radio
from sample.gui.Numeric import Numeric as gui_Numeric, Currency as gui_Currency


def run():
#     if parameter['interface'] == 'gui':
#         root = Tk()
#         GUI(root)
#         root.mainloop()
#     else:
        CLI()


class CLI:
    def __init__(self):
        self.symbol = cli_Alpha(self, 'Enter the ticker symbol')
        # if symbol was not passed in parameters
        self.symbol.retrieve_input()
        # else populate from parameters
        self.asset_type = cli_Radio(self, ['stock', 'cryptocurrency'])
        self.quantity = cli_Numeric(self, 'Enter the # of shares you own')
        self.current_average = cli_Currency(self, 'Enter your current average')
        self.current_price = cli_Currency(self, 'Enter the current market price')
        self.allotted_money = cli_Currency(self, 'Enter the amount you willing to spend today')
        self.potential_averages = []  # list of PotentialAverage instances

        self.run_cli()

    def run_cli(self):
        if not file_helper.file_exists(self.get_symbol()):
            print(f'The {self.get_symbol()} file is not in the symbols folder.\n')
            self.asset_type.retrieve_input()
            self.quantity.retrieve_input()
            self.current_average.retrieve_input()
            # if current_price was not passed in parameters
            self.current_price.retrieve_input()
            # else assign to variable
            file_helper.create_new_file(self)
        else:
            file_helper.assign_file_data_to_variables(self)
            # if current_price was passed in parameters: assign to variable
        menu.update(self)
        self.retrieve_allotted_money()
        self.potential_averages = []
        self.calculate_potentials()
        for potential_average in self.potential_averages:
            print(potential_average)

    def calculate_potentials(self):
        """The user may not want to spend all of the money they designated,
        so this will calculate the potential averages incrementally"""
        if self.get_asset_type() == 'stock':
            # set number of iteration using integer division: "How many shares you can buy"
            iterations = self.get_allotted_money() // self.get_current_price()
            cost_per = self.get_current_price() / iterations
            print('You can buy', iterations, 'shares of', self.get_symbol())
        else:
            iterations = int(sqrt(self.get_allotted_money()))
            cost_per = self.get_allotted_money() / iterations

        for curr_iter in range(iterations):
            self.potential_averages.append(PotentialAverage(self, curr_iter + 1, cost_per))

    def retrieve_allotted_money(self):
        while True:
            self.allotted_money.reset_and_ask_question()
            if self.get_allotted_money() >= 1.00:
                # user has designated more than a dollar
                if self.get_asset_type() == 'stock':
                    # this symbol is a stock
                    if self.get_allotted_money() > self.get_current_price():
                        # user can buy one or more shares (in multiples of integers)
                        return
                    else:
                        # cannot buy a single share with the allotted money
                        print(f'Invalid: Allotted money must be greater than {self.current_price}.\n')
                else:
                    # this symbol is a crypto: user can buy a fraction of a crypto coin.
                    return
            else:
                print('Invalid: Allotted money must be greater than $0.99.\n')

    def get_symbol(self):
        return self.symbol.input.upper()

    def get_asset_type(self):
        return self.asset_type.input

    def get_type(self):
        s = ''
        if float(self.get_quantity()) != 1:
            s = 's'
        return f'share{s}' if self.get_asset_type() == 'stock' else f'coin{s}'

    def get_quantity(self):
        return self.quantity.input

    def get_current_average(self):
        return self.current_average.input

    def get_current_price(self):
        return self.current_price.input

    def get_allotted_money(self):
        return float(self.allotted_money.input)

    def __str__(self):
        """Returns the stock in string format."""
        return (f'{self.symbol}, the {self.asset_type}:\n'
                f'\tYou previously purchased {self.quantity} {self.get_type()} of {self.symbol}.\n'
                f'\tYour current average of {self.symbol} is {self.current_average}.\n'
                f'\t{self.symbol}\'s current market price is {self.current_price}.\n')


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
        return gui_Alpha(self, index)

    def _create_radio_frame(self, index):
        return gui_Radio(self, index)

    def _create_numeric_frame(self, index):
        return gui_Numeric(self, index)

    def _create_currency_frame(self, index):
        return gui_Currency(self, index)

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
