from fastapi import FastAPI
import logging
from scrapper import *
from mysql_interface import mysqlInterface

app = FastAPI()

MONGO_URL = "mongodb"
MYSQL_HOST = "mysql"
MYSQL_USER = "admin"
MYSQL_PWD = "admin"
MYSQL_DB = "listings"

# Configure logging
logging.basicConfig(level=logging.INFO)

@app.get("/")
async def root(): 
    try:
        logging.info("Accessing root endpoint...")

        scrapper = Scrapper()
        listings = scrapper.get_listings()
        logging.info("Listings scrapped")

        db_interface = DataBaseInterface(MONGO_URL)
        db_interface.write_listings(listings)
        logging.info("Listings sent to MongoDB")


        mysql_interface = mysqlInterface(MYSQL_HOST, MYSQL_USER, MYSQL_PWD, MYSQL_DB)
        mysql_interface.write_listings(listings)
        logging.info("Listings sent to mysql")


        _json = {"data": [x.serialize() for x in listings]}
        return _json
    except Exception as e:
        return "<h1>Something went wrong in root accesspoint</h1><br><h2>Exception: {} </br> {}".format(str(e))

if __name__ == '__main__':
    scrapper = Scrapper()
    listings = scrapper.get_listings()
    print("Listings ({}) fetched".format(len(listings)))

    db_interface = DataBaseInterface(MONGO_URL)
    db_interface.write_listings(listings)
    print("Listing sent to mongoDB")

    mysql_interface = mysqlInterface(MYSQL_HOST, MYSQL_USER, MYSQL_PWD, MYSQL_DB)
    mysql_interface.write_listings(listings)
    print("Listing sent to mysql")

