from tkinter import *
from math import sqrt
from sample import file_helper, menu, parameters
from sample.average import PotentialAverage
from sample.format import Price
from sample.classes.Alpha import CliAlpha, GuiAlpha
from sample.classes.Radio import CliRadio, GuiRadio
from sample.classes.Numeric import CliCurrency, CliNumeric, GuiCurrency, GuiNumeric
from sample.classes.TitleBar import TitleBar
from sample.classes.Transform import Transform


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
        self.define_variables()
        self.run_cli()

    def create_variables(self):
        self.symbol = CliAlpha(self, 'symbol', 'Enter the ticker symbol')
        if not self.get('symbol'):
            self.symbol.retrieve_input()
        self.asset_type = CliRadio(self, 'asset_type', parameters.asset_type_choices())
        self.quantity = CliNumeric(self, 'quantity', 'Enter the # of shares you own')
        self.current_average = CliCurrency(self, 'current_average', 'Enter your current average')
        self.market_price = CliCurrency(self, 'market_price', 'Enter the current market price')
        self.allotted_money = CliCurrency(self, 'allotted_money', 'Enter the amount you willing to spend today')

    def run_cli(self):
        while True:
            # ask user if they wish to update an values
            menu.update(self)

            # ask user for how much they are willing to spend today
            self.retrieve_allotted_money()
            self.potential_averages = []
            self.calculate_potentials()

            # prints potential averages incrementally based on the allotted_money given
            for potential_average in self.potential_averages:
                print(potential_average)
            print()

            if menu.ending_menu(self.get('symbol')) == 'different':
                # user selects to continue the program and choose a different symbol
                self.reset_variables()

    def define_variables(self):
        if not file_helper.file_exists(self.get('symbol')):
            # file does not exist: ask for input one variable at a time
            self.ask_for_variable_input()
        else:
            # file exists, so import the variables and assign them to arg_dict
            self.arg_dict, success = file_helper.import_from_file(self.get('symbol'), self.arg_dict)
            if not success:
                # if the file was invalid format: ask for input one variable at a time
                self.ask_for_variable_input()
        print()

        # save data to the file (overwrites any existing data)
        file_helper.export_to_file(self.arg_dict)

    def reset_variables(self):
        """Erases all relevant variables in the arg_dict dictionary:
        symbol, asset_type, quantity, current_average, market_price"""
        for key in file_helper.file_keys() + ['symbol']:
            # resets the arg_dict values to None
            self.set(key, None)
        self.symbol.retrieve_input()
        self.define_variables()

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

        if iterations > 10:
            # if the potential averages would be a wall of text: scale it down to ~10 potential averages
            scale = int(iterations // 10)
            if 14 < iterations < 20:
                # iterations is between [15, 19] => [7, 9]
                scale = 2

            if scale > 1:
                # if scale is worth calculating (and prevents ZeroDivisionError)
                iterations //= scale
                cost_per *= scale

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

        self.arg_dict = arg_dict

        self._frames = self._create_frames()
        self.focused_frame = 0  # location of the cursor (once user clicks/tabs to an Entry's textbox)

        self._create_gui_widgets()
        self.root.mainloop()

    def _create_frames(self):
        return [
            {  # Title Bar Frame
                'frame_var': None,
                'label': 'Title Bar',
                'options': [('×', 'ne')],
                'type': 'TitleBar',
            },
            {  # Symbol Frame
                'description': 'Enter the ticker symbol.',
                'frame_var': None,
                'index': 1,
                'key': 'symbol',
                'label': 'Symbol',
                'type': 'Alpha',
            },
            {  # Asset Type Frame
                'frame_var': None,
                'index': 2,
                'key': 'asset_type',
                'label': 'Asset Type',
                'options': parameters.asset_type_choices(),
                'type': 'Radio',
            },
            {  # Quantity Frame
                'description': 'Enter the # of shares you own.',
                'frame_var': None,
                'index': 3,
                'key': 'quantity',
                'label': 'Quantity',
                'type': 'Numeric',
            },
            {  # Current Average Frame
                'description': 'Enter your current average.',
                'frame_var': None,
                'index': 4,
                'key': 'current_average',
                'label': 'Current Average',
                'type': 'Currency',
            },
            {  # Market Price Frame
                'description': 'Enter the current market price.',
                'frame_var': None,
                'index': 5,
                'key': 'market_price',
                'label': 'Market Price',
                'type': 'Currency',
            },
            {  # Allotted Money Frame
                'description': 'Enter the amount you willing to spend today.',
                'frame_var': None,
                'index': 6,
                'key': 'allotted_money',
                'label': 'Allotted Money',
                'type': 'Currency',
            },
            {  # Potential Average Frame
                'frame_var': None,
                'index': 7,
                'key': 'potential_average',
                'label': 'Potential Average',
                'options': ['T-Chart', 'Graph'],
                'type': 'Transform',
            }
        ]

    def _create_frame_type(self, index):
        frame_type = self.get(index, 'type')
        if frame_type == 'TitleBar':
            return TitleBar(self, index)
        if frame_type == 'Alpha':
            return GuiAlpha(self, index)
        if frame_type == 'Radio':
            return GuiRadio(self, index)
        if frame_type == 'Numeric':
            return GuiNumeric(self, index)
        if frame_type == 'Currency':
            return GuiCurrency(self, index)
        if frame_type == 'Transform':
            return Transform(self, index)

    def _create_gui_widgets(self):
        self.create_next_frame(0)  # create TitleBar Frame
        self.create_next_frame(1)  # create Alpha 'Symbol' Frame
        if self.arg_dict['symbol']:
            value = self.arg_dict['symbol'].upper()
            if len(value) > 4:
                value = value[:4]
                self.arg_dict['symbol'] = value.lower()
            # self.symbol_string.set(value)
            self.create_next_frame(2)  # Create Radio 'Asset Type' Frame
            self.populate_from_file()

    def _resize_frame(self):
        self.root.update_idletasks()
        w = 450 if self.root.winfo_reqwidth() < 450 else self.root.winfo_reqwidth()
        h = self.root.winfo_reqheight()
        self.root.geometry(f'{w}x{h}')

    def create_next_frame(self, next_index):
        """Will create the next frame if:
        1. The next_index has a value (it exists) in the GUI._frames dict
          and
        2. The next_index's Frame has not been already created"""
        if next_index < self.len_frames() and self.get(next_index, 'frame_var') is None:
            self._frames[next_index]['frame_var'] = self._create_frame_type(next_index)
            self._resize_frame()

    def destroy_all_frames_after(self, keep_index):
        for curr_index in range(self.len_frames()):
            if curr_index > keep_index and self.get(curr_index, 'frame_var'):
                self.get(curr_index, 'frame_var').destroy_frame()
        temp_dict = {
            'interface': self.arg_dict['interface'],
            'symbol': self.arg_dict['symbol'],
        }
        for index, key in zip(range(2, keep_index), file_helper.file_keys()):
            if key in self.arg_dict.keys():
                temp_dict[key] = self.arg_dict[key]
        self.arg_dict = temp_dict

    def destroy_frame(self, index):
        """Destroys the Frame (and all nested widgets recursively) at a given index of GUI._frames
        Sets all modified attributes to their original values. See GUI._create_frames()"""
        if self.get(index, 'frame_var'):
            self.get(index, 'frame_var').destroy()  # recursively destroys the Frame and all widgets inside it
            self._frames[index]['frame_var'] = None  # forget the reference, ∴ send to GC
            self._resize_frame()  # resize the frame since this Frame was destroyed
        else:
            print(index, 'has not been created')

    def get(self, index, key):
        """Accessor of the GUI._frames variable"""
        return self._frames[index][key]

    def get_keys(self, index):
        return self._frames[index].keys()

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

    def len_frames(self):
        return len(self._frames)

    def populate_from_file(self):
        """Read data from file, create the Frame, then populate with data"""
        if file_helper.file_exists(self.arg_dict['symbol']):
            self.arg_dict, success = file_helper.import_from_file(self.arg_dict['symbol'], self.arg_dict)
            if success:
                for index in range(1, self.len_frames() - 1):
                    # Create the Frame
                    self.create_next_frame(index)
                    if index <= 5:
                        self.focused_frame = index

                    if index in [1, 3, 4, 5]:
                        # arg_dict has an entry for this Frame
                        key = self.get(index, 'key')

                        if key not in self.arg_dict.keys():
                            break
                        if self.arg_dict[key] is None:
                            print('The file\'s', key, 'value is invalid.')
                            break
                        value = self.arg_dict[self.get(index, 'key')]
                        if isinstance(value, str):
                            value = value.upper()
                        self.get(index, 'frame_var').set_string(value)
                        # intro_char = ''
                        # if self.get(index, 'frame_var').intro_char:
                        #     intro_char = self.get(index, 'frame_var').intro_char
                        # # self.get(index, 'StringVar').set(f'{intro_char}{value}')
                    elif index is 2:
                        # asset_type Radio Frame
                        options = parameters.asset_type_choices()
                        option_text = options[self.arg_dict['asset_type'] != options[0]]
                        # self.get(index, 'frame_var').last_button_selected = option_text
                        self.get(index, 'frame_var').select(option_text)
                # resize the gui root once all the Frames have been created
                self._resize_frame()

    def save_to_file(self):
        if self.focused_frame <= 5:
            valid_entries = True
            for index in [1, 2, 3, 4, 5]:
                if self.get(index, 'frame_var'):
                    if self.get(index, 'frame_var').is_empty():
                        # the Frame is empty: do not save to file
                        valid_entries = False
                        break
                    # else: the Frame is not empty
                else:
                    # The Frame has not been created yet: do not save to file
                    valid_entries = False
                    break

            if valid_entries:
                file_helper.export_to_file(self.arg_dict)
                print(' ', self.arg_dict['symbol'].lower(), 'was written to file.')
