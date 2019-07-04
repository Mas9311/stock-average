from tkinter import *
from sample import file_helper
from sample.gui.EntryBaseClass import EntryBaseClass


class Alpha(EntryBaseClass):
    """The only characters that will remain in this Frame's Entry textbox are Alpha letters: {A, B, ..., Z}.
    Feel free to type a lowercase letter, because the text is replaced with CAPITAL letters.
    All other printable characters {'c', '1', '~', ' ', ...} will be deleted in-place.
    Meta keys {Shift, Tab, Left, Control, Escape, ...} will not alter the Entry's textbox."""
    def __init__(self, parent, index):
        super().__init__(parent, index)
        self.last_text_entered = None
        self.valid_chars = [('a', 'z'), ('A', 'Z')]

        self.entry.bind('<KeyRelease>', self.alpha_entry_key_released)  # key pressed => key released

    def _rewrite_in_all_caps(self):
        """If we received a valid letter [azAZ]: clear the entry text and re-write in ALL CAPS"""
        curr_symbol = self.entry.get().upper()
        cursor_pos = self.entry.index(INSERT)
        self.entry.delete(0, END)
        self.entry.insert(0, curr_symbol)
        self.entry.icursor(cursor_pos)

    def alpha_entry_key_released(self, event):
        """Called every time a key on the keyboard is released while the cursor is in the Alpha Entry's textbox.
        If the key pressed is a printable character: check if it a valid character.
         If it is a valid character [azAZ]: convert the Entry's text to ALL CAPS.
          If the length of the Entry's text is greater than 4: truncate the last character.
         Else the char is a digit or punctuation: delete it in place. (doesn't move the cursor)
        If the textbox's last character is a space, delete it.
        If the textbox contains a space anywhere else: clear all text. (the description is present)
        If no characters currently remain in the textbox: destroy all gui after this Frame.
        Else the is at least one character: check if the file exists"""
        if self.parent.is_char_printable(event.char):
            # Received a printable character: {alpha || numeric || punctuation}
            if self.parent.is_char_valid(event.char, self.valid_chars):
                # Received valid input: [azAZ]
                self._rewrite_in_all_caps()  # [AZ]

                if len(self.entry.get()) <= 4:
                    print('Symbol:', self.entry.get())
                else:
                    # Length is >= 5, ∴ delete the last letter
                    self._delete_character(4, to_i=END)
            else:
                # Received invalid input: {numeric || punctuation}
                if not self._delete_spaces():
                    self._delete_character(INSERT, -1)

        if not self._destroyed_for_empty_input():
            # If at least one character remains
            if file_helper.file_exists(self.entry.get().lower()):
                # If user previously saved a file for this symbol, load it!
                self.parent.populate_from_file()
            else:
                # Else the file does not exist
                if self.last_text_entered != self.entry.get():
                    # If the symbol has changed: destroy all gui below this Frame
                    self.parent.destroy_all_frames_after(self.index)
                self.parent.create_next_frame(self.index + 1)

        self.last_text_entered = self.entry.get()
