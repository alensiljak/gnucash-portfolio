"""
A DTO class for data transfer.
"""
class Messenger:
    """
    Class used as a dictionary to pass data. A typical DTO.
    Properties are initialized in constructor, on creation of the object.
    http://python-3-patterns-idioms-test.readthedocs.io/en/latest/Messenger.html
    """
    def __init__(self, **kwargs):
        self.__dict__ = kwargs
