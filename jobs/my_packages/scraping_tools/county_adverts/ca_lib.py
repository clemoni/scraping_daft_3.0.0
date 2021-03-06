# module
import my_packages.fp_tools.fp_lib as fp
import my_packages.scraping_tools.global_lib as global_lib
from my_packages.scraping_tools.scraping_advert import sa_main as sam


def init_url(*, county, page=0):
    """
    Initialize a dictionary from a specific page
    from the ads from a given County.
    Each entries is a part of the url to retrieve
    the page result of the adverts of a County.

    Parameters
    ----------
    county : [str]
        One county from Ireland.
    page : int, optional
        the page number of list of ads, by default 0

    Returns
    -------
    [dic]
        The different part of an url of the
        result of the adverts of a County.
    """
    return {
        'base': 'https://www.daft.ie',
        'general_search': '/property-for-rent/',
        'county': county,
        'page': f'?from={page}&pageSize=20'
    }

# ________________________________________________________________
# CALCUL LIMIT

# retrieves from the page results the maximun number of pages for a given county.
# There is 20 advertismenents per page
# Then extract the total number of advertisement to calculate the limit


def extract_element_adverts_count(county_adverts):
    """
    Retrieve the element h1 
    that contains the total number
    of adverts for a given county

    Parameters
    ----------
    county_adverts : [class]
        instanciated bs4 class of list of adverts
        for a given county.

    Returns
    -------
    [str]
       Element html h1 that contains number
    """
    return county_adverts.main.find('h1', {'data-testid': 'search-h1'})


get_encapsulated_adverts_count_from_element = global_lib.get_text_from_element


def get_adverts_counts_number(extracted_counts):
    """
    Retrives the number of adverts per county 
    the html element.

    Parameters
    ----------
    extracted_counts : [str]
        An HTML element that contains the nubmers of adverts.

    Returns
    -------
    [str]
        A string of the number of adverts for a given county.
    """
    int_number = extracted_counts.split()[0]
    if int_number.find(',') != -1:
        int_number = int_number.replace(',', '')
    return int_number


convert_adverts_counts_to_int = global_lib.convert_to_int


def calculate_limit(num_ads):
    if num_ads % 20 != 0:
        return num_ads + 20
    else:
        return num_ads


get_calculated_limit = fp.compose_5(
    calculate_limit,
    convert_adverts_counts_to_int,
    get_adverts_counts_number,
    get_encapsulated_adverts_count_from_element,
    extract_element_adverts_count
)


# ________________________________________________________________

#


def get_advert_object_from_adverts_county_page(*,
                                               links_from_county_page,
                                               county,
                                               iter_links=None,
                                               output=None,
                                               fn=sam.get_advert_object_from_county_link):
    """
    Recursive function.
    For a given page result (ie. page 0 on 30 pages)
    that contains a list of adverts a given county, 
    the function get_advert_object_from_county_link
    is applied. 

    This function returns a dictionary of all the essential information 
    related to the advert.

    Parameters
    ----------
    links_from_county_page : [list]
        list of all partial urls of all the adverts for a
        given page results.
    county : [str]
        an irish county
    iter_links : [list], optional
        links_from_county_page is copy to this
        variables in order to preserve integrity of it.
        For each new function call the last index is poped out 
        of inter_linls.
    output : [list], optional
        Return an list of dictionaries.
    fn : [function], optional
        the function that is used to
        retrieved data from each advert,
        by default sam.get_advert_object_from_county_link

    Returns
    -------
    output [list]
    """

    iter_links = iter_links if iter_links is not None else [
        *links_from_county_page]

    output = output if output is not None else []

    if len(iter_links) == 0:
        return output

    else:
        # print('running get new advert...')

        link = iter_links.pop(0)

        advert_object = fn(county=county, advert_url=link)

        output.append(advert_object.get_advert)

        return get_advert_object_from_adverts_county_page(links_from_county_page=links_from_county_page,
                                                          iter_links=iter_links,
                                                          county=county,
                                                          output=output)

# ________________________________________________________________
# alternative to get_advert_object_from_adverts_county_page
# using list comprehension
# when testing get_advert_object_from_adverts_county_page
# is faster by 3s
#
# last test :
# - get_advert_object exection time : 11s6
# - alternative execution time : 13s2


def get_dic_from_advert_object(advert_object):
    return advert_object.get_advert


get_advert_object = fp.compose_parse_2(
    get_dic_from_advert_object,
    sam.get_advert_object_from_county_link
)


def alternate_get_advert_object_from_adverts_county_page(*,
                                                         links_from_county_page,
                                                         county,
                                                         fn=get_advert_object):

    return [fn(county, link) for link in links_from_county_page]


# ________________________________________________________________
