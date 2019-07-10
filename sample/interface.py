from tkinter import *
from math import sqrt
from sample import file_helper, menu, parameters
from sample.average import PotentialAverage
from sample.format import Price
from sample.cli.Alpha import CliAlpha
from sample.cli.Radio import Radio as cli_Radio
from sample.cli.Numeric import Numeric as cli_Numeric, Currency as cli_Currency
from sample.gui.TitleBar import TitleBar
from sample.gui.Alpha import Alpha as gui_Alpha
from sample.gui.Radio import Radio as gui_Radio
from sample.gui.Numeric import Numeric as gui_Numeric, Currency as gui_Currency


def run():
    arg_dict = parameters.retrieve_parameters()
    if arg_dict['interface']:
        GUI(Tk(), arg_dict)
    else:
        CLI(arg_dict)


class CLI:
    def __init__(self, arg_dict):
        self.arg_dict = arg_dict

        self.symbol = None
        self.asset_type = None
        self.quantity = None
        self.current_average = None
        self.market_price = None
        self.allotted_money = None
        self.potential_averages = None  # list of PotentialAverage instances

        self.create_variables()
        self.run_cli()

    def create_variables(self):
        self.symbol = CliAlpha(self, 'symbol', 'Enter the ticker symbol')
        if not self.get('symbol'):
            self.symbol.retrieve_input()
        self.asset_type = cli_Radio(self, 'asset_type', parameters.asset_type_choices())
        self.quantity = cli_Numeric(self, 'quantity', 'Enter the # of shares you own')
        self.current_average = cli_Currency(self, 'current_average', 'Enter your current average')
        self.market_price = cli_Currency(self, 'market_price', 'Enter the current market price')
        self.allotted_money = cli_Currency(self, 'allotted_money', 'Enter the amount you willing to spend today')

    def run_cli(self):
        if not file_helper.file_exists(self.get('symbol')):
            self.ask_for_variable_input()
        else:
            self.arg_dict, success = file_helper.import_from_file(self.get('symbol'), self.arg_dict)
            if not success:
                self.ask_for_variable_input()
        print()

        # save data to the file (overwrites any existing data)
        file_helper.export_to_file(self.arg_dict)

        # ask user if they wish to update an values
        menu.update(self)

        # ask user for how much they are willing to spend today
        self.retrieve_allotted_money()
        self.potential_averages = []
        self.calculate_potentials()

        # prints potential averages incrementally based on the allotted_money given
        for potential_average in self.potential_averages:
            print(potential_average)

    def ask_for_variable_input(self):
        print(f'The {self.symbol} file is not in the symbols folder.\n')
        self.asset_type.retrieve_input()
        self.quantity.retrieve_input()
        self.current_average.retrieve_input()
        if not self.get('market_price'):
            # if user did not pass market price in execution arguments
            self.market_price.retrieve_input()

    def calculate_potentials(self):
        """The user may not want to spend all of the money they designated,
        so this will calculate the potential averages incrementally"""
        if self.get('asset_type') == 'stock':
            # set number of iteration using integer division: "How many shares you can buy"
            iterations = int(self.get('allotted_money') // self.get('market_price'))
            cost_per = self.get('market_price')
            print('You can buy', iterations, 'shares of', self.symbol, 'at', Price(cost_per))
        else:
            iterations = int(sqrt(self.get('allotted_money')))
            cost_per = self.get('allotted_money') / iterations

        for curr_iter in range(iterations):
            self.potential_averages.append(PotentialAverage(self, curr_iter + 1, cost_per))

    def retrieve_allotted_money(self):
        while True:
            self.allotted_money.reset_and_ask_question()
            if self.get('allotted_money') >= 1.00:
                # user has designated more than a dollar
                if self.get('asset_type') == 'stock':
                    # this symbol is a stock
                    if self.get('allotted_money') > self.get('market_price'):
                        # user can buy one or more shares (in multiples of integers)
                        return
                    else:
                        # cannot buy a single share with the allotted money
                        print(f'Invalid: Allotted money must be greater than {self.market_price}.\n')
                else:
                    # this symbol is a crypto: user can buy a fraction of a crypto coin.
                    return
            else:
                print('Invalid: Allotted money must be greater than $0.99.\n')

    def set(self, key, value):
        self.arg_dict[key] = value

    def get(self, key):
        return self.arg_dict[key] if key in self.arg_dict else ''

    def get_type(self):
        s = ''
        try:
            if float(self.get('quantity')) != 1:
                s = 's'
        except TypeError:
            pass
        return f'share{s}' if self.get('asset_type') == 'stock' else f'coin{s}'

    def __str__(self):
        """Returns the stock in string format."""
        return (f'{self.symbol}, the {self.asset_type}:\n'
                f'  You previously purchased {self.quantity} {self.get_type()} of {self.symbol}.\n'
                f'  Your current average of {self.symbol} is {self.current_average}.\n'
                f'  {self.symbol}\'s current market price is {self.market_price}.\n')


class GUI(Frame):
    def __init__(self, parent, arg_dict):
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
        self.root.mainloop()

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
