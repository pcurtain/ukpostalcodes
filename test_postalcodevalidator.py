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

        self.bad_first = 'QC1A 1BB' # can't be Q
        self.bad_seconds = 'IJZ'
        self.bad_thirds = 'ILMNOPQRVXYZ'
        self.bad_fourths = 'CDFGIJKLOQSTUZ'

    def test_is_alphanumeric(self):
        code, result = validate(self.not_string)
        self.assertEqual(code, RESULT_CODES['nonchar'][0])
        code, result = validate(self.known_good[0])
        self.assertEqual(code, RESULT_CODES['valid'][0])

    def test_length(self):
        for postalcode in (self.too_long, self.too_short):
            code, result = validate(postalcode)
            self.assertEqual(code, RESULT_CODES['length'][0])

    def test_has_space(self):
        code, result = validate(self.space_missing)
        self.assertEqual(code, RESULT_CODES['nospace'][0])

    def test_inner_invalid(self):
        code, result = validate(self.not_string)
        self.assertEqual(code, RESULT_CODES['nonchar'][0])
        for postalcode in ('EC1A BB9', 'EC1A 9B', 'EC1A B99'):
            code, result = validate(postalcode)
            self.assertEqual(code, RESULT_CODES['innerbad'][0])

    def test_outer_invalid(self):
        # TODO add *more* bad outer codes, 2nd, 3rd and 4th positions
        for postalcode in ('QC1A 1BB', 'E1J 1BB', 'EI1A 1BB', 'EC1I 1BB'):
            code, result = validate(postalcode)
            self.assertEqual(code, RESULT_CODES['outerbad'][0])

    def test_knowns_all_pass(self):
        for postalcode in self.known_good:
            code, result = validate(postalcode)
            self.assertEqual(code, RESULT_CODES['valid'][0])

    
