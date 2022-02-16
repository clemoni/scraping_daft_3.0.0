# modules
import my_packages.scraping_tools.global_lib as global_lib
from my_packages.scraping_tools.county_adverts import ca_lib as lib, ca_scraping_page_lib as scraping_lib
# from my_packages.scraping_tools.county_adverts import ca_scraping_page_lib as scraping_lib
from my_packages.scraping_tools.bs4 import bs4_lib as bs4


class CountyAdverts():
    def __init__(self, *, investigated_county):
        self.county = investigated_county
        self.url = lib.init_url(county=investigated_county)
        self.get_limit(self)

    def change_page(self, page_number):
        self.url['page'] = f'?from={page_number}&pageSize=20'

    def get_advertisements_per_page_given_a_page(self, page_number):
        self.change_page(page_number)
        bas4_adverts_per_page = self.get_advertisements_per_page(
            self.url['base'],
            self.url['general_search'],
            self.url['county'],
            self.url['page'])
        return bas4_adverts_per_page

    @property
    def get_all_adverts_for_county(self):
        all_adverts = self.get_all_adverts(self)
        return global_lib.flatten_array(all_adverts)

    @staticmethod
    def get_advertisements_per_page(*url):
        return bs4.get_app(*url)

    @staticmethod
    def get_limit(self):
        bas4_adverts_per_page = self.get_advertisements_per_page(
            self.url['base'],
            self.url['general_search'],
            self.url['county'])

        self.limit = lib.get_calculated_limit(bas4_adverts_per_page)

    @staticmethod
    def get_all_adverts(self,
                        current_page=0,
                        output=None,
                        fn_get_links=scraping_lib.get_links_for_county_adverts_page,
                        fn_get_advert=lib.get_advert_object_from_adverts_county_page,):

        output = output if output is not None else []

        if current_page > self.limit:
            return output
        else:
            print(f'scraping new page {current_page}')

            bas4_adverts_per_page = self.get_advertisements_per_page_given_a_page(
                page_number=current_page)

            links_per_page = fn_get_links(bas4_adverts_per_page)

            list_adverts_object = fn_get_advert(links_from_county_page=links_per_page,
                                                county=self.county)

            output.append(list_adverts_object)

            next_page = current_page+20

            return self.get_all_adverts(self, current_page=next_page, output=output)
