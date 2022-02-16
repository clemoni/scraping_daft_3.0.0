# modules
import functools
import my_packages.fp_tools.fp_lib as fp


def is_element_available(fn):
    @functools.wraps(fn)
    def wrapper(element):
        return fn(element) if element else None
    return wrapper


def is_element_available_NoneArray(fn):
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


@is_element_available
def convert_to_int(n):
    return int(n)


@is_element_available
def convert_to_float(n):
    return float(n)


def is_digit(element):
    return element.isdigit()


def format_dic_keys(key): return key.lower().replace(' ', '_')


def strip_content(content): return content.strip(' ')


def apply_fn_to_list(fn):
    @functools.wraps(fn)
    def wrapper(given_list):
        return [fn(i) for i in given_list]
    return wrapper


def convert_to_dic(fn1=format_dic_keys, fn2=strip_content):
    def wrapper(elements_list):
        return {fn1(i[0]): fn2(i[1]) for i in elements_list}
    return wrapper


def flatten_array(res):
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
