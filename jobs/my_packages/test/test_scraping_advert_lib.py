import my_packages.scraping_tools.scraping_advert.sa_lib as sa
import my_packages.fp_tools.fp_lib as fp
from my_packages.test.fake_advert import FakeAdvert
import unittest


class TestScrapingAdvertLib(unittest.TestCase):

    def setUp(self):
        self.fake_advert = FakeAdvert()

#  test advert id
    def test_get_advert_id_number(self):
        self.assertEqual(sa.get_advert_id_number(
            self.fake_advert.get_ID), 27679331)

    def test_get_advert_id_number_if_none_element(self):
        self.assertEqual(sa.get_advert_id_number(None), None)

# test rent frequency price
    def test_get_advert_frequency_rent(self):
        self.assertEqual(sa.get_advert_frequency_rent(
            self.fake_advert.get_PRICE_FREQUENCY), 'month')

    def test_get_advert_frequency_rent_if_none_element(self):
        self.assertEqual(sa.get_advert_frequency_rent(None), None)

    def test_get_advert_price_rent(self):
        self.assertEqual(sa.get_advert_price_rent(
            self.fake_advert.get_PRICE_FREQUENCY), 1325.0)

    def test_get_advert_price_rent_if_none_element(self):
        self.assertEqual(sa.get_advert_price_rent(None), None)


# test property type

    def test_get_property_type(self):
        self.assertEqual(sa.get_property_type(
            self.fake_advert.get_POPERTY_TYPE), 'Apartment')

    def test_get_property_type_if_None_element(self):
        self.assertEqual(sa.get_property_type(None), None)

# test overview

    def test_get_overview(self):
        self.assertEqual(sa.get_overview(
            self.fake_advert.get_OVERVIEW), {'double_bedroom': '2',
                                             'bathroom': '2',
                                             'furnished': 'Yes',
                                             'lease': 'Minimum 1 Year'})

    def test_get_overview_if_None_element(self):
        self.assertEqual(sa.get_overview(None), {})

# test Facitliies

    def test_get_facilities(self):
        self.assertEqual(sa.get_facilities(
            self.fake_advert.get_FACILITIES), '\n - Parking - \n - Central Heating - \n')

    def test_get_facilities_if_None_element(self):
        self.assertEqual(sa.get_facilities(None), None)

# test BER id

    def test_get_ber_id(self):
        self.assertEqual(sa.get_ber_id(
            self.fake_advert.get_BER), 'BER EXEMPT')

    def test_get_ber_id_if_None_element(self):
        self.assertEqual(sa.get_ber_id(None), None)

    def test_get_ber_number(self):
        self.assertEqual(sa.get_ber_number(
            self.fake_advert.get_BER), None)

    def test_get_ber_number_if_None_element(self):
        self.assertEqual(sa.get_ber_number(None), None)

# test author

    def test_get_author(self):
        self.assertEqual(sa.get_author(
            self.fake_advert.get_AUTHOR), 'Carma Property')

    def test_get_author_if_None_element(self):
        self.assertEqual(sa.get_author(None), None)

# test description

    def test_get_description(self):
        self.assertEqual(sa.get_description(
            self.fake_advert.get_DESCRIPTION), 'Beautiful 2 Bedroom, 2 bathroom apartment in a rural setting.')

    def test_get_description_if_None_element(self):
        self.assertEqual(sa.get_description(None), None)

# test geo

    def test_get_geo(self):
        self.assertEqual(sa.get_geo(
            self.fake_advert.get_GEO), {'latitude': -8.637080874, 'longitude': 51.926800047})

    def test_get_geo_if_None_element(self):
        self.assertEqual(sa.get_geo(None), {
                         'latitude': None, 'longitude': None})

# test address

    def test_get_address(self):
        self.assertEqual(sa.get_address(
            self.fake_advert.get_ADDRESS), 'Cloghroe House, Cloghroe, Co. Cork')

    def test_get_address_if_None_element(self):
        self.assertEqual(sa.get_address(None), None)


if __name__ == "__main__":

    unittest.main(verbosity=2)
