import logging
import functools

def trycatch(func):
    """
    Decorator for try-catch-finally block
    Usage:
        @trycatch
        def func(*args, **kwargs):
            # Function body
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            retVal = False
            retVal = func(*args, **kwargs)
        except Exception as e:
            logging.exception("Exception Occurred {exception}".format(e))
        finally:
            return retVal
    return wrapper
