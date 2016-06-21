"""
UK Postal Code Validator - Assigned by Apostolis for Scurri 

    Write a library that supports validating and formatting post codes for UK.
    The details of which post codes are valid and which are the parts they
    consist of can be found at
    https://en.wikipedia.org/wiki/Postcodes_in_the_United_Kingdom#Validation

    Please, avoid any third-party APIs. The interface that this library
    provides to the callers is your choice.  Btw, ignore
    https://en.wikipedia.org/wiki/Postcodes_in_the_United_Kingdom#Special_cases
    There is no need to waste your time in those extra cases. That is not what
    we want to see.
"""

"""
From the wikipedia page:
    As all formats end with 9AA, the first part of a postcode can easily be
    extracted by ignoring the last three characters
    Areas with only single-digit districts: BR, FY, HA, HD, HG, HR, HS, HX, JE,
    LD, SM, SR, WC, WN, ZE (although WC is always subdivided by a further
    letter, e.g. WC1A).  
    Areas with only double-digit districts: AB, LL, SO.
    Areas with a district '0' (zero): BL, BS, CM, CR, FY, HA, PR, SL, SS (BS is
    the only area to have both a district 0 and a district 10).
    The following central London single-digit districts have been further
    divided by inserting a letter after the digit and before the space: EC1-EC4
    (but not EC50), SW1, W1, WC1, WC2, and part of E1 (E1W), N1 (N1C and N1P),
    NW1 (NW1W) and SE1 (SE1P).
"""

import re

# first part is the outward code (varies greatly)
# The letters QVX are not used in the first position.
first =    'ABCDEFGHIJKLMNOPRSTUWYZ'
# The letters IJZ are not used in the second position.
second =    'ABCDEFGHKLMNOPQRSTUVWXY'
# The only letters to appear in the third position are ABCDEFGHJKPSTUW when the
# structure starts with A9A.
third =    'ABCDEFGHJKSTUW' 
# The only letters to appear in the fourth position are ABEHMNPRVWXY when the
# structure starts with AA9A.
fourth =    'ABEHMNPRVWXY'

def outer_is_valid(outercode):
    valid = False
    if re.match('[%s][1-9]$' % (first), outercode): valid = True
    if re.match('[%s][1-9]\d$' % (first), outercode): valid = True
    if re.match('[%s][%s]\d$' % (first, second), outercode): valid = True
    if re.match('[%s][%s][1-9]\d$' % (first, second), outercode): valid = True
    if re.match('[%s][1-9][%s]$' % (first, third), outercode): valid = True
    if re.match('[%s][%s][1-9][%s]$' % (first, second, fourth), outercode): valid = True
    return valid


# second part is the inward code; 
## inward code is exactly 3 alphanumeric chars
## postcode sector followed by postcode unit
## The final two letters do not use the letters CIKMOV, so as not to resemble
## digits or each other when hand-written.
inward = 'ABDEFGHJLNPQRSTUWXYZ'
def inner_is_valid(innercode):
    if re.match('\d[%s][%s]$' % (inward, inward), innercode):
        return True

# Because I'm thinking of this as a library, best to return a result in every
# case that gives the validation result. Decided to extend http 406 for the errors.
RESULT_CODES = { 
    'valid': (0, 'Post Code is Valid'),
    'length': (4061, 'Length is less than 6 or more than 8 characters'),
    'nospace': (4062, 'String missing space character'),
    'nonchar': (4063, 'The inner code is not valid'),
    'outerbad': (4064, 'The outer code is not valid'),
    'innerbad': (4065, 'The inner code is not valid'),
}


def validate(postalcode):
    """Validate a UK Postal Code aiming for the fastest exits.
    """
    if not isinstance(postalcode, basestring):
        return RESULT_CODES['nonchar']
    postalcode = postalcode.strip()
    # length 6 to 8 characters including the space
    if not len(postalcode) in (6, 7, 8):    # could say 'range(6,9)'... less clear
        return RESULT_CODES['length']
    # contains a single space (shortcut, testing that 'split' returns two parts)
    code_parts = postalcode.split()
    if len(code_parts) != 2:
        return RESULT_CODES['nospace']
    outercode, innercode = code_parts
    if not outer_is_valid(outercode):
        return RESULT_CODES['outerbad']
    if not inner_is_valid(innercode):
        return RESULT_CODES['innerbad']

    return RESULT_CODES['valid']


if __name__ == '__main__':
    """ To test, run:  python ukpostalcodevalidator.py EC1A 1BB
        Obvious extension, depending on need, would be to flesh out an
        extensive command line handler with getopts to allow for checking all
        of a file and sending exceptions to a file, perhaps splitting valid and
        invalid codes into separate files."""

    import sys
    postalcode = ' '.join(sys.argv[1:])
    result = validate(postalcode)
    print "result: %d, explanation: %s" % result
