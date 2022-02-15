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


def extract_element_adverts_count(county_adverts):
    return county_adverts.main.find('h1', {'data-testid': 'search-h1'})


get_encapsulated_adverts_count_from_element = global_lib.get_text_from_element


def get_adverts_counts_number(extracted_counts):
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


def get_advert_object_from_adverts_county_page(*, links_from_county_page,
                                               county,
                                               iter_links=None,
                                               output=None,
                                               fn=sam.get_advert_object_from_county_link):

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
