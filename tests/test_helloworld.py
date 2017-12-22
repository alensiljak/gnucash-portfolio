""" 
The most basic example of unit tests with Python.
Ref: http://pythontesting.net/framework/pytest/pytest-introduction/
"""

# unit test example

import unittest

class TestClass(unittest.TestCase):
    """ Test class for unittest """

    def test_multiplication(self):
        """ Demo for unittest """
        self.assertEqual(3 * 4, 12)

# and the pytest version:

def test_multiplication_pytest():
    """ The same test with pytest """
    assert 3 * 4 == 12
