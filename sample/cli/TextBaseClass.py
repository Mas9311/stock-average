class TextBaseClass:
    def __init__(self, parent, message):
        self.parent = parent  # CLI instance
        self.message = message
        self.user_input = None  # unverified input
        self.input = None
        self.valid_chars = None
        self.intro_char = ''

    def retrieve_input(self):
        while True:
            self.user_input = input(f'{self.message}.\n> {self.intro_char}').strip().lower()
            if self.input_is_valid():
                self.input = self.user_input
                return

    def input_is_valid(self):
        if not self.input_in_valid_length():
            print()
            return False

        for input_index in range(len(self.user_input)):
            input_char = self.user_input[input_index]
            is_valid = True

            for valid in self.valid_chars:
                if isinstance(valid, tuple):
                    if valid[0] <= input_char <= valid[1]:
                        # this character is valid
                        is_valid = True
                        break
                    else:
                        is_valid = False

                if isinstance(valid, str):
                    if input_char == valid:
                        # this character is valid
                        is_valid = True
                        break
                    else:
                        is_valid = False

            if not is_valid:
                print('Invalid:', repr(input_char), 'is an invalid character.\n')
                return False

                # else: continue checking

        # user_input passed all invalid checks ∴ char is valid
        print()
        return True

    def input_in_valid_length(self):
        if len(self.user_input) is 0:
            print('Invalid: input is not long enough.')
            return False
        return True
