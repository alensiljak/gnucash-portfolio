""" Generic models """

class ValidationResult:
    """ The result of validation """
    def __init__(self):
        self.valid = False
        self.message = None
