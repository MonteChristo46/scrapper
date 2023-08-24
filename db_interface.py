from typing import *
import pymongo

class DataBaseInterface():

    def __init__(self, db_adress: str, db_password: str = None) -> None:
        self.client = pymongo.MongoClient(db_adress)

    def write_listings(self, listings: List["Listing"]) -> None: 
        db = self.client.airbnbData # DBName
        collection = db.listings # Listings Table
        result = collection.insert_many([x.serialize() for x in listings])

