import unittest
from ukpostalcodevalidator import validate, RESULT_CODES

class PostalCodeValidatorTestCase(unittest.TestCase):
    def setUp(self):

        self.known_good = ('EC1A 1BB', 'W1A 0AX', 'M1 1AE', 'B33 8TH', 'CR2 6XH', 'DN55 1PT')
        self.invented_bad = ('AAW1A 0AX', 'W1A 0', '11M AE11', '11MA 1PT')
        self.not_string = 91100
        self.space_missing = 'EC1A1BB'
        self.too_long = 'EC1A 1BBB'
        self.too_short = 'EC1'

    def test_rejects_number(self):
        code, result = validate(self.not_string)
        self.assertEqual(code, RESULT_CODES['nonchar'])

    def test_has_space(self):
        pass

    def test_inner_is_length_three(self):
        pass

    def test_inner_is_valid(self):
        pass

    def test_rejects_too_long(self):
        pass


