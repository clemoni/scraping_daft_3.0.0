'''
Main module of county advert

CountyAdvert is use a class
to represent all the adverts related
to a county in daft.ie.

All the apps are display in results list
divided in different pages.
'''

# modules
import my_packages.scraping_tools.global_lib as global_lib
from my_packages.scraping_tools.county_adverts import ca_lib as lib, ca_scraping_page_lib as scraping_lib
# from my_packages.scraping_tools.county_adverts import ca_scraping_page_lib as scraping_lib
from my_packages.scraping_tools.bs4 import bs4_lib as bs4


class CountyAdverts():
    """
    Represent the search of all the adverts
    retlated to a specific county.
    """

    def __init__(self, *, investigated_county):
        self.county = investigated_county
        self.url = lib.init_url(county=investigated_county)
        self.get_limit(self)

    # Calculate the number max of page results (limit)
    # instantiates the property self.limit
    # get_limit is called when class CountyAdverts is instanciated

    @staticmethod
    def get_limit(self):

        bas4_adverts_per_page = bs4.get_app(
            self.url['base'],
            self.url['general_search'],
            self.url['county'])

        self.limit = lib.get_calculated_limit(bas4_adverts_per_page)

    # Modify the page number
    # form url dictionnary
    # (property of class CountyAdverts)

    def change_page(self, page_number):
        self.url['page'] = f'?from={page_number}&pageSize=20'

    # Get the adverts from a specific page nubmer
    # given pages results
    # for a specific county

    def get_advertisements_per_page_given_a_page(self, page_number):
        """
        Get HTML page from an instantiated bs4 object, 
        the adverts of specific page number
        for a specific county on daft.ie


        Parameters
        ----------
        page_number : [int]
            The page number from a page results

        Returns
        -------
        [obj]
            The HTML page of the adverts for specific page number. 
        """
        self.change_page(page_number)

        return bs4.get_app(
            self.url['base'],
            self.url['general_search'],
            self.url['county'],
            self.url['page'])

    @staticmethod
    def get_all_adverts(self,
                        current_page=0,
                        output=None,
                        fn_get_links=scraping_lib.get_links_for_county_adverts_page,
                        fn_get_advert=lib.get_advert_object_from_adverts_county_page,):
        """
        Recursive function.
        For each page number until limit is reached
        fn_get_advert is going to be called. 

        1 - get_advertisements_per_page_given_a_page() for a specific page nubmer
        2 - retrieves all the partial links from the adverts list from extracted html content
        3 - for each partial links from the adverts called fn_get_advert 

        fn_get_advert is by default get_advert_object_from_adverts_county_page 

        Parameters
        ----------
        current_page : int, optional
            The page number where the function start the recursion, by default 0
        output : list, optional
            the return value, which a list
            containing dictionaries for every adverts, by default None
        fn_get_links : fun, optional
            the function used to retrieve all the partial links
            from the url content,
            by default scraping_lib.get_links_for_county_adverts_page
        fn_get_advert : fun, optional
            the function used to 
            retrieve all essential information 
            from an advert. It return a dictionary,
            by default lib.get_advert_object_from_adverts_county_page

        Returns
        -------
        list
            Returns a nested list, each nested list containing the dictionaries
            for every adverts of a specific page number.
        """

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

    @property
    def get_all_adverts_for_county(self):
        """
        Retuns a list of dictionaries. 
        Each dictionary having the essential information
        of an advert for a given county.

        Given that 

        Returns
        -------
        list
            Returns a list of dictionaries for every adverts
        """
        all_adverts = self.get_all_adverts(self)
        return global_lib.flatten_array(all_adverts)
