from typing import List
import mysql.connector

class mysqlInterface:
    def __init__(self, db_host: str, db_user: str, db_password: str, db_name: str) -> None:
        self.db_host = db_host
        self.db_user = db_user
        self.db_password = db_password
        self.db_name = db_name

    def write_listings(self, listings: List["Listing"]) -> None:
        
        connection = mysql.connector.connect(
            host=self.db_host,
            port=3306,
            user=self.db_user,
            password=self.db_password,
            database=self.db_name
        )

        cursor = connection.cursor()

        insert_query = "INSERT INTO listings (title, price, subtitle, rating, num_ratings, url) VALUES (%s, %s, %s, %s, %s, %s)"

        values = [listing.serialize() for listing in listings]
        records_to_insert = [(value['title'], value['price'], value['subtitle'], value['rating'], value['num_ratings'], value['url']) for value in values]

        cursor.executemany(insert_query, records_to_insert)
        connection.commit()

        cursor.close()