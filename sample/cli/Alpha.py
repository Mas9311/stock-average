from .TextBaseClass import TextBaseClass


class Alpha(TextBaseClass):
    def __init__(self, parent, message):
        super().__init__(parent, message)
        self.valid_chars = [('a', 'z'), ('A', 'Z')]
