def simple_error_compare(new_error, old_error):
    """
    Returns True if symbol/item should not be considered
    """
    return new_error >= old_error

def simple_limit_compare(new_error, error_limit):
    """
    Returns True if symbol/item should not be considered
    """
    return new_error > error_limit
