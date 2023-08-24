
from bs4 import BeautifulSoup
import requests

class Scrapper:

    def __init__(self): 
        self.base_url: str = "https://www.airbnb.com/s/Dresden/homes?tab_id=home_tab"


    def get_some(self): 
        html = requests.get(self.base_url).text
        x = 1


if __name__ == "__main__":
    scrapper = Scrapper()
    scrapper.get_some()

