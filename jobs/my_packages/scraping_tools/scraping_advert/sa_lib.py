# modules
import re
import my_packages.fp_tools.fp_lib as fp
import functools
from my_packages.scraping_tools import global_lib


#########################################
#         SCRAPRING THE ADVERT          #
#########################################

# On a single Advert page, the following information are retrieve:
#     - id
#     - rent (price and frequence. ie. 2000 / month)
#     - type ('house', 'flat', ...)
#     - overview
#     - facilities (opt.)
#     - BER (opt.)
#     - description
#     - author
#     - geolocation ( lat/long and addresses)

##############################
#         ADVERT ID          #
##############################


# first extract:
# <p class="DaftIDText__StyledDaftIDParagraph-vbn7aa-0 iWkymm">
# Daft ID: <!-- -->26455566
# </p>
# Alternative : ad.find('p', {'class':'iWkymm'}).get_text()


@global_lib.is_element_available
def extract_element_id(advert):
    """
    Retrieves the HTML element that contains the ID number
    of the advert. 

    ie. 
    extract_element_id(advert=a_given_advert) 
    >>> '<p class="DaftIDText__StyledDaftIDParagraph-vbn7aa-0 dcUjaz">Daft ID: <!-- -->27679331</p>'

    Parameters
    ----------
    advert : [class]
        The advert from daft.com instanciated with as a class 'bs4.BeautifulSoup'

    Returns
    -------
    [str]
        The HTML element that contains the Advert ID.
    """
    return advert.find('p', {'class': re.compile('DaftIDText.')})


get_encapuslated_id_from_element_id = global_lib.get_text_from_element


@global_lib.is_element_available
def get_id_string_number(encapsulated_id):
    """
    Extracts the ID number from a encapsulated ID. 

    ie. extract_id_number(encapsulated_id='Daft ID: 27679331') => '27679331'

    Parameters
    ----------
    encapsulated_id : [str]
        A string as "Daft ID: 26369624"

    Returns
    -------
    [str]
        A string representing a sequence of number.
        ie. 26369624
    """
    return encapsulated_id.lstrip('Daft ID: ')


convert_id_string_to_int = global_lib.convert_to_int

get_advert_id_number = fp.compose_4(
    convert_id_string_to_int,
    get_id_string_number,
    get_encapuslated_id_from_element_id,
    extract_element_id)


##############################
#       ADVERT RENT          #
##############################


# ie retrieve "€3,100 per month"
@global_lib.is_element_available
def extract_element_price_frequency(advert):
    """
    Retrieves the span element that contains the
    price frequency of a given advert.

    Parameters
    ----------
    advert : [class]
        The advert from daft.com instanciated with as a class 'bs4.BeautifulSoup'

    Returns
    -------
    [str]
        The span element that contains the price frequency
    """
    price = advert.find('div', {'data-testid': 'price'})
    return price.span


get_price_frequency_from_element = global_lib.get_text_from_element


# ie retrieve "month" from "€3,100 per month"
@global_lib.is_element_available
def get_fequency_from_price_frequency(price_frequency):
    """
    Get the frequency of the rent from an encapsulated price/frequency string.

    ie. "€3,100 per month" > gives "month"

    Parameters
    ----------
    price_frequency : [str]
        A string with price frequency. 

    Returns
    -------
    [str]
        The fequency of a given price/frequency.
    """
    return 'month' if 'per month' in price_frequency else 'week'


# ie format 3,100 from from "€3,100 per month"
@global_lib.is_element_available
def get_price_from_price_frequency(price_frequency):
    """
    Get the price of the rent from an encapsulated price/frequency string.

    ie. "€3,100 per month" > give "3100"

    Parameters
    ----------
    price_frequency : [str]
        A string with price frequency.

    Returns
    -------
    [str]
        The price of a given price/frequency. 
    """
    return price_frequency.split()[0].lstrip('€').replace(',', '')


convert_rent_prince_to_float = global_lib.convert_to_float

# compose type functions
get_advert_frequency_rent = fp.compose_3(
    get_fequency_from_price_frequency,
    get_price_frequency_from_element,
    extract_element_price_frequency)

# compose price functions
get_advert_price_rent = fp.compose_4(
    convert_rent_prince_to_float,
    get_price_from_price_frequency,
    get_price_frequency_from_element,
    extract_element_price_frequency)


# When one information
# is split in two.
# ie RENT is two information Price and the Frequency
# init_format_compose from fp is used.
# init_format_compose performes as follow:
# vals = [f(x) for f in funcs]
# {key: vals[i] for i, key in enumerate(keys.values())}
#
# Format to data:  {'Price': '3,100', 'Type': 'month'}
get_rent = fp.init_format_compose(
    get_advert_price_rent, get_advert_frequency_rent, k_1='Price', k_2='Frequency')


##############################
#        ADVERT TYPE         #
##############################


# Retrieve 'House' fom <p data-testid='property-type'>
@global_lib.is_element_available
def extract_element_property_type(advert):
    """
    Retrieves the p element that contains the
    propery type of a given advert.

    Parameters
    ----------
    advert : [class]
        The advert from daft.com instanciated with as a class 'bs4.BeautifulSoup'

    Returns
    -------
    [str]
        The p element that contains the property type

    """
    return advert.find('p', {'data-testid': 'property-type'})


get_property_type_from_element = global_lib.get_text_from_element

get_property_type = fp.compose(
    get_property_type_from_element, extract_element_property_type)

##############################
#      ADVERT OVERVIEW       #
##############################


@global_lib.is_element_available
def extract_element_overview(advert):
    """
    Retrieves the div element that contains the
    overviews of a given advert.

    Parameters
    ----------
    advert : [class]
        The advert from daft.com instanciated with as a class 'bs4.BeautifulSoup'

    Returns
    -------
    [str]
        The overview from an advert.
    [NoneType]
        If not property type retrieved, returns None

    """
    return advert.find('div', {'data-testid': 'overview'})


@global_lib.is_element_available_NoneArray
def get_li_from_element(element_overview):
    return element_overview.ul.children


@global_lib.apply_fn_to_list
@global_lib.is_element_available_NoneArray
def format_overview(overview_li):
    """
    Retrieves the text contant from elevement overview
    and split element li between the
    overview type and information about it.

    ie. format_overview("<li>bathroom : 2</li>")
    >>> ["bathroom", "2"]

    Parameters
    ----------
    overview_li : [str]
        an li overview element

    Returns
    -------
    [List]
        An a list of lenght 2
    """
    return overview_li.get_text().split(':')


def filter_fn_to_list(fn):
    """
    filter a list of nested list elements
    with a given function
    using list comprehension. 
    For each element filter first element. i[0]

    Parameters
    ----------
    fn : [function]
        A function applied to first element i[0] nested list. 

    """
    @functools.wraps(fn)
    def wrapper(given_list):
        return [i for i in given_list if fn(i[0])]
    return wrapper


@filter_fn_to_list
@global_lib.is_element_in_list
def filter_useful_overview():
    """
    Tuple elements used to filter a list of elements.

    @global_lib.is_element_in_list is the function used
    to filter tuple element

    @filter_fn_to_list return a list comprehension 
    of filtered element

    Returns
    -------
    tuple
        The typle of element we wish to keep
    """
    return 'Double Bedroom', 'Single Bedroom', 'Bathroom', 'Furnished', 'Lease'


format_filtered_overview = global_lib.convert_to_dic()

get_overview = fp.compose_5(
    format_filtered_overview,
    filter_useful_overview,
    format_overview,
    get_li_from_element,
    extract_element_overview)

##############################
#     ADVERT FACILITIES      #
##############################


@global_lib.is_element_available
def get_element_facilities(advert):
    """Retrieves the facilities from an advert.
    If no facilities are found retrieves None.

    Parameters
    ----------
    advert : [class]
        The advert from daft.com instanciated with as a class 'bs4.BeautifulSoup'

    Returns
    -------
    [str]
        [description]
    [NoneType]
        If no facilities retrieved, returns None
    """
    return advert.find('div', {'data-testid': 'facilities'})


@global_lib.is_element_available
def get_li_from_element_facilities(element_facilities):
    """
    Get the children (li) from HTML elements (ul)
    that contains the facilities of an advert.

    Parameters
    ----------
    element_facilities : [str]
        A div element that contains the facilities of an advert.

    Returns
    -------
    [str]
        the children element (li) that lists the facilities of an advert.
    """
    return element_facilities.ul.children


@global_lib.is_element_available
@global_lib.apply_fn_to_list
def get_facility_from_element(facility_li):
    """
    Get the  the content text facility form a the li element. 

    @global_lib.apply_fn_to_list: Apply the function to an 
    a list of elements facilities.

    Parameters
    ----------
    facility_li : 'str'
        A html element (li) that contains a facility of an advert.

    Returns
    -------
    [str]
        The content text of the li element
    """
    return global_lib.get_text_from_element(facility_li)


@global_lib.is_element_available
def convert_facility_list_to_string(facility_list):
    """
    Merge the facilities to a string. 

    Parameters
    ----------
    facility_list : [list]
        A facilities list that contains all the facilities 
        associates to an advert.

    Returns
    -------
    [str]
        A string that contains all the facilities associated to
        an advert.
    """
    return ' - '.join(facility_list)


get_facilities = fp.compose_4(
    convert_facility_list_to_string,
    get_facility_from_element,
    get_li_from_element_facilities,
    get_element_facilities
)

##############################
#          ADVERT BER        #
##############################


@global_lib.is_element_available
def extract_element_ber(advert):
    """
    Retrieves the HTML element (div)
    that contains the BER associated to an advert.

    Parameters
    ----------
    advert : [class]
        The advert from daft.com instanciated with as a class 'bs4.BeautifulSoup'


    Returns
    -------
    [str]
        The HTML elment that contains the BER.
    """
    return advert.find('div', {'data-testid': 'ber'})


@global_lib.is_element_available
def get_ber_from_element(element_ber):
    """
    Get the BER ID from an HTML
    element that contains the BER associated of an advert.

    Parameters
    ----------
    element_ber : [str]
        An HTML element that contains the BER.

    Returns
    -------
    [str]
        The BER ID
    """
    return element_ber.img['alt']


def convert_ber_if_ber_exempt(ber):
    """
    If BER is type EXEMPT, 
    the retrived value will be 
    SI_666, needs to be converted 
    to BER EXEMPT

    Parameters
    ----------
    ber : [str]
        The BER rate associated to an advert.

    Returns
    -------
    [str]
        The BER rate associated to an advert.
    """
    return 'BER EXEMPT' if ber == 'SI_666' else ber


get_ber_id = fp.compose_3(
    convert_ber_if_ber_exempt,
    get_ber_from_element,
    extract_element_ber
)


@global_lib.is_element_available
def extract_ber_number_element(advert):
    """
    Retrieves the HTML element (p)
    that contains the BER number.

    Parameters
    ----------
    advert : [class]
        The advert from daft.com instanciated with as a class 'bs4.BeautifulSoup'


    Returns
    -------
    [str]
        The HTML element that contains the BER number.
    """
    return advert.find('p', {'data-testid': 'ber-code'})


get_encapuslated_ber_number_from_element = global_lib.get_text_from_element


@global_lib.is_element_available
def get_ber_number_from_encapsulated(encapuslated_ber_number):
    """
    Get the BER number for the retrieved content

    Parameters
    ----------
    encapuslated_ber_number : [str]
        The BER content retrieved from element.

    Returns
    -------
    [str]
        The BER number.
    """
    return encapuslated_ber_number.lstrip('BER No: ')


get_ber_number = fp.compose_3(
    get_ber_number_from_encapsulated,
    get_encapuslated_ber_number_from_element,
    extract_ber_number_element
)

get_ber = fp.init_format_compose(
    get_ber_id, get_ber_number, k_1='BER', k_2='BER n')

##############################
#       ADVERT AUTHOR        #
##############################


@global_lib.is_element_available
def extracted_element_author(advert):
    """
    Retrieves the HTML element (p)
    that contains the author associated with the
    advert.

    Parameters
    ----------
    advert : [class]
        The advert from daft.com instanciated with as a class 'bs4.BeautifulSoup'

    Returns
    -------
    [str]
        HTML element that contains the author
    """
    return advert.find('p', {'class': re.compile('ContactPanel__ImageLabel.')})


get_author_from_element = global_lib.get_text_from_element

get_author = fp.compose(get_author_from_element, extracted_element_author)

##############################
#     ADVERT DESCRIPTION     #
##############################

# Description is large text with
# some escape sequence, Asterisk.
# We tried to clean the text as best as possible


@global_lib.is_element_available
def extract_element_description(advert):
    """
    Retrives the property description of an advert.
    If no description is found, returns None.

    Parameters
    ----------
    advert : [class]
        The advert from daft.com 
        instanciated with as a class 'bs4.BeautifulSoup'

    Returns
    -------
    [str]
        A description of the property.
    [NoneType]
        If there is no value retrieved.
    """
    return advert.find('div', {'data-testid': 'description'})


get_description_from_element = global_lib.get_text_from_element


@global_lib.is_element_available
def format_description(description):
    return description.lstrip('Description**').replace('\r', '').replace('\n', ' ')


# compose follow the classic form of
# 1- extract information
# 2- format information
get_description = fp.compose_3(
    format_description,
    get_description_from_element,
    extract_element_description)


##############################
#     ADVERT GEOLOCATION     #
##############################

# 3 information are related to GEOLOCATION:
#     - geocoloation (lat/long)
#     - the address from the advert
#     - the address from geocoder


#     ADVERT GEOLOCATION LAT/LONG     #

@global_lib.is_element_available
def extract_element_geo(advert):
    """
    Retrieves the google map url associated to the property.

    Parameters
    ----------
    advert : [class]
        The advert from daft.com 
        instanciated with as a class 'bs4.BeautifulSoup'

    Returns
    -------
    [str]
        The google map address associated to the property.

    """
    return advert.find('a', {'data-testid': 'streetview-button'})


@global_lib.is_element_available
def get_geo_from_element(element_geo):
    return element_geo['href']


@global_lib.is_element_available
def format_geo(geo):
    """Extract the latitude and longitude from the google map url.
    If no value parses, returns None.

    Parameters
    ----------
    geo : [str]
        The google map url associated to the property.


    Returns
    -------
    [list[str]]
        The latitute and longitude
    [NoneType]
        If there is no value retrieved.
    """
    output = geo.lstrip(
        'https://www.google.com/maps/@?api=1&map_action=pano&viewpoint=').split(',')
    output.reverse()
    return output


def format_tested_geo(tested_geo):
    """
    Convert a list of the latitute and longitude values
    to a dictionary. 
    Convert the string latitude and longitude to float number.

    Parameters
    ----------
    tested_geo : [list[str]]
        A list of latitude and longitude.

    Returns
    -------
    [dic]
        A dictionary of the latitude and longitude converted to float. 
        Returns None if a list of None value are parsed to the function. 
    """
    if tested_geo:
        latitute, longitude = tested_geo
        res = {'latitude': float(latitute), 'longitude': float(longitude)}
    else:
        res = {'latitude': None, 'longitude': None}

    return res


get_geo = fp.compose_4(
    format_tested_geo,
    format_geo,
    get_geo_from_element,
    extract_element_geo)


##############################
#     ADDRESS                 #
##############################

@global_lib.is_element_available
def extract_element_address(advert):
    """
    Retrieves the element address from advert.

    Parameters
    ----------
   advert : [class]
        The advert from daft.com 
        instanciated with as a class 'bs4.BeautifulSoup'

    Returns
    -------
    [str]
        The address fron an advert.
    """
    return advert.find('h1', {'data-testid': 'address'})


get_address_from_element = global_lib.get_text_from_element

get_address = fp.compose(get_address_from_element, extract_element_address)


get_ad_data = fp.init_format_compose(get_advert_id_number, get_advert_price_rent, get_advert_frequency_rent,
                                     get_address, get_property_type,
                                     get_facilities, get_ber_id, get_ber_number, get_author,
                                     get_description,  k_1='advert_id', k_2='rent_amount', k_3='rent_frequency',
                                     k_4='address', k_5='rent_type',
                                     k_6='facilities', k_7='ber', k_8='ber_n', k_9='author',
                                     k_10='description')
if __name__ == "__main__":
    print('main : to be build')
