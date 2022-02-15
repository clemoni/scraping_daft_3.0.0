import functools


def try_action(*, fn):
    """Encapuslts a function into a Try Cath

    Parameters
    ----------
    fn : [fun]
        A given function that might raise error message 
    """
    @functools.wraps(fn)
    def wrapper(*args):
        """Parse kwarg parameter

        Returns
        -------
        res : [dic]
            paramerts later parse into a function

        """

        try:
            res = fn(*args)

        except Exception as e:
            print(e)
        else:
            return res

    return wrapper
