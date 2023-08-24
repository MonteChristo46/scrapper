
from bs4 import BeautifulSoup
import requests
import re
from typing import *
from db_interface import DataBaseInterface


class Listing: 

    def __init__(self, title:str = None, price:str= None, subtitle:str = None, rating: float = None, num_ratings: int = None, url:str= None):
        self.title: str = title
        self.price: float = price
        self.subtitle: str = subtitle
        self.rating: float = rating
        self.num_ratings: int = num_ratings 
        self.url = str = url
        self.review = ""
        self.owner = ""



    def serialize(self) -> str: 
        _json = {
            "title": str(self.title), 
            "price": float(self.price), 
            "subtitle": str(self.subtitle), 
            "rating": float(self.rating) if self.rating is not None else -1, 
            "num_ratings": int(self.num_ratings) if self.num_ratings is not None else -1,
            "url": str(self.url),
            "review": "",
            "owner": ""
        }

        return _json
    
class Review:
    def __init__(self, author: str, date: str, text:str):
        self.author = author
        self.date = date
        self.text = text


class Owner: 
    def __init__(self, name: str, is_super_host: bool, reviews: List["Review"]) -> None:
        pass



class Scrapper:


    def __init__(self, city: str): 
        self.base_url: str = "https://www.airbnb.com/s/Dresden/homes?tab_id=home_tab"

    @staticmethod
    def __extract_numerical(string: str) -> Union[float, None]:
        """
        The regular expression matchtes the first occurence of a numerical value followed by "per night"
        """
        match = re.search(r'\d+(\.\d+)?(?=\s*per night)', string)
        if match: 
            val = match.group()
            return float(val)
        else: 
            return None
        
    @staticmethod
    def __extract_reviews(string:str) -> Tuple[float, int, None]:
        match = re.search(r'(\d+(?:\.\d{1,2})?)\s*\((\d+)\)', string)
        if match: 
            float_value = match.group(1)
            int_value = match.group(2)
            return float_value, int_value
        else: 
            return None
        
    def get_review_scores(self, listing_page: str) -> List[str]:
        """_summary_

        <DIV WRAPPER>
            <DIV CONTAINER>
                <DIV ROW > 
                    <DIV NAME/>
                    <DIV>
                        <SPAN RATING><SPAN/>
                    <DIV>
                </DIV>
            </DIV>
        <DIV>

        <div data-section-id="REVIEWS DEFAULT" >
            <div class="_a3qxec"><div class="_y1ba89">
                Cleanliness</div>
                <div class="_bgq2leu"><div class="_7pay" aria-label="4.9 out of 5.0" role="img">
                <span class="_1hewo85" style="width: 98%;"></span>
                </div><span class="_4oybiu" aria-hidden="true">4.9</span></div>
            </div>
        </div>  
        Args:
            listing_page (str): _description_

        Returns:
            List[str]: _description_
        """
        pass

    def get_reviews():
        pass

    def get_owner(self, Listing_page: str) -> str:
        """_summary_
        <div data-section-id="HOST_PROFILE_DEFAULT"/>
        Args:
            Listing_page (str): _description_

        Returns:
            str: _description_
        """
    def get_is_superhost()->bool:
        pass

    def get_description(self, listing_page: str) -> str:
        pass

    def calendar(self, listing_page: str): 
        pass

    def get_cleaning_fee() -> str: 
        pass

    def get_tags() -> str: 
        pass

    # TODO still in works refactor get listing_cards AND INPUT htmk string
    def get_listings(self): 
        html = requests.get(self.base_url).text
        soup = BeautifulSoup(html, "html.parser")
        listing_containers = soup.find_all(attrs={"itemprop": "itemListElement"})

        listings = []
        for item_list in listing_containers: 
            listing = Listing()
            for obj in item_list: 
                if obj.name == "meta":
                    if obj.attrs['itemprop'] == "name": 
                        listing.subtitle = obj["content"]
                    if obj.attrs["itemprop"] == "url": 
                        listing.url = obj["content"]
                else: 
                    title = obj.find(attrs = {"data-testid": "listing-card-title"}).next
                    listing.title = title

                    # TODO there is the possibility that the wrong price is getting extracted. 
                    price_list = []
                    review_list = []
                    for span in obj.find_all("span"):
                        if isinstance(span.next, str):
                            _val = self.__extract_numerical(span.next)
                            _review = self.__extract_reviews(span.next)
                            if _val:
                                price_list.append(_val)
                            if _review:
                                review_list.append(_review)
                    if len(price_list) > 1: 
                        raise Warning("Invalid Prices - For listing {} more prices have been found!".format(title))
                    if len(review_list) > 1: 
                        raise Warning("Invalid Reviews - For listing {} more prices have been found!".format(title))
                    
                    listing.price = None if len(price_list) == 0 else price_list[0]
                    listing.rating = None if len(review_list) == 0 else review_list[0][0]
                    listing.num_ratings = None if len(review_list) == 0 else review_list[0][1]
                    listings.append(listing)

        
        return listings



"""

    
    https://www.airbnb.com/s/Dresden/homes?tab_id=home_tab // Listings for one week from request day
    https://www.airbnb.com/s/Dresden/homes?tab_id=home_tab&&checkin=2023-08-23&checkout=2023-09-29



    https://www.airbnb.com/s/Dresden/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_lengths%5B%5D=one_week&monthly_start_date=2023-08-01&monthly_length=3&price_filter_input_type=0&price_filter_num_nights=5&channel=EXPLORE&query=Dresden&place_id=ChIJqdYaECnPCUcRsP6IQsuxIQQ
https://www.airbnb.com/s/Dresden/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_lengths%5B%5D=one_week&monthly_start_date=2023-08-01&monthly_length=3&price_filter_input_type=0&price_filter_num_nights=5&channel=EXPLORE&query=Dresden&place_id=ChIJqdYaECnPCUcRsP6IQsuxIQQ&date_picker_type=calendar&source=structured_search_input_header&search_type=filter_change&checkin=2023-07-23&checkout=2023-07-29   

 <div data_testid="card-container"/>
            <div data_testid="listing-card-title"/>
            <div data_testid="listing-card-subtitle"/>
            <div data_testid="listing-card-subtitle"/>

            <div>
                <span class="a8jt5op dir dir-ltr">€&nbsp;75 per night, originally €&nbsp;129</span>
            </div>
    </div>


    <div itemprop="itemListElement" itemscope="" itemtype="http://schema.org/ListItem">
        <meta itemprop="name" content="Little apartment with a view">
        <meta itemprop="position" content="1">
        <meta itemprop="url" />
        <div>
            <div data_testid="listing-card-title"/>
            <div data_testid="listing-card-subtitle"/>
        </div>
    </div>


    <span class="_1y74zjx">€&nbsp;70&nbsp;</span>


    Format Rating: 4.83 (63)

    """