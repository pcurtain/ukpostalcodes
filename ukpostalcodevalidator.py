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

# second part is the inward code; 
## inward code is exactly 3 alphanumeric chars
## postcode sector followed by postcode unit
## The final two letters do not use the letters CIKMOV, so as not to resemble
## digits or each other when hand-written.
inward = 'ABDEFGHJLNPQRSTUWXYZ'

# Because I'm thinking of this as a library, best to return a result in every
# case that gives the validation result. Decided to extend http 406 for the errors.
RESULT_CODES = { 
    'valid': (0, 'Post Code is Valid'),
    'length': (4061, 'Length is less than 6 or more than 8 characters'),
    'nospace': (4062, 'String missing space character'),
    'badouter': (4063, 'The outer code is not valid'),
    'badinner': (4064, 'The inner code is not valid'),
    'nonchar': (4065, 'The inner code is not valid'),
}

def validate(postalcode):
    """Validate a UK Postal Code aiming for the fastest exits.
    """
    # length 6 to 8 characters including the space
    if not isinstance(postalcode, basestring):
        return RESULT_CODES['nonchar']
    if not len(postalcode) in (6, 7, 8):    # could say 'range(6,9)'... less clear
        return RESULT_CODES['length']
    # contains a single space
