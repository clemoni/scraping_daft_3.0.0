"""
Global library helper function used 
in sub libraries. 
"""
import functools

import tornado


def is_element_available(fn):
    """
    Thes is a given element is not None. 

    If not, a function is applied to said element. 

    If none, return none

    Parameters
    ----------
    fn : [function]
        A function that is applied to the element

    Returns
    -------
    [function]
        if not none
    [typeNone] 
        if None element
    """
    @functools.wraps(fn)
    def wrapper(element):
        return fn(element) if element else None
    return wrapper


def is_element_available_NoneArray(fn):
    """
    Test if a given element is not None. 

    If not, a function is applied to said element. 

    If none, return an array with one None element. 

    is_element_available_NoneArray used for sepcific type of test. 
    Where curried function are applied and tested element
    is expected to be an array.

    Parameters
    ----------
    fn : [function]
        A function that is applied to the element

    Returns
    -------
    [function]
        if not none
    [typeNone] 
        if None element
    """
    @functools.wraps(fn)
    def wrapper(element):
        return fn(element) if element else [None]
    return wrapper


def is_element_in_list(fn):
    @functools.wraps(fn)
    def wrapper(element):
        if element in fn():
            return element
    return wrapper


# TODO Add test function
# like try catch
# for convert_to_int
# and convert_to_float
# So that given element are
# convertible

@is_element_available
def convert_to_int(n):
    """
    Convert string to integer

    Parameters
    ----------
    n : [str]
        A given string or any element
        convertible to int

    Returns
    -------
    [int]
        an integer
    """
    return int(n)


@is_element_available
def convert_to_float(n):
    """
    Convert any possible element 
    to a float type.

    Parameters
    ----------
    n : [str]
        an element convertible to float

    Returns
    -------
    [float]
        a converted float elent
    """
    return float(n)


def is_digit(element):
    """
    Test is element is a digit.

    Parameters
    ----------
    element : [string]


    Returns
    -------
    [bool]
        True is element is a digit.
    """
    return element.isdigit()


def format_dic_keys(key): return key.lower().replace(' ', '_')


def strip_content(content):
    """
    Strip space from a string

    Parameters
    ----------
    content : [str]

    Returns
    -------
    [str]
    """
    return content.strip(' ')


def apply_fn_to_list(fn):
    """
    A apply a  given function fn
    to each element of a givenlist
    through list comprehension.

    Parameters
    ----------
    fn : [function]
        A given function, applied to each element of a list

    Returns
    -------
    [list]
    """
    @functools.wraps(fn)
    def wrapper(given_list):
        return [fn(i) for i in given_list]
    return wrapper


def convert_to_dic(fn1=format_dic_keys, fn2=strip_content):
    """
    Convert a list of tuple to an dictionary.
    Where i[0] will be the key
    and i[1] the value for each tuple.

    On top of tap a function fn1 is applied for each new, 
    and a fucntion fn2 is applied for each 
    associated value

    Parameters
    ----------
    fn1 : [fn], optional
        by default format_dic_keys
    fn2 : [fn], optional
         by default strip_content
    """
    def wrapper(elements_list):
        return {fn1(i[0]): fn2(i[1]) for i in elements_list}
    return wrapper


def flatten_array(res):
    """
    Flatten nested list in 
    one list

    Parameters
    ----------
    res : [list]
        A nested list

    Returns
    -------
    [list]
        a flatten list
    """
    out = []
    for ads in res:
        out = [*out, *ads]
    return out


def filter_fn_to_list(fn):
    """
    filter a list of nested list elements
    with a given function
    using list comprehension. 
    For each element filter first element. i

    Parameters
    ----------
    fn : [function]
        A function applied to first element i nested list. 

    """
    @functools.wraps(fn)
    def wrapper(given_list):
        return [i for i in given_list if fn(i)]
    return wrapper


@is_element_available
def get_text_from_element(element):
    """
    Get the text content of the string representation 
    of an HTML element.

    Parameters
    ----------
    element : [str]
        A given HTML element

    Returns
    -------
    [str]
        The text content from that element
    """
    return element.get_text()
