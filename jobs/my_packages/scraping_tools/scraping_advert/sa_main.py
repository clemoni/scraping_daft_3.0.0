# modules
from my_packages.scraping_tools.scraping_advert import sa_lib as lib
from my_packages.scraping_tools.bs4 import bs4_lib as bs4
from datetime import date


class Advert():
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
        return self.__dict__


def get_advert_object_from_county_link(county, advert_url):
    bas4_advert = bs4.get_app('https://www.daft.ie', advert_url)
    return Advert(county=county, url=advert_url,  bs4_advert=bas4_advert)
