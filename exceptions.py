class FSMIPR_Exception(Exception):
    """Base exception for all things FSMIPR-related"""

    pass

class EmptyInputException(FSMIPR_Exception):
    """There are no characters left in the input string"""

    pass

class InvalidInputException(FSMIPR_Exception):
    """There is not a defined transition for the given input at the current state"""

    pass
