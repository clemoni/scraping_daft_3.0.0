# modules

import my_packages.fp_tools.fp_lib as fp
from my_packages.scraping_tools import global_lib


#  ________________________________________________________________
# ________________________________________________________________
# GET ADVERTS

def extract_container_adverts(county_adverts):
    return county_adverts.find('ul', {'data-testid': 'results'})


def get_children_from_container_adverts(container_adverts):
    return container_adverts.children


@global_lib.filter_fn_to_list
def filter_li_from_children(element):
    if element.name == 'li':
        return element


# ________________________________________________________________
# CHECK FOR SUB ADVERTS


def extract_global_advert(advert):
    return advert.find('div', {'data-testid': 'sub-units-container'})


def get_sub_adverts_from_global_advert(global_advert):
    return global_advert.find('ul', {'data-testid': 'sub-units'}).find_all('li')


get_sub_adverts = fp.compose(
    get_sub_adverts_from_global_advert, extract_global_advert)


# ________________________________________________________________
# GET PRICE OF ADS to check is not fake


def extract_price_element(advert):
    return advert.find('div', {'data-testid': 'price'})


get_price_from_element = global_lib.get_text_from_element


def format_price(price):
    return price.split()[0].lstrip('€').replace(',', '')


is_price_digit = global_lib.is_digit

is_advert_has_price = fp.compose_4(
    is_price_digit,
    format_price,
    get_price_from_element,
    extract_price_element
)

# ________________________________________________________________
# GLOBAL TEST
# if advert does not have price
# and if advert does not is not global (no subs adverts)
# >> its fake
# Avoid having too much loop


@global_lib.apply_fn_to_list
def get_subs_but_not_fake(advert):
    has_price = is_advert_has_price(advert)
    is_global = extract_global_advert(advert)

    if has_price or is_global:
        if is_global:
            return get_sub_adverts(advert)
        else:
            return advert


@global_lib.filter_fn_to_list
def filter_none_value(advert):
    if advert != None:
        return advert


@global_lib.apply_fn_to_list
def get_link_from_advert(advert):
    return advert.a['href'] if advert.a else advert['href']


# ________________________________________________________________
# fn get_county_adverts to retrieve all adverts in a page

get_links_for_county_adverts_page = fp.compose_7(
    get_link_from_advert,
    global_lib.flatten_array,
    filter_none_value,
    get_subs_but_not_fake,
    filter_li_from_children,
    get_children_from_container_adverts,
    extract_container_adverts
)
