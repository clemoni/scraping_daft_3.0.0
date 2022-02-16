'''
scrapint_advert

This module helps gather essential information from 
an advert page in daft.ie. 

The main access is with the function:
    
    - get_advert_object_from_county_link(county, advert_url)
    This function instanciate first a bs4 class from a given url and county. 
    A Advert class is then intanciated with the retrieved advert from the
    bs4 istance.
    
The class Advert gathered all the essential information needed to be inserted 
in an database. 


'''
from my_packages.scraping_tools.scraping_advert import sa_lib as lib
from my_packages.scraping_tools.bs4 import bs4_lib as bs4
from datetime import date


class Advert():
    '''
    Representation of an advert page from daft.ie. 
    '''

    def __init__(self, *, county, url, bs4_advert):
        self.county = county.title()
        self.url = url
        self.advert_id = lib.get_advert_id_number(bs4_advert)
        self.rent_amount = lib.get_advert_price_rent(bs4_advert)
        self.rent_frequency = lib.get_advert_frequency_rent(bs4_advert)
        self.address = lib.get_address(bs4_advert)
        self.rent_type = lib.get_property_type(bs4_advert)
        self.overview = lib.get_overview(bs4_advert)
        self.facilities = lib.get_facilities(bs4_advert)
        self.ber = lib.get_ber_id(bs4_advert)
        self.ber_n = lib.get_ber_number(bs4_advert)
        self.author = lib.get_author(bs4_advert)
        self.description = lib.get_description(bs4_advert)
        self.set_latitude_longitude(self, bs4_advert)
        self.created_at = date.today()
        self.closed_at = None
        self.is_closed = False

    @staticmethod
    def set_latitude_longitude(self, bs4_advert):
        geo = lib.get_geo(bs4_advert)
        self.latitude = geo['latitude']
        self.longitude = geo['longitude']

    @property
    def get_advert(self):
        '''
        Getter method. 
        Return an dictionary of 
        the properties of the class Advert.

        Returns
        -------
        [dic]
            The properties of the class Advert.
        '''
        advert = self.__dict__
        overview = advert.pop('overview')
        return {**advert, **overview}


def get_advert_object_from_county_link(county, advert_url):
    '''
    Return an instanciated class Advert 
    given a county and the partial url of advert page 
    from daft.ie.

    Parameters
    ----------
    county : [str]
        On of the irish county
    advert_url : [str]
        The partial url of an advert page.

        ie. /for-rent/house-70-castledawson-sion-hill-blackrock-co-dublin/3677804

    Returns
    -------
    [obj]
        An instanciated class Advert
    '''
    bas4_advert = bs4.get_app('https://www.daft.ie', advert_url)
    return Advert(county=county, url=advert_url,  bs4_advert=bas4_advert)
