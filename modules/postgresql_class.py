import pandas as pd
import psycopg2

class Postgresql:
    """
    This is the module for adding records to the database.
    Tables:
    - Recipes (ingredients per 1 serving)
    - Nutrients (ingredient micronutrients per 100g)
    """
    def __init__(self):
        DB_NAME = ""
        DB_USER = ""
        DB_PASS = ""
        DB_HOST = ""
        DB_PORT = ""

        try:
            conn = psycopg2.connect(database=DB_NAME,
                                    user=DB_USER,
                                    password=DB_PASS,
                                    host=DB_HOST,
                                    port=DB_PORT)
            print("Database connected successfully")
        except:
            print("Database not connected successfully")

if __name__ == "__main__":
    Postgresql()