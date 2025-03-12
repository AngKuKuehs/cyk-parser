def simple_error_compare(new_error, old_error):
    """
    Returns True if symbol/item should not be considered
    """
    if old_error == None:
        return False
    return new_error >= old_error

def simple_limit_compare(new_error, error_limit):
    """
    Returns True if symbol/item should not be considered
    """
    return new_error > error_limit

def ord_error_compare(new_error, old_error):
    """
    Returns True if symbol/item should not be considered
    """
    if old_error == None:
        return False
    if new_error[0] == old_error[0]:
        return new_error[1] >= old_error[1]
    return new_error[0] >= old_error[0]

def ord_limit_compare(new_error, error_limit):
    """
    Returns True if symbol/item should not be considered
    """
    if new_error[0] == error_limit[0]:
        return new_error[1] > error_limit[1]
    return new_error[0] > error_limit[0]