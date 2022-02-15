from bs4 import BeautifulSoup


class FakeAdvert():
    ID = '<p class="DaftIDText__StyledDaftIDParagraph-vbn7aa-0 dcUjaz">Daft ID: <!-- -->27679331</p>'

    PRICE_FREQUENCY = '''<div class="TitleBlock__Price-sc-1avkvav-3 cpwlUn" data-testid="price">
    <p><span class="TitleBlock__StyledSpan-sc-1avkvav-4 bNjvqX">€1,325 per month<!-- --></span></p>
    </div>'''

    POPERTY_TYPE = '<p class="TitleBlock__CardInfoItem-sc-1avkvav-8 ZPiKU" data-testid="property-type">Apartment</p>'

    OVERVIEW = '''<div class="PropertyPage__ContentSection-sc-14jmnho-3 fkZFrY" data-testid="overview">
    <h3 class="PropertyPage__H3-sc-14jmnho-6 cukWnM">Property Overview</h3>
    <ul class="PropertyPage__InfoSection-sc-14jmnho-7 fKJXQL">
    <li><span class="PropertyPage__ListLabel-sc-14jmnho-10 jrAxIM">Double Bedroom</span>:<!-- -->2</li>
    <li><span class="PropertyPage__ListLabel-sc-14jmnho-10 jrAxIM">Bathroom</span>:<!-- -->2</li>
    <li><span class="PropertyPage__ListLabel-sc-14jmnho-10 jrAxIM">Available From</span>:<!-- -->Immediately</li>
    <li><span class="PropertyPage__ListLabel-sc-14jmnho-10 jrAxIM">Furnished</span>:<!-- -->Yes</li>
    <li><span class="PropertyPage__ListLabel-sc-14jmnho-10 jrAxIM">Lease</span>:<!-- -->Minimum 1 Year</li></ul></div>'''

    FACILITIES = '''<div class="PropertyPage__ContentSection-sc-14jmnho-3 fkZFrY" data-testid="facilities">
    <h3 class="PropertyPage__H3-sc-14jmnho-6 cukWnM">Property Facilities</h3>
    <ul class="PropertyDetailsList__PropertyDetailsListContainer-sc-1cjwtjz-0 ffRuVo">
    <li class="PropertyDetailsList__PropertyDetailsListItem-sc-1cjwtjz-1 hsbAVe">Parking</li>
    <li class="PropertyDetailsList__PropertyDetailsListItem-sc-1cjwtjz-1 hsbAVe">Central Heating</li>
    </ul></div>'''

    BER = '''<div class="PropertyPage__ContentSection-sc-14jmnho-3 fkZFrY" data-testid="ber">
    <h3 class="PropertyPage__H3-sc-14jmnho-6 cukWnM">BER Details</h3>
    <img alt="SI_666" class="BerDetails__BerImage-sc-14a3wii-0 etlFKB" 
    src="https://hermes.daft.ie/dsch-daft-frontend/0.1.1578/static/images/ber/SI_666.svg"/></div>'''

    AUTHOR = '''<p class="ContactPanel__ImageLabel-sc-18zt6u1-6 ghgJoc">Carma Property</p>'''

    DESCRIPTION = '''<div class="PropertyPage__StandardParagraph-sc-14jmnho-8 iOxyyd" data-testid="description">Beautiful 2 Bedroom, 2 bathroom apartment in a rural setting.</div>'''

    GEO = '''<a
    aria-label="Street View"
    class="NewButton__StyledButtonHrefLink-yem86a-3 hzIHZl"
    data-testid="streetview-button"
    data-tracking="LaunchStreet"
    href="https://www.google.com/maps/@?api=1&amp;map_action=pano&amp;viewpoint=51.926800047,-8.637080874"
    rel="noreferrer noopener"
    target="_blank"
    ></a>'''

    ADDRESS = '''<h1 class="TitleBlock__Address-sc-1avkvav-7 hRrWaj" data-testid="address">Cloghroe House, Cloghroe, Co. Cork</h1>'''

    @staticmethod
    def convert_element_to_bs4(element):
        return BeautifulSoup(element, 'lxml')

    @property
    def get_ID(self):
        return self.convert_element_to_bs4(self.ID)

    @property
    def get_PRICE_FREQUENCY(self):
        return self.convert_element_to_bs4(self.PRICE_FREQUENCY)

    @property
    def get_POPERTY_TYPE(self):
        return self.convert_element_to_bs4(self.POPERTY_TYPE)

    @property
    def get_OVERVIEW(self):
        return self.convert_element_to_bs4(self.OVERVIEW)

    @property
    def get_FACILITIES(self):
        return self.convert_element_to_bs4(self.FACILITIES)

    @property
    def get_BER(self):
        return self.convert_element_to_bs4(self.BER)

    @property
    def get_AUTHOR(self):
        return self.convert_element_to_bs4(self.AUTHOR)

    @property
    def get_DESCRIPTION(self):
        return self.convert_element_to_bs4(self.DESCRIPTION)

    @property
    def get_GEO(self):
        return self.convert_element_to_bs4(self.GEO)

    @property
    def get_ADDRESS(self):
        return self.convert_element_to_bs4(self.ADDRESS)
