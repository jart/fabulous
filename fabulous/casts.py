"""A series of functions that provide useful casts from strings into other common objects.

Mainly for usage with input_object in the above package.
"""

from os import path

def yes_no(value):
    """For a yes or no question, returns a boolean.
    """
    if value.lower() in ('yes','y'):
        return True
    if value.lower() in ('no','n'):
        return False
    raise ValueError, "value should be 'yes' or 'no'"


def file(value, **kwarg):
    """value should be a path to file in the filesystem.
    
    returns a file object
    """
    #a bit weird, but I don't want to hard code default values
    try:
        f = open(value, **kwarg)
    except IOError, e:
        raise ValueError, "unable to open %s : %s" % (path.abspath(value), e)
    return f