class DSL_Error(Exception):
    """Base exception for FSMIPR DSL"""

    pass


class MalformedCommandError(DSL_Error):
    """The command entered was malformed and cannot be read"""

    pass


class DoesNotExistError(DSL_Error):
    """Someone attempted to make reference to an object that does not exist in the context"""

    pass
