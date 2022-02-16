import functools
from bs4 import BeautifulSoup
from urllib.request import urlopen


def try_action(fn):
    """Encapuslts a function into a Try Cath

    Parameters
    ----------
    fn : [fun]
        A given function that might raise error message 
    """
    @functools.wraps(fn)
    def wrapper(*args):
        try:
            res = fn(*args)

        except Exception as e:
            print(e)
        else:
            return res

    return wrapper


def init_get_app(*, parser='lxml'):
    """Initialise the function get_app with a specific 
    parser for beautifulSoup.

    Parameters
    ----------
    parser : [str]
        A parser available for beautifulSoup

    """
    @try_action
    def get_app(*urls):
        """Retrieve the HTML of given url

        Parameters
        ----------
        urls : [dic]
        A dictionary where entries reprensent the url

        Returns
        -------
        [str]
            The HTML page
        """
        url = ''.join(urls)
        html = urlopen(url)
        return BeautifulSoup(html.read(), parser)

    return get_app


get_app = init_get_app()
