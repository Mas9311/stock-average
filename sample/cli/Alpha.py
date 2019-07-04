from .TextBaseClass import TextBaseClass


class Alpha(TextBaseClass):
    def __init__(self, message):
        super().__init__(message)
        self.valid_chars = [('a', 'z'), ('A', 'Z')]
