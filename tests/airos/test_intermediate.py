import unittest

from netjsonconfig.backends.airos.airos import intermediate_to_list


class TestIntermediateConversion(unittest.TestCase):

    def test_dict_conversion(self):
        i = [{'spam': {'eggs': 'spam and eggs'}}]

        o = [{'spam.eggs': 'spam and eggs'}]

        self.assertEqual(intermediate_to_list(i), o)

    def test_list_conversion(self):
        i = [{'kings': [{'henry': 'the first'}, {'jacob': 'the second'}]}]

        o = [{'kings.1.henry': 'the first', 'kings.2.jacob': 'the second'}]

        self.assertEqual(intermediate_to_list(i), o)

    def test_multiple_conversion(self):
        i = [
                {'snakes': {'loved': 'yes'}},
                {'dogs': {'loved': 'yes'}},
            ]

        o = [
                {'snakes.loved': 'yes'},
                {'dogs.loved': 'yes'},
            ]

        self.assertEqual(intermediate_to_list(i), o)
